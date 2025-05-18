from litestar.plugins.sqlalchemy import repository

from src.core.models.token import Token


class TokenRepository(repository.SQLAlchemySyncRepository[Token]):
    model_type = Token
