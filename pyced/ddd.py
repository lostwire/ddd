import inspect

from aggregate import Event, Snapshot, AggregateRoot

class Saga(dict):
    def __init__(self, api):
        self._api = api

    @classmethod
    def started_by(cls):
        output = []
        for member in inspect.getmembers(cls, inspect.isfunction):
            function_name = member[0]
            if function_name.startswith('handle_'):
                output.append(function_name.split('_', 1)[-1].replace('_','.'))
        return output
