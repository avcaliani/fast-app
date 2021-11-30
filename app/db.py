from datetime import datetime
from typing import List, Dict, Union, Optional
from uuid import uuid4

from app.models import User

# TODO: Save to a database in the future...
USERS: Dict[str, User] = {}


def get(user_id: Optional[str] = None) -> Union[User, List[User]]:
    print(f'Users Available: {len(USERS)}')
    if not user_id:
        return list(USERS.values())
    return USERS.get(user_id)


def create(user: User) -> User:
    user_id = str(uuid4())
    user.id = user_id
    USERS[user_id] = user
    print(f'New User: {user}')
    return user


def update(user_id: str, new_data: User):
    user = USERS[user_id]
    user.updated_at = datetime.utcnow()
    if new_data.name:
        user.name = new_data.name
    if new_data.email:
        user.email = new_data.email
    if new_data.birthdate:
        user.birthdate = new_data.birthdate
    if new_data.mood:
        user.mood = new_data.mood
    if new_data.balance:
        user.balance = new_data.balance
    return user


def delete(user_id: str):
    if user_id not in USERS:
        raise RuntimeError(f'User {user_id} not found!')
    del USERS[user_id]
    return user_id
