from fastapi import APIRouter
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import string
import random
import os

video_path = "/data/code/wanghuan/web_abnormal/videos"




def random_filename(length=8):
    return ''.join(
        random.choices(string.ascii_letters + string.digits, k=length)
        ) + ".mp4"

router = APIRouter(
    prefix="/video",
    tags=["video"],
    responses={404: {"description": "Not found"}})

@router.post("/videofile")
async def create_file(file: bytes = File(default=None)):
    filepath = os.path.join(video_path, random_filename())
    with open(filepath, "wb") as f:
        f.write(file)
    return {"succee":1, "filepath":filepath}


@router.post("/videoupload")
async def upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        filepath = os.path.join(video_path, file.filename)
        with open(filepath, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        await file.close()
    return {"message": f"Successfuly uploaded {file.filename}"}