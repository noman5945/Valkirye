from fastapi import APIRouter
from server.app.services.keyManageServices import keyManagementService

router = APIRouter()

key_management_service=keyManagementService()

@router.get("/keys/public/{username}")
def get_public_key(username:str):
    public_key=key_management_service.getPublicKey_local(username=username)
    return{
        "pub_key":public_key
    }

