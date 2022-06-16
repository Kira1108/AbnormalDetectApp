# Web abnormal content detection

## 1. 下载资源文件
下载dataset文件夹，解压到app目录下面      

到项目根目录执行以下操作
## 2. 虚拟环境
```bash
python -m venv env
```

## 3. 安装依赖
```bash
pip install -r requirements.txt
```
## 4. 配置
app/config.py
```python
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
USE_GPU = False # 是否使用GPU
```


## 4. 启动应用
```bash
./start_app.sh
```