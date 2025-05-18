from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime

from . import Base


class Token(Base):
    __tablename__ = "tokens"
    token: Mapped[str] = mapped_column(String(256), unique=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(True))
