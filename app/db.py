import random
from datetime import datetime, date
from typing import List, Union, Optional
from uuid import uuid4

from app.enums import Mood
from app.models import User

# TODO: Save to a database in the future...
USERS = {
    '8a166a1c-d0ca-46e6-ad16-ac953c9011a7': User(
        id='8a166a1c-d0ca-46e6-ad16-ac953c9011a7',
        name='Bart Simpson',
        email='bart@github.com',
        birthdate=date(1997, 4, 9),
        mood=Mood.happy,
        balance=round(random.uniform(1., 2) * 1000, 2),
        # Password = '12345678'
        password='$2b$12$g2QT3pQPL.Mfh424k/j4r.tmjDrK623jlEw3ftjypA5eWCjGCeVPi',
    )
}


def get(user_id: Optional[str] = None) -> Union[User, List[User]]:
    print(f'Users Available: {len(USERS)}')
    if not user_id:
        return list(USERS.values())
    return USERS.get(user_id)


def get_by_email(email: str) -> Optional[User]:
    for user in USERS.values():
        if user.email == email:
            return user
        return None


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
