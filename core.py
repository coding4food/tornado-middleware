import typing

import tornado.web

import abstractions
from middleware.exception import convert_exception_to_response


class BaseHandler(tornado.web.RequestHandler):
    delegate: abstractions.AppDelegate
    request_handler: abstractions.AppDelegate

    def initialize(self, **kwargs):
        delegate = kwargs.pop('delegate')

        if not callable(delegate):
            raise ValueError('delegate must be callable')

        self.delegate = delegate
        self.request_handler = convert_exception_to_response(delegate)

    def _make_request(self) -> abstractions.HTTPRequest:
        return abstractions.HTTPRequest(
            url=self.request.uri,
            path=self.request.path,
            query=self.request.query,
            method=self.request.method,
            headers=dict(self.request.headers),
            body=self.request.body
        )

    def _write_response(self, response: abstractions.HTTPResponse):
        self.set_status(response.status_code)

        for k, v in response.headers.items():
            self.set_header(k, v)

        self.finish(response.body)

    async def _process_request(self, *args, **kwargs):
        response = await self.request_handler(self._make_request())

        self._write_response(response)

    async def get(self, *args, **kwargs):
        await self._process_request(*args, **kwargs)

    async def post(self, *args, **kwargs):
        await self._process_request(*args, **kwargs)


Route = typing.Tuple[str, abstractions.AppDelegate]


class TornadoService:
    routes: typing.List[Route]

    def __init__(self, routes: typing.List[Route]):
        if not isinstance(routes, (list, tuple)):
            raise ValueError('routes')

        self.routes = routes

    def make_application(self, **settings) -> tornado.web.Application:
        handlers = [(path, BaseHandler, dict(delegate=delegate), next(iter(name), None)) for path, delegate, *name in self.routes]
        return tornado.web.Application(handlers, **settings)

    def run(self, port, host: str = "", **settings):
        app = self.make_application(**settings)
        app.listen(port, host)
