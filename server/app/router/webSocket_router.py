from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from server.app.websocket.connection_manager import socketManager

router = APIRouter()


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):

    username = None

    try:

        await websocket.accept()

        auth_data = await websocket.receive_json()

        print(auth_data)

    except WebSocketDisconnect:

        if username:

            await socketManager.disconnect(username)