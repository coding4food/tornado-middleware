import functools

from tornado.routing import PathMatches


class MethodMatches(PathMatches):
    """Matches request path and maethod."""
    def __init__(self, path_pattern, method: str):
        super().__init__(path_pattern)
        self.method = method.upper()

    def match(self, request):
        result = super().match(request)

        if result is not None:
            if request.method.upper() != self.method:
                return None

        return result


class Router:
    _routes = []

    def __call__(self, path: str, name=None, method: str = None):
        def wrapper(func):
            if method is None:
                self._routes.append((path, func, name))
            else:
                self._routes.append((MethodMatches(path, method), func, name))
            return func

        return wrapper

    get = functools.partialmethod(__call__, method='GET')
    post = functools.partialmethod(__call__, method='POST')
    put = functools.partialmethod(__call__, method='PUT')
    patch = functools.partialmethod(__call__, method='PATCH')
    delete = functools.partialmethod(__call__, method='DELETE')

    def get_routes(self):
        return tuple(self._routes)


route = Router()
