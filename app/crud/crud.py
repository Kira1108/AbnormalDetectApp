from sqlalchemy.orm import Session
from sqlalchemy import update
from app.models import (
    OCRModel, 
    TextModel, 
    SexModel, 
    VideoModel, 
    VideoFrames)

def save_ocr_result(db:Session, ocr_result, content_id, image_id, image_path):
    for box in ocr_result:
        box_result = OCRModel(
            text = box.text,
            confidence = box.confidence,
            topleft = str(box.topleft),
            topright = str(box.topright),
            bottomright = str(box.bottomright),
            bottomleft = str(box.bottomleft),
            content_id = content_id,
            image_id = image_id,
            image_path = image_path
        )
        db.add(box_result)
        db.commit()


def save_text_result(db:Session, text_result, content_id):
    for record in text_result.result:
        text_model = TextModel(
            content_id = content_id,
            text = record['text'],
            sensitive = record['sensitive'],
            sensitive_words = str(record['sensitive_words'])
        )
        db.add(text_model)
        db.commit()


def save_sex_result(db:Session, sex_result, content_id, image_id, image_path):
    sex = SexModel(
        content_id = content_id,
        image_id = image_id,
        image_path = image_path,
        **sex_result.sex_model_result
    )

    db.add(sex)
    db.commit()

def save_video_raw(db:Session, video_path:str, content_id):
    video = VideoModel(
        video_path = video_path, 
        content_id = content_id, 
        is_processed = False)
    db.add(video)
    db.commit()


def get_next_video(db: Session):
    return db.query(VideoModel)\
        .filter(VideoModel.is_processed == 0)\
        .order_by(VideoModel.create_time.asc())\
        .first()


def update_video_status(db: Session, video):
    db.execute(update(VideoModel)\
        .where(VideoModel.content_id == video.content_id)\
        .values(is_processed = True))
    db.commit()


def save_video_frame(db: Session, video_content_id, image_content_id, image_path):
    video_frame = VideoFrames(
        video_content_id = video_content_id,
        image_content_id = image_content_id,
        image_path = image_path
    )
    db.add(video_frame)
    db.commit()

