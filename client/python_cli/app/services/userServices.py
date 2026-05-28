from client.python_cli.app.services.httpServices import HttpService
class UserServices:
    def __init__(self) -> None:
        self.httpService=HttpService()

    async def getOnlineUsers(self):
        response=await self.httpService.get('/users/online')
        data=response.json()
        
        print("\nOnline Users:")

        for user in data["online_users"]:

            print(f"- {user}")