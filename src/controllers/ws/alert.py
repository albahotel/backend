from litestar import WebSocket
from litestar.di import Provide
from litestar.handlers import WebsocketListener
import orjson

from src.core.schemas.alert import (
    WSCommand,
    AlertsReadData,
    AlertReadData,
    AlertCreateData,
    AlertCompleteData,
    AlertGetData,
)
from src.core.repositories import AlertRepositoryAsync
from src.core.providers import provide_async_alert_repository
from src.core.models import Alert

from typing import List


class AlertWSController(WebsocketListener):
    path = "/alert"
    active_connections: List[WebSocket] = []
    dependencies = {
        "alert_repository": Provide(provide_async_alert_repository),
    }

    async def on_accept(self, socket: WebSocket) -> None:
        self.active_connections.append(socket)

    async def on_disconnect(self, socket: WebSocket) -> None:
        self.active_connections.remove(socket)

    async def on_receive(
        self,
        socket: WebSocket,
        data: str,
        alert_repository: AlertRepositoryAsync,
    ) -> None:
        try:
            raw_data = orjson.loads(data.encode())
            command = WSCommand(**raw_data)
            match command.action:
                case "get_awaiting_alerts":
                    alerts = await alert_repository.get_awaiting_alerts()
                    message = AlertsReadData(alerts=[AlertReadData(**alert.to_dict()) for alert in alerts])
                    await socket.send_json(message.__dict__, serializer=orjson.dumps)
                    return

                case "create_alert":
                    if not isinstance(command.data, dict):
                        raise ValueError("Invalid data type")
                    alert_data = AlertCreateData(**command.data).__dict__
                    alert = await alert_repository.add(
                        Alert(**alert_data), auto_commit=True
                    )

                    await socket.send_json(
                        {
                            "action": "create_alert",
                            "data": alert.to_dict(),
                        },
                        serializer=orjson.dumps,
                    )
                    return

                case "complete_alert":
                    if not isinstance(command.data, dict):
                        raise ValueError("Invalid data type")
                    alert = await alert_repository.complete(
                        alert_id=AlertCompleteData(**command.data).alert_id,
                    )

                    await socket.send_json(
                        {
                            "action": "complete_alert",
                            "data": alert.to_dict(),
                        },
                        serializer=orjson.dumps,
                    )
                    return

                case "get_alert_status":
                    if not isinstance(command.data, dict):
                        raise ValueError("Invalid data type")
                    alert = await alert_repository.get(AlertGetData(**command.data).alert_id)
                    await socket.send_json(
                        {
                            "action": "get_alert_status",
                            "data": alert.to_dict(),
                        },
                        serializer=orjson.dumps,
                    )
                    return

        except Exception as e:
            await socket.send_json({"error": str(e), "status": "error"})

    async def _broadcast(self, data: dict) -> None:
        for connection in self.active_connections:
            await connection.send_json(data)
