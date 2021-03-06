import functools

import tornado.httputil

from abstractions import HTTPResponse
from handlers.bind_request import ArgumentResolveError


def response_for_exception(request: tornado.httputil.HTTPServerRequest, error: Exception) -> HTTPResponse:
    if isinstance(error, ArgumentResolveError):
        return HTTPResponse(status_code=400, error=error)

    return HTTPResponse(status_code=500, error=error)


def convert_exception_to_response(func):
    @functools.wraps(func)
    async def wrapper(request: tornado.httputil.HTTPServerRequest) -> HTTPResponse:
        try:
            return await func(request)
        except Exception as e:
            return response_for_exception(request, e)

    return wrapper
