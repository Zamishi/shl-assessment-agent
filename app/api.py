from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

from app.agent import SHLAgent
from app.retriever import Retriever
from app.utils import load_catalog

# -----------------------------
# FastAPI App
# -----------------------------

app = FastAPI(
    title="SHL Assessment Recommendation Agent",
    version="1.0.0",
    description="Conversational AI agent for recommending SHL assessments."
)

# -----------------------------
# Load catalog once at startup
# -----------------------------

catalog = load_catalog()
retriever = Retriever(catalog)
agent = SHLAgent(retriever)


# -----------------------------
# Request Models
# -----------------------------

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# -----------------------------
# Endpoints
# -----------------------------

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    return agent.chat(
        [message.model_dump() for message in request.messages]
    )