import typing

from dataclasses import dataclass, field

from tornado.httputil import HTTPServerRequest


@dataclass
class HTTPResponse:
    status_code: int = 500
    headers: dict = field(default_factory=dict)
    body: bytes = b''
    error: Exception = None


AppDelegate = typing.Callable[[HTTPServerRequest], typing.Coroutine[typing.Any, typing.Any, HTTPResponse]]

Middleware = typing.Callable[[AppDelegate], AppDelegate]
