from litestar.plugins.sqlalchemy import repository
from sqlalchemy import select

from datetime import datetime, date
from typing import List

from src.core.models.alert import Alert


class AlertRepository(repository.SQLAlchemySyncRepository[Alert]):
    model_type = Alert

    def get_awaiting_alerts(self) -> List[Alert]:
        stmt = select(Alert).where(Alert.completed_at.is_(None))
        return list(self.session.execute(stmt).scalars().all())
    
    def get_alerts(self, date_from: date, date_to: date) -> List[Alert]:
        stmt = select(Alert).where(Alert.created_at.between(date_from, date_to)).order_by(Alert.created_at)
        return list(self.session.execute(stmt).scalars().all())


class AlertRepositoryAsync(repository.SQLAlchemyAsyncRepository[Alert]):
    model_type = Alert

    async def get_awaiting_alerts(self) -> List[Alert]:
        stmt = select(Alert).where(Alert.completed_at.is_(None))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_awaiting_alerts_from_list(self, ids: List[int]) -> List[Alert]:
        stmt = select(Alert).where(Alert.id.in_(ids))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def complete(self, alert_id: int):
        alert = await self.session.get(Alert, alert_id)
        if alert is None:
            raise ValueError(f"Alert with id {alert_id} not found")
        alert.completed_at = datetime.now()
        await self.session.commit()
        return alert
