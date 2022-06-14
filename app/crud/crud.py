from sqlalchemy.orm import Session
from app.models import OCRModel, TextModel, SexModel

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
    for record in text_result:
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
