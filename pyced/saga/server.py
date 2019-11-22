import aiopg
import asyncio
import logging
import configparser

import pyced.api
import pyced.store
import pyced.saga.model

logger = logging.getLogger(__name__)

def init(config_file, loop=None):
    config = configparser.ConfigParser()
    config.read(config_file)
    loop = asyncio.get_event_loop()
    db = loop.run_until_complete(aiopg.create_pool(loop=loop,**dict(config.items('db'))))
    store = pyced.store.init(config.get('store', 'url'), loop=loop)
    model = pyced.saga.Model(db)
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
            aggregate,  = event_name.split('.')
            if not aggregate in self._handlers:
                self._store.subscribe(aggregate)
            if not event_name in self._handlers:
                self._handlers[event_name] = []
            self._handlers[event_name].append(saga)

    def __call__(self, event):
        aggregate, name = event.name.split('.')

    def run(self):
        self._store.consume(self)
