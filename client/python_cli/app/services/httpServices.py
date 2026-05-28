import httpx

class HttpService:
    def __init__(self) -> None:
        self.base_url="http://127.0.0.1:8000"
        self.client=httpx.AsyncClient(
            base_url=self.base_url
        )

    async def post(self,endpoint:str,data:dict,headers:dict|None=None):
        response=await self.client.post(
            endpoint,
            json=data,
            headers=headers
        )
        return response
    
    async def get(self,endpoint:str,headers:dict|None=None):
        response=await self.client.get(endpoint,headers=headers)
        return response
    
    async def close(self):
        await self.client.aclose()