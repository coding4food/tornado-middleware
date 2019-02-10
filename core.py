import asyncio
import collections
from typing import Sequence

import tornado.httputil
import tornado.routing

from abstractions import AppDelegate, Middleware
from middleware.exception import convert_exception_to_response


class PipelineRouter(tornado.routing.ReversibleRuleRouter):
    def __init__(self, rules=None, middleware: Sequence[Middleware] = None):
        super().__init__(rules)
        self.middleware = middleware if isinstance(middleware, collections.Sequence) else []

    def get_target_delegate(self, target, request, **target_params):
        target_kwargs = target_params.get('target_kwargs')
        return PipelineDelegate(request, middleware=self.middleware, **target_kwargs)


class PipelineDelegate(tornado.httputil.HTTPMessageDelegate):
    request_handler: AppDelegate

    def __init__(self, request: tornado.httputil.HTTPServerRequest, delegate: AppDelegate,
                 middleware: Sequence[Middleware], *args, **kwargs):
        self.request = request
        self.delegate = delegate
        self.middleware = middleware
        self._chunks = []

        self.load_middleware()

    def load_middleware(self):
        self.request_handler = convert_exception_to_response(self.delegate)

        for middleware in reversed(self.middleware):
            handler = middleware(self.request_handler)
            self.request_handler = convert_exception_to_response(handler)

    def data_received(self, chunk):
        self._chunks.append(chunk)

    def finish(self):
        self.request.body = b''.join(self._chunks)
        self.request._parse_body()
        asyncio.create_task(self.handle_request())

    def on_connection_close(self):
        self._chunks = None

    async def handle_request(self):
        response = await self.request_handler(self.request)
        reason = tornado.httputil.responses.get(response.status_code, 'Unknown')
        await self.request.connection.write_headers(
            tornado.httputil.ResponseStartLine('', response.status_code, reason),
            tornado.httputil.HTTPHeaders(response.headers),
            response.body)
        self.request.connection.finish()
