from litestar import Router

from .booking import BookingController
from .room import RoomController
from .category import CategoryController
from .alert import AlertController
from .customer import CustomerController

api_router = Router(
    path="/api",
    route_handlers=[
        BookingController,
        RoomController,
        CategoryController,
        AlertController,
        CustomerController,
    ],
)

__all__ = ["api_router"]
