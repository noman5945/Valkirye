import asyncio

from client.python_cli.app.services.authServices import AuthenticationServices
from client.python_cli.app.services.userServices import UserServices
from client.python_cli.app.services.websocketServices import WebsocketClientService
from client.python_cli.app.services.cryptoServices import CryptoServices
from client.python_cli.app.services.chatServices import ChatService
from client.python_cli.app.services.keyServices import KeyServices

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

    async def chatMenu(self, current_user: str, keyService: KeyServices):

        crypto_service = CryptoServices()
        chat_service = ChatService(
            self.socketClientService,
            crypto_service,
            keyService
        )

        background_task = asyncio.create_task(
            chat_service.receive_loop(current_user=current_user)
        )

        async def interruptible_input(prompt: str) -> str | None:
            """
            Shows input prompt but cancels it if a chat request arrives.
            Returns None if interrupted, otherwise returns what user typed.
            """
            chat_service.request_event.clear()

            input_task = asyncio.create_task(asyncio.to_thread(input, prompt))
            interrupt_task = asyncio.create_task(chat_service.request_event.wait())

            done, pending = await asyncio.wait(
                [input_task, interrupt_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in pending:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

            if interrupt_task in done:
                return None  # chat request arrived
            return input_task.result()

        async def handle_pending_requests():
            while not chat_service.incoming_requests.empty():
                payload = chat_service.incoming_requests.get_nowait()
                sender = payload["sender"]

                print(f"\n[{sender} wants to chat — type A to accept or Enter to skip]")
                answer = await asyncio.to_thread(input, "Accept? (A): ")

                if answer.strip().upper() != "A":
                    print(f"Skipped request from {sender}.")
                    continue

                await chat_service.send_chat_accept(
                    sender=current_user,
                    receiver=sender
                )
                print(f"Accepted. Waiting for session key from {sender}...")

                for _ in range(10):
                    if chat_service.cryptoService.is_ready():
                        break
                    await asyncio.sleep(0.5)

                if not chat_service.cryptoService.is_ready():
                    print("[Session key never arrived — aborting]")
                    return

                print(f"Secure chat with {sender}. Type /exit to leave.")
                while True:
                    message = await asyncio.to_thread(input, f"{current_user}: ")
                    if message.strip() == "/exit":
                        print("Left chat.")
                        break
                    await chat_service.send_message(
                        sender=current_user,
                        receiver=sender,
                        plain_text=message
                    )

        try:
            while True:
                await handle_pending_requests()

                print("\n" + "=" * 60)
                print(f"Welcome {current_user}")
                print("=" * 60)
                print("1. Show Online Users")
                print("2. Start Chat")
                print("3. Logout")

                # ← This input can now be interrupted by incoming chat request
                choice = await interruptible_input("Select Option: ")

                if choice is None:
                    # Interrupted — a chat request arrived mid-prompt
                    print("\n[Incoming chat request!]")
                    continue  # loop back → handle_pending_requests() runs

                if choice == "1":
                    await self.getUsersService()

                elif choice == "2":
                    receiver = await asyncio.to_thread(input, "Enter username: ")

                    await chat_service.send_chat_request(
                        sender=current_user,
                        receiver=receiver
                    )

                    accepted, i_am_initiator = await chat_service.wait_for_accept(
                        sender=current_user,
                        receiver=receiver
                    )
                    if not accepted:
                        continue

                    if i_am_initiator:
                        await chat_service.send_session_key(
                            sender=current_user,
                            receiver=receiver
                        )
                        print(f"Secure chat started with {receiver}. Type /exit to leave.")
                    else:
                        print(f"Waiting for session key from {receiver}...")
                        for _ in range(20):  # 10 seconds
                            if chat_service.cryptoService.is_ready():
                                break
                            await asyncio.sleep(0.5)

                        if not chat_service.cryptoService.is_ready():
                            print("[Session key never arrived — aborting]")
                            continue

                        print(f"Secure chat with {receiver}. Type /exit to leave.")

                    while True:
                        message = await asyncio.to_thread(input, f"{current_user}: ")
                        if message.strip() == "/exit":
                            print("Left chat.")
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

        finally:
            background_task.cancel()