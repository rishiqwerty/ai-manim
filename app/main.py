from fastapi import FastAPI
from pydantic import BaseModel
from .routers import chat_routes
app = FastAPI()

app.include_router(chat_routes.router, prefix="/chat", tags=["chat"])
# Define a Pydantic model for the request body
class Conversation(BaseModel):
    user: str
    message: str
    id: int

# 
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/conversation/")
async def create_conversation(item: Conversation):
    import logging
    print(f"messagege - {item.message}")
    return {"item": item}