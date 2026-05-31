from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from secrets import token_bytes

class CryptoServices:
    def __init__(self) -> None:
        self.key = None
        self.aesgcm = None
        self.ready = False
    
    def set_session_key(
        self,
        session_key: bytes
    ):

        self.key = session_key
        self.aesgcm = AESGCM(session_key)
        self.ready = True
    
    def clear_session(self) -> None:

        self.key = None
        self.aesgcm = None

    def is_ready(self) -> bool:

        return self.aesgcm is not None

    def encrypt_text_AES(self,plainText:str):
        if self.aesgcm is None:
            raise Exception(
            "Session key not established"
            )
        nonce=token_bytes(12)
        cipherText=self.aesgcm.encrypt(nonce,plainText.encode(),None)
        return nonce,cipherText
    


    def decrypt_text_AES(self,nonce:bytes,cipherText:bytes):
        try:
            if self.aesgcm is None:
                raise Exception(
                "Session key not established"
            )
            return self.aesgcm.decrypt(
                nonce,
                cipherText,
                None
            ).decode()

        except Exception as e:

            print(f"Decryption failed: {e}")
            raise