import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from llm.parser import parse_query
from backend.services import handle_query

app = FastAPI()
UI_FILE = Path(__file__).resolve().parent.parent / "ui" / "index.html"

class ChatRequest(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
def home():
    return UI_FILE.read_text(encoding="utf-8")


@app.post("/chat")
def chat(req: ChatRequest):
    parsed = parse_query(req.message)
    result = handle_query(parsed)
    return {"message": req.message, "parsed": parsed, "result": result}


@app.get("/health")
def health():
    return {"ok": True, "status": "healthy"}
