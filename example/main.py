import asyncio

from core import TornadoService
from example.handlers.bound import bound
from example.handlers.dependency import HandlerWithDependency
from example.handlers.throwing import throw
from example.handlers.wrapped import wrapped
from middleware import request_id

if __name__ == "__main__":
    routes = [
        ('/hello', HandlerWithDependency('hello')),
        ('/bound', bound),
        ('/throw', throw),
        ('.*', wrapped)
    ]

    TornadoService(routes, [request_id.request_id_middleware]).run(5000)

    loop = asyncio.get_event_loop()
    loop.run_forever()
