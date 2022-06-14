from fastapi import FastAPI
from app import routers
from app.database import create_mysql_database_if_not_exists, engine
from app.models import Base


app = FastAPI()

app.include_router(routers.image.router)
app.include_router(routers.text.router)
app.include_router(routers.scrape.router)
app.include_router(routers.website.router)
app.include_router(routers.videos.router)

@app.on_event("startup")
def init_db():
    create_mysql_database_if_not_exists()
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "success"}
