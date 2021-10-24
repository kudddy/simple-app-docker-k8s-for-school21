from sqlalchemy import select, func, desc, or_, Table

from plugins.pg.tables import user_data


# дописать
def get_city(user_id: int):
    query = select([user_data.c.city]).where(user_data.c.user_id == user_id)
    return query


def upload_test_data():
    data = [
        {
            "user_id": 123,
            "city": "moscow"
        },
        {
            "user_id": 234,
            "city": "saint-p"
        },
        {
            "user_id": 345,
            "city": "akhtubinsk"
        },
    ]
    return user_data.insert().values(data)
