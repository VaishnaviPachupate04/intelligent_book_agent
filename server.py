from fastapi import FastAPI
from pydantic import BaseModel
from engine import run_agent

app = FastAPI()

class ChatRequest(BaseModel):
    user_input: str
    conversation_history: list = []

@app.get("/")
def home():
    return {"status": "Book Agent Running"}

@app.post("/chat")
def chat(req: ChatRequest):
    result = run_agent(req.user_input, req.conversation_history)
    return result