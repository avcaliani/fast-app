from datetime import datetime
from random import choices, randint

from fastapi import FastAPI

from config import settings

SECRET = settings.SECRET
EMOJIS = settings.EMOJIS

app = FastAPI()


@app.get("/")
async def root():
    return {
        "lucky_emojis": choices(EMOJIS, k=randint(1, len(EMOJIS))),
        'secret': SECRET,
        'consulted_at': datetime.utcnow()
    }
