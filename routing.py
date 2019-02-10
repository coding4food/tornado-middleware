from core import PipelineDelegate


class Router:
    _routes = []

    def __call__(self, path: str, name=None):
        def wrapper(func):
            self._routes.append((path, PipelineDelegate, {'delegate': func}, name))
            return func

        return wrapper

    def get_routes(self):
        return tuple(self._routes)


route = Router()
