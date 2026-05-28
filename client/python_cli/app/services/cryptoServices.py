from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from secrets import token_bytes

class CryptoServices:
    def __init__(self,key:bytes) -> None:
        self.key=key
        self.aesgcm=AESGCM(self.key)

    def encrypt_text_AES(self,plainText:str):
        nonce=token_bytes(12)
        cipherText=self.aesgcm.encrypt(nonce,plainText.encode(),None)
        return nonce,cipherText


    def decrypt_text_AES(self,nonce:bytes,cipherText:bytes):
        try:

            return self.aesgcm.decrypt(
                nonce,
                cipherText,
                None
            ).decode()

        except Exception as e:

            print(f"Decryption failed: {e}")
            raise