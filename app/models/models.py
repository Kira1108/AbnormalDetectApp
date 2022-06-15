from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func
from app.database import Base


class OCRModel(Base):
    __tablename__ = 'ocr_result'
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Text)
    image_id  = Column(Integer)
    image_path = Column(Text)
    create_time = Column(DateTime, default = func.now())
    text = Column(Text)
    confidence = Column(Float)
    topleft = Column(String(50))
    topright = Column(String(50))
    bottomright = Column(String(50))
    bottomleft = Column(String(50))


class SexModel(Base):
    __tablename__ = 'sex_result'
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Text)
    image_id  = Column(Integer)
    image_path = Column(Text)
    create_time = Column(DateTime, default = func.now())
    drawings = Column(Float)
    hentai = Column(Float)
    neutral = Column(Float)
    porn = Column(Float)
    sexy = Column(Float)


class TextModel(Base):
    __tablename__ = 'text_result'
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Text)
    create_time = Column(DateTime, default = func.now())
    text = Column(Text)
    sensitive = Column(Boolean)
    sensitive_words = Column(Text)


class VideoModel(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Text)
    create_time = Column(DateTime, default = func.now())
    video_path = Column(String(200))
    is_processed = Column(Boolean, default = False)


class VideoFrames(Base):
    __tablename__ = 'video_frames'
    id = Column(Integer, primary_key=True, index=True)
    video_content_id = Column(Text)
    image_content_id = Column(Text)
    image_path = Column(String(200))
    create_time = Column(DateTime, default = func.now())





