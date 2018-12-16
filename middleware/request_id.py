import functools
import uuid

import tornado.web

from abstractions import RequestHandlerDelegate, HTTPResponse

def request_id_middleware(delegate: RequestHandlerDelegate) -> RequestHandlerDelegate:
    @functools.wraps(delegate)
    async def wrapper(handler: tornado.web.RedirectHandler) -> HTTPResponse:
        request_id = handler.request.headers.get('X-Request-Id', str(uuid.uuid4()))
        handler.request_id = request_id
        response = await delegate(handler)
        response.headers['X-Request-Id'] = request_id

    return wrapper
