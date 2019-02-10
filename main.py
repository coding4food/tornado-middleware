import asyncio

from tornado.httpserver import HTTPServer

from abstractions import HTTPResponse
from core import PipelineRouter, PipelineDelegate
from middleware.request_id import request_id_middleware


@request_id_middleware
async def foo(request):
    return HTTPResponse(
        status_code=200,
        headers={'Content-Type': 'application/json', 'Foo': 'bar'},
        body=b'{"foo": "bar"}')


async def throw(request):
    1 / 0


if __name__ == "__main__":
    HTTPServer(PipelineRouter([
        ('/throw', PipelineDelegate, {'delegate': throw}),
        ('.*', PipelineDelegate, {'delegate': foo})
    ])).listen(5000)

    loop = asyncio.get_event_loop()
    loop.run_forever()
