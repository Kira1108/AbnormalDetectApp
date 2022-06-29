from app.crud import (
    get_next_video, 
    update_video_status,
    save_video_frame,
    save_sex_result,
    save_ocr_result,
    save_text_result,
    get_video_result)

from app.routers.image import (ocr, sex)
from app.routers.text import dfa_parser
from app.reader import extract_video, ImageReader
from app.config import VIDEO_EXTRACT_PATH, VIDEO_CALLBACK_URL, KPS
from app.database import SessionLocal
from app.utils import md5_id

import os
import time
import logging
import glob
import requests
from sqlalchemy.orm import Session
logger = logging.getLogger('uvicorn')



def process_image(db:Session, image_path:str, content_id:str):
    img = ImageReader(path = image_path).read()

    image_id = int(os.path.basename(image_path).split(".")[0].split("_")[-1])

    r_sex = sex.predict(img)
    save_sex_result(db, r_sex, content_id, image_id, image_path)

    r_ocr = ocr.detect(img)
    save_ocr_result(db, r_ocr, content_id, image_id, image_path)

    texts = [t.text for t in r_ocr]
    r_text = dfa_parser.parse(texts)
    save_text_result(db, r_text, content_id)



def process_next_video():
    while True:
        video = get_next_video(SessionLocal())

        if video is None:
            logger.info("No video to process")
            time.sleep(5)
            continue
        else:
            extract_video(video.video_path, VIDEO_EXTRACT_PATH, kps = KPS)
            dest_path = os.path.join(VIDEO_EXTRACT_PATH, video.content_id)
            logger.info(f"Extracting video from {video.video_path} to {dest_path}")

            # save video frames to database
            image_files = glob.glob(os.path.join(dest_path, "*.jpg"))
            for im in image_files:
                image_content_id = md5_id()
                try:
                    logger.info(f"Processing image: {im}")
                    save_video_frame(SessionLocal(), video.content_id, image_content_id, im)
                    process_image(SessionLocal(), im, image_content_id)
                except Exception as e:
                    logger.error(f"Error processing image {im}")
                    logger.error(e)

            # update processing status
            update_video_status(SessionLocal(), video)
            import json
            json_content = json.dumps(get_video_result(video.content_id))
            with open("videojson.json",'w') as f:
                f.write(json_content)

        if VIDEO_CALLBACK_URL != "":
            requests.post(VIDEO_CALLBACK_URL, json=get_video_result(video.content_id))
    
