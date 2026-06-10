from fastapi import FastAPI

from app.api.v1.routes.event_router import router as event_router

app = FastAPI()

app.include_router(event_router, prefix="/api/v1")
