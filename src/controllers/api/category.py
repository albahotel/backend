from litestar import Controller, get
from litestar.di import Provide

from typing import List

from src.core.models import Category
from src.core.schemas.category import CategoryReadDTO
from src.core.providers import provide_category_repository
from src.core.repositories import CategoryRepository


class CategoryController(Controller):
    path = "/category"
    dependencies = {
        "category_repository": Provide(provide_category_repository),
    }
    tags = ["Category"]
    return_dto = CategoryReadDTO

    @get(path="/", sync_to_thread=False, exclude_from_auth=True)
    def get_all(self, category_repository: CategoryRepository) -> List[Category]:
        return category_repository.list()
