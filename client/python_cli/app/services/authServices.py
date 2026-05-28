from client.python_cli.app.services.httpServices import (HttpService)

class AuthenticationServices:
    def __init__(self) -> None:
        self.httpService=HttpService()
        self.token=None
        self.current_user=None

    async def userLogin(self,username:str,password:str):
        
        payload={
            "username":username,
            "password":password
        }
        response=await self.httpService.post(
            '/auth/login',
            payload
        )
        data=response.json()
        if response.status_code != 200:
            raise Exception(data)
        self.token=data["token"]
        self.current_user=data["username"]
        return data
    async def userLogout(self,token):
        payload={
            "token":token
        }
        response=await self.httpService.post(
            '/auth/logout',
            payload
        )
        data=response.json()
        if response.status_code != 200:
            raise Exception(data)
        return data

    