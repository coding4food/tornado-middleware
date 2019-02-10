import tornado.httputil

from abstractions import HTTPResponse


class HandlerWithDependency:
    def __init__(self, greeting: str):
        self.greeting = greeting

    async def __call__(self, request: tornado.httputil.HTTPServerRequest) -> HTTPResponse:
        name = request.query_arguments.get('name', [b''])[0].decode()
        return HTTPResponse(
            status_code=200,
            body='{greeting}, {name}'.format(greeting=self.greeting, name=name).encode()
        )
