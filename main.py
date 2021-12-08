from datetime import datetime
from random import choices, randint
from time import time
from typing import Optional

from fastapi import Depends, FastAPI, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from app import db, dependencies
from app.enums import Mood
from app.models import User, Login
from app.utils import auth
from config import settings

SECRET = settings.SECRET
EMOJIS = settings.EMOJIS

app = FastAPI()

# TODO List
#   - Database (SQL or NoSQL)
#   - Multiple Modules
#   - Unit Tests
#   - Logging

app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(time() - start_time)
    return response


@app.get('/', response_class=HTMLResponse)
async def root():
    with open('static/index.html', 'r', encoding='utf8') as file:
        return HTMLResponse(
            content=file.read().rstrip(),
            status_code=200
        )


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('static/favicon.ico')


@app.post("/auth")
async def get_token(login: Login):
    user = db.get_by_email(login.username)
    password_ok = auth.check_password(plain=login.password, hashed=user.password)
    if not user or not password_ok:
        raise auth.EXCEPTION_INVALID_CREDENTIALS
    return auth.create_token(
        subject=user.email,
        mood=user.mood.value if user.mood else ''
    )


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
    # TODO: Remove password from body!
    # TODO: Protect other endpoints
    return {
        'users': db.get(),
        'consulted_at': datetime.utcnow()
    }


@app.get("/users/me")
async def who_am_i(user: User = Depends(dependencies.get_user)):
    # TODO: Add Middleware to add consulted at.
    return user.dict(exclude={'password'})


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
