from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Dense, Flatten
from tensorflow.keras.models import Model
from app.config import ABNORMAL_WINDOW_MODEL_PATH
import cv2
import numpy as np
from pydantic import BaseModel
import tensorflow as tf
tf.random.set_seed(0)
import logging
logger = logging.getLogger(__name__)

INPUT_DIM = (150, 80, 3)


def create_model():
    inputs = Input(shape = INPUT_DIM)
    x = Conv2D(64,3,activation = 'relu', strides = 10)(inputs)
    x = MaxPooling2D()(x)
    x = Conv2D(32,3,activation = 'relu')(inputs)
    x = MaxPooling2D()(x)
    x = Conv2D(32,3,activation = 'relu')(inputs)
    x = MaxPooling2D()(x)
    x = Flatten()(x)
    x = Dense(128, activation = 'relu')(x)
    outputs = Dense(1, activation = 'sigmoid')(x)
    model = Model(inputs, outputs)
    return model


def load_model():
    logger.info("Loading abnormal window detection model")
    return tf.keras.models.load_model(ABNORMAL_WINDOW_MODEL_PATH)


class AbnWindowInfo(BaseModel):
    confidence:float
    is_abnormal:bool

class AbnormaWindowDetect():
    def __init__(self, thresh = 0.5):
        # self.model = create_model()
        self.model = load_model()
        # logger.info("Loading weights from {}".format(ABNORMAL_WINDOW_MODEL_PATH))
        # self.model.load_weights(ABNORMAL_WINDOW_MODEL_PATH)
        self.thresh = thresh

    def _preprocess(self, img):
        img = cv2.resize(img, (80, 150))
        img = img / 255.0
        return img

    def predict(self, img):
        img = self._preprocess(img)
        confidence = self.model.predict(np.array([img])).flatten()[0]
        is_abnormal = confidence > self.thresh
        return AbnWindowInfo(confidence=confidence, is_abnormal=is_abnormal)
