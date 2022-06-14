from fastapi import APIRouter,File, UploadFile, Depends
import os
from app.config import VIDEO_FILE_PATH
from app.crud import save_video_raw
from app.utils import md5_id
from app.database import get_db

from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/video",
    tags=["video"],
    responses={404: {"description": "Not found"}})

@router.post("/videofile")
async def create_file(file: bytes = File(default=None),db: Session = Depends(get_db)):
    content_id = md5_id()
    filepath = os.path.join(VIDEO_FILE_PATH, f"{content_id}.mp4")
    with open(filepath, "wb") as f:
        f.write(file)
    save_video_raw(db, filepath, content_id)
    return {"succee":True, "filepath":filepath,"content_id":content_id}


@router.post("/videoupload")
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content_id = md5_id()
    try:
        contents = await file.read()
        filepath = os.path.join(VIDEO_FILE_PATH, f"{content_id}.mp4")
        with open(filepath, 'wb') as f:
            f.write(contents)
        save_video_raw(db, filepath, content_id)
    except Exception:
        return {"message": "There was an error uploading the video file"}
    finally:
        await file.close()
    return {"succee":True, "filepath":filepath,"content_id":content_id}