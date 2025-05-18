from litestar.plugins.sqlalchemy import repository

from src.core.models.admin import Admin


class AdminRepository(repository.SQLAlchemySyncRepository[Admin]):
    model_type = Admin
