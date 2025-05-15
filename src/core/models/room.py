from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .booking import Booking

from . import Base


class Room(Base):
    __tablename__ = "rooms"

    number: Mapped[int] = mapped_column(Integer(), unique=True)
    bookings: Mapped[List["Booking"]] = relationship(back_populates="room")
    capacity: Mapped[int] = mapped_column(Integer())
