"""
storing active users
connect/disconnect
send private message
"""
from fastapi import WebSocket

class WebSocketConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[str, WebSocket]={}

    async def connect(self,username:str,websocket:WebSocket):
        await websocket.accept()
        self.active_connections[username]=websocket
        print(f"User {username} connected")

    async def disconnect(self,username:str):
        if username in self.active_connections:
            del self.active_connections[username]

            print(f"{username} disconnected")
    
    async def send_private_message(
        self,
        receiver_id: str,
        payload:dict
    ):
        websocket = self.active_connections.get(receiver_id)

        if websocket:
            await websocket.send_json(payload)
    
    def get_online_users(self):

        return list(self.active_connections.keys())

    def is_user_online(self, user_id: str):

        return user_id in self.active_connections

socketManager=WebSocketConnectionManager()
