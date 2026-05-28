from fastapi import APIRouter
from pydantic import BaseModel
from server.app.services.authenticationServices import AuthenticationService

router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

auth_service=AuthenticationService()


class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str

class LogoutRequest(BaseModel):
    token:str

@router.post("/register")
async def register(data: RegisterRequest):

    return await auth_service.create_new_account(
        data.username,
        data.password
    )


@router.post("/login")
async def login(data: LoginRequest):

    return await auth_service.user_login(
        data.username,
        data.password
    )

@router.post("/logout")
async def logout(data:LogoutRequest):
    return await auth_service.user_logout(data.token)