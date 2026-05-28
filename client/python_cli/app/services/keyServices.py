from Crypto.PublicKey import RSA
import os

class KeyServices:
    
    KEY_DIR = "keys"

    PRIVATE_KEY_FILE = os.path.join(
        KEY_DIR,
        "private.pem"
    )

    PUBLIC_KEY_FILE = os.path.join(
        KEY_DIR,
        "public.pem"
    )

    def __init__(self) -> None:
        pass

    def generate_keys(self):

        if not os.path.exists(self.KEY_DIR):
            os.makedirs(self.KEY_DIR)

        key = RSA.generate(2048)

        private_key = key.export_key()
        public_key = key.publickey().export_key()

        with open(self.PRIVATE_KEY_FILE, "wb") as private_file:
            private_file.write(private_key)

        with open(self.PUBLIC_KEY_FILE, "wb") as public_file:
            public_file.write(public_key)

        print("RSA keys generated")

    def load_private_key(self):

        with open(self.PRIVATE_KEY_FILE, "rb") as file:
            private_key = RSA.import_key(
                file.read()
            )

        return private_key

    def load_public_key(self):

        with open(self.PUBLIC_KEY_FILE, "rb") as file:
            public_key = RSA.import_key(
                file.read()
            )

        return public_key


