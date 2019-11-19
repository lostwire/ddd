import asyncio

import pyced.store

def init(store_url):
    loop = asyncio.get_event_loop()
    store = pyced.store.init(store_url)
    loop.run_until_complete(store.register('username'))
    loop.run_until_complete(store.login('username'))
    return Server(store, loop)

class Server(object):
    def __init__(self, store, loop):
        self._store = store
        self._loop = loop
        self._jar = {}
    def subscribe(self, name, handler):
        self._jar[name] = handler
        self._loop.run_until_complete(self._store.subscribe(name))
    async def consume(self, event):
        print(event.name, event.data)
    def run(self):
        self._store.consume_sync(self.consume)
