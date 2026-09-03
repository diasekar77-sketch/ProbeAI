import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import ollama

from app.services.pipeline import InvestigationPipeline
from app.db.database import SessionManager

app = FastAPI(title="ProbeAI Intelligence Hub API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_manager = SessionManager()


class InvestigationRequest(BaseModel):
    query: str
    chat_history: list = []
    use_web: bool = True
    model: str = "llama3:latest"
    document_context: str = ""
    session_id: str | None = None
    temperature: float = 0.7


class SessionSaveRequest(BaseModel):
    session_id: str | None = None
    title: str
    payload: list


@app.get("/api/models")
def get_models():
    try:
        models_list = ollama.list()
        names = [
            m.get("model", "llama3:latest")
            for m in models_list.get("models", [])
        ]
        if not names:
            names = ["llama3:latest", "mistral:latest"]
        return {"models": names}
    except Exception:
        return {"models": ["llama3:latest", "mistral:latest"]}


@app.post("/api/investigate")
def investigate(request: InvestigationRequest):
    def event_generator():
        try:
            pipeline = InvestigationPipeline()
            stream = pipeline.run_query_stream(
                query=request.query,
                history=request.chat_history,
                use_web=request.use_web,
                model_name=request.model,
                document_context=request.document_context,
                session_id=request.session_id,
                temperature=request.temperature,
            )
            for chunk in stream:
                yield chunk
        except Exception as e:
            yield json.dumps({"type": "token", "data": f"\n\n[Error: {e}]"}) + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")


@app.get("/api/sessions")
def get_sessions():
    return {"sessions": db_manager.list_sessions()}


@app.get("/api/sessions/{session_id}")
def get_session(session_id: str):
    session_data = db_manager.get_session(session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
    return session_data


@app.post("/api/sessions")
def save_session(request: SessionSaveRequest):
    new_id = db_manager.save_session(
        session_id=request.session_id,
        title=request.title,
        messages=request.payload,
    )
    return {"session_id": new_id, "status": "success"}


@app.delete("/api/sessions/{session_id}")
def delete_session(session_id: str):
    db_manager.delete_session(session_id)
    return {"status": "success"}


@app.delete("/api/sessions")
def clear_all_sessions():
    db_manager.clear_sessions()
    return {"status": "success"}