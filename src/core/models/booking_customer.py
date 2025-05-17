from sqlalchemy import ForeignKey, Column, Table

from . import Base

booking_customer = Table(
    "booking_customer",
    Base.metadata,
    Column("booking_id", ForeignKey("bookings.id"), primary_key=True),
    Column("customer_id", ForeignKey("customers.id"), primary_key=True),
)
