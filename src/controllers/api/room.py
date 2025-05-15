from litestar import Controller, get, post
from litestar.di import Provide
from litestar.exceptions import HTTPException

from typing import List
from datetime import date

from src.core.models import Room
from src.core.schemas.room import RoomReadDTO, RoomWriteDTO
from src.core.providers import provide_room_repository, provide_booking_repository
from src.core.repositories import RoomRepository


class RoomController(Controller):
    path = "/room"
    dependencies = {
        "booking_repository": Provide(provide_booking_repository),
        "room_repository": Provide(provide_room_repository),
    }
    return_dto = RoomReadDTO

    @get(path="/free", sync_to_thread=False)
    def get_free_rooms(
        self, date_in: date, date_out: date, room_repository: RoomRepository
    ) -> List[Room]:
        return room_repository.get_free_rooms(date_in, date_out)

    @post(path="/", dto=RoomWriteDTO, sync_to_thread=False)
    def create(self, data: Room, room_repository: RoomRepository) -> Room:
        if room_repository.get_one_or_none(number=data.number) is not None:
            raise HTTPException(
                status_code=400, detail=f"Room with number {data.number} already exists"
            )
        return room_repository.add(data, auto_commit=True)
