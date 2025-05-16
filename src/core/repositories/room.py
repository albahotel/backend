from litestar.plugins.sqlalchemy import repository
from sqlalchemy import and_, not_, exists

from datetime import date
from typing import List, Optional

from src.core.models import Room, Booking


class RoomRepository(repository.SQLAlchemySyncRepository[Room]):
    model_type = Room

    def get_free_rooms(self, start_date: date, end_date: date) -> List[Room]:
        overlapping = exists().where(
            and_(
                Booking.room_number == Room.number,
                Booking.date_in < end_date,
                Booking.date_out > start_date,
            )
        )

        query = self.session.query(Room).filter(not_(overlapping)).order_by(Room.number)

        return query.all()

    def is_room_available(
        self,
        number: int,
        start_date: date,
        end_date: date,
        exclude_booking_id: Optional[int] = None,
    ) -> bool:
        if start_date >= end_date:
            return False

        query = exists().where(
            and_(
                Booking.room_number == number,
                Booking.date_in < end_date,
                Booking.date_out > start_date,
                *([Booking.id != exclude_booking_id] if exclude_booking_id else []),
            )
        )

        return not self.session.query(query).scalar()
