from typing import List
from pydantic import BaseModel, Field


class UserCityReq(BaseModel):
    message_name: str
    user_id: int


class UserCityResp(BaseModel):
    message_name: str
    status: bool
    user_id: int
    city: List[str]


data = {
    "message_name": "GET_CITY",
    "user_id": 123,
}

# Более сложный пример
data = {
    "update_id": 243475549,
    "message": {
        "message_id": 9450,
        "from": {
            "id": 81432612,
            "is_bot": False,
            "first_name": "Kirill",
            "username": "kkkkk_kkk_kkkkk",
            "language_code": "ru"
        },
        "chat": {
            "id": 81432612,
            "first_name": "Kirill",
            "username": "kkkkk_kkk_kkkkk",
            "type": "private"
        },
        "date": 1589404439,
        "text": "Да"
    }
}


class From(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    username: str or None = None
    language_code: str = None


class Chat(BaseModel):
    id: int
    first_name: str
    username: str or None = None
    type: str


class InlineKeyboard(BaseModel):
    text: str
    callback_data: str or None = None
    url: str or None = None


class ReplyMarkup(BaseModel):
    inline_keyboard: List[List[InlineKeyboard]]


class Message(BaseModel):
    message_id: int
    frm: From = Field(..., alias='from')
    chat: Chat
    date: int
    edit_date: int = None
    text: str
    reply_markup: ReplyMarkup = None


class CallbackQuery(BaseModel):
    id: str
    frm: From = Field(..., alias='from')
    message: Message
    chat_instance: str
    data: str


class Updater(BaseModel):
    update_id: int
    message: Message = None
    callback_query: CallbackQuery = None

    def its_callback(self):
        if self.callback_query:
            return True
        else:
            return False

    def get_message_id(self):

        if self.its_callback():
            message_id = self.callback_query.message.message_id
        else:
            message_id = self.message.message_id

        return message_id

    def get_chat_id(self):
        if self.its_callback():
            chat_id = self.callback_query.message.chat.id
        else:
            chat_id = self.message.chat.id

        return chat_id

    def get_text(self):
        if self.its_callback():
            text = self.callback_query.data
        else:
            text = self.message.text

        return text

    def get_user_id(self):
        if self.its_callback():
            user_id = self.callback_query.frm.id
        else:
            user_id = self.message.frm.id
        return user_id

    def get_username(self):
        if self.its_callback():
            username = self.callback_query.frm.username
        else:
            username = self.message.frm.username
        return username


data_for_callback = {
    "update_id": 632560344,
    "callback_query": {
        "id": "349750407818784147",
        "from": {
            "id": 81432612,
            "is_bot": False,
            "first_name": "Kirill",
            "username": "kkkkk_kkk_kkkkk",
            "language_code": "ru"
        },
        "message": {
            "message_id": 874,
            "from": {
                "id": 1238618041,
                "is_bot": True,
                "first_name": "work_founder",
                "username": "work_founder_bot"
            },
            "chat": {
                "id": 81432612,
                "first_name": "Kirill",
                "username": "kkkkk_kkk_kkkkk",
                "type": "private"
            },
            "date": 1600692962,
            "edit_date": 1600693642,
            "text": "печень",
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {
                            "text": "лола",
                            "callback_data": "A1"
                        }
                    ]
                ]
            }
        },
        "chat_instance": "4891727470677092353",
        "data": "A1"
    }
}

data = {
    "update_id": 632563156,
    "callback_query": {
        "id": "349750406158492068",
        "from": {
            "id": 81432612,
            "is_bot": False,
            "first_name": "Kirill",
            "username": "kkkkk_kkk_kkkkk",
            "language_code": "ru"
        },
        "message": {
            "message_id": 3571,
            "from": {
                "id": 1238618041,
                "is_bot": True,
                "first_name": "work_founder",
                "username": "work_founder_bot"
            },
            "chat": {
                "id": 81432612,
                "first_name": "Kirill",
                "username": "kkkkk_kkk_kkkkk",
                "type": "private"
            },
            "date": 1634143616,
            "edit_date": 1634143625,
            "text": "💥 Название позиции: Ведущий аудитор\n💥 Описание: **Обязанности сотрудника:**\n\n\\- Получение, обработка и визуализация данных (кроме данных банка используем и\nданные внешних источников);\n\n\\- Проведение исследований процессов банка, проверка гипотез, презентация\nрезультатов, формирование аудиторских отчетов;\n\n\\- Аудит процессов, связанных с реализацией в Банке Комплаенс-функции (ПОД/ФТ,\nконфликт интересов и т.д.) и ESG-стратегии Банка, координацией команды\nпроекта;\n\n\\- Разработка алгоритмов проверок.\n\n **Наши ожидания от кандидата:**\n\n\\- Высшее о...\n\nПоказать еще❓",
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {
                            "text": "Полное описание и отклик",
                            "url": "https://my.sbertalents.ru/#/job-requisition/2094129"
                        },
                        {
                            "text": "Расширенный профиль",
                            "callback_data": "Расширенный"
                        }
                    ],
                    [
                        {
                            "text": "Назад к выбору",
                            "callback_data": "В начало"
                        },
                        {
                            "text": "Следующая",
                            "callback_data": "Следующая"
                        }
                    ],
                    [
                        {
                            "text": "В избранное",
                            "callback_data": "В избранное"
                        },
                        {
                            "text": "Показать избранные",
                            "callback_data": "Избранное"
                        }
                    ],
                    [
                        {
                            "text": "Очистить историю просмотров",
                            "callback_data": "Очистить"
                        }
                    ]
                ]
            }
        },
        "chat_instance": "4891727470677092353",
        "data": "В начало"
    }
}

m = Updater(**data)

print(m.get_text())

response_from_tlg = {
    "ok": False,
    "error_code": 400,
    "description": "Bad Request: message text is empty"
}
