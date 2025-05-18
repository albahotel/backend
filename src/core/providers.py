# Example of provider:
#
# def prodive_some_repo(session: Session):
#     return SomeRepo(session=session)
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories import (
    BookingRepository,
    RoomRepository,
    CategoryRepository,
    AlertRepository,
    AlertRepositoryAsync,
    CustomerRepository,
    TokenRepository,
    AdminRepository,
)


def provide_booking_repository(session: Session):
    return BookingRepository(session=session)


def provide_room_repository(session: Session):
    return RoomRepository(session=session)


def provide_category_repository(session: Session):
    return CategoryRepository(session=session)


def provide_alert_repository(session: Session):
    return AlertRepository(session=session)


async def provide_async_alert_repository(async_session: AsyncSession):
    return AlertRepositoryAsync(session=async_session)


def provide_customer_repository(session: Session):
    return CustomerRepository(session=session)


def provide_token_repository(session: Session):
    return TokenRepository(session=session)


def provide_admin_repository(session: Session):
    return AdminRepository(session=session)
