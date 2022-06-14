from typing import List
from paddleocr import PaddleOCR
import numpy as np
from pydantic import BaseModel
from abc import ABC, abstractmethod


class BboxInfo(BaseModel):
    text: str
    confidence: float = None
    topleft: List = None
    topright: List = None
    bottomright: List = None
    bottomleft: List = None


class OcrBase(ABC):

    @abstractmethod
    def detect(self, img) -> List[BboxInfo]:
        ...

    @abstractmethod
    def extract_texts(self, img) -> List[str]:
        ...


class Ocr(OcrBase):
    """
        Extract texts from image files
        ```python
        ocr = Ocr()
        ocr.detect(img) # get detailed detection information
        ocr.extract_texts(img) # only get list of string texts
        ```
    """

    def __init__(self, use_gpu=False):
        self.detector = PaddleOCR(use_angle_cls=False, use_gpu=use_gpu)

    def cvt_bbox(self, line):
        topleft, topright, bottomright, bottomleft \
            = np.array(line[0]).astype(np.int32).tolist()

        text, confidence = line[1]

        return BboxInfo(topleft=topleft,
                        topright=topright,
                        bottomright=bottomright,
                        bottomleft=bottomleft,
                        text=text,
                        confidence=confidence)

    def detect(self, img) -> List[BboxInfo]:
        result = self.detector.ocr(img)
        return [self.cvt_bbox(line) for line in result]

    def extract_texts(self, img) -> List[str]:
        return [bbox.text for bbox in self.detect(img)]
