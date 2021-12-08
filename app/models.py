from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel

from app.enums import Mood


class User(BaseModel):
    id: Optional[str] = None
    enabled: bool = True
    name: str
    email: str
    birthdate: date
    mood: Optional[Mood] = None
    balance: Optional[float] = 0.0
    password: str
    updated_at: Optional[datetime] = datetime.utcnow()
    created_at: Optional[datetime] = datetime.utcnow()
