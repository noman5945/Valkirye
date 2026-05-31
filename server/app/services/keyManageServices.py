import os
from fastapi.responses import PlainTextResponse
from fastapi import HTTPException

class keyManagementService:
    def __init__(self) -> None:
        pass

    def getPublicKey_local(self,username:str):
        # This is temporary
        path=f"keys/{username}_public.pem"
        if not os.path.exists(path):
            raise HTTPException(status_code=404,detail="Key file not found")
        with open(path,"r")as file:
            publicKey=file.read()
        
        return publicKey
        
    def getPublicKey_db(self):
        pass