from litestar.plugins.sqlalchemy import repository

from src.core.models.customer import Customer


class CustomerRepository(repository.SQLAlchemySyncRepository[Customer]):
    model_type = Customer
