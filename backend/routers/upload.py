import os
import tempfile
import shutil
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.session import create_session, get_session, update_session

router = APIRouter()

_TMP_DIR = os.path.join(tempfile.gettempdir(), "prioritization_tool")
os.makedirs(_TMP_DIR, exist_ok=True)


@router.post("/upload")
async def upload_files(
    method: str = Form(...),
    requirements_file: Optional[UploadFile] = File(None),
    weights_file: Optional[UploadFile] = File(None),
    data_file: Optional[UploadFile] = File(None),
    scale_file: Optional[UploadFile] = File(None),
    criteria_file: Optional[UploadFile] = File(None),
    alternatives_file: Optional[UploadFile] = File(None),
    session_id: Optional[str] = Form(None),
):
    if session_id and get_session(session_id):
        sid = session_id
    else:
        sid = create_session(method)

    session_dir = os.path.join(_TMP_DIR, sid)
    os.makedirs(session_dir, exist_ok=True)

    saved = {}

    async def save(upload: Optional[UploadFile], key: str):
        if upload and upload.filename:
            path = os.path.join(session_dir, f"{key}_{upload.filename}")
            with open(path, "wb") as f:
                shutil.copyfileobj(upload.file, f)
            saved[key] = path

    await save(requirements_file, "requirements_file")
    await save(weights_file, "weights_file")
    await save(data_file, "data_file")
    await save(scale_file, "scale_file")
    await save(criteria_file, "criteria_file")
    await save(alternatives_file, "alternatives_file")

    if not saved:
        raise HTTPException(status_code=400, detail="Не загружено ни одного файла")

    existing = get_session(sid)["files"]
    existing.update(saved)
    update_session(sid, method=method, files=existing)

    return {"session_id": sid, "file_keys": list(saved.keys())}
