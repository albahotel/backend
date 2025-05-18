from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .booking import Booking
    from .alert import Alert

from . import Base


class Room(Base):
    __tablename__ = "rooms"

    number: Mapped[int] = mapped_column(Integer(), unique=True)
    level: Mapped[int] = mapped_column(Integer(), nullable=True)
    capacity: Mapped[int] = mapped_column(Integer())

    bookings: Mapped[List["Booking"]] = relationship(back_populates="room")
    alerts: Mapped[List["Alert"]] = relationship(back_populates="room")

    plate_token: Mapped[str] = mapped_column(String(256), nullable=True, unique=True)
    mac_address: Mapped[str] = mapped_column(String(256), nullable=True, unique=True)
