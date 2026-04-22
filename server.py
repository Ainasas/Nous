from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Core.Brain import processar_conversa

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Message(BaseModel):
    message: str
    user: str = "Ainas"

@app.post("/chat")
async def chat(body: Message):
    response = processar_conversa(body.message)
    return {"response": response}