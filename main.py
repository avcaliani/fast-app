from datetime import datetime
from random import choices, randint
from typing import Optional

from fastapi import FastAPI

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
async def mood(item: Mood):
    messages = {
        Mood.happy: 'If in doubt, Meriadoc, always follow your nose!',
        Mood.angry: 'You must trust yourself. Trust your own strength.',
        Mood.insightful: 'Even the very wise cannot see all ends.',
    }
    return {
        'message': messages.get(item),
        'item': item,
        'consulted_at': datetime.utcnow()
    }


@app.post('/user')
async def create_user(user: User):
    return {
        'user': db.create(user),
        'consulted_at': datetime.utcnow()
    }


@app.get('/user/{user_id}')
async def get_user(user_id: str):
    return {
        'user': db.get(user_id),
        'consulted_at': datetime.utcnow()
    }


@app.put('/user/{user_id}')
async def get_user(user_id: str, user: User):
    return {
        'user': db.update(user_id, user),
        'consulted_at': datetime.utcnow()
    }
