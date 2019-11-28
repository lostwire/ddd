import logging
import functools

import aiohttp.web

logger = logging.getLogger(__name__)

def init(loop=None, **args):
    if not loop:
        loop = asyncio.get_event_loop()
    return Server(aiohttp.web.Application(loop=loop), args)

async def json_output(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return aiohttp.web.json_response(f(*args, **kwargs))
    return wrapper

class Server(object):
    def __init__(self, app, args):
        self._app = app
        self._args = args

    def register(self, path, handler):
        logger.info("Registering handler for %s", path)
        self._app.router.add_get(path, functools.partial(json_output, handler))

    def run(self):
        logger.info("Starting server")
        aiohttp.web.run_app(self._app, **self._args)

class App(object):
    def __init__(self, store, loop):
        self._jar = jar
        self._loop = loop
        self._store = store

    async def on_event(self, event):
        aggregate, method = event.name.split('.')
        logger.info("Event arrived %s", event)
        try:
            if aggregate in self._jar:
                await getattr(self._jar[aggregate], method)(event)
        except Exception as e:
            logger.error(str(e))

    def run(self):
        self._loop.run_until_complete(self._store.consume(self.on_event))
