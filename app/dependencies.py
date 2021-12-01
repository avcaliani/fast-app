from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app import db
from app.utils import auth

SCHEME = OAuth2PasswordBearer(tokenUrl="token")


async def get_user(token: str = Depends(SCHEME)):
    payload = auth.decode(token)
    if not payload or 'sub' not in payload:
        raise auth.EXCEPTION_INVALID_CREDENTIALS
    user = db.get_by_email(email=payload.get('sub'))
    if user is None:
        raise auth.EXCEPTION_INVALID_CREDENTIALS
    if not user.enabled:
        raise HTTPException(status_code=400, detail="Inactive user!")
    return user
