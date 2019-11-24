import sys
import inspect
import logging
import functools

logger = logging.getLogger(__name__)

class AggregateRoot(dict):
    def __init__(self, id):
        self._data = {'id': id, 'version': 0}

    @classmethod
    def get_name(cls):
        if hasattr(cls, '__aggregate_name__'):
            return cls.__aggregate_name__
        return cls.__name__

    @property
    def name(self):
        return self.get_name()

    @property
    def id(self):
        return self._data['id']

    @property
    def version(self):
        return self._data['version']

    def throw(self, event_name, **kwargs):
        module = sys.modules[self.__module__]
        if hasattr(module, event_name):
            event = getattr(module, event_name)
        else:
            event = Event
        headers = {
            'version': self.version + 1,
            'stream': self.id
        }
        event_name = '.'.join((self.name, event_name))
        raise event(kwargs, headers, event_name)

    async def apply(self, events):
        async for event in events:
            method_name = 'apply_' + event.name.split('.')[-1]
            if hasattr(self, method_name):
                getattr(self, method_name)(event)
            else:
                self.update(event.data)
            self._data['version'] = self._data['version'] + 1

    def snapshot(self):
        raise Snapshot(self, {})

    def apply_Snapshot(self, **kwargs):
        self.update(kwargs)

class Event(Exception):
    def __init__(self, data, headers, name=None):
        self._data = {'name':name, 'data':data, 'headers': headers}

    @property
    def name(self):
        if self._data['name']:
            return self._data['name']
        return self.__class__.__name__

    @property
    def data(self):
        return self._data['data']

    @property
    def headers(self):
        return self._data['headers']

class Snapshot(Event):
    pass

class Saga(dict):
    @classmethod
    def get_name(cls):
        if hasattr(cls, '__aggregate_name__'):
            return cls.__aggregate_name__
        return cls.__name__

    @classmethod
    def started_by(cls):
        output = []
        for member in inspect.getmembers(cls, inspect.isfunction):
            function_name = member[0]
            if function_name.startswith('handle_'):
                output.append(function_name.split('_', 1)[-1].replace('_','.'))
        return output

    @property
    def name(self):
        return self.get_name()

    async def __call__(self, api, event):
        method_name = 'handle_' + event.name.replace('.','_')
        logger.info("calling %s", method_name)
        if hasattr(self, method_name):
            await getattr(self, method_name)(api, event)
