from litestar import Controller, get, post, delete, patch
from litestar.di import Provide
from litestar.exceptions import HTTPException

from typing import List
from datetime import date

from src.core.models import Booking
from src.core.schemas.booking import BookingReadDTO, BookingWriteDTO, BookingUpdateDTO
from src.core.providers import provide_booking_repository, provide_room_repository
from src.core.repositories import BookingRepository, RoomRepository


class BookingController(Controller):
    path = "/booking"
    dependencies = {
        "booking_repository": Provide(provide_booking_repository),
        "room_repository": Provide(provide_room_repository),
    }
    return_dto = BookingReadDTO

    @get(path="/", sync_to_thread=False)
    def get_all(
        self,
        level: int,
        start_date: date,
        end_date: date,
        booking_repository: BookingRepository,
    ) -> List[Booking]:
        if start_date >= end_date:
            raise HTTPException(
                detail="Дата выезда должна быть позже даты заезда", status_code=400
            )

        return booking_repository.get_for_period(
            level=level, start_date=start_date, end_date=end_date
        )

    @get(path="/{id:int}", sync_to_thread=False)
    def get(self, id: int, booking_repository: BookingRepository) -> Booking:
        booking = booking_repository.get_one_or_none(id=id)
        if booking is None:
            raise HTTPException(
                status_code=404, detail=f"Booking with ID {id} not found"
            )
        return booking

    @post(path="/", dto=BookingWriteDTO, sync_to_thread=False)
    def create(
        self,
        data: Booking,
        booking_repository: BookingRepository,
        room_repository: RoomRepository,
    ) -> Booking:
        if room_repository.get_one_or_none(number=data.room_number) is None:
            raise HTTPException(
                status_code=404, detail=f"Room with number {data.room_number} not found"
            )
        if not room_repository.is_room_available(
            data.room_number, data.date_in, data.date_out
        ):
            raise HTTPException(status_code=400, detail="Room is not free")
        return booking_repository.add(data, auto_commit=True)

    @delete(path="/{id:int}", sync_to_thread=False)
    def delete(self, id: int, booking_repository: BookingRepository) -> None:
        if booking_repository.get_one_or_none(id=id) is None:
            raise HTTPException(
                status_code=404, detail=f"Booking with ID {id} not found"
            )
        booking_repository.delete(id, auto_commit=True)

    @patch(path="/{id:int}", dto=BookingUpdateDTO, sync_to_thread=False)
    def partial(
        self, id: int, data: Booking, booking_repository: BookingRepository
    ) -> Booking:
        if booking_repository.get_one_or_none(id=id) is None:
            raise HTTPException(
                status_code=404, detail=f"Booking with ID {id} not found"
            )
        data.id = id
        return booking_repository.update(data, auto_commit=True)
