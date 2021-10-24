from sqlalchemy import select, func, desc, or_, Table

from plugins.pg.tables import user_data


# дописать
def get_city(user_id: int):
    query = select([user_data.c.city]).where(user_data.c.user_id == user_id)
    return query




