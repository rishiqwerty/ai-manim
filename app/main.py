from app.core.middleware.annoynomous_track_middleware import anonymous_tracking_middleware
from fastapi import FastAPI
from pydantic import BaseModel
from .routers import chat_routes
app = FastAPI()
app.middleware("http")(anonymous_tracking_middleware)

app.include_router(chat_routes.router, prefix="/chat", tags=["chat"])
