'''
http_code: provide explanations of each possible HTTP status code

This module grew out of frustration with the standard Python HTTPStatus module,
which provides codes and short meanings but not enough detail to serve as
explanations.  It also does not contain all codes that servers may return.
This http_meanings module offers longer explanations of http status codes.

Example usage:

    from commonpy.http_code import http_code_meaning
    print(http_code_meaning(200))

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2018-2020 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

from http import HTTPStatus


# Global definitions.
# .............................................................................

# The explanations of the codes were drawn from the following web page:
#
# The last update date listed on the page at the time was Mar 19, 2018.
# The content is licensed CC-BY-SA 2.5.  The contributors to that page are
# listed as follows: ry0id, ExE_Boss, afaulconbridge, vy-let, mgold, Jens.B,
# ColdSauce, fscholz, Theseven567, sivasain, arulnithi, rctgamer3, groovecoder,
# dovgart, Sheppy, fusionchess.

http_meanings = {
    100 : (HTTPStatus.CONTINUE.phrase, "This interim response indicates that everything so far is OK and that the client should continue with the request or ignore it if it is already finished."),

    101 : (HTTPStatus.SWITCHING_PROTOCOLS.phrase, "This code is sent in response to an Upgrade request header by the client, and indicates the protocol the server is switching to."),

    102 : (HTTPStatus.PROCESSING.phrase, "This code indicates that the server has received and is processing the request, but no response is available yet."),

    200 : (HTTPStatus.OK.phrase, "The request has succeeded."),

    201 : (HTTPStatus.CREATED.phrase, "The request has succeeded and a new resource has been created as a result of it. This is typically the response sent after a POST request, or after some PUT requests."),

    202 : (HTTPStatus.ACCEPTED.phrase, "The request has been received but not yet acted upon. It is non-committal, meaning that there is no way in HTTP to later send an asynchronous response indicating the outcome of processing the request. It is intended for cases where another process or server handles the request, or for batch processing."),

    203 : (HTTPStatus.NON_AUTHORITATIVE_INFORMATION.phrase, "This response code means returned meta-information set is not exact set as available from the origin server, but collected from a local or a third party copy. Except this condition, 200 OK response should be preferred instead of this response."),

    204 : (HTTPStatus.NO_CONTENT.phrase, "There is no content to send for this request, but the headers may be useful. The user-agent may update its cached headers for this resource with the new ones."),

    205 : (HTTPStatus.RESET_CONTENT.phrase, "This response code is sent after accomplishing request to tell user agent reset document view which sent this request."),

    206 : (HTTPStatus.PARTIAL_CONTENT.phrase, "This response code is used because of range header sent by the client to separate download into multiple streams."),

    207 : (HTTPStatus.MULTI_STATUS.phrase, "A Multi-Status response conveys information about multiple resources in situations where multiple status codes might be appropriate."),

    208 : (HTTPStatus.ALREADY_REPORTED.phrase, "Used inside a DAV: propstat response element to avoid enumerating the internal members of multiple bindings to the same collection repeatedly."),

    226 : (HTTPStatus.IM_USED.phrase, "The server has fulfilled a GET request for the resource, and the response is a representation of the result of one or more instance-manipulations applied to the current instance."),

    300 : (HTTPStatus.MULTIPLE_CHOICES.phrase, "The request has more than one possible response. The user-agent or user should choose one of them. There is no standardized way of choosing one of the responses."),

    301 : (HTTPStatus.MOVED_PERMANENTLY.phrase, "This response code means that the URI of the requested resource has been changed. Probably, the new URI would be given in the response."),

    302 : (HTTPStatus.FOUND.phrase, "This response code means that the URI of requested resource has been changed temporarily. New changes in the URI might be made in the future. Therefore, this same URI should be used by the client in future requests."),

    303 : (HTTPStatus.SEE_OTHER.phrase, "The server sent this response to direct the client to get the requested resource at another URI with a GET request."),

    304 : (HTTPStatus.NOT_MODIFIED.phrase, "This is used for caching purposes. It tells the client that the response has not been modified, so the client can continue to use the same cached version of the response."),

    305 : (HTTPStatus.USE_PROXY.phrase, "Was defined in a previous version of the HTTP specification to indicate that a requested response must be accessed by a proxy. It has been deprecated due to security concerns regarding in-band configuration of a proxy."),

    307 : (HTTPStatus.TEMPORARY_REDIRECT.phrase, "The server sends this response to direct the client to get the requested resource at another URI with same method that was used in the prior request. This has the same semantics as the 302 Found HTTP response code, with the exception that the user agent must not change the HTTP method used: If a POST was used in the first request, a POST must be used in the second request."),

    308 : (HTTPStatus.PERMANENT_REDIRECT.phrase, "This means that the resource is now permanently located at another URI, specified by the Location: HTTP Response header. This has the same semantics as the 301 Moved Permanently HTTP response code, with the exception that the user agent must not change the HTTP method used: If a POST was used in the first request, a POST must be used in the second request."),

    400 : (HTTPStatus.BAD_REQUEST.phrase, "This response means that server could not understand the request due to invalid syntax."),

    401 : (HTTPStatus.UNAUTHORIZED.phrase, "Although the HTTP standard specifies 'unauthorized', semantically this response means 'unauthenticated'. That is, the client must authenticate itself to get the requested response."),

    402 : (HTTPStatus.PAYMENT_REQUIRED.phrase, "This response code is reserved for future use. Initial aim for creating this code was using it for digital payment systems however this is not used currently."),

    403 : (HTTPStatus.FORBIDDEN.phrase, "The client does not have access rights to the content, i.e. they are unauthorized, so server is rejecting to give proper response. Unlike 401, the client's identity is known to the server."),

    404 : (HTTPStatus.NOT_FOUND.phrase, "The server can not find requested resource. In the browser, this means the URL is not recognized. In an API, this can also mean that the endpoint is valid but the resource itself does not exist. Servers may also send this response instead of 403 to hide the existence of a resource from an unauthorized client. This response code is probably the most famous one due to its frequent occurence on the web."),

    405 : (HTTPStatus.METHOD_NOT_ALLOWED.phrase, "The request method is known by the server but has been disabled and cannot be used. For example, an API may forbid DELETE-ing a resource. The two mandatory methods, GET and HEAD, must never be disabled and should not return this error code."),

    406 : (HTTPStatus.NOT_ACCEPTABLE.phrase, "This response is sent when the web server, after performing server-driven content negotiation, doesn't find any content following the criteria given by the user agent."),

    407 : (HTTPStatus.PROXY_AUTHENTICATION_REQUIRED.phrase, "This is similar to 401 but authentication is needed to be done by a proxy."),

    408 : (HTTPStatus.REQUEST_TIMEOUT.phrase, "This response is sent on an idle connection by some servers, even without any previous request by the client. It means that the server would like to shut down this unused connection. This response is used much more since some browsers, like Chrome, Firefox 27+, or IE9, use HTTP pre-connection mechanisms to speed up surfing. Also note that some servers merely shut down the connection without sending this message."),

    409 : (HTTPStatus.CONFLICT.phrase, "This response is sent when a request conflicts with the current state of the server."),

    410 : (HTTPStatus.GONE.phrase, "This response would be sent when the requested content has been permenantly deleted from server, with no forwarding address. Clients are expected to remove their caches and links to the resource. The HTTP specification intends this status code to be used for 'limited-time, promotional services'. APIs should not feel compelled to indicate resources that have been deleted with this status code."),

    411 : (HTTPStatus.LENGTH_REQUIRED.phrase, "Server rejected the request because the Content-Length header field is not defined and the server requires it."),

    412 : (HTTPStatus.PRECONDITION_FAILED.phrase, "The client has indicated preconditions in its headers which the server does not meet."),

    413 : (HTTPStatus.REQUEST_ENTITY_TOO_LARGE.phrase, "Request entity is larger than limits defined by server; the server might close the connection or return an Retry-After header field."),

    414 : (HTTPStatus.REQUEST_URI_TOO_LONG.phrase, "The URI requested by the client is longer than the server is willing to interpret."),

    415 : (HTTPStatus.UNSUPPORTED_MEDIA_TYPE.phrase, "The media format of the requested data is not supported by the server, so the server is rejecting the request."),

    416 : (HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE.phrase, "The range specified by the Range header field in the request can't be fulfilled; it's possible that the range is outside the size of the target URI's data."),

    417 : (HTTPStatus.EXPECTATION_FAILED.phrase, "This response code means the expectation indicated by the Expect request header field can't be met by the server."),

    418 : ("I'm a teapot", "The server refuses the attempt to brew coffee with a teapot."),

    421 : ("Misdirected Request", "The request was directed at a server that is not able to produce a response. This can be sent by a server that is not configured to produce responses for the combination of scheme and authority that are included in the request URI."),

    422 : (HTTPStatus.UNPROCESSABLE_ENTITY.phrase, "The request was well-formed but was unable to be followed due to semantic errors."),

    423 : (HTTPStatus.LOCKED.phrase, "The resource that is being accessed is locked."),

    424 : (HTTPStatus.FAILED_DEPENDENCY.phrase, "The request failed due to failure of a previous request."),

    426 : (HTTPStatus.UPGRADE_REQUIRED.phrase, "The server refuses to perform the request using the current protocol but might be willing to do so after the client upgrades to a different protocol. The server sends an Upgrade header in a 426 response to indicate the required protocol(s)."),

    428 : (HTTPStatus.PRECONDITION_REQUIRED.phrase, "The origin server requires the request to be conditional. Intended to prevent the 'lost update' problem, where a client GETs a resource's state, modifies it, and PUTs it back to the server, when meanwhile a third party has modified the state on the server, leading to a conflict."),

    429 : (HTTPStatus.TOO_MANY_REQUESTS.phrase, "The user has sent too many requests in a given amount of time ('rate limiting')."),

    431 : (HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE.phrase, "The server is unwilling to process the request because its header fields are too large. The request MAY be resubmitted after reducing the size of the request header fields."),

    451 : ("Unavailable For Legal Reasons", "The user requests an illegal resource, such as a web page censored by a government."),

    500 : (HTTPStatus.INTERNAL_SERVER_ERROR.phrase, "The server has encountered a situation it doesn't know how to handle."),

    501 : (HTTPStatus.NOT_IMPLEMENTED.phrase, "The request method is not supported by the server and cannot be handled. The only methods that servers are required to support (and therefore that must not return this code) are GET and HEAD."),

    502 : (HTTPStatus.BAD_GATEWAY.phrase, "This error response means that the server, while working as a gateway to get a response needed to handle the request, got an invalid response."),

    503 : (HTTPStatus.SERVICE_UNAVAILABLE.phrase, "The server is not ready to handle the request. Common causes are a server that is down for maintenance or that is overloaded. Note that together with this response, a user-friendly page explaining the problem should be sent. This responses should be used for temporary conditions and the Retry-After: HTTP header should, if possible, contain the estimated time before the recovery of the service. The webmaster must also take care about the caching-related headers that are sent along with this response, as these temporary condition responses should usually not be cached."),

    504 : (HTTPStatus.GATEWAY_TIMEOUT.phrase, "This error response is given when the server is acting as a gateway and cannot get a response in time."),

    505 : (HTTPStatus.HTTP_VERSION_NOT_SUPPORTED.phrase, "The HTTP version used in the request is not supported by the server."),

    506 : (HTTPStatus.VARIANT_ALSO_NEGOTIATES.phrase, "The server has an internal configuration error: transparent content negotiation for the request results in a circular reference."),

    507 : (HTTPStatus.INSUFFICIENT_STORAGE.phrase, "The server has an internal configuration error: the chosen variant resource is configured to engage in transparent content negotiation itself, and is therefore not a proper end point in the negotiation process."),

    508 : (HTTPStatus.LOOP_DETECTED.phrase, "The server detected an infinite loop while processing the request."),

    510 : (HTTPStatus.NOT_EXTENDED.phrase, "Further extensions to the request are required for the server to fulfill it."),

    511 : (HTTPStatus.NETWORK_AUTHENTICATION_REQUIRED.phrase, "The 511 status code indicates that the client needs to authenticate to gain network access."),
}


# Utility functions.
# .............................................................................

def http_code_meaning(status_code):
    '''Return a textual description of the given status_code value.'''
    if not isinstance(status_code, int):
        raise ValueError('Status code must be an integer')
    if not status_code in http_meanings:
        raise ValueError('Status code {} not recognized'.format(status_code))
    return http_meanings[status_code][1]
