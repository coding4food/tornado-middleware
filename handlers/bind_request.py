import functools
import json
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import get_type_hints, Any, MutableSet

from marshmallow.schema import SchemaMeta

from abstractions import HTTPRequest, HTTPResponse, AppDelegate


class RequestArgumentResolver(metaclass=ABCMeta):
    @abstractmethod
    def can_resolve_type(self, arg_type: type) -> bool:
        pass

    @abstractmethod
    def resolve(self, request: HTTPRequest, arg_name: str, arg_type: type) -> Any:
        pass


ARGUMENT_RESOLVERS: MutableSet[RequestArgumentResolver] = set()


def register_resolver(resolver: RequestArgumentResolver):
    if not isinstance(resolver, RequestArgumentResolver):
        raise TypeError

    ARGUMENT_RESOLVERS.add(resolver)


@dataclass
class Header:
    name: str


Json = object()


class SchemaResolver(RequestArgumentResolver):
    def can_resolve_type(self, arg_type: type):
        return isinstance(arg_type, SchemaMeta)

    def resolve(self, request: HTTPRequest, arg_name: str, arg_type: type):
        result, _ = arg_type(strict=True).loads(request.body)
        return result


class JsonResolver(RequestArgumentResolver):
    ALLOWED_METHODS = ['POST', 'PUT', 'PATCH']

    def can_resolve_type(self, arg_type: type):
        return arg_type is Json

    def resolve(self, request: HTTPRequest, arg_name: str, arg_type: type):
        if request.headers.get('Content-Type') == 'application/json' and request.method.upper() in self.ALLOWED_METHODS:
            return json.loads(request.body)

        raise ArgumentResolveError(arg_type)


class HeaderResolver(RequestArgumentResolver):
    def can_resolve_type(self, arg_type: type):
        return isinstance(arg_type, Header)

    def resolve(self, request: HTTPRequest, arg_name: str, arg_type: Header):
        return request.headers.get(arg_type.name, None)


class ArgumentResolveError(Exception):
    def __init__(self, arg_type: type):
        super().__init__()
        self.arg_type = arg_type

    def __str__(self):
        return "Unexpected argument type: {arg_type}".format(arg_type=self.arg_type)


def _resolve_argument_value(request: HTTPRequest, arg_name, arg_type):
    for resolver in ARGUMENT_RESOLVERS:
        if resolver.can_resolve_type(arg_type):
            return resolver.resolve(request, arg_name, arg_type)
    else:
        raise ArgumentResolveError(arg_type)


def bind_arguments(func) -> AppDelegate:
    """
    Binds arguments of passed function deriving them from type hinsts and `HTTPServerRequest`.
    :param func: a request handling function with optionally declared arguments, the first argument is request
    :return: An `AppDelegate` deriving inner handler arguments from type hints and `HTTPServerRequest`.
    """
    @functools.wraps(func)
    async def wrapper(request: HTTPRequest) -> HTTPResponse:
        annotations = get_type_hints(func)
        annotations.pop('return', None)

        kwargs = {arg_name: _resolve_argument_value(request, arg_name, arg_type)
                  for arg_name, arg_type in annotations.items()}

        return await func(request, **kwargs)

    return wrapper


register_resolver(SchemaResolver())
register_resolver(JsonResolver())
register_resolver(HeaderResolver())


__all__ = ['bind_arguments', 'Json', 'Header', 'RequestArgumentResolver', 'register_resolver']
