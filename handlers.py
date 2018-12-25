import asyncio
import functools
import typing
from contextlib import asynccontextmanager

import tornado.httputil
import tornado.routing

from abstractions import AppDelegate, HTTPResponse
from middleware.request_id import request_id_middleware


class CustomRouter(tornado.routing.ReversibleRuleRouter):
    def get_target_delegate(self, target, request, **target_params):
        target_kwargs = target_params.get('target_kwargs')
        return CustomDelegate(request, **target_kwargs)


class CustomDelegate(tornado.httputil.HTTPMessageDelegate):
    def __init__(self, request: tornado.httputil.HTTPServerRequest, delegate: AppDelegate, *args, **kwargs):
        self.request = request
        self.delegate = delegate
        self._chunks = []

    def data_received(self, chunk):
        self._chunks.append(chunk)

    def finish(self):
        self.request.body = b''.join(self._chunks)
        self.request._parse_body()
        asyncio.create_task(self.handle_request())

    def on_connection_close(self):
        self._chunks = None

    async def handle_request(self):
        response = await self.delegate(self.request)
        reason = tornado.httputil.responses.get(response.status_code, 'Unknown')
        await self.request.connection.write_headers(
            tornado.httputil.ResponseStartLine('', response.status_code, reason),
            tornado.httputil.HTTPHeaders(response.headers),
            response.body)
        self.request.connection.finish()
