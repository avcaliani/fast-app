from fastapi import APIRouter
from fastapi.responses import FileResponse, HTMLResponse

from app.models import Login
from app.utils import auth, db

router = APIRouter()


@router.get('/', response_class=HTMLResponse)
async def root():
    with open('static/index.html', 'r', encoding='utf8') as file:
        return HTMLResponse(
            content=file.read().rstrip(),
            status_code=200
        )


@router.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('static/favicon.ico')


@router.post("/auth")
async def get_token(login: Login):
    user = db.get_by_email(login.username)
    password_ok = auth.check_password(plain=login.password, hashed=user.password)
    if not user or not password_ok:
        raise auth.EXCEPTION_INVALID_CREDENTIALS
    return auth.create_token(
        subject=user.email,
        mood=user.mood.value if user.mood else ''
    )
