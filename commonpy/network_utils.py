'''
network_utils.py: network utilities

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2018-2023 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

from   ipaddress import ip_address
from   os import stat
import socket
import urllib.parse

if __debug__:
    from sidetrack import log

from .interrupt import wait, interrupted, raise_for_interrupts
from .exceptions import ArgumentError, Interrupted, InternalError, NoContent
from .exceptions import AuthenticationFailure, ServiceFailure, NetworkFailure
from .exceptions import RateLimitExceeded
from .string_utils import antiformat


# Internal constants.
# .............................................................................

_MAX_RECURSIVE_CALLS = 10
'''How many times can certain network functions call themselves upon
encountering a network error before they stop and give up.'''

_MAX_CONSECUTIVE_FAILS = 3
'''Maximum number of times we back off and try again.  This also affects the
maximum wait time that will be reached after repeated retries.'''

_KNOWN_HTTP_METHODS = ['get', 'post', 'head', 'options', 'put', 'delete', 'patch']
'''Known http methods.'''


# Main functions.
# .............................................................................

def network_available(address="8.8.4.4", port=53, timeout=5):
    '''Return True if it appears we have a network connection, False if not.
    By default, this attempts to contact one of the Google DNS servers (as a
    plain TCP connection, not as an actual DNS lookup).  Argument 'address'
    and 'port' can be used to test a different server address and port.  The
    socket connection is attempted for 'timeout' seconds.
    '''
    # Portions of this code are based on the answer by user "7h3rAm" posted to
    # Stack Overflow here: https://stackoverflow.com/a/33117579/743730
    try:
        if __debug__: log('testing if we have a network connection')
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((address, port))
        if __debug__: log('we have a network connection')
        return True
    except (socket.error, socket.timeout):
        if __debug__: log(f'could not connect to {address} in {timeout} sec')
        return False


def hostname(url):
    parts = urllib.parse.urlsplit(url)
    if parts.scheme:
        return parts.hostname
    else:
        # urllib.parse doesn't provide a hostname.  Try a different way.
        import tldextract
        return '.'.join(part for part in tldextract.extract(url) if part)


def scheme(url):
    parsed = urllib.parse.urlsplit(url)
    return parsed.scheme


def netloc(url):
    parsed = urllib.parse.urlsplit(url)
    if parsed.netloc:
        return parsed.netloc
    elif not url.startswith('http') and '//' not in url:
        # Add a fake "http://" so that urllib.parse can figure out the netloc.
        parsed = urllib.parse.urlsplit('http://' + url)
        return parsed.netloc
    else:
        # Last-ditch effort.
        return parsed.path


def on_localhost(url):
    if not url:
        return False
    host = hostname(url)
    # The following approach is based on code posted by user "georgexsh" on
    # 2017-12-21 to https://stackoverflow.com/a/47919356/743730
    for family in (socket.AF_INET, socket.AF_INET6):
        try:
            addrinfo = socket.getaddrinfo(host, None, family, socket.SOCK_STREAM)
        except socket.gaierror:
            break
        else:
            for _, _, _, _, sockaddr in addrinfo:
                address_part = sockaddr[0]
                if ip_address(address_part).is_loopback:
                    if __debug__: log(f'address seems to be on localhost: {url}')
                    return True
    if __debug__: log(f'address not on localhost: {url}')
    return False


def timed_request(method, url, client=None, **kwargs):
    '''Perform a network access, automatically retrying if exceptions occur.

    The value given to parameter "method" must be a string chosen from among
    valid HTTP methods, such as "get", "post", or "head".  If "client" is
    not None, it is used as an httpx.Client object. Other keyword arguments
    are passed to the network method.

    If not given a Client object, the default timeouts for network connect,
    read, and write are 15 seconds.  It enables HTTP 2.0 and disables SSL
    verification.

    This method retries connections in cases of network exceptions.  It also
    retries connections one time when the server returns certain HTTP status
    codes, specifically 400, 409, 502, 503, and 504.  These are sometimes the
    result of temporary server problems or other issues and disappear when a
    second attempt is made after a brief pause.
    '''
    import httpx

    def addurl(text):
        return f'{text} for {url}'

    if client is None:
        timeout = httpx.Timeout(15, connect=15, read=15, write=15)
        client = httpx.Client(timeout=timeout, http2=True, verify=False)
    elif client == 'stream':
        client = httpx.stream

    failures = 0
    error = None
    while failures < _MAX_CONSECUTIVE_FAILS and not interrupted():
        try:
            if __debug__: log(addurl(f'doing http {method}'))
            func = getattr(client, method)
            response = func(url, **kwargs)
            # For some statuses, retry once, in case it's a transient problem.
            code = response.status_code
            if __debug__: log(addurl(f'got response with code {code}'))
            if code not in [400, 409, 502, 503, 504] or failures > _MAX_CONSECUTIVE_FAILS:
                return response
            else:
                failures += 1
        except KeyboardInterrupt as ex:
            if __debug__: log(addurl(f'network {method} interrupted by {antiformat(ex)}'))
            raise
        except ImportError as ex:
            # Explicit test needed b/c httpx depends on other things that don't
            # always declare all their dependencies properly.
            log('import error: ' + str(ex))
            raise
        except (TypeError, httpx.UnsupportedProtocol) as ex:
            # Bad arguments to the call, like passing data to a 'get'.
            if __debug__: log(addurl(f'exception {antiformat(ex)}'))
            raise ArgumentError('Bad or invalid arguments in network call')
        except (httpx.CookieConflict, httpx.StreamError, httpx.TooManyRedirects,
                httpx.DecodingError, httpx.ProtocolError, httpx.ProxyError,
                httpx.ConnectError) as ex:
            # Probably indicates a deeper issue.  Don't do our lengthy retry
            # sequence, but try one more time, in case it's transient.
            if __debug__: log(addurl(f'exception {antiformat(ex)}'))
            if failures > 0:
                raise
            if __debug__: log(addurl('will retry one more time after brief pause'))
        except Exception as ex:         # noqa PIE786
            # Problem might be transient.  Don't quit right away.
            failures += 1
            if __debug__: log(addurl(f'exception (failure #{failures}): {antiformat(ex)}'))
            # Record the first error we get, not the subsequent ones, because
            # in the case of network outages, the subsequent ones will be
            # about being unable to reconnect and not the original problem.
            if not error:
                error = ex
        if failures == 0:
            # Pause briefly b/c it's rarely a good idea to retry immediately.
            if __debug__: log(addurl('pausing briefly before retrying'))
            wait(0.5)
            failures += 1
        elif failures <= _MAX_CONSECUTIVE_FAILS:
            # Pause with exponential back-off, reset failure count & try again.
            pause = 10 * failures * failures
            if __debug__: log(addurl('pausing due to consecutive failures'))
            wait(pause)
        else:
            if __debug__: log(addurl('exceeded max failures'))
            raise error
    if interrupted():
        if __debug__: log(addurl('interrupted'))
        raise Interrupted(addurl('Network request has been interrupted'))
    else:
        # In theory, we should never reach this point.  If we do, then:
        raise InternalError(addurl('Unexpected case in timed_request'))


def net(method, url, client=None, handle_rate=True,
        polling=False, recursing=0, **kwargs):
    '''Invoke HTTP "method" on 'url' with optional keyword arguments provided.

    Returns a tuple of (response, exception), where the first element is
    the response from the get or post http call, and the second element is
    an exception object if an exception occurred.  If no exception occurred,
    the second element will be None.  This allows the caller to inspect the
    response even in cases where exceptions are raised.

    If keyword 'client' is not None, it's assumed to be a Python HTTPX Client
    object to use for the network call.  Settings such as timeouts should be
    done by the caller creating appropriately-configured Client objects.

    If keyword 'handle_rate' is True, this function will automatically pause
    and retry if it receives an HTTP code 429 ("too many requests") from the
    server.  If False, it will return the exception RateLimitExceeded instead.

    If keyword 'polling' is True, certain statuses like 404 are ignored and
    the response is returned; otherwise, they are considered errors.  The
    behavior when True is useful in situations where a URL does not exist until
    something is ready at the server, and the caller is repeatedly checking
    the URL.  It is up to the caller to implement the polling schedule and
    call this function (with polling = True) as needed.

    This method always passes the argument follow_redirects = True to the
    underlying Python HTTPX library network calls.
    '''
    import httpx 

    if method.lower() not in _KNOWN_HTTP_METHODS:
        raise ValueError(f'Method must be one of {", ".join(_KNOWN_HTTP_METHODS)}.')

    def info(text, details=''):
        msg = f'{text} for {url}'
        if details:
            msg += (' (' + details + ')')
        return msg

    resp = None
    try:
        resp = timed_request(method, url, client, follow_redirects=True, **kwargs)
    except (httpx.NetworkError, httpx.ProtocolError) as ex:
        # timed_request() will have retried, so if we get here, time to bail.
        if __debug__: log(info(f'network exception: {antiformat(ex)}'))
        is_on_localhost = on_localhost(url)
        reason = antiformat(ex)
        if isinstance(ex, httpx.ConnectError) and is_on_localhost:
            if __debug__: log(info('returning ServiceFailure'))
            return (resp, ServiceFailure(info(f'Access failure ({reason})')))
        elif is_on_localhost or network_available():
            if __debug__: log(info('returning ServiceFailure'))
            return (resp, ServiceFailure(info(f'Server error ({reason})')))
        else:
            if __debug__: log(info('returning NetworkFailure'))
            return (resp, NetworkFailure(info('Network failure ({reason})')))
    except Exception as ex:             # noqa PIE786
        # Not a network or protocol error, and not a normal server response.
        if __debug__: log(info(f'returning exception: {antiformat(ex)}'))
        return (resp, ex)

    # Interpret the response.  Note that the requests library handles code 301
    # and 302 redirects automatically, so we don't need to do it here.
    error = None
    code = resp.status_code
    reason = resp.reason_phrase
    text = resp.text                    # Sometimes this holds more details.
    if code == 400:
        error = ServiceFailure(info('Server rejected the request', text))
    elif code in [401, 402, 403, 407, 451, 511]:
        error = AuthenticationFailure(info('Access is forbidden', text))
    elif code in [404, 410] and not polling:
        error = NoContent(info("No content found", text))
    elif code in [405, 406, 409, 411, 412, 413, 414, 417, 428, 431, 505, 510]:
        error = InternalError(info(f'Server returned code {code} ({reason})', text))
    elif code in [415, 416]:
        error = ServiceFailure(info(f'Server rejected the request ({reason})', text))
    elif code == 429:
        if handle_rate and recursing < _MAX_RECURSIVE_CALLS:
            pause = 5 * (recursing + 1)   # +1 b/c we start with recursing = 0.
            if __debug__: log(info('rate limit hit -- pausing', text))
            wait(pause)                   # 5 s, then 10 s, then 15 s, etc.
            if __debug__: log(info(f'doing recursive call #{recursing + 1}', text))
            return net(method, url, client, handle_rate, polling, recursing + 1, **kwargs)
        error = RateLimitExceeded(info('Server blocking requests due to rate limits', text))
    elif code in [500, 501, 502, 503, 504, 506, 507, 508]:
        error = ServiceFailure(info(f'Server error (code {code} -- {reason})', text))
    elif not (200 <= code < 400):
        error = NetworkFailure(info(f'Unable to resolve {url}', text))
    # The error msg will have had the URL added already; no need to do it here.
    if __debug__:                       # noqa SIM102
        if error:
            log('returning error ' + str(error))
    return (resp, error)


def network(method, url, client=None, handle_rate=True,
            polling=False, recursing=0, **kwargs):
    '''Invoke HTTP "method" on 'url' with optional keyword arguments provided.

    This is an alternative to net(). The difference is that this function only
    returns one value (the response object from HTTPX); if any error occurs,
    it raises an exception. (Compare this to net(...), which returns 2 values.)
    '''
    response, error = net(method, url, client, handle_rate,
                          polling, recursing, **kwargs)
    if error:
        raise error
    return response


def download_file(url, local_destination):
    '''Returns True if the content at 'url' could be downloaded to the file
    'local_destination', and False otherwise. It does not throw an exception.'''

    def addurl(text):
        return f'{text} for {url}'

    try:
        download(url, local_destination)
    except Exception as ex:             # noqa PIE786
        if __debug__: log(f'download exception: {antiformat(ex)}')
        return False
    else:
        return True


def download(url, local_destination, recursing=0):
    '''Download the 'url' to the file 'local_destination'.'''
    import httpx

    def addurl(text):
        return f'{text} for {url}'

    timeout = httpx.Timeout(15, connect=15, read=15, write=15)
    with httpx.stream('get', url, verify=False, timeout=timeout,
                      follow_redirects=True) as resp:
        code = resp.status_code
        if code == 202:
            # Code 202 = Accepted, "received but not yet acted upon."
            wait(2)                     # Sleep a short time and try again.
            raise_for_interrupts()
            recursing += 1
            if recursing <= _MAX_RECURSIVE_CALLS:
                if __debug__: log('calling download(url) recursively for code 202')
                download(url, local_destination, recursing)
            else:
                raise ServiceFailure(addurl('Exceeded max retries for code 202'))
        elif 200 <= code < 400:
            with open(local_destination, 'wb') as f:
                for chunk in resp.iter_bytes():
                    raise_for_interrupts()
                    f.write(chunk)
            resp.close()
            size = stat(local_destination).st_size
            if __debug__: log(f'wrote {size} bytes to file {local_destination}')
        elif code in [401, 402, 403, 407, 451, 511]:
            raise AuthenticationFailure(addurl('Access is forbidden'))
        elif code in [404, 410]:
            raise NoContent(addurl('No content found'))
        elif code in [405, 406, 409, 411, 412, 414, 417, 428, 431, 505, 510]:
            raise InternalError(addurl(f'Server returned code {code}'))
        elif code in [415, 416]:
            raise ServiceFailure(addurl('Server rejected the request'))
        elif code == 429:
            raise RateLimitExceeded('Server blocking further requests due to rate limits')
        elif code == 503:
            raise ServiceFailure('Server is unavailable -- try again later')
        elif code in [500, 501, 502, 506, 507, 508]:
            raise ServiceFailure(addurl(f'Internal server error (HTTP code {code})'))
        else:
            raise NetworkFailure(f'Unable to resolve {url}')
