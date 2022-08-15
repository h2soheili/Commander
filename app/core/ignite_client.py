from typing import List, Any, Coroutine

from pyignite import AioClient
from pyignite.exceptions import SocketError
from pyignite.datatypes.cache_config import CacheMode, CacheAtomicityMode
from pyignite.datatypes.prop_codes import PROP_NAME, PROP_CACHE_MODE, PROP_BACKUPS_NUMBER, PROP_CACHE_ATOMICITY_MODE

from app.command import setup_database_queries
from app.utils.global_log import log_factory

logger = log_factory.get_logger(__name__)


class IgniteClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.client = AioClient()
        self.cache = self.client.get_or_create_cache({
            PROP_NAME: 'cache',
            PROP_CACHE_MODE: CacheMode.REPLICATED,
            PROP_BACKUPS_NUMBER: 2,
            PROP_CACHE_ATOMICITY_MODE: CacheAtomicityMode.TRANSACTIONAL
        })

    async def connect(self):
        await self.client.connect(self.host, self.port)

    async def sync_data(self):
        pass

    async def migrate(self):
        pass

    async def initial_setup(self):
        # create tables/indexes
        for query in setup_database_queries():
            await self.client.sql(query)

    async def query(self, query: str, query_args: List[Any]) -> list:
        res = []
        try:
            async with self.client.sql(query, query_args=query_args) as cursor:
                async for row in cursor:
                    res.append(row)
                return res
        except (OSError, SocketError) as e:
            print(f'IgniteClient query error: {e}')