from litestar import Router

from .alert import AlertWSController

ws_router = Router(
    path="/ws",
    route_handlers=[AlertWSController],
)

__all__ = ["ws_router"]
