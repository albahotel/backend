from litestar.plugins.sqlalchemy import repository
from sqlalchemy import and_, select
from sqlalchemy.orm import joinedload

from datetime import date
from typing import List

from src.core.models.room import Room
from src.core.models.booking import Booking


class BookingRepository(repository.SQLAlchemySyncRepository[Booking]):
    model_type = Booking

    def get_for_period(
        self, level: int, start_date: date, end_date: date
    ) -> List[Booking]:
        stmt = (
            select(Booking)
            .join(Room, Booking.room_number == Room.number)
            .options(joinedload(Booking.room))
            .where(
                and_(
                    Room.level == level,
                    Booking.date_in < end_date,
                    Booking.date_out > start_date,
                )
            )
            .order_by(Booking.date_in)
        )
        return list(self.session.execute(stmt).scalars().all())
