import logging
import functools

import aiohttp.web

logger = logging.getLogger(__name__)

def init(**args):
    return Server(aiohttp.web.Application(), args)

async def json_output(f, *args, **kwargs):
    return aiohttp.web.json_response(await f(*args, **kwargs))

class Server(object):
    def __init__(self, app, args):
        self._app = app
        self._args = args
    def register(self, path, handler):
        logger.info("Registering handler for %s", path)
        self._app.router.add_get(path, functools.partial(json_output, handler))
    def add_on_startup(self, callback):
        self._app.on_startup.append(callback)
    def add_on_cleanup(self, callback):
        self._app.on_cleanup.append(callback)
    def run(self):
        logger.info("Starting server")
        aiohttp.web.run_app(self._app, **self._args)
