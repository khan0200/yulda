import logging
from collections import defaultdict

from fastapi import WebSocket

logger = logging.getLogger("yulda.websocket")


class ConnectionManager:
    def __init__(self) -> None:
        self._connections: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, user_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections[user_id].add(websocket)

    def disconnect(self, user_id: str, websocket: WebSocket) -> None:
        self._connections[user_id].discard(websocket)
        if not self._connections[user_id]:
            self._connections.pop(user_id, None)

    async def send_to_user(self, user_id: str, payload: dict) -> None:
        sockets = list(self._connections.get(user_id, ()))
        for ws in sockets:
            try:
                await ws.send_json(payload)
            except Exception:
                logger.warning("Failed to push to socket for user %s, disconnecting", user_id)
                self.disconnect(user_id, ws)


manager = ConnectionManager()
