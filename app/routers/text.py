from fastapi import APIRouter
from pydantic import BaseModel
from app.text_algo import DFAParser, TextInfo
from typing import List



dfa_parser = DFAParser()

router = APIRouter(
    prefix="/text",
    tags=["text"],
    responses={404: {"description": "Not found"}},
)

class TextInput(BaseModel):
    text:List[str]

@router.post("/dfa", response_model=TextInfo)
async def parse_text(texts:TextInput):
    return dfa_parser.parse(texts.text)