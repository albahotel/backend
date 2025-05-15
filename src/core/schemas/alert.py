from litestar.plugins.sqlalchemy import SQLAlchemyDTO, SQLAlchemyDTOConfig

from src.core.models import Alert


class AlertReadDTO(SQLAlchemyDTO[Alert]):
    config = SQLAlchemyDTOConfig(exclude={"room", "category"})
