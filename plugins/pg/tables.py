from sqlalchemy import (
    Column, Integer,
    MetaData, String, Table
)

from sqlalchemy.types import UserDefinedType

# SQLAlchemy рекомендует использовать единый формат для генерации названий для
# индексов и внешних ключей.
# https://docs.sqlalchemy.org/en/13/core/constraints.html#configuring-constraint-naming-conventions
convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s'
}

metadata = MetaData(naming_convention=convention)


# добавлена поддерка типа CUBE
class CUBE(UserDefinedType):
    def get_col_spec(self, **kw):
        return "CUBE"


# описываем структуру база таблицы
user_data = Table(
    'user_data',
    metadata,
    Column('user_id', Integer),
    Column('city', String)
)
