import asyncio

from client.python_cli.app.services.authServices import AuthenticationServices
from client.python_cli.app.services.userServices import UserServices
from client.python_cli.app.services.websocketServices import WebsocketClientService
from client.python_cli.app.services.cryptoServices import CryptoServices
from client.python_cli.app.services.chatServices import ChatService
from secrets import token_bytes

class CLIinterfaceServices:
    def __init__(self) -> None:
        self.authServices=AuthenticationServices()
        self.socketClientService=WebsocketClientService()
        self.userService=UserServices()
        

    async def loginService(self):
        print("=" * 60)
        print("LOGIN")
        print("=" * 60)

        username = input("Username: ")
        password = input("Password: ")

        try:
            response=await self.authServices.userLogin(username,password)
            print("\nLogin Successfull")
            print(response)
            await self.socketClientService.connect(username)
            return {
                "token":response["token"],
                "current_user":response["username"]
            }
        except Exception as e:
            print("\nLogin failed")
            print(f"\n Error:{e}")


    async def logoutService(self,token):
        if not token:
            print("You are not logged in.")
        try:
            response=await self.authServices.userLogout(token)
            await self.socketClientService.disconnect()
            print(response)
        except Exception as e:
            print("\nLogout failed")
            print(f"\nError:{e}")

    async def getUsersService(self):
        await self.userService.getOnlineUsers()   

    async def chatMenu(self, current_user: str):

        while True:

            print("\n" + "=" * 60)
            print(f"Welcome {current_user}")
            print("=" * 60)

            print("1. Show Online Users")
            print("2. Start Chat")
            print("3. Logout")

            choice = input("Select Option: ")

            if choice == "1":

                await self.getUsersService()

            elif choice == "2":
                #shared_key = token_bytes(32)
                shared_key = b'12345678901234567890123456789012' #Tmeporary
                crypto_service = CryptoServices(shared_key)
                chat_service = ChatService(
                    self.socketClientService,
                    crypto_service
                )
                
                receiver = input("Enter username: ")
                print(
                    f"Secure chat started with {receiver}"
                )

                receiver_task = asyncio.create_task(
                    chat_service.receive_loop()
                )

                while True:

                    message = await asyncio.to_thread(
                        input,
                        f"{current_user}: "
                    )

                    if message == "/exit":
                        receiver_task.cancel()
                        break

                    await chat_service.send_message(
                        sender=current_user,
                        receiver=receiver,
                        plain_text=message
                    )

            elif choice == "3":

                break

            else:

                print("Invalid option")