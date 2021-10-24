import logging
from collections import AsyncIterable
from pathlib import Path

from aiohttp.web_app import Application
from asyncpgsa import PG
from asyncpgsa.transactionmanager import ConnectionTransactionContextManager
from sqlalchemy import Numeric, cast, func
from sqlalchemy.sql import Select

from plugins.config import cfg

CENSORED = '***'
DEFAULT_PG_URL = cfg.app.hosts.pg.url
MAX_QUERY_ARGS = 32767
MAX_INTEGER = 2147483647

pg_pool_min_size = 10
pg_pool_max_size = 10
PROJECT_PATH = Path(__file__).parent.parent.resolve()

log = logging.getLogger(__name__)


async def setup_pg(app: Application) -> PG:
    log.info('Connecting to database: %s', DEFAULT_PG_URL)

    app['pg'] = PG()
    await app['pg'].init(
        str(DEFAULT_PG_URL),
        min_size=pg_pool_min_size,
        max_size=pg_pool_max_size
    )
    await app['pg'].fetchval('SELECT 1')
    log.info('Connected to database %s', DEFAULT_PG_URL)

    try:
        yield
    finally:
        log.info('Disconnecting from database %s', DEFAULT_PG_URL)
        await app['pg'].pool.close()
        log.info('Disconnected from database %s', DEFAULT_PG_URL)


def rounded(column, fraction: int = 2):
    return func.round(cast(column, Numeric), fraction)


class SelectQuery(AsyncIterable):
    """
    Используется чтобы отправлять данные из PostgreSQL клиенту сразу после
    получения, по частям, без буфферизации всех данных.
    """
    PREFETCH = 1000

    slots = (
        'query', 'transaction_ctx', 'prefetch', 'timeout'
    )

    def __init__(self, query: Select,
                 transaction_ctx: ConnectionTransactionContextManager,
                 prefetch: int = None,
                 timeout: float = None):
        self.query = query
        self.transaction_ctx = transaction_ctx
        self.prefetch = prefetch or self.PREFETCH
        self.timeout = timeout

    async def __aiter__(self):
        async with self.transaction_ctx as conn:
            cursor = conn.cursor(self.query, prefetch=self.prefetch,
                                 timeout=self.timeout)
            async for row in cursor:
                yield row
