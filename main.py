import asyncio

from tornado.web import Application

if __name__ == "__main__":
    app = Application()
    app.listen(5000)

    loop = asyncio.get_event_loop()
    loop.run_forever()