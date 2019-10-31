import functools

import pydec.exceptions

def unpack_event_data(callback):
    @functools.wraps(callback)
    def wrapper(obj, event):
        return callback(obj, **event.data)
    return wrapper

def expect_new_aggregate(callback):
    @functools.wraps(callback)
    def wrapper(obj, *args, **kwargs):
        if obj.version:
            raise pydec.exceptions.AggregateAlreadyInitialized()
        return callback(obj, *args, **kwargs)
    return wrapper
