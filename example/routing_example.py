import asyncio
import functools
import json
import logging

import tornado.httputil
from tornado.httpserver import HTTPServer

from abstractions import HTTPResponse, AppDelegate
from core import PipelineRouter
from handlers.bind_request import Json, Header, bind_arguments
from middleware.request_id import request_id_middleware
from routing import route

logging.basicConfig(level=logging.DEBUG)


@route('/foo')
async def foo(request) -> HTTPResponse:
    return HTTPResponse(
        status_code=200,
        body=b'foo'
    )


@route('/broken')
async def broken(request) -> HTTPResponse:
    1 / 0


@route('/bound')
@bind_arguments
async def bound(request, data: Json, message_id: Header('X-Request-Id')) -> HTTPResponse:
    data.update({'message_id': message_id})
    return HTTPResponse(
        status_code=200,
        headers={'Content-Type': 'application/json'},
        body=json.dumps(data).encode()
    )


def logging_middleware(func: AppDelegate) -> AppDelegate:
    @functools.wraps(func)
    async def wrapper(request: tornado.httputil.HTTPServerRequest) -> HTTPResponse:
        response = await func(request)

        logging.debug('{method} {path} {status} {error}'.format(
            method=request.method.upper(),
            path=request.uri,
            status=response.status_code,
            error=response.error
        ))

        return response

    return wrapper


if __name__ == '__main__':
    HTTPServer(PipelineRouter(
        route.get_routes(),
        [logging_middleware, request_id_middleware]
    )).listen(5050)

    loop = asyncio.get_event_loop()
    loop.run_forever()
