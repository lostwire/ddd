import aiopg
import configparser

import pyced.store

def init():
    return Server()

class Server(object):
    def __init__(self, db, store):
        self._db = db
        self._store = store
        self._handlers = {}

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
