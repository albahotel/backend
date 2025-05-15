from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .alert import Alert

from . import Base


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    alerts: Mapped[List["Alert"]] = relationship(back_populates="category")
