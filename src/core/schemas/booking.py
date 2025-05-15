from litestar.plugins.sqlalchemy import SQLAlchemyDTO, SQLAlchemyDTOConfig

from src.core.models import Booking


class BookingReadDTO(SQLAlchemyDTO[Booking]):
    config = SQLAlchemyDTOConfig(exclude={"room"})


class BookingWriteDTO(SQLAlchemyDTO[Booking]):
    config = SQLAlchemyDTOConfig(exclude={"id", "room"})


class BookingUpdateDTO(SQLAlchemyDTO[Booking]):
    config = SQLAlchemyDTOConfig(exclude={"id", "room"}, partial=True)
