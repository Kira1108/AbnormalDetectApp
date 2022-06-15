from app.crud import (
    get_next_video, 
    update_video_status,
    save_video_frame)
from app.reader import extract_video
from app.config import VIDEO_EXTRACT_PATH
from app.database import SessionLocal
from app.utils import md5_id
import os
import shutil
import time
import logging
import glob
logger = logging.getLogger('uvicorn')


def process_next_video():
    while True:
        video = get_next_video(SessionLocal())

        if video is None:
            logger.info("No video to process")
            time.sleep(5)
        
        else:
            extract_video(video.video_path, VIDEO_EXTRACT_PATH)
            dest_path = os.path.join(VIDEO_EXTRACT_PATH, video.content_id)
            logger.info(f"Extracting video from {video.video_path} to {dest_path}")

            # save video frames to database
            image_files = glob.glob(os.path.join(dest_path, "*.jpg"))
            for im in image_files:
                image_content_id = md5_id()
                save_video_frame(SessionLocal(), video.content_id, image_content_id, im)

            # update processing status
            update_video_status(SessionLocal(), video)

        