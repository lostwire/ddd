import sys
import logging

from pyced.aggregate import AggregateRoot, Event
from pyced.decorators import unpack_event_data, expect_new_aggregate
from pyced.store import init as store_init

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

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
