import uuid
import atexit
import asyncio
import functools

import aiohttp
import aiohttp.web

import pyced.store

def init(store_url, loop=None):
    if not loop:
        loop = asyncio.get_event_loop()
    app = aiohttp.web.Application(loop=loop)
    store = pyced.store.init(store_url, loop)
    return Server(app, store, loop)

async def wrapper(store, aggregate_class, req):
    method = req.match_info['method']
    response = aiohttp.web.Response(text='OK')
    if method.startswith('create'):
        id = str(uuid.uuid4())
        response.headers['Stream'] = id
    else:
        id = req.headers['id']
    print(id)
    aggregate = aggregate_class(id)
    stream = store.get_stream(id)
    await aggregate.apply(stream)
    data = await req.post()
    try:
        getattr(aggregate, method)(**data)
    except pyced.aggregate.Event as e:
        headers = { 'stream': id }
        if 'Version' in req.headers:
            headers['version'] = req.headers['version']
        e.headers.update(headers)
        await store.add_event(e)
    return response

class Server(object):
    def __init__(self, app, store, loop):
        self._jar = {}
        self._app = app
        self._loop = loop
        self._store = store

    def register(self, aggregate):
        name = aggregate.get_name()
        self._jar[name] = aggregate
        callback = functools.partial(wrapper, self._store, aggregate)
        self._app.router.add_post('/'+name+'/{method}', callback)

    def run(self):
        runner = aiohttp.web.AppRunner(self._app)
        self._loop.run_until_complete(runner.setup())
        site = aiohttp.web.TCPSite(runner, '0.0.0.0', 8082)
        self._loop.run_until_complete(site.start())
        try:
            self._loop.run_forever()
        except KeyboardInterrupt:
            print("Stopped")
