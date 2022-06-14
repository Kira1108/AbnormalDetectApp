from pydantic import BaseModel
from fastapi import APIRouter
from typing import List, Dict
from .image import ocr, sex, window
from .text import dfa_parser
from app.ocr import BboxInfo
from app.text_algo import TextInfo
from app.abn_window_algo import AbnWindowInfo
from app.sex_algo import SexInfo
from app.reader import ImageReader
import operator
import json
import base64
import logging
logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/website",
    tags=["website"],
    responses={404: {"description": "Not found"}},
)


class ContentInfo(BaseModel):
    url: str
    content: str


class AppInfo(BaseModel):
    app_name: str


class WebsiteRequestModel(BaseModel):
    timestamp: int
    reader_type: str
    model: List[str]
    url_list: List[ContentInfo]
    uuid: str
    app_info: AppInfo


sample_data = {'timestamp': 1630336230,
               'reader_type': 'image',
               'model': ['sex', 'ocr_text'],
               'url_list': [
                   {'url': 'data/2021-08-30 23/image/http__www_ceair_com_/a588acbace2a2bda1f6e714cd0f33399.jpg',
                    'content': 'bb64'}],
               'uuid': '6aa2082209a411ec9f5fb0a46069e598',
               'app_info': {'app_name': 'http://www.ceair.com/'}
               }

req = WebsiteRequestModel(**sample_data)


class WebSiteScanner():

    def _ocr(self, img) -> List[BboxInfo]:
        return ocr.detect(img)

    def _texts(self, texts) -> TextInfo:
        return dfa_parser.parse(texts)

    def _window(self, img) -> AbnWindowInfo:
        return window.predict(img)

    def _sex(self, img) -> SexInfo:
        return sex.predict(img)

    def _ocr_text(self, img) -> TextInfo:
        bboxes = self._ocr(img)
        return self._texts([box.text for box in bboxes])

    def _get_text_all_result(self, textinfo: TextInfo) -> List[Dict]:
        return [t for t in textinfo.result]

    def _filter_text_result(self, textinfo: TextInfo) -> List[Dict]:
        return [t for t in textinfo.result if t['sensitive']]

    def response_to(self, req: WebsiteRequestModel):

        common_info = {
            "timestamp": req.timestamp,
            "uuid": req.uuid,
            "app_info": req.app_info.dict()
        }

        print(common_info)

        model_result = {
            'sex': None,
            'text': None,
            'ocr': None,
            'ocr_text': None,
            'popup': None
        }

        content = req.url_list[0].content

        try:
            # 解码图片和文字中的文字保证后续算法可用
            if req.reader_type == 'image':
                content = ImageReader(content=content).read()

            if req.reader_type == 'text':
                decoded = base64.b64decode(content)
                content = json.loads(decoded)
        except Exception as e:
            logger.error(str(e))
            return common_info.update(model_result)

        if 'ocr_text' in req.model:
            # 图片文字异常检测
            try:
                r = self._ocr_text(content)
                model_result['ocr_text_all'] = self._get_text_all_result(r)
                r = self._filter_text_result(r)

                model_result['ocr_text'] = r
            except Exception as e:
                logger.error(str(e))
                model_result['ocr_text'] = 'error'

        if 'text' in req.model:
            # 文字异常检测
            try:
                r = self._texts(content)
                model_result['text_all'] = self._get_text_all_result(r)

                r = self._filter_text_result(r)
                model_result['text'] = r
            except:
                model_result['text'] = 'error'
        # 图片中的文字提取
        if 'ocr' in req.model:
            try:
                r = self._ocr(content)
                model_result['ocr'] = [
                    {'text': box.text, 'confidence': box.confidence}
                    for box in r]
            except Exception as e:
                logger.error(str(e))
                model_result['ocr'] = 'error'

        if 'popup' in req.model:
            try:
                r = self._window(content)
                model_result['popup'] = r.dict()
            except Exception as e:
                logger.error(str(e))
                model_result['popup'] = 'error'

        if 'sex' in req.model:
            try:
                r = self._sex(content).result
                sex_type = max(r.items(), key=operator.itemgetter(1))[0]
                if sex_type == 'porn' or sex_type == 'sex':
                    res = {'is_abnormal': 1, 'confidence': r[sex_type]}
                else:
                    res = {'is_abnormal': 0, 'confidence': 1}
                model_result['sex'] = res
            except Exception as e:
                logger.error(str(e))
                model_result['sex'] = 'error'

        common_info.update(model_result)
        common_info.update({'url': req.url_list[0].url})
        return common_info


scanner = WebSiteScanner()


@router.post("/scan")
async def parse_website(req: WebsiteRequestModel):
    return scanner.response_to(req)
