from litestar.plugins.sqlalchemy import repository

from src.core.models.alert import Alert


class AlertRepository(repository.SQLAlchemySyncRepository[Alert]):
    model_type = Alert
