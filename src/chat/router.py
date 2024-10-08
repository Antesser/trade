from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy import insert, select
from chat.models import Messages
from database import async_session_maker, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/chat", tags=["chat"])


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, add_to_database: bool):
        if add_to_database:
            await self.add_messages(message)
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    async def add_messages(message: str):
        async with async_session_maker() as session:
            statement = insert(Messages).values(message=message)
            await session.execute(statement)
            await session.commit()


manager = ConnectionManager()


@router.get("/last_messages")
async def get_last_messages(
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Messages).order_by(Messages.id.asc()).limit(5)
    result = await session.execute(query)
    result = result.all()
    return [message[0].as_dict() for message in result]


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(
                f"Client #{client_id} says: {data}", add_to_database=True
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(
            f"Client #{client_id} left the chat", add_to_database=False
        )
