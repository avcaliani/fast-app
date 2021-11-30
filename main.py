from datetime import datetime
from random import choices, randint
from typing import Optional

from fastapi import FastAPI, Query, HTTPException

from app import db
from app.enums import Mood
from app.models import User
from config import settings

SECRET = settings.SECRET
EMOJIS = settings.EMOJIS

app = FastAPI()


@app.get('/')
async def root():
    return {'api': 'fast-app', 'version': '0.0.1', 'consulted_at': datetime.utcnow()}


@app.get('/emoji')
async def emojis(limit: Optional[int] = None):
    return {
        'lucky_emojis': choices(EMOJIS, k=limit if limit else randint(1, len(EMOJIS))),
        'secret': SECRET,
        'consulted_at': datetime.utcnow()
    }


@app.get('/emoji/{item}')
async def get_emoji(item: int):
    return {
        'emoji': EMOJIS[item],
        'item': item,
        'item_type': type(item),
        'consulted_at': datetime.utcnow()
    }


@app.get('/mood/{item}')
async def mood(
        item: Mood,
        text_mode: Optional[str] = Query(None, min_length=4, max_length=8, regex=r'CAPS(LOCK)?')):
    messages = {
        Mood.happy: 'If in doubt, Meriadoc, always follow your nose!',
        Mood.angry: 'You must trust yourself. Trust your own strength.',
        Mood.insightful: 'Even the very wise cannot see all ends.',
    }
    msg = messages.get(item)
    return {
        'message': msg.upper() if text_mode in ['CAPS', 'CAPSLOCK'] else msg,
        'item': item,
        'consulted_at': datetime.utcnow()
    }


@app.get('/users')
async def get_users():
    return {
        'users': db.get(),
        'consulted_at': datetime.utcnow()
    }


@app.get('/users/{user_id}')
async def get_user(user_id: str):
    return {
        'user': db.get(user_id),
        'consulted_at': datetime.utcnow()
    }


@app.post('/users', status_code=201)
async def create_user(user: User):
    return {
        'user': db.create(user),
        'consulted_at': datetime.utcnow()
    }


@app.put('/users/{user_id}')
async def get_user(user_id: str, user: User):
    return {
        'user': db.update(user_id, user),
        'consulted_at': datetime.utcnow()
    }


@app.delete('/users/{user_id}')
async def delete_user(user_id: str):
    try:
        return {
            'user': db.delete(user_id),
            'consulted_at': datetime.utcnow()
        }
    except RuntimeError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
