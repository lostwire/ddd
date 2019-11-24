import os
import logging

import aiopg
import asyncio
import configparser

import pyced.api
import pyced.store
import pyced.saga.model

logger = logging.getLogger(__name__)

def init(config_file=None, loop=None):
    if not config_file:
        config_file = os.environ.get('CONFIG')
    config = configparser.ConfigParser()
    config.read(config_file)
    loop = asyncio.get_event_loop()
    db = loop.run_until_complete(aiopg.create_pool(loop=loop,**dict(config.items('db'))))
    store = pyced.store.init(config.get('store', 'url'), loop=loop)
    loop.run_until_complete(store.register(config.get('store','username')))
    loop.run_until_complete(store.login(config.get('store','username')))
    model = pyced.saga.model.Model(db)
    logger.info("Saga server initialized")
    return Server(loop, model, store, config.get('general', 'api_url'))

class Server(object):
    def __init__(self, loop, model, store, api_url):
        self._loop = loop
        self._model = model
        self._store = store
        self._api_url = api_url
        self._handlers = {}

    def get_api(self, saga):
        """ Return pyced.api object for saga instance """
        return pyced.api.init(self._api_url, { 'saga': saga_id })

    def initialize(self):
        """ Initialize saga tables """
        self._loop.run_until_complete(self._model.initialize())

    def register(self, saga):
        for event_name in saga.started_by():
            aggregate, name = event_name.split('.')
            if not aggregate in self._handlers:
                self._handlers[aggregate] = {}
                self._loop.run_until_complete(self._store.subscribe(aggregate))
            if not name in self._handlers[aggregate]:
                self._handlers[aggregate][name] = []
            self._handlers[aggregate][name].append(saga)
            logger.info("Registered event handler %s in %s", event_name, aggregate)

    async def __call__(self, event):
        aggregate, name = event.name.split('.')
    async def on_event(self, event):
        logger.info("Received event %s", event.name)
        aggregate, name = event.name.split('.')
        if aggregate in self._handlers and name in self._handlers[aggregate]:
            for handler in self._handlers[aggregate][name]:
                logger.info("Calling method %s at aggregate %s", name, aggregate)
                handler = handler()
                await handler(pyced.api.init(self._api_url), event)

    def run(self):
        self._loop.run_until_complete(self._store.consume(self.on_event))
