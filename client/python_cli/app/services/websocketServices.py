import websockets
import json

class WebsocketClientService:
    def __init__(self) -> None:
        self.websocket=None
    
    async def connect(self,username:str):
        uri=f"ws://127.0.0.1:8000/ws/{username}"
        self.websocket=await websockets.connect(uri,ping_interval=None)
        print("Connected to websocket")
    
    async def send_json(self, payload: dict):
        if not self.websocket:
            raise Exception("Websocket not connected")
        await self.websocket.send(json.dumps(payload))

    async def receive_json(self):
        if not self.websocket:
            raise Exception("Websocket not connected")
        data=await self.websocket.recv()
        return json.loads(data)
    
    async def disconnect(self):
        if self.websocket:
            await self.websocket.close()
            self.websocket = None

        print("Disconnected from websocket")
    
     

