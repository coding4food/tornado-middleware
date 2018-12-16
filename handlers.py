import typing

import tornado.web

from abstractions import Middleware
from middleware.request_id import request_id_middleware


class BaseRequestHandler(tornado.web.RequestHandler):
    MIDDLEWARE: typing.List[Middleware] = [
        request_id_middleware
    ]