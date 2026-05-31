import asyncio
from client.python_cli.app.services.cryptoServices import CryptoServices
from client.python_cli.app.services.websocketServices import WebsocketClientService
from client.python_cli.app.services.keyServices import KeyServices


class ChatService:

    def __init__(
        self,
        websocket: WebsocketClientService,
        cryptoService: CryptoServices,
        keyService: KeyServices
    ) -> None:
        self.cryptoService = cryptoService
        self.websocket = websocket
        self.keyManager = keyService
        self.active_peer: str | None = None
        self._accept_event = asyncio.Event()  # fires when peer accepts
        self.request_event = asyncio.Event()
        self.incoming_requests: asyncio.Queue = asyncio.Queue()

    async def send_chat_request(self, sender: str, receiver: str):
        payload = {
            "type": "chat_request",
            "sender": sender,
            "receiver": receiver
        }
        await self.websocket.send_json(payload)
        print(f"Chat request sent to {receiver}, waiting for acceptance...")

    async def wait_for_accept(self, sender: str, receiver: str) -> tuple[bool, bool]:
        """
        Returns (accepted, i_am_initiator).

        Three cases:
        1. Peer sends chat_accept → they accepted our request → we are initiator
        2. Peer sends chat_request too (mutual) → resolve with alphabetical tiebreaker
        3. Timeout → False, False
        """
        try:
            async with asyncio.timeout(30):
                while True:
                    # Case 2: mutual request — check queue
                    try:
                        payload = self.incoming_requests.get_nowait()
                        if payload.get("sender") == receiver:
                            i_am_initiator = sender < receiver
                            if not i_am_initiator:
                                # I lose tiebreaker — send accept so they unblock
                                await self.send_chat_accept(
                                    sender=sender,
                                    receiver=receiver
                                )
                            return True, i_am_initiator
                        else:
                            # Request from someone else — put back and ignore for now
                            await self.incoming_requests.put(payload)
                    except asyncio.QueueEmpty:
                        pass

                    # Case 1: peer accepted normally
                    if self._accept_event.is_set():
                        self._accept_event.clear()
                        return True, True

                    await asyncio.sleep(0.1)

        except asyncio.TimeoutError:
            print("Chat request timed out.")
            return False, False

    async def send_chat_accept(self, sender: str, receiver: str):
        payload = {
            "type": "chat_accept",
            "sender": sender,
            "receiver": receiver
        }
        await self.websocket.send_json(payload)

    async def send_session_key(self, sender: str, receiver: str):
        receiver_public_key = await self.keyManager.get_public_key(username=receiver)
        session_key = self.keyManager.generate_session_key()
        encrypted_key = self.keyManager.encrypt_session_key(session_key, receiver_public_key)
        self.cryptoService.set_session_key(session_key)
        self.active_peer = receiver

        payload = {
            "type": "session_key",
            "sender": sender,
            "receiver": receiver,
            "encrypted_key": encrypted_key.hex()
        }
        await self.websocket.send_json(payload)
        print(f"Session key sent to {receiver}")

    async def handle_session_key(self, payload: dict):
        encrypted_key = bytes.fromhex(payload["encrypted_key"])
        session_key = self.keyManager.decrypt_session_key(encrypted_key)
        self.cryptoService.set_session_key(session_key)
        self.active_peer = payload["sender"]
        print(f"\n[Session key received — chat ready]")

    async def send_message(self, sender: str, receiver: str, plain_text: str):
        nonce, cipher_text = self.cryptoService.encrypt_text_AES(plain_text)
        payload = {
            "type": "private_message",
            "sender": sender,
            "receiver": receiver,
            "nonce": nonce.hex(),
            "cipher_text": cipher_text.hex()
        }
        await self.websocket.send_json(payload)

    async def receive_loop(self, current_user: str, on_chat_request=None):
        while True:
            try:
                payload = await self.websocket.receive_json()
                msg_type = payload.get("type")

                if msg_type == "chat_request":
                    await self.incoming_requests.put(payload)
                    self.request_event.set()

                elif msg_type == "chat_accept":
                    # Initiator unblocked — safe to send session key now
                    print(f"\n[{payload['sender']} accepted — establishing session]")
                    self._accept_event.set()

                elif msg_type == "session_key":
                    await self.handle_session_key(payload)

                elif msg_type == "private_message":
                    if not self.cryptoService.is_ready():
                        print("\n[Message received but session not ready]")
                        continue
                    nonce = bytes.fromhex(payload["nonce"])
                    cipher_text = bytes.fromhex(payload["cipher_text"])
                    message = self.cryptoService.decrypt_text_AES(nonce, cipher_text)
                    print(f"\n{payload['sender']}: {message}")
                    print(f"{current_user}: ", end="", flush=True)

                else:
                    print(f"\n[Unknown message type: {msg_type}]")

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Receive error: {e}")
                break