from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from passlib.context import CryptContext  # type: ignore

from . import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Admin(Base):
    __tablename__ = "admins"
    username: Mapped[str] = mapped_column(String(256), unique=True)
    password: Mapped[str] = mapped_column(String(256))

    def set_password(self, password: str):
        self.password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)
