"""
Simply read an image from a path, use are going to use ImageReader directly
"""

from .base import Reader
import numpy as np
import cv2
from PIL import Image
# import cairosvg
import io
from dataclasses import dataclass
import base64
import io
import numpy as np


@dataclass
class CommonImageFileReader(Reader):
    path: str

    def read(self):
        img = cv2.imread(self.path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img


# @dataclass
# class SVGFileReader(Reader):
#     path: str

#     def read(self):
#         stream = io.BytesIO(cairosvg.svg2png(url=self.path, ))
#         img = Image.open(stream)

#         background = Image.new("RGB", img.size, (255, 255, 255))
#         background.paste(img, mask=img.split()[3])
#         return np.array(background)


@dataclass
class Base64Reader(Reader):
    content:str
    def read(self):
        imgdata = base64.b64decode(self.content)
        image = Image.open(io.BytesIO(imgdata)).convert('RGB')
        return np.array(image)


PROCESSORS = {
    "base64": Base64Reader,
    # "svg": SVGFileReader,clear
    "jpg": CommonImageFileReader,
    "png": CommonImageFileReader,
    "jpeg": CommonImageFileReader,
    "default": CommonImageFileReader
}


@dataclass
class ImageReader(Reader):
    '''Pass a path if read a image file, if base64, pass a content'''
    path: str = None
    content: str = None

    def __post_init__(self):
        if self.content:
            filetype = 'base64'
            self.reader = PROCESSORS['base64'](self.content)
        else:
            filetype = self.path.split(".")[-1]
            self.reader = PROCESSORS.get(filetype, PROCESSORS['default'])(self.path)

    def read(self):
        return self.reader.read()
