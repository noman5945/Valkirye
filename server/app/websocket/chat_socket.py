"""
websocket endpoint
token validation
message loop
"""

from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from server.app.websocket.connection_manager import socketManager

router=APIRouter()

@router.websocket("/ws/{username}")
async def websocket_chat(
    websocket:WebSocket,
    username:str
):
    try:
        print(f"→ WebSocket endpoint reached for {username}") 
        await socketManager.connect(username,websocket)
        
        print(f"{username} connected")
        try:
            while True:
                data = await websocket.receive_json()
                print(f"Received from {username}: {data}")

                receiver = data.get("receiver")
                if receiver:
                    await socketManager.send_private_message(
                        receiver_id=receiver,
                        payload=data
                    )
                else:
                    print(f"No receiver in message: {data}")
                
        except WebSocketDisconnect:
            await socketManager.disconnect(username)
    except Exception as e:
        print(f"Fatal error occured while connection to socket: {e}")