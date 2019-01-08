import functools
import uuid

import tornado.httputil

from abstractions import AppDelegate, HTTPResponse


def request_id_middleware(delegate: AppDelegate) -> AppDelegate:
    @functools.wraps(delegate)
    async def wrapper(request: tornado.httputil.HTTPServerRequest) -> HTTPResponse:
        request_id = request.headers.get('X-Request-Id', str(uuid.uuid4()))
        request.request_id = request_id
        response = await delegate(request)
        response.headers['X-Request-Id'] = request_id

        return response

    return wrapper
