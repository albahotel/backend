from litestar.plugins.sqlalchemy import SQLAlchemyDTO, SQLAlchemyDTOConfig

from src.core.models import Room


class RoomReadDTO(SQLAlchemyDTO[Room]):
    config = SQLAlchemyDTOConfig()


class RoomWriteDTO(SQLAlchemyDTO[Room]):
    config = SQLAlchemyDTOConfig(exclude={"id", "bookings", "alerts"})


class RoomUpdateDTO(SQLAlchemyDTO[Room]):
    config = SQLAlchemyDTOConfig(exclude={"id", "bookings", "alerts"}, partial=True)
