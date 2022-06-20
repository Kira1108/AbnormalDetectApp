import os

SEX_IMAGE_DIM = 224 # 鉴黄色图片尺寸
SEX_MODEL_PATH = "app/datasets/nsfw_model.h5" # 鉴黄模型路径
HTML_IMAGE_DEFAULT_PATH = "./images" # 图片文件爬虫路径
SENSITIVE_PATH = "app/datasets/words_correct111.txt" # 异常词语库
ABNORMAL_WINDOW_MODEL_PATH = 'app/datasets/saved_models/window_model' # 异常弹窗模型路径
VIDEO_FILE_PATH = "videos/raw_videos" # 原始视频存放路径
VIDEO_EXTRACT_PATH = "videos/video_frames" # 抽帧存储文件夹路径
VIDEO_KEEP_RECENT_DAYS = 1 # 保留最近几天的视频文件
VIDEO_REMOVE_INTERVAL = 30 # 多少分钟调度清除任务一次
VIDEO_CALLBACK_URL = "" # 视屏处理结果回调地址
KPS = 1 # 每秒多少帧
USE_GPU = False # 是否使用GPU




def create_tmp_folders():
    if not os.path.exists(VIDEO_FILE_PATH):
        os.makedirs(VIDEO_FILE_PATH)

    if not os.path.exists(VIDEO_EXTRACT_PATH):
        os.makedirs(VIDEO_EXTRACT_PATH)

