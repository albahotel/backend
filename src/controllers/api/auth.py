from litestar import post, Controller, get
from litestar.di import Provide
from litestar.exceptions import HTTPException
from datetime import datetime, timedelta
import secrets

from src.core.providers import (
    provide_admin_repository,
    provide_token_repository,
    provide_booking_repository,
)
from src.core.models import Admin, Token
from src.core.schemas.admin import AdminWriteDTO
from src.core.repositories import AdminRepository, TokenRepository, BookingRepository


class AuthController(Controller):
    path = "/auth"
    tags = ["Authentication"]
    dependencies = {
        "admin_repository": Provide(provide_admin_repository),
        "token_repository": Provide(provide_token_repository),
        "booking_repository": Provide(provide_booking_repository),
    }

    @post(path="/admin/login", dto=AdminWriteDTO, exclude_from_auth=True)
    async def admin_login(
        self,
        data: Admin,
        admin_repository: AdminRepository,
        token_repository: TokenRepository,
    ) -> Token:
        admin = admin_repository.get_one_or_none(username=data.username)
        if not admin or not admin.verify_password(data.password):
            raise HTTPException("Invalid credentials", status_code=401)

        token = Token(
            token=secrets.token_urlsafe(64),
            is_admin=True,
            expires_at=datetime.now() + timedelta(hours=8),
        )
        return token_repository.add(token)

    @post(path="/admin/register", dto=AdminWriteDTO, exclude_from_auth=True)
    async def admin_register(
        self,
        data: Admin,
        admin_repository: AdminRepository,
    ) -> Admin:
        if admin_repository.exists(username=data.username):
            raise HTTPException("Username already exists", status_code=400)

        admin = Admin(username=data.username)
        admin.set_password(data.password)
        return admin_repository.add(admin)

    @get(path="/mobile_token")
    async def create_mobile_token(
        self,
        id: int,
        token_repository: TokenRepository,
        booking_repository: BookingRepository,
    ) -> str:
        data = booking_repository.get_one_or_none(id=id)
        if data is None:
            raise HTTPException("Booking not found", status_code=404)
        print("flag1")
        token = Token(
            token=secrets.token_urlsafe(64),
            is_admin=False,
            expires_at=data.date_out + timedelta(hours=12),
        )
        print("flag2")
        token = token_repository.add(token, auto_commit=True)
        print(token)
        return f"{token.token};{data.room.plate_token};{data.room.mac_address};{data.room_number}"
