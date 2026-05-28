from server.app.models.user_model import UserModel, USER_COLLECTION
from server.app.models.session_model import SessionModel, SESSION_COLLECTION
from server.app.database.connection import get_db
from server.app.security.hashing import hash_password, verify_password
from server.app.security.token import generate_session_token
from datetime import datetime, timezone

class AuthenticationService:

    async def create_new_account(self, userName: str, password: str):
        db = get_db()

        # Check if user exists
        existing_doc = await db[USER_COLLECTION].find_one({"username": userName})
        if existing_doc:
            raise Exception("User already exists")

        hashed_password = hash_password(password)

        # Create new user
        user_dict = {
            "username": userName,
            "password_hash": hashed_password
        }
        result = await db[USER_COLLECTION].insert_one(user_dict)
        # Optionally, we can fetch the created user here, but not necessary.

        return {"message": "Account created"}

    async def user_login(self, userName: str, password: str):
        db = get_db()

        # Find user
        user_doc = await db[USER_COLLECTION].find_one({"username": userName})
        if not user_doc:
            raise Exception("Invalid credentials")

        # Convert ObjectId to string for Pydantic compatibility
        user_doc["_id"] = str(user_doc["_id"])
        user = UserModel(**user_doc)

        # Verify password
        if not verify_password(password, user.password_hash):
            raise Exception("Invalid credentials")

        token = generate_session_token()

        # Create session
        session_dict = {
            "user_id": user.id,          # user.id is the string _id
            "token": token,
            "created_at": datetime.now(timezone.utc)
        }
        await db[SESSION_COLLECTION].insert_one(session_dict)

        return {"token": token,"username":userName}

    async def user_logout(self, token: str):
        db = get_db()
        # Delete the session
        await db[SESSION_COLLECTION].delete_one({"token": token})
        return {"message":"Logged Out Successfully"}