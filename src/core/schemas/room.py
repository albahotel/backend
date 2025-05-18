from litestar.plugins.sqlalchemy import SQLAlchemyDTO, SQLAlchemyDTOConfig

from src.core.models import Room


class RoomReadDTO(SQLAlchemyDTO[Room]):
    config = SQLAlchemyDTOConfig(exclude={"alerts"})


class RoomWriteDTO(SQLAlchemyDTO[Room]):
    config = SQLAlchemyDTOConfig(
        exclude={"id", "bookings", "alerts", "plate_token", "mac_address"}
    )


class RoomUpdateDTO(SQLAlchemyDTO[Room]):
    config = SQLAlchemyDTOConfig(exclude={"id", "bookings", "alerts"}, partial=True)
