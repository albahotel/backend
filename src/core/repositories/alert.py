from litestar.plugins.sqlalchemy import repository

from datetime import datetime

from src.core.models.alert import Alert


class AlertRepository(repository.SQLAlchemySyncRepository[Alert]):
    model_type = Alert


class AlertRepositoryAsync(repository.SQLAlchemyAsyncRepository[Alert]):
    model_type = Alert

    async def complete(self, alert_id: int):
        alert = await self.session.get(Alert, alert_id)
        if alert is None:
            raise ValueError(f"Alert with id {alert_id} not found")
        alert.completed_at = datetime.now()
        await self.session.commit()
        return alert
