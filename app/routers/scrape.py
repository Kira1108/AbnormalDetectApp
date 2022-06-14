from logging import StringTemplateStyle
from fastapi import APIRouter
from pydantic import BaseModel
from app.reader.html import SimpleHtmlReader, HTMLInfo
from typing import Optional
from typing import List




router = APIRouter(
    prefix="/scrape",
    tags=["scrape"],
    responses={404: {"description": "Not found"}},
)

class TextInput(BaseModel):
    text:List[str]

@router.get("/site", response_model=HTMLInfo)
async def scrape_site(url:str, download_img:bool = False, download_path:str = None):
    if download_img and download_path:
        html_reader = SimpleHtmlReader(url, download_img, download_path)
    else:
        html_reader = SimpleHtmlReader(url, download_img)
    return html_reader.read()