from litestar import Litestar, get
# from litestar.plugins.sqlalchemy import SyncSessionConfig, SQLAlchemySyncConfig, SQLAlchemyPlugin

# from src.core.config import settings


@get("/")
def index() -> dict[str, str]:
    return {"hello": "world"}

# session_config = SyncSessionConfig(expire_on_commit=False)
# sqlalchemy_config = SQLAlchemySyncConfig(
#     connection_string=settings.db_url, session_config=session_config, create_all=False
# )

# sqlalchemy_plugin = SQLAlchemyPlugin(config=sqlalchemy_config)

app = Litestar(
    route_handlers=[index],
    # plugins=[sqlalchemy_plugin]
)