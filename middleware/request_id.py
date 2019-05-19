import functools
import uuid

from abstractions import AppDelegate, HTTPResponse, HTTPRequest


def request_id_middleware(delegate: AppDelegate) -> AppDelegate:
    @functools.wraps(delegate)
    async def wrapper(request: HTTPRequest) -> HTTPResponse:
        request_id = request.headers.get('X-Request-Id', str(uuid.uuid4()))
        request.request_id = request_id
        response = await delegate(request)
        response.headers['X-Request-Id'] = request_id

        return response

    return wrapper
