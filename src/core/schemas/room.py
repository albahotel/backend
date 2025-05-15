from litestar.plugins.sqlalchemy import SQLAlchemyDTO, SQLAlchemyDTOConfig

from src.core.models import Room

class RoomReadDTO(SQLAlchemyDTO[Room]):
    config = SQLAlchemyDTOConfig()

class RoomWriteDTO(SQLAlchemyDTO[Room]):
    config = SQLAlchemyDTOConfig(exclude={"id"})
    
class RoomUpdateDTO(SQLAlchemyDTO[Room]):
    config = SQLAlchemyDTOConfig(exclude={"id"}, partial=True)