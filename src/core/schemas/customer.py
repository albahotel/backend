from litestar.plugins.sqlalchemy import SQLAlchemyDTO, SQLAlchemyDTOConfig

from src.core.models import Customer


class CustomerReadDTO(SQLAlchemyDTO[Customer]):
    config = SQLAlchemyDTOConfig()


class CustomerWriteDTO(SQLAlchemyDTO[Customer]):
    config = SQLAlchemyDTOConfig(exclude={"id", "bookings"})


class CustomerUpdateDTO(SQLAlchemyDTO[Customer]):
    config = SQLAlchemyDTOConfig(exclude={"id", "room"}, partial=True)
