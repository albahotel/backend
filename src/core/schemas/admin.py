from litestar.plugins.sqlalchemy import SQLAlchemyDTO, SQLAlchemyDTOConfig

from src.core.models import Admin


class AdminReadDTO(SQLAlchemyDTO[Admin]):
    config = SQLAlchemyDTOConfig()


class AdminWriteDTO(SQLAlchemyDTO[Admin]):
    config = SQLAlchemyDTOConfig(exclude={"id"})
