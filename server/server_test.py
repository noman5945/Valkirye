from fastapi import FastAPI
import asyncio, sys
 
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "minimal works"}