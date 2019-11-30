""" Classes and functions for managing aggregates """

import uuid
import atexit
import asyncio
import logging
import functools

import aiohttp
import aiohttp.web

import pyced.ddd
import pyced.store

logger = logging.getLogger(__name__)

def init(store_url, loop=None):
    if not loop:
        loop = asyncio.get_event_loop()
    app = aiohttp.web.Application(loop=loop)
    store = pyced.store.init(store_url, loop)
    return Server(app, store, loop)

async def wrapper(store, aggregate_class, req):
    """ Translates HTTP request into aggregate method call """
    method = req.match_info['method']
    response = aiohttp.web.Response(text='OK')
    if method.startswith('create'):
        id = str(uuid.uuid4())
        response.headers['Stream'] = id
    else:
        id = req.headers['id']
    aggregate = aggregate_class(id)
    stream = store.get_stream(id)
    await aggregate.apply(stream)
    data = await req.post()
    logger.info("Executing command %s with args %s", method, data)
    try:
        getattr(aggregate, method)(**data)
    except pyced.ddd.Event as e:
        e.headers['stream'] = id
        await store.add_event(e)
    return response

class Server(object):
    """ Aggregate registry
        Example:
        
        import pyced.ddd
        import pyced.command
        
        class User(pyced.ddd.AggregateRoot):
            def create(self, name):
                self.throw('UserCreated', name=name)
            def apply_UserCreated(self, name):
                self['name'] = name
                
        server = pyced.command.init()
        server.register(User)
        server.run()
    """
    def __init__(self, app, store, loop):
        self._app = app
        self._loop = loop
        self._store = store

    def register(self, aggregate):
        """ Add aggregate to the pool """
        name = aggregate.get_name()
        callback = functools.partial(wrapper, self._store, aggregate)
        self._app.router.add_post('/'+name+'/{method}', callback)
        logger.info("Adding %s to the server", name)

    def run(self):
        runner = aiohttp.web.AppRunner(self._app)
        self._loop.run_until_complete(runner.setup())
        site = aiohttp.web.TCPSite(runner, '0.0.0.0', 8082)
        self._loop.run_until_complete(site.start())
        try:
            self._loop.run_forever()
        except KeyboardInterrupt:
            print("Stopped")
