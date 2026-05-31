class SecureKeyExchange:
    """
    X25519 Diffie-Hellman key exchange.
    MITM cannot derive the session key even if they intercept all traffic,
    because the raw shared secret never travels over the wire.
    
    Note: still vulnerable to active MITM unless public keys are
    verified out-of-band (this is what Signal's "safety numbers" solve).
    """
    def __init__(self, keyService, websocket):
        self.keyService = keyService
        self.websocket = websocket

    async def initiate(self, sender: str, receiver: str) -> None:
        dh_public = self.keyService.generate_dh_keypair()
        await self.websocket.send_json({
            "type": "dh_init",
            "sender": sender,
            "receiver": receiver,
            "dh_public": dh_public.hex()
        })

    async def respond(self, payload: dict, current_user: str) -> bytes:
        peer_public = bytes.fromhex(payload["dh_public"])
        dh_public = self.keyService.generate_dh_keypair()
        aes_key = self.keyService.derive_shared_key(peer_public)

        await self.websocket.send_json({
            "type": "dh_response",
            "sender": current_user,
            "receiver": payload["sender"],
            "dh_public": dh_public.hex()
        })
        return aes_key

    async def complete(self, payload: dict) -> bytes:
        peer_public = bytes.fromhex(payload["dh_public"])
        return self.keyService.derive_shared_key(peer_public)