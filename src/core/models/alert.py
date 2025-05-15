from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .room import Room
    from .category import Category

from . import Base


class Alert(Base):
    __tablename__ = "alerts"
    comment: Mapped[str] = mapped_column(String(255), nullable=True)

    room_number: Mapped[int] = mapped_column(ForeignKey("rooms.number"), nullable=True)
    room: Mapped["Room"] = relationship(back_populates="alerts")

    category_name: Mapped[str] = mapped_column(
        ForeignKey("categories.name"), nullable=True
    )
    category: Mapped["Category"] = relationship(back_populates="alerts")

    created_at: Mapped[datetime] = mapped_column(DateTime(True), default=datetime.now())
    completed_at: Mapped[datetime] = mapped_column(DateTime(True), nullable=True)
