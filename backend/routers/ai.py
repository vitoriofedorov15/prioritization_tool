import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from services.session import get_session, update_session
from services import ai_service

router = APIRouter()


class SessionRequest(BaseModel):
    session_id: str


class ChatRequest(BaseModel):
    session_id: str
    message: str
    history: list = []


@router.post("/ai/interpret")
async def interpret(req: SessionRequest):
    session = get_session(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Сессия не найдена")
    if not session.get("results"):
        raise HTTPException(status_code=400, detail="Сначала выполните расчёт")

    if session.get("ai_summary"):
        return {"summary": session["ai_summary"], "ai_available": True}

    if not ai_service.AI_AVAILABLE:
        return {"summary": None, "ai_available": False}

    try:
        summary = ai_service.generate_interpretation(session["method"], session["results"])
        update_session(req.session_id, ai_summary=summary)
        return {"summary": summary, "ai_available": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ai/conflicts")
async def detect_conflicts(req: SessionRequest):
    session = get_session(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Сессия не найдена")

    conflicts = session.get("conflicts", [])
    if not conflicts:
        return {"conflicts": [], "ai_available": ai_service.AI_AVAILABLE}

    if session.get("ai_conflicts"):
        return {"conflicts": session["ai_conflicts"], "ai_available": True}

    try:
        enriched = ai_service.analyze_conflicts_with_ai(conflicts, session["method"])
        update_session(req.session_id, ai_conflicts=enriched)
        return {"conflicts": enriched, "ai_available": ai_service.AI_AVAILABLE}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ai/chat")
async def chat(req: ChatRequest):
    session = get_session(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Сессия не найдена")

    history = req.history or session.get("chat_history", [])

    async def event_stream():
        full_response = ""
        try:
            async for chunk in ai_service.stream_chat(session, req.message, history):
                yield chunk
                if chunk.startswith("data: "):
                    try:
                        data = json.loads(chunk[6:])
                        if "chunk" in data:
                            full_response += data["chunk"]
                    except Exception:
                        pass
        finally:
            new_history = history + [
                {"role": "user", "content": req.message},
                {"role": "assistant", "content": full_response},
            ]
            update_session(req.session_id, chat_history=new_history[-20:])

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.get("/sessions")
async def list_sessions():
    from services.session import get_all_completed_sessions
    sessions = get_all_completed_sessions()
    return {
        sid: {
            "method": s["method"],
            "alternatives": list(s["results"].keys()) if s.get("results") else [],
        }
        for sid, s in sessions.items()
    }


@router.get("/session/{session_id}")
async def get_session_data(session_id: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Сессия не найдена")
    return {
        "method": session["method"],
        "results": session.get("results"),
        "conflicts": session.get("ai_conflicts") or session.get("conflicts", []),
        "ai_summary": session.get("ai_summary"),
    }
