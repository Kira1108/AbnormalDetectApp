from fastapi import APIRouter, Depends
from typing import List
from pydantic import BaseModel

from app.ocr import Ocr, BboxInfo
from app.sex_algo import SexDetector, SexInfo
from app.abn_window_algo import AbnWindowInfo, AbnormaWindowDetect
from app.reader import ImageReader
from app.config import USE_GPU
from app.utils import md5_id
from app.crud import save_ocr_result,save_sex_result
from app.database import get_db
from sqlalchemy.orm import Session



ocr = Ocr(use_gpu=USE_GPU)
sex = SexDetector()
window = AbnormaWindowDetect()

router = APIRouter(
    prefix="/image",
    tags=["image"],
    responses={404: {"description": "Not found"}},
)

class OcrResponse(BaseModel):
    result: List[BboxInfo]


@router.get("/ocr", response_model=OcrResponse)
async def parse_ocr(path:str, db: Session = Depends(get_db)):
    img = ImageReader(path).read()
    r = ocr.detect(img)
    save_ocr_result(db, r,md5_id(), 0, "")
    return OcrResponse(result = r)


@router.get("/sex", response_model=SexInfo)
async def parse_sex(path:str, db: Session = Depends(get_db)):
    img = ImageReader(path).read()
    r = sex.predict(img)
    save_sex_result(db, r, md5_id(), 0, "")
    return r


@router.get("/window", response_model=AbnWindowInfo)
async def parse_window(path:str):
    img = ImageReader(path).read()
    return window.predict(img)

