from pydantic import BaseModel, Field
from typing import Optional

# Collection name constant (used in repositories)
USER_COLLECTION = "users"

class UserModel(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    username: str
    password_hash: str

    model_config = {
        "populate_by_name": True,          # allows both "id" and "_id"
        "json_schema_extra": {
            "example": {
                "username": "john_doe",
                "password_hash": "hashedsecret123"
            }
        }
    }