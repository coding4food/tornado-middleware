import asyncio

from core import TornadoService
from example.handlers.bound import bound
from example.handlers.dependency import HandlerWithDependency
from example.handlers.throwing import throw
from example.handlers.wrapped import wrapped

if __name__ == "__main__":
    routes = [
        ('/hello', HandlerWithDependency('hello')),
        ('/bound', bound),
        ('/throw', throw),
        ('.*', wrapped)
    ]

    TornadoService(routes).run(5000)

    loop = asyncio.get_event_loop()
    loop.run_forever()
