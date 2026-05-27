import uuid
from typing import Dict, Any, Optional

sessions: Dict[str, Dict[str, Any]] = {}


def create_session(method: str) -> str:
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "method": method,
        "files": {},
        "results": None,
        "ai_summary": None,
        "conflicts": [],
        "ai_conflicts": [],
        "chat_history": [],
    }
    return session_id


def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    return sessions.get(session_id)


def update_session(session_id: str, **kwargs):
    if session_id in sessions:
        sessions[session_id].update(kwargs)


def get_all_completed_sessions() -> Dict[str, Dict[str, Any]]:
    return {sid: s for sid, s in sessions.items() if s.get("results") is not None}
