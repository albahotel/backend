from litestar.plugins.sqlalchemy import SQLAlchemyDTO, SQLAlchemyDTOConfig

from src.core.models import Booking


class BookingReadDTO(SQLAlchemyDTO[Booking]):
    config = SQLAlchemyDTOConfig()


class BookingWriteDTO(SQLAlchemyDTO[Booking]):
    config = SQLAlchemyDTOConfig(exclude={"id", "room", "customers"})


class BookingUpdateDTO(SQLAlchemyDTO[Booking]):
    config = SQLAlchemyDTOConfig(exclude={"id"}, partial=True)
