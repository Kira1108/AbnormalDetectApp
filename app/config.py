import os

SEX_IMAGE_DIM = 224
SEX_MODEL_PATH = "app/datasets/nsfw_model.h5"
HTML_IMAGE_DEFAULT_PATH = "./images"
SENSITIVE_PATH = "app/datasets/words_correct111.txt"
ABNORMAL_WINDOW_MODEL_PATH = 'app/datasets/saved_models/window_model'
VIDEO_FILE_PATH = "./videos/raw_videos"
VIDEO_EXTRACT_PATH = "./videos/video_frames"
USE_GPU = False



def create_tmp_folders():
    if not os.path.exists(VIDEO_FILE_PATH):
        os.makedirs(VIDEO_FILE_PATH)

    if not os.path.exists(VIDEO_EXTRACT_PATH):
        os.makedirs(VIDEO_EXTRACT_PATH)

