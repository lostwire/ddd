""" Saga model, DB interface """

import json
import logging

import pyced.saga.sql

logger = logging.getLogger(__name__)

class Model(object):
    def __init__(self, db):
        self._db = db

    async def initialize(self):
        """ Create all required tables """
        await self.run_queries(pyced.saga.sql.INITIALIZE_SAGA)

    async def reinitialize(self):
        """ Re-create all required tables """
        await self.run_queries(pyced.saga.sql.REINITIALIZE_SAGA)

    async def run_queries(self, queries):
        with (await self._db.cursor()) as cur:
            for query in queries:
                await cur.execute(query)
                logger.info(query)

    async def get_data(self, id):
        with (await self._db.cursor()) as cur:
            await cur.execute("SELECT data FROM saga WHERE id = %s", [id])
            return json.loads(await cur.fetchone()[0])

    async def set_data(self, id, data):
        with (await self._db.cursor()) as cur:
            data = json.dumps(data)
            await cur.execute("UPDATE saga SET data = %s WHERE id = %s", [data, id])
            logger.info("Saving saga data")
