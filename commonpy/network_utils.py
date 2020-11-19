'''
network_utils.py: network utilities

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2018-2020 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

import httpx
import socket
import ssl
import tldextract
import urllib

if __debug__:
    from sidetrack import log

from .exceptions import *
from .interrupt import wait, interrupted


# Internal constants.
# .............................................................................

_MAX_RECURSIVE_CALLS = 10
'''How many times can certain network functions call themselves upon
encountering a network error before they stop and give up.'''

_MAX_CONSECUTIVE_FAILS = 3
'''Maximum number of consecutive failures before pause and try another round.'''

_MAX_RETRIES = 5
'''Maximum number of times we back off and try again.  This also affects the
maximum wait time that will be reached after repeated retries.'''


# Main functions.
# .............................................................................

def network_available(address = "8.8.8.8", port = 53, timeout = 5):
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
    except Exception:
        if __debug__: log('could not connect to https://www.google.com')
        return False


def hostname(url):
    if url.startswith('http'):
        parsed = urllib.parse.urlsplit(url)
        return parsed.hostname
    else:
        # urllib.parse doesn't provide a hostname.  Try a different way.
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


def timed_request(method, url, client = None, **kwargs):
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
    def addurl(text):
        return f'{text} for {url}'

    if client is None:
        timeout = httpx.Timeout(connect = 15, read = 15, write = 15)
        client = httpx.Client(timeout = timeout, http2 = True, verify = False)

    failures = 0
    retries = 0
    error = None
    while failures < _MAX_CONSECUTIVE_FAILS and not interrupted():
        try:
            if __debug__: log(addurl(f'doing http {method}'))
            func = getattr(client, method)
            response = func(url, **kwargs)
            # For some statuses, retry once, in case it's a transient problem.
            code = response.status_code
            if __debug__: log(addurl(f'got response with code {code}'))
            if code not in [400, 409, 502, 503, 504] or failures > 0:
                return response
            else:
                failures += 1
        except (KeyboardInterrupt, UserCancelled) as ex:
            if __debug__: log(addurl(f'network {method} interrupted by {str(ex)}'))
            raise
        except (httpx.CookieConflict, httpx.StreamError, httpx.ProxyError,
                httpx.DecodingError, httpx.ProtocolError,
                httpx.RequestBodyUnavailable, httpx.TooManyRedirects) as ex:
            # Probably indicates a deeper issue.  Don't do our lengthy retry
            # sequence, but try one more time, in case it's transient.
            if __debug__: log(addurl(f'exception {str(ex)}'))
            if failures > 0:
                raise
            failures += 1
            if __debug__: log(addurl('retrying one more time after brief pause'))
        except Exception as ex:
            # Problem might be transient.  Don't quit right away.
            failures += 1
            if __debug__: log(addurl(f'exception (failure #{failures}): {str(ex)}'))
            # Record the first error we get, not the subsequent ones, because
            # in the case of network outages, the subsequent ones will be
            # about being unable to reconnect and not the original problem.
            if not error:
                error = ex
        if failures >= _MAX_CONSECUTIVE_FAILS:
            # Pause with exponential back-off, reset failure count & try again.
            if retries < _MAX_RETRIES:
                retries += 1
                failures = 0
                pause = 10 * retries * retries
                if __debug__: log(addurl(f'pausing due to consecutive failures'))
                wait(pause)
            else:
                if __debug__: log(addurl('exceeded max failures and max retries'))
                raise error
        # Pause briefly b/c it's rarely a good idea to retry immediately.
        if __debug__: log(addurl('pausing briefly before retrying'))
        wait(0.5)
    if interrupted():
        if __debug__: log(addurl('interrupted'))
        raise Interrupted(addurl('Network request has been interrupted'))
    else:
        # In theory, we should never reach this point.  If we do, then:
        raise InternalError(addurl('Unexpected case in timed_request'))


def net(method, url, client = None, handle_rate = True,
        polling = False, recursing = 0, **kwargs):
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

    This method always passes the argument allow_redirects = True to the
    underlying Python HTTPX library network calls.
    '''
    def addurl(text):
        return f'{text} for {url}'

    resp = None
    try:
        resp = timed_request(method, url, client, allow_redirects = True, **kwargs)
    except (httpx.NetworkError, httpx.ProtocolError) as ex:
        # timed_request() will have retried, so if we get here, time to bail.
        if __debug__: log(addurl(f'got network exception: {str(ex)}'))
        if not network_available():
            if __debug__: log(addurl('returning NetworkFailure'))
            return (resp, NetworkFailure(addurl('Network connectivity failure')))
        else:
            if __debug__: log(addurl('failed > 1 times -- returning ServiceFailure'))
            return (resp, ServiceFailure(addurl('Network or server error {str(ex)}')))
    except Exception as ex:
        # Not a network or protocol error, and not a normal server response.
        if __debug__: log(addurl(f'returning exception: {str(ex)}'))
        return (resp, ex)

    # Interpret the response.  Note that the requests library handles code 301
    # and 302 redirects automatically, so we don't need to do it here.
    error = None
    code = resp.status_code
    reason = resp.reason_phrase
    if code == 400:
        error = ServiceFailure(addurl('Server rejected the request'))
    elif code in [401, 402, 403, 407, 451, 511]:
        error = AuthenticationFailure(addurl('Access is forbidden'))
    elif code in [404, 410] and not polling:
        error = NoContent(addurl("No content found"))
    elif code in [405, 406, 409, 411, 412, 413, 414, 417, 428, 431, 505, 510]:
        error = InternalError(addurl(f'Server returned code {code} ({reason})'))
    elif code in [415, 416]:
        error = ServiceFailure(addurl('Server rejected the request ({reason})'))
    elif code == 429:
        if handle_rate and recursing < _MAX_RECURSIVE_CALLS:
            pause = 5 * (recursing + 1)   # +1 b/c we start with recursing = 0.
            if __debug__: log(addurl('rate limit hit -- pausing'))
            wait(pause)                   # 5 s, then 10 s, then 15 s, etc.
            if __debug__: log(addurl(f'doing recursive call #{recursing + 1}'))
            return net(method, url, client, handle_rate, polling, recursing + 1, **kwargs)
        error = RateLimitExceeded(addurl('Server blocking requests due to rate limits'))
    elif code in [500, 501, 502, 503, 504, 506, 507, 508]:
        error = ServiceFailure(addurl(f'Server error (code {code} -- {reason})'))
    elif not (200 <= code < 400):
        error = NetworkFailure(addurl(f'Unable to resolve {url}'))
    # The error msg will have had the URL added already; no need to do it here.
    if __debug__: log('returning {}'.format(f'{error}' if error else f'response for {url}'))
    return (resp, error)
