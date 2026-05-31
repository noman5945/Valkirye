import asyncio
from client.python_cli.app.services.cli_Insterface_Services import CLIinterfaceServices
from client.python_cli.app.services.keyServices import KeyServices

async def main():
    cli_interface_service=CLIinterfaceServices()
    current_user=None
    current_token=None
    
    while True:
        print("=== Valkirye Secure Chat (with vulnerable key exchange) ===")
        print("1. Login")
        print("2. Logout")
        print("3. Exit")

        choice = input("Select Option: ")

        if choice == "1":

            data=await cli_interface_service.loginService()
            if data:
                current_token = data["token"]
                current_user = data["current_user"]

                print(f"\nCurrent User: {current_user}")
                keyservice=KeyServices(current_user)
                keyservice.initialize_keys()

                await cli_interface_service.chatMenu(current_user=current_user,keyService=keyservice)

        elif choice == "2":

            if not current_token:

                print("\nNo active session")

            else:

                await cli_interface_service.logoutService(current_token)

                current_token = None
                current_user = None

                print("\nLogged out successfully")

        elif choice == "3":

            print("\nExiting...")
            break

        else:

            print("\nInvalid Option")


asyncio.run(main())