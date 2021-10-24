import logging

from aiohttp.web_response import Response
from aiohttp_apispec import docs, response_schema
from pydantic import ValidationError

from .base import BaseView
from message_schema import UserCityReq, UserCityResp
from plugins.pg.query import get_city

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)


class GetUserCity(BaseView):
    URL_PATH = r'/city/'

    @docs(summary="Ручка возвращает город в котором живет пользователь", tags=["Basic methods"],
          description="Просто возвращаем город пользователяв",
          parameters=[
              {
                  'in': 'json',
                  'name': 'message_name',
                  'schema': {'type': 'string', 'format': 'string'},
                  'required': 'true',
                  'description': 'message name'
              },
              {
                  'in': 'json',
                  'name': 'user_id',
                  'schema': {'type': 'string', 'format': 'string'},
                  'required': 'true',
                  'description': 'user id'
              }
          ]
          )
    @response_schema(UserCityResp(), description="Возвращаем ранее добавлены комментарии к фотографии, "
                                                 "сортированные по дате")
    async def post(self):

        data: dict = await self.request.json()

        try:
            user = UserCityReq(**data)
        except ValidationError as e:
            log.info("validation error - %s", e)
            return Response(body={
                "message_name": "GET_CITY",
                "status": False,
                "desk": "wrong_input"
            })

        query = get_city(user.user_id)

        result = []
        for row in await self.pg.fetch(query):
            result.append(row['city'])

        log.info("Message with data %s success successfully worked", data)

        return Response(body={
            "message_name": "GET_CITY",
            "status": True,
            "user_id": result,
            "city": "Moscow"
        })
