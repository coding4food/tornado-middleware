import typing

from tornado.httputil import HTTPServerRequest
from tornado.web import RequestHandler

from collections import namedtuple

HTTPResponse = namedtuple('HTTPResponse', ['status_code', 'headers', 'body'])

AppDelegate = typing.Callable[[HTTPServerRequest], typing.Coroutine[typing.Any, typing.Any, HTTPResponse]]
RequestHandlerDelegate = typing.Callable[[RequestHandler], typing.Coroutine[typing.Any, typing.Any, HTTPResponse]]

Middleware = typing.Callable[[AppDelegate], AppDelegate]
RequestHandlerMiddleware = typing.Callable[[RequestHandlerDelegate], RequestHandlerDelegate]
