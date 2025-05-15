from litestar import Router

from .booking import BookingController
from .room import RoomController

api_router = Router(
    path="/api",
    route_handlers=[BookingController, RoomController],
)

__all__ = ["api_router"]
