from litestar.plugins.sqlalchemy import repository
from sqlalchemy import and_, not_, exists

from datetime import date
from typing import List

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
