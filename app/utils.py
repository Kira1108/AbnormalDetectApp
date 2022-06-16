from datetime import datetime
import hashlib
from datetime import datetime
import os
import glob
import logging
import shutil
from app.config import (
    VIDEO_FILE_PATH, 
    VIDEO_EXTRACT_PATH,
    VIDEO_KEEP_RECENT_DAYS)
logger = logging.getLogger('uvicorn')

  
def md5_id():
    str2hash = str(datetime.now().timestamp())
    return hashlib.md5(str2hash.encode()).hexdigest()


def remove_file(keep_recent_days = VIDEO_KEEP_RECENT_DAYS):
    video_glob = os.path.join(VIDEO_FILE_PATH, '*.mp4')
    vide_extract_glob = os.path.join(VIDEO_EXTRACT_PATH, '*')

    videofiles = glob.glob(video_glob)
    video_extract_files = glob.glob(vide_extract_glob)

    if len(videofiles) ==0 and len(video_extract_files) == 0:
        logger.info("No file or folder to remove")

    for f in videofiles:
        modify_time = os.path.getmtime(f)
        modify_time = datetime.fromtimestamp(int(modify_time))
        if (datetime.now() - modify_time).days >= keep_recent_days:
            os.remove(f)
        logger.info(f"Removing file {f}")

    for folder in video_extract_files:
        modify_time = os.path.getmtime(folder)
        modify_time = datetime.fromtimestamp(int(modify_time))
        if (datetime.now() - modify_time).days >= keep_recent_days:
            shutil.rmtree(folder)
        logger.info(f"Removing folder {folder}")