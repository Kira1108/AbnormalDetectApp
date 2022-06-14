import os
os.environ['TFHUB_CACHE_DIR'] = "app/datasets/tfhub_modules"
import numpy as np
import tensorflow as tf
from tensorflow import keras
import tensorflow_hub as hub
from app.config import SEX_IMAGE_DIM, SEX_MODEL_PATH
import cv2
from pydantic import BaseModel
from typing import Dict
import logging
logger = logging.getLogger(__name__)



def _preprocessing(img):
    img = cv2.resize(img, (SEX_IMAGE_DIM, SEX_IMAGE_DIM))
    img = img / 255.
    return img


def _load_model(model_path=SEX_MODEL_PATH):
    if model_path is None or (not os.path.exists(model_path)):
        raise ValueError("Unable to load model from model path")


    print("Loading sex model")
    model = tf.keras.models.load_model(model_path, custom_objects={
                                    'KerasLayer': hub.KerasLayer})
    print("Loading sex model done.")

    return model
 
def _predict(model, nd_images):
    """ Classify given a model, image array (numpy)...."""

    model_preds = model.predict(nd_images)
    # preds = np.argsort(model_preds, axis = 1).tolist()

    categories = ['drawings', 'hentai', 'neutral', 'porn', 'sexy']

    probs = []
    for i, single_preds in enumerate(model_preds):
        single_probs = {}
        for j, pred in enumerate(single_preds):
            single_probs[categories[j]] = round(float(pred), 6) * 100
        probs.append(single_probs)
    return probs


class SexInfo(BaseModel):
    sex_model_result:Dict[str,float]

class SexDetector():
    def __init__(self):
        self.model = _load_model()

    def predict(self, img):
        img = _preprocessing(img)
        img = np.array([img])
        return SexInfo(sex_model_result = _predict(self.model, img)[0])

