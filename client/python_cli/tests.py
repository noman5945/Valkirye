from client.python_cli.app.services.keyServices import KeyServices
import asyncio

async def tests():
    print("Public Key fetch test")
    keyservice=KeyServices("thor")
    public_key=await keyservice.get_public_key("thor")
    session_key=keyservice.generate_session_key()
    #public_key=keyservice.load_public_key_local()
    encrypted=keyservice.encrypt_session_key(session_key,public_key) # type: ignore
    decrypted=keyservice.decrypt_session_key(encrypted)
    print(session_key.hex())
    print(decrypted.hex())
    print(session_key == decrypted)


asyncio.run(tests()) 