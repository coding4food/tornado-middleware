import functools
import typing
from contextlib import asynccontextmanager

import tornado
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
        print('awaiting')
        self.handle_request()
        print('awaited')

    def on_connection_close(self):
        self._chunks = None

    @tornado.gen.coroutine
    def handle_request(self):
        response = yield self.delegate(self.request)
        reason = tornado.httputil.responses.get(response.status_code, 'Unknown')
        print('writing headers')
        yield self.request.connection.write_headers(
            tornado.httputil.ResponseStartLine('', response.status_code, reason),
            tornado.httputil.HTTPHeaders(response.headers),
            response.body)
        self.request.connection.finish()
        print('finished')
