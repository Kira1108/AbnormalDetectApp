from fastapi import APIRouter
from app.ocr import Ocr, BboxInfo
from app.sex_algo import SexDetector, SexInfo
from app.abn_window_algo import AbnWindowInfo, AbnormaWindowDetect
from pydantic import BaseModel
from app.reader import ImageReader
from app.config import USE_GPU
from typing import List

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
async def parse_ocr(path:str):
    img = ImageReader(path).read()
    r = ocr.detect(img)

    return OcrResponse(result = r)


@router.get("/sex", response_model=SexInfo)
async def parse_sex(path:str):
    img = ImageReader(path).read()
    return sex.predict(img)


@router.get("/window", response_model=AbnWindowInfo)
async def parse_window(path:str):
    img = ImageReader(path).read()
    return window.predict(img)

