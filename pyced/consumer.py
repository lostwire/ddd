import asyncio
import es
import time
loop = asyncio.get_event_loop()
id = '92b7bd9b-b646-4268-9560-192aa5d2ebf0'
def consumer(routing_key, body, headers):
    print(routing_key, body, headers)
class ProjectConsumer(es.MethodWrapper):
    def __init__(self, db):
        self._db = db
    def Created(self, id, headers, name):

c = es.Consumer(id, loop)
loop.run_until_complete(c.register_consumer('Project', consumer))
time.sleep(3)
loop.run_until_complete(c.consume())
