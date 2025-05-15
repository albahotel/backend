from litestar import Controller, get
from litestar.di import Provide

from typing import List
from datetime import date

from src.core.models import Room
from src.core.schemas.room import RoomReadDTO
from src.core.providers import provide_room_repository, provide_booking_repository
from src.core.repositories import RoomRepository

class RoomController(Controller):
    path = "/room"
    dependencies = {"booking_repository": Provide(provide_booking_repository), "room_repository": Provide(provide_room_repository)}
    return_dto = RoomReadDTO
    
    @get(path="/free")
    def get_rooms(self, date_in: date, date_out: date, room_repository: RoomRepository) -> List[Room]:
        return room_repository.get_free_rooms(date_in, date_out)
