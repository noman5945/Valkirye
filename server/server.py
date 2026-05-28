import asyncio, sys
from fastapi import FastAPI
from server.app.router.auth_router import router as authRouter
from server.app.websocket.chat_socket import router as chatRouter
from server.app.router.user_router import router as userRouter
from server.app.database.connection import init_db

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app=FastAPI()

@app.get("/")
def home():
    return {"message": "Secure Chat Server Running"}

@app.on_event("startup")
async def startUp():
    await init_db() 

app.include_router(authRouter)
app.include_router(chatRouter)
app.include_router(userRouter)