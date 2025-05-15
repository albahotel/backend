from litestar.plugins.sqlalchemy import repository

from src.core.models.booking import Booking


class BookingRepository(repository.SQLAlchemySyncRepository[Booking]):
    model_type = Booking
