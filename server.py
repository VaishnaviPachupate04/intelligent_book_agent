from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Try importing agent safely
try:
    from engine import run_agent
except Exception as e:
    run_agent = None
    print("IMPORT ERROR:", e)

class ChatRequest(BaseModel):
    user_input: str
    conversation_history: list = []

@app.get("/")
def home():
    return {"status": "Book Agent Running"}

@app.post("/chat")
def chat(req: ChatRequest):
    if run_agent is None:
        return {"error": "Agent failed to load. Check logs."}
    return run_agent(req.user_input, req.conversation_history)
