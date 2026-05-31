from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from client.python_cli.app.services.httpServices import (HttpService)
from typing import cast
import os

class KeyServices:
    KEY_DIR = "keys"

    def __init__(self,username:str) -> None:
        self.username = username

        self.private_key_path = os.path.join(
            self.KEY_DIR,
            f"{username}_private.pem"
        )

        self.public_key_path = os.path.join(
            self.KEY_DIR,
            f"{username}_public.pem"
        )

        self.httpService=HttpService()
    
    def initialize_keys(self):

        if (
            os.path.exists(self.private_key_path)
            and
            os.path.exists(self.public_key_path)
        ):

            print("RSA keys already exist")
            return

        os.makedirs(self.KEY_DIR, exist_ok=True)

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        public_key = private_key.public_key()

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open(self.private_key_path, "wb") as private_file:
            private_file.write(private_pem)

        with open(self.public_key_path, "wb") as public_file:
            public_file.write(public_pem)

        print("RSA keys generated")
        
    def generate_rsa_keys(self):

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        public_key = private_key.public_key()

        return private_key, public_key
    
    def load_private_key(self)->RSAPrivateKey:

        with open(self.private_key_path, "rb") as file:

            return cast(
                RSAPrivateKey,
                serialization.load_pem_private_key(
                file.read(),
                password=None
                )
            ) 
                

    def load_public_key_local(self):

        with open(self.public_key_path, "rb") as file:

            return serialization.load_pem_public_key(
                file.read()
            )
    
    async def get_public_key(self,username:str)->RSAPublicKey:
        response=await self.httpService.get(f"/keys/public/{username}")
        print(response.status_code)
        print(response.text)
        print(response.json())
        pub_key:str=response.json()["pub_key"]
        
        if response.status_code != 200:
            raise Exception(
                response.json()["detail"]
            )
        
        public_key = serialization.load_pem_public_key(
            pub_key.encode()
        )
        return cast(RSAPublicKey, public_key)
    
    def generate_session_key(self):
        return os.urandom(32)
    
    def encrypt_session_key(self,session_key:bytes,public_key:RSAPublicKey):
        if not isinstance(public_key, RSAPublicKey):
            raise TypeError("Expected RSAPublicKey")
        encrypted_key = public_key.encrypt(
            session_key,
            padding=padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return encrypted_key
    
    def decrypt_session_key(self,encrypted_session_key:bytes):
        private_key=self.load_private_key()
        decrypted_key = private_key.decrypt(
            encrypted_session_key,
            padding=padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return decrypted_key



