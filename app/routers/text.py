from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List

from app.text_algo import DFAParser, TextInfo
from app.utils import md5_id
from app.crud import save_text_result
from app.database import get_db
from sqlalchemy.orm import Session


dfa_parser = DFAParser()

router = APIRouter(
    prefix="/text",
    tags=["text"],
    responses={404: {"description": "Not found"}},
)

class TextInput(BaseModel):
    text:List[str]

@router.post("/dfa", response_model=TextInfo)
async def parse_text(texts:TextInput, db: Session = Depends(get_db)):
    r = dfa_parser.parse(texts.text)
    save_text_result(db, r, md5_id())
    return r