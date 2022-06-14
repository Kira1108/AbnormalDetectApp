import requests
import html2text
from .base import Reader
from dataclasses import dataclass
from urllib.parse import urlparse, urljoin
import html2text
from lxml import etree
from typing import List
from pydantic import BaseModel
import os
import urllib.parse
import hashlib
from app.config import HTML_IMAGE_DEFAULT_PATH
import logging
logger = logging.getLogger(__name__)


class HTMLInfo(BaseModel):
    texts: List[str] = None
    image_urls: List[str] = None
    image_save_path: str = None


def download_img(url, folder_path):
    logger.info(f'Downloading image from {url}')
    filename = url.split("/")[-1]
    save_path = os.path.join(folder_path, filename)
    img_stream = requests.get(url).content
    with open(save_path, 'wb') as f:
        f.write(img_stream)


def gen_hash(val):
    hash_object = hashlib.md5(val.encode())
    md5_hash = hash_object.hexdigest()
    return md5_hash


@dataclass
class SimpleHtmlReader(Reader):
    url: str
    download_img: bool = False
    download_path: str = HTML_IMAGE_DEFAULT_PATH

    def __post_init__(self):
        parsed_url = urlparse(self.url)

        # make a base url to join image strings
        self.base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        # make a download path for each image page
        quoted_url = urllib.parse.quote(self.url)
        self.download_path = os.path.join(self.download_path, gen_hash(parsed_url.netloc))

        if self.download_img and (not os.path.exists(self.download_path)):
            os.makedirs(self.download_path)

        self.is_read = False

    def _request(self):
        self.html = requests.get(self.url).content.decode('utf-8')
        self.is_read = True

    def read_text(self) -> List[str]:
        if not self.is_read:
            self._request()

        results = []
        for line in html2text.html2text(self.html).split("\n"):
            r = line.strip()
            if len(r) > 0:
                results.append(r)
        return results

    def read_image_url(self) -> List[str]:
        if not self.is_read:
            self._request()

        rel_urls = etree.HTML(self.html).xpath("//img/@src")
        image_urls = []
        for u in rel_urls:
            if not u.startswith('http'):
                image_urls.append(urljoin(self.base_url, u))
            else:
                image_urls.append(u)
        return image_urls

    def read(self):
        texts = self.read_text()
        image_urls = self.read_image_url()
        info = HTMLInfo(texts=texts, image_urls=image_urls, image_save_path=self.download_path)

        if not self.download_img:
            return info

        for url_ in image_urls:
            try:
                download_img(url_, self.download_path)
            except Exception as e:
                logger.warning(f"Failed to download image from {url_}")
                logger.warning(e)
        return info
