from fastapi import APIRouter
from server.app.websocket.connection_manager import socketManager

router=APIRouter()

@router.get("/users/online")
async def get_online_users():
    return{
        "online_users":socketManager.get_online_users()
    }