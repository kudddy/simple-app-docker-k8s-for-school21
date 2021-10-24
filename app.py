import logging

from types import AsyncGeneratorType, MappingProxyType
from typing import AsyncIterable, Mapping

from aiohttp import PAYLOAD_REGISTRY
from aiohttp.web_app import Application
from aiohttp_apispec import setup_aiohttp_apispec

from handlers import HANDLERS

from plugins.pg.connector import setup_pg
from payloads import AsyncGenJSONListPayload, JsonPayload

MEGABYTE = 1024 ** 2
MAX_REQUEST_SIZE = 70 * MEGABYTE

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)


def create_app() -> Application:
    """
    Создает экземпляр приложения, готового к запуску
    """
    app = Application(
        client_max_size=MAX_REQUEST_SIZE
    )
    # регистрируем коннектор к pg(синглтон)
    app.cleanup_ctx.append(setup_pg)
    # Регистрация обработчика
    for handler in HANDLERS:
        log.debug('Registering handler %r as %r', handler, handler.URL_PATH)

        app.router.add_route('*', handler.URL_PATH, handler)

    setup_aiohttp_apispec(app=app, title="schoolbackend21", swagger_path='/')
    # Автоматическая сериализация в json данных в HTTP ответах
    PAYLOAD_REGISTRY.register(AsyncGenJSONListPayload,
                              (AsyncGeneratorType, AsyncIterable))
    PAYLOAD_REGISTRY.register(JsonPayload, (Mapping, MappingProxyType))
    return app
