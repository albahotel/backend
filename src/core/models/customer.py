from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import date
from typing import TYPE_CHECKING, List

from . import Base
from .booking_customer import booking_customer

if TYPE_CHECKING:
    from .booking import Booking


class Customer(Base):
    __tablename__ = "customers"

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    passport: Mapped[str] = mapped_column(String(256), nullable=False)
    bookings: Mapped[List["Booking"]] = relationship(
        secondary=booking_customer, back_populates="customers"
    )

    birthday: Mapped[date] = mapped_column(Date())
