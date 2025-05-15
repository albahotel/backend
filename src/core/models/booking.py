from sqlalchemy import String, Date, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .room import Room
from . import Base

class Booking(Base):
    __tablename__ = "bookings"    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    room_number: Mapped[int] = mapped_column(ForeignKey("rooms.number"))
    room: Mapped["Room"] = relationship(back_populates="bookings")
    
    customer: Mapped[str] = mapped_column(String(50))
    passport: Mapped[String] = mapped_column(String(10))
    peoples: Mapped[int] = mapped_column(Integer())
    
    date_in: Mapped[date] = mapped_column(Date())
    date_out: Mapped[date] = mapped_column(Date())

    