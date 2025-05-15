from litestar.plugins.sqlalchemy import repository

from src.core.models.category import Category


class CategoryRepository(repository.SQLAlchemySyncRepository[Category]):
    model_type = Category
