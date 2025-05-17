from litestar import Controller, get
from litestar.di import Provide

from typing import List

from src.core.models import Alert
from src.core.schemas.alert import AlertReadDTO
from src.core.providers import provide_alert_repository
from src.core.repositories import AlertRepository


class AlertController(Controller):
    path = "/alert"
    dependencies = {
        "alert_repository": Provide(provide_alert_repository),
    }
    tags = ["Alert"]
    return_dto = AlertReadDTO

    @get(path="/", sync_to_thread=False)
    def get_all(self, alert_repository: AlertRepository) -> List[Alert]:
        return alert_repository.list()
