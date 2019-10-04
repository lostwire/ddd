class AggregateRoot(dict):
    def apply(self, events):
        for event in events:
            getattr(self, 'apply_' + event.__class__.__name__)(**event.get_data())
    def snapshot(self):
        raise Snapshot(**self)
    def apply_Snapshot(self, **kwargs):
        self.update(kwargs)

class Event(Exception):
    def __init__(self, **kwargs):
        self._data = kwargs
    def get_data(self):
        return self._data

class Snapshot(Event):
    pass
