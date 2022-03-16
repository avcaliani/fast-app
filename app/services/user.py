import logging as log
from uuid import uuid4

from app.models import User
from app.utils import auth, mongo

COLLECTION = "users"


async def find(id_: str = None, email: str = None) -> dict:
    """Return user by Id or e-mail.

    Args:
        id_ (str): User Id.
        email (str):  User e-Mail.

    Returns:
        dict: User.
    """
    condition = {"_id": id_} if id_ else {"email": email}
    user = await mongo.find_one(COLLECTION, condition)
    return User(**user).dict(exclude={"password"})


async def create(user: User) -> dict:
    """Create user into the database.

    Args:
        user (User): User Data.

    Returns:
        dict: Created User.
    """
    user.id = str(uuid4())
    user.password = auth.hash_password(user.password)
    user = await mongo.create(COLLECTION, user)
    log.info(f"New Record! Collection: {COLLECTION} | Data: {user}")
    return User(**user).dict()
