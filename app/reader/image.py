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


def b64string2numpy(b64string):
    """Convert a base64 encoded string to numpy array
    Args:
        b64string (_type_): string of encoded bytes
        format (str, optional): string of byte
    Returns:
        _type_: np.array
    """
    
    # if isinstance(b64string, str):
    #     b64string = b64string.encode()
    
    buff = io.BytesIO(base64.b64decode(b64string))
    image = Image.open(buff)
    
    image = np.array(image)
    if image.shape[-1] == 4:
        image = image[:, :, :3]
    return image

@dataclass
class Base64Reader(Reader):
    content:str
    def read(self):
        return b64string2numpy(self.content)


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
