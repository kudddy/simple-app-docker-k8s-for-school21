import asyncio

from asyncpgsa import PG

from plugins.config import cfg
from plugins.pg.query import upload_test_data

loop = asyncio.get_event_loop()


async def generate_data():
    # Инициализируем соединение с базой данных
    pg = PG()

    pg_pool_min_size = 10
    pg_pool_max_size = 10

    await pg.init(
        str(cfg.app.hosts.pg.url),
        min_size=pg_pool_min_size,
        max_size=pg_pool_max_size
    )

    query_create = "create table user_data ( user_id integer, city varchar);"
    await pg.fetch(query_create)
    query = upload_test_data()
    await pg.fetch(query)


loop.run_until_complete(generate_data())
