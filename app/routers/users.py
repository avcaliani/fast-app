from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from app import dependencies
from app.models import User
from app.utils import db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(dependencies.get_user)]
)


@router.get('/')
async def get_users():
    # TODO: Remove password from body!
    # TODO: Protect other endpoints
    return {
        'users': db.get(),
        'consulted_at': datetime.utcnow()
    }


@router.get("/me")
async def who_am_i(user: User = Depends(dependencies.get_user)):
    # TODO: Add Middleware to add consulted at.
    return user.dict(exclude={'password'})


@router.get('/{user_id}')
async def get_user(user_id: str):
    return {
        'user': db.get(user_id),
        'consulted_at': datetime.utcnow()
    }


@router.post('/', status_code=201)
async def create_user(user: User):
    return {
        'user': db.create(user),
        'consulted_at': datetime.utcnow()
    }


@router.put('/{user_id}')
async def get_user(user_id: str, user: User):
    return {
        'user': db.update(user_id, user),
        'consulted_at': datetime.utcnow()
    }


@router.delete('/{user_id}')
async def delete_user(user_id: str):
    try:
        return {
            'user': db.delete(user_id),
            'consulted_at': datetime.utcnow()
        }
    except RuntimeError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
