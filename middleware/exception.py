import functools

import tornado.httputil

from abstractions import HTTPResponse


def response_for_exception(request: tornado.httputil.HTTPServerRequest, error: Exception) -> HTTPResponse:
    return HTTPResponse(status_code=500, error=error)


def convert_exception_to_response(func):
    @functools.wraps(func)
    async def wrapper(request: tornado.httputil.HTTPServerRequest) -> HTTPResponse:
        try:
            return await func(request)
        except Exception as e:
            return response_for_exception(request, e)

    return wrapper
