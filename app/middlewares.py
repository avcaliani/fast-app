from datetime import datetime
from typing import Callable

from fastapi import Request
from fastapi.responses import StreamingResponse


async def add_process_time_header(request: Request, call_next: Callable) -> StreamingResponse:
    start_time = datetime.utcnow()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str((datetime.utcnow() - start_time))
    return response
