from fastapi import FastAPI

from app.api.v1.routes.booking_router import router as booking_router
from app.api.v1.routes.event_router import router as event_router

app = FastAPI()

app.include_router(event_router, prefix="/api/v1")
app.include_router(booking_router, prefix="/api/v1")
