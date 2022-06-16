from app.database import engine


from dataclasses import dataclass

@dataclass
class SexResultSchema:
    video_content_id:str
    image_content_id:str
    drawings:float
    hentai:float
    neutral:float
    porn:float
    sex:float

    @property
    def is_sensitive(self):
        dic = {
            "drawings":self.drawings,
            "hentai":self.hentai,
            "neutral":self.neutral,
            "porn":self.porn,
            "sex":self.sex
        }

        k = max(dic, key = dic.get) 
        return (k in ['hentai','porn','sexy']) and getattr(self, k) > 50

    def dict(self):
        return {
            "image_content_id":self.image_content_id,
            "drawings":self.drawings,
            "hentai":self.hentai,
            "neutral":self.neutral,
            "porn":self.porn,
            "sex":self.sex,
            "is_sensitive":self.is_sensitive 
        }

@dataclass
class TextResultSchema:
    video_content_id:str
    image_content_id:str
    text:str
    is_sensitive:bool
    sensitive_words:str
    topleft:str
    bottomright:str

    def dict(self):
        return {
            "image_content_id":self.image_content_id,
            "text":self.text,
            "is_sensitive":self.is_sensitive,
            "sensitive_words":self.sensitive_words,
            'topleft':self.topleft,
            'bottomright':self.bottomright
        }

def get_video_sex_result(video_content_id):

    sql = f"""
    select vf.video_content_id, vf.image_content_id, s.drawings, s.hentai, s.neutral, s.porn, s.sexy from video_frames vf
    inner join sex_result s on s.content_id = vf.image_content_id
    where video_content_id = '{video_content_id}'

    """

    with engine.connect() as conn:
        result = conn.execute(sql).cursor.fetchall()

    return [SexResultSchema(*r) for r in result]

def get_video_sensitive_sex(video_content_id):

    result = get_video_sex_result(video_content_id)
    sex_pics = list(filter(lambda x:x.is_sensitive, result))
    video_sensitive = len(sex_pics) > 0

    return {
        "is_sensitive":video_sensitive,
        "sex_images":[s.dict() for s in sex_pics]
        }

def get_video_text_result(video_content_id):

    sql = f"""
    select vf.video_content_id, vf.image_content_id, t.text, t.sensitive, t.sensitive_words, o.topleft, o.bottomright from video_frames vf
    inner join ocr_result o on o.content_id = vf.image_content_id
    inner join text_result t on t.content_id = o.content_id
    where video_content_id = '{video_content_id}'
    """

    with engine.connect() as conn:
        result = conn.execute(sql).cursor.fetchall()

    return [TextResultSchema(*r) for r in result]

def get_video_sensitive_text(video_content_id):
    result = get_video_text_result(video_content_id)
    illegal_text = list(filter(lambda x:x.is_sensitive, result))
    video_sensitive = len(illegal_text) > 0

    return {
        "is_sensitive":video_sensitive,
        "illegal_text":[s.dict() for s in illegal_text]    
    }

def get_video_result(video_content_id):
    sex_result = get_video_sensitive_sex(video_content_id)
    text_result = get_video_sensitive_text(video_content_id)
    return {
        "video_content_id":video_content_id,
        "is_sensitive":sex_result['is_sensitive'] or text_result['is_sensitive'],
        "sex_result":sex_result,
        "text_result": text_result
    }