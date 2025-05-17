from litestar.plugins.sqlalchemy import SQLAlchemyDTO, SQLAlchemyDTOConfig

from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Union, Optional, List

from src.core.models import Alert


class AlertReadDTO(SQLAlchemyDTO[Alert]):
    config = SQLAlchemyDTOConfig(exclude={"room", "category"})


class AlertCreateDTO(SQLAlchemyDTO[Alert]):
    config = SQLAlchemyDTOConfig(
        exclude={"id", "room", "category", "created_at", "completed_at"}
    )


@dataclass
class AlertReadData:
    """For mobile app"""

    id: int
    room_number: int
    category_name: str
    created_at: datetime
    comment: Optional[str] = None
    completed_at: Optional[datetime] = None


@dataclass
class AlertsReadData:
    """For admin panel"""

    alerts: List[AlertReadData]
    action: str = "get_awaiting_alerts"


@dataclass
class AlertCreateData:
    """For mobile app"""
    room_number: int
    category_name: str
    comment: Optional[str] = None


@dataclass
class AlertCompleteData:
    """For admin panel"""

    alert_id: int


@dataclass
class AlertGetData:
    """For mobile app"""

    alert_id: int


@dataclass
class WSCommand:
    action: Literal["create_alert", "complete_alert", "get_alert_status", "get_alerts"]
    data: Optional[dict] = None
