from fastapi import APIRouter, Depends
from typing import List
from pydantic import BaseModel

from app.ai.ocr import Ocr, BboxInfo
from app.ai.sex_algo import SexDetector, SexInfo
from app.ai.abn_window_algo import AbnWindowInfo, AbnormaWindowDetect
from app.reader import ImageReader
from app.config import USE_GPU
from app.utils import md5_id
from app.crud import save_ocr_result,save_sex_result, save_text_result
from app.database import get_db
from .text import dfa_parser
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


@router.get("/ocr_local", response_model=OcrResponse)
async def parse_ocr(path:str, db: Session = Depends(get_db)):
    img = ImageReader(path).read()
    r = ocr.detect(img)
    save_ocr_result(db, r,md5_id(), 0, "")
    return OcrResponse(result = r)


@router.get("/sex_local", response_model=SexInfo)
async def parse_sex(path:str, db: Session = Depends(get_db)):
    img = ImageReader(path).read()
    r = sex.predict(img)
    save_sex_result(db, r, md5_id(), 0, "")
    return r


@router.get("/window_local", response_model=AbnWindowInfo)
async def parse_window(path:str):
    img = ImageReader(path).read()
    return window.predict(img)

# == post requests

class Base64Input(BaseModel):
    image:str

@router.post("/ocr", response_model=OcrResponse)
async def parse_ocr(image:Base64Input, db: Session = Depends(get_db)):
    img = ImageReader(content = image.image).read()
    r = ocr.detect(img)
    save_ocr_result(db, r,md5_id(), 0, "")
    return OcrResponse(result = r)


@router.post("/sex", response_model=SexInfo)
async def parse_sex(image:Base64Input, db: Session = Depends(get_db)):
    img = ImageReader(content = image.image).read()
    r = sex.predict(img)
    save_sex_result(db, r, md5_id(), 0, "")
    return r

@router.post("/all")
async def parse_all(image:Base64Input, db: Session = Depends(get_db)):
    img = ImageReader(content = image.image).read()

    content_id = md5_id()

    r_sex = sex.predict(img)
    save_sex_result(db, r_sex, content_id, 0, "")

    r_ocr = ocr.detect(img)
    save_ocr_result(db, r_ocr, content_id, 0, "")

    texts = [t.text for t in r_ocr]
    r_text = dfa_parser.parse(texts)
    save_text_result(db, r_text, content_id)

    text_sensitive = any(record['sensitive'] for record in r_text.result)

    sex_dic = r_sex.sex_model_result

    max_key = max(sex_dic, key = sex_dic.get)
    sex_sensitive = max_key in ['hentai','porn','sexy'] and sex_dic[max_key] > 50

    return {
        "image_content_id":content_id,
        "is_sensitive":text_sensitive or sex_sensitive,
        "sex_result": r_sex.sex_model_result, 
        "text_result": r_text.result
        }



@router.post("/window", response_model=AbnWindowInfo)
async def parse_window(image:Base64Input):
    img = ImageReader(image.image).read()
    return window.predict(img)

