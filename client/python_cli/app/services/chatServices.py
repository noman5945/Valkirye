from client.python_cli.app.services.cryptoServices import CryptoServices
from client.python_cli.app.services.websocketServices import WebsocketClientService


class ChatService:

    def __init__(
        self,
        websocket: WebsocketClientService,
        cryptoService: CryptoServices
    ) -> None:

        self.cryptoService = cryptoService
        self.websocket = websocket

    async def send_message(self,sender:str,receiver:str,plain_text: str):

        nonce, cipher_text = self.cryptoService.encrypt_text_AES(
            plain_text
        )

        payload = {
            "type": "private_message",
            "sender": sender,
            "receiver": receiver,
            "nonce": nonce.hex(),
            "cipher_text": cipher_text.hex()
        }

        await self.websocket.send_json(payload)

    async def receive_message(self):

        payload = await self.websocket.receive_json()

        nonce = bytes.fromhex(payload["nonce"])

        cipher_text = bytes.fromhex(
            payload["cipher_text"]
        )

        plain_text = self.cryptoService.decrypt_text_AES(
            nonce,
            cipher_text
        )

        return {
            "sender": payload["sender"],
            "message": plain_text
        }
    
    async def receive_loop(self):

        while True:
            try:
                data = await self.receive_message()

                print(f"\n{data['sender']}: {data['message']}")

            except Exception as e:
                print(f"Receive error: {e}")
                break

    async def start_chat(self):
        while True:

            try:

                message = await self.receive_message()

                print(
                    f"\n{message['sender']}: "
                    f"{message['message']}"
                )

            except Exception as e:

                print(f"Receive error: {e}")

                break