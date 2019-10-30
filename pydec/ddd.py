class AggregateRoot(dict):
    def __init__(self, id):
        self._data = {'id': id, 'version': 0}

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]

    def _raise(self, name, **kwargs):
        pass

    def apply(self, events):
        for event in events:
            method_name = 'apply_' + event.name
            getattr(self, method_name)(**event.data)

    def snapshot(self):
        raise Snapshot(**self)

    def apply_Snapshot(self, **kwargs):
        self.update(kwargs)

class Event(Exception):
    def __init__(self, name, data, headers):
        self._data = {'name':None,'data':None}
        self.data = kwargs

    def __name__(self):
        return self.__class__.__name__

    @property
    def name(self):
        return self._data['name']

    @property
    def data(self):
        return self._data

    @data.setter
    def set_data(self, value):
        self._data['data'] = value

class CustomEvent(Event):
    def __init__(self, name, data, headers):
        self.__name__ = name
        self.__data__ = data
        self.__headers__ = headers

class Snapshot(Event):
    pass
