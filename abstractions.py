import typing

from dataclasses import dataclass, field

from tornado.httputil import HTTPHeaders


@dataclass
class HTTPRequest:
    url: str
    path: str
    query: str
    method: str = 'GET'
    headers: HTTPHeaders = field(default_factory=HTTPHeaders)
    body: bytes = b''


@dataclass
class HTTPResponse:
    status_code: int = 500
    headers: HTTPHeaders = field(default_factory=HTTPHeaders)
    body: bytes = b''
    error: Exception = None


AppDelegate = typing.Callable[[HTTPRequest], typing.Coroutine[typing.Any, typing.Any, HTTPResponse]]

Middleware = typing.Callable[[AppDelegate], AppDelegate]
