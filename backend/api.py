from pathlib import Path

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

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
    try:
        result = handle_query(req.message)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Chat handling failed: {exc}") from exc

    return {"message": req.message, "result": result}


@app.get("/health")
def health():
    return {"ok": True, "status": "healthy"}
