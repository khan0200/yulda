from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from jose import JWTError
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.deps import get_db
from app.core.security import decode_access_token
from app.repositories.user_repository import UserRepository
from app.websocket.manager import manager

router = APIRouter(tags=["websocket"])


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str | None = Query(default=None),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    auth_token = token or websocket.cookies.get("access_token")
    if not auth_token:
        await websocket.close(code=4401)
        return

    try:
        payload = decode_access_token(auth_token)
    except JWTError:
        await websocket.close(code=4401)
        return

    user_id = payload.get("sub")
    user = await UserRepository(db).find_by_id(user_id)
    if not user:
        await websocket.close(code=4401)
        return

    await manager.connect(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
