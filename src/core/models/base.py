from litestar.plugins.sqlalchemy import base


class Base(base.BigIntBase):
    __abstract__ = True
