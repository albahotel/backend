from litestar import Litestar, get
from litestar.di import Provide
from litestar.plugins.sqlalchemy import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SyncSessionConfig,
    SQLAlchemySyncConfig,
    SQLAlchemyPlugin,
)
from litestar.config.cors import CORSConfig
from redis import asyncio as aioredis

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from src.core.db_helper import db_helper
from src.core.config import settings
from src.controllers.api import api_router
from src.controllers.ws import ws_router


@get("/")
def index() -> dict[str, str]:
    return {"hello": "world"}


session_config = SyncSessionConfig(expire_on_commit=False)
async_session_config = AsyncSessionConfig(expire_on_commit=False)

sqlalchemy_config = SQLAlchemySyncConfig(
    connection_string=settings.database.url,
    session_config=session_config,
    create_all=False,
    session_dependency_key="session",
)

async_sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=settings.database.async_url,
    session_config=async_session_config,
    create_all=False,
    session_dependency_key="async_session",
)

sqlalchemy_plugin = SQLAlchemyPlugin(config=sqlalchemy_config)
async_sqlalchemy_plugin = SQLAlchemyPlugin(config=async_sqlalchemy_config)

cors_config = CORSConfig(allow_origins=["*"])


@asynccontextmanager
async def redis_connection(app: Litestar) -> AsyncGenerator[None, None]:
    redis = getattr(app.state, "redis", None)
    if redis is None:
        app.state.redis = aioredis.from_url(
            settings.redis.url + "/0",
            decode_responses=False,
            encoding="utf-8",
        )

    try:
        yield
    finally:
        await app.state.redis.close()


app = Litestar(
    route_handlers=[index, api_router, ws_router],
    plugins=[sqlalchemy_plugin, async_sqlalchemy_plugin],
    cors_config=cors_config,
    lifespan=[redis_connection],
    dependencies={"db_session": Provide(db_helper.session_dependency)},
)
