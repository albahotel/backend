from litestar import Controller, get, post, delete, patch
from litestar.di import Provide
from litestar.exceptions import HTTPException

from typing import List, Optional

from src.core.models import Customer
from src.core.schemas.customer import (
    CustomerReadDTO,
    CustomerWriteDTO,
    CustomerUpdateDTO,
)
from src.core.providers import provide_customer_repository
from src.core.repositories import CustomerRepository


class CustomerController(Controller):
    path = "/customer"
    tags = ["Customer"]
    dependencies = {
        "customer_repository": Provide(provide_customer_repository),
    }
    return_dto = CustomerReadDTO

    @get(path="/", sync_to_thread=False)
    def get_list(
        self,
        customer_repository: CustomerRepository,
        name: Optional[str] = None,
    ) -> List[Customer]:
        if name:
            result = customer_repository.get_one_or_none(name=name)
            if result is None:
                raise HTTPException(
                    status_code=404, detail=f"Customer with name {name} not found"
                )
            return [result]
        return customer_repository.list()

    @get(path="/{id:int}", sync_to_thread=False)
    def get(self, id: int, customer_repository: CustomerRepository) -> Customer:
        customer = customer_repository.get_one_or_none(id=id)
        if customer is None:
            raise HTTPException(
                status_code=404, detail=f"Customer with ID {id} not found"
            )
        return customer

    @post(path="/", dto=CustomerWriteDTO, sync_to_thread=False)
    def create(
        self,
        data: Customer,
        customer_repository: CustomerRepository,
    ) -> Customer:
        return customer_repository.add(data, auto_commit=True)

    @delete(path="/{id:int}", sync_to_thread=False)
    def delete(self, id: int, customer_repository: CustomerRepository) -> None:
        if customer_repository.get_one_or_none(id=id) is None:
            raise HTTPException(
                status_code=404, detail=f"Customer with ID {id} not found"
            )
        customer_repository.delete(id, auto_commit=True)

    @patch(path="/{id:int}", dto=CustomerUpdateDTO, sync_to_thread=False)
    def partial(
        self, id: int, data: Customer, customer_repository: CustomerRepository
    ) -> Customer:
        if customer_repository.get_one_or_none(id=id) is None:
            raise HTTPException(
                status_code=404, detail=f"Customer with ID {id} not found"
            )
        data.id = id
        return customer_repository.update(data, auto_commit=True)
