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

## 图片接口
请求接口

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/image/all' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "image": "iVBORw0KGgoAAAANSUhEUgAACagAAAFICAYAAAC/NYsHAAAMamlDQ1BJQ0MgUHJvZmlsZQAASImVlwdYU8kWgOeWJCQkoQQiICX0JkivUkJoEQSkCjZCEkgoMSYEFTu6qODaRRQruiqi6FoAWVTEXhbF3hcLKsq6WFAUlTchAV33le/N982d/545c86Zc2fuvQOAVg9PKs1FtQHIk+TL4iNCWGNS01ikp4AAjAAKAPDl8eVSdlxcNGQw0P69vL8BEGV71Ulp65/9/7XoCoRyPgDIOMgZAjk/D3ITAPh6vlSWDwBRKbecki9V8hzIejIYIORVSs5S8U4lZ6i4sV8nMZ4D+TIAGlQeT5YFAP0elLMK+FnQDv0zZBeJQCwBQGsY5EC+iCeArIx9WF7eJCWXQ7aD+lLIMB7gk/Gdzay/2c8YtM/jZQ2yal79RSNULJfm8qb9n6n53yUvVzHgwwZWqkgWGa+cP8zhrZxJUUqmQu6UZMTEKnMNuUcsUOUdAJQiUkQmqfRRY76cA/"
}'
```

返回示例
```json
{
  "image_content_id": "d08716b395986a3ba2176a24fd52fe72",
  "is_sensitive": true,
  "sex_result": {
    "drawings": 6.3732999999999995,
    "hentai": 0.2313,
    "neutral": 93.3058,
    "porn": 0.0217,
    "sexy": 0.0679
  },
  "text_result": [
    {
      "text": "Environment Variables",
      "sensitive": false,
      "sensitive_words": []
    },
    {
      "text": "When you start the mysql image, you can adjust the configuration of the MysQL instance by passing one or more environment variables on the docker run command line. Do note",
      "sensitive": false,
      "sensitive_words": []
    }

  ]
}
```

## 视频接口
请求接口
```python
curl -X 'POST' \
  'http://127.0.0.1:8000/video/videofile' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@big_buck_bunny_720p_5mb.mp4;type=video/mp4'
```

返回示例
```json
{
  "succee": true,
  "filepath": "videos/raw_videos/34a976b28637f557aadc7d309e9e4e00.mp4",
  "content_id": "34a976b28637f557aadc7d309e9e4e00"
}
```

