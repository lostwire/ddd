from pyced.store import init as store_init
from pyced.aggregate import AggregateRoot, Event
from pyced.decorators import unpack_event_data, expect_new_aggregate

class Command(object):
    def __init__(self, name, data, headers):
        self._data = { 'name': name, 'data': data, 'headers': headers }

    @property
    def name(self):
        return self._data['name']

    @property
    def data(self):
        return self._data['data']

    @property
    def headers(self):
        return self._data['headers']
