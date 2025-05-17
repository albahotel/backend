from sqlalchemy import Date, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import date
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .room import Room
    from .customer import Customer

from . import Base
from .booking_customer import booking_customer


class Booking(Base):
    __tablename__ = "bookings"

    room_number: Mapped[int] = mapped_column(ForeignKey("rooms.number"))
    room: Mapped["Room"] = relationship(back_populates="bookings")

    customers: Mapped[List["Customer"]] = relationship(
        secondary=booking_customer, back_populates="bookings"
    )
    peoples: Mapped[int] = mapped_column(Integer())

    date_in: Mapped[date] = mapped_column(Date())
    date_out: Mapped[date] = mapped_column(Date())
