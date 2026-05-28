from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

SESSION_COLLECTION = "sessions"

class SessionModel(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    user_id: str
    token: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True
    }