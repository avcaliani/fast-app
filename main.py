from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

from app import middlewares
from app.routers import base, emoji, mood, users

app = FastAPI()

# TODO List
#   - Database (SQL or NoSQL)
#   - Unit Tests
#   - Logging

# 👇 Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# 👇 Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(BaseHTTPMiddleware, dispatch=middlewares.add_process_time_header)

# 👇 Routers
app.include_router(base.router)
app.include_router(emoji.router)
app.include_router(mood.router)
app.include_router(users.router)
