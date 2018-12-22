import typing

from dataclasses import dataclass, field

from tornado.httputil import HTTPServerRequest

from collections import namedtuple

@dataclass
class HTTPResponse:
    status_code: int = 500
    headers: dict = field(default_factory=dict)
    body: bytes = b''

AppDelegate = typing.Callable[[HTTPServerRequest], typing.Coroutine[typing.Any, typing.Any, HTTPResponse]]

Middleware = typing.Callable[[AppDelegate], AppDelegate]
