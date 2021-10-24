from aiohttp.web_urldispatcher import View
from asyncpgsa import PG
# aiohttp_cors.WebViewMixig


class BaseView(View):
    URL_PATH: str

    @property
    def pg(self) -> PG:
        return self.request.app['pg']
