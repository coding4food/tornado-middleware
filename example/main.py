import asyncio

from tornado.httpserver import HTTPServer

from core import PipelineRouter, PipelineDelegate
from example.handlers.bound import bound
from example.handlers.throwing import throw
from example.handlers.wrapped import wrapped

if __name__ == "__main__":
    HTTPServer(PipelineRouter([
        ('/bound', PipelineDelegate, {'delegate': bound}),
        ('/throw', PipelineDelegate, {'delegate': throw}),
        ('.*', PipelineDelegate, {'delegate': wrapped})
    ])).listen(5000)

    loop = asyncio.get_event_loop()
    loop.run_forever()
