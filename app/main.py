from fastapi import FastAPI
from app import routers
from app.database import create_mysql_database_if_not_exists, engine
from app.config import create_tmp_folders,VIDEO_REMOVE_INTERVAL
from app.models import Base
from threading import Thread
from app.video_process import process_next_video

from apscheduler.schedulers.background import BackgroundScheduler
from app.utils import remove_file

import logging

logger = logging.getLogger('uvicorn')


app = FastAPI()

app.include_router(routers.image.router)
app.include_router(routers.text.router)
app.include_router(routers.scrape.router)
app.include_router(routers.website.router)
app.include_router(routers.videos.router)


@app.on_event("startup")
def init_project():

    # create database and folders
    create_mysql_database_if_not_exists()
    create_tmp_folders()

    # create all tables
    Base.metadata.create_all(bind=engine)

    # start video processing thread

    scheduler = BackgroundScheduler()
    scheduler.add_job(remove_file,'interval',
                      minutes=VIDEO_REMOVE_INTERVAL)
    scheduler.start()
    
    logger.info("Start clearnup task successfully")
    consumer = Thread(target=process_next_video)
    consumer.start()

@app.get("/")
async def root():
    return {"message": "success"}
