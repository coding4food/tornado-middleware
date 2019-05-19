import typing

from dataclasses import dataclass, field


@dataclass
class HTTPRequest:
    url: str
    path: str
    query: str
    method: str = 'GET'
    headers: dict = field(default_factory=dict)
    body: bytes = b''


@dataclass
class HTTPResponse:
    status_code: int = 500
    headers: dict = field(default_factory=dict)
    body: bytes = b''
    error: Exception = None


AppDelegate = typing.Callable[[HTTPRequest], typing.Coroutine[typing.Any, typing.Any, HTTPResponse]]

Middleware = typing.Callable[[AppDelegate], AppDelegate]
