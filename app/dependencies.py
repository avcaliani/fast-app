from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.services import user as service
from app.utils import auth

# It will use "/auth" as default endpoint for authentication.
SCHEME = OAuth2PasswordBearer(tokenUrl="auth")


async def get_user(token: str = Depends(SCHEME)):
    payload = auth.decode(token)
    if not payload or "sub" not in payload:
        raise auth.EXCEPTION_INVALID_CREDENTIALS
    user = await service.find(email=payload.get("sub"))
    if user is None:
        raise auth.EXCEPTION_INVALID_CREDENTIALS
    if not user.get("enabled"):
        raise HTTPException(status_code=400, detail="Inactive user!")
    return user
