from app.crud import get_next_video, update_video_status
from app.reader import extract_video
from app.config import VIDEO_EXTRACT_PATH
from app.database import SessionLocal
import os
import shutil
import time
import logging
logger = logging.getLogger('uvicorn')


def process_next_video():
    while True:
        video = get_next_video(SessionLocal())
        if video is None:
            logger.info("No video to process")
        else:
            dest_path = os.path.join(VIDEO_EXTRACT_PATH, video.content_id)
            logger.info("Extracting video: %s", dest_path)
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)
            
            os.makedirs(dest_path)
            extract_video(video.video_path, dest_path)
            update_video_status(SessionLocal(), video)

        time.sleep(10)