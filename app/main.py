from fastapi import FastAPI
from app import routers
from app.database import create_mysql_database_if_not_exists, engine
from app.config import create_tmp_folders
from app.models import Base
from threading import Thread
from app.video_process import process_next_video


app = FastAPI()

app.include_router(routers.image.router)
app.include_router(routers.text.router)
app.include_router(routers.scrape.router)
app.include_router(routers.website.router)
app.include_router(routers.videos.router)


@app.on_event("startup")
def init_db():
    create_mysql_database_if_not_exists()
    create_tmp_folders()
    Base.metadata.create_all(bind=engine)

    consumer = Thread(target=process_next_video)
    consumer.start()


@app.get("/")
async def root():
    return {"message": "success"}
