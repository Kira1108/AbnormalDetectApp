# from sqlalchemy import create_engine
# import pandas as pd
# import numpy as np



# engine = create_engine('mysql+pymysql://root:root123@localhost:5306/test_db')
# databases = pd.read_sql_query("show databases", engine)
# df = pd.DataFrame(np.random.random((3,3)), columns = ['A','B','C'])
# df.to_sql("testtable", engine, index = False, if_exists = "replace")
# pd.read_sql_query("select * from testtable", engine)



from app.database import get_db, SessionLocal
from app.models import VideoModel
from fastapi import Depends
from sqlalchemy.orm import Session

def get_next_video(db: Session):
    return db.query(VideoModel)\
        .filter(VideoModel.is_processed == 0)\
        .order_by(VideoModel.create_time.asc())\
        .first()

print(get_next_video(SessionLocal()).video_path)



