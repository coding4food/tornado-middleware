import urllib.parse

from abstractions import HTTPResponse, HTTPRequest


class HandlerWithDependency:
    def __init__(self, greeting: str):
        self.greeting = greeting

    async def __call__(self, request: HTTPRequest) -> HTTPResponse:
        query = urllib.parse.parse_qs(request.query)
        name = query.get('name')[0]
        return HTTPResponse(
            status_code=200,
            body='{greeting}, {name}'.format(greeting=self.greeting, name=name).encode()
        )
