import sys
import functools

class AggregateRoot(dict):
    def __init__(self, id):
        self._data = {'id': id, 'version': 0}

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
        raise event(kwargs, headers, event_name)

    def apply(self, events):
        for event in events:
            method_name = 'apply_' + event.name
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
