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
更改数据库地址·
app/database.py
```python
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root123@localhost:5306/app_db"
```


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


回调接口返回示例
```json
{
  "video_content_id": "0380aceafcdc615ae5dcae6e893210d7", // 视频ID
  "is_sensitive": true, // 整个视频
  "sex_result": {  //涉黄监测结果
    "is_sensitive": true, //整个视频是否涉黄 
    "sex_images": [ // 涉黄的图片list， 有多张图片都存在这个list里面
      {
        "image_content_id": "b79558b3a887d5900cda65dded3f541f", // 图片id
        "drawings": 0.3938, // 普通绘画的概率
        "hentai": 3.5093, // 黄色绘画的概率
        "neutral": 33.0526, // 中性图片的概率
        "porn": 61.5685, // 黄色图片的概率
        "sex": 1.4758, // 性感图片的概率
        "is_sensitive": true // 图片是否涉黄敏感
      }
    ]
  },
  "text_result": { // ocr后文字监测的结果
    "is_sensitive": true, // 整个视频是否有敏感文字
    "illegal_text": [ //有敏感文字的图片，文字内容，敏感文字内容，敏感文字位置
      {
        "image_content_id": "9907396b9550f247849686842620a637", //图片id
        "text": "/scrape/site Scrape Site", // 敏感文字原始信息
        "is_sensitive": 1, // 是否敏感
        "sensitive_words": "['rape', 'rape']", // 敏感文字列表
        "topleft": "[283, 2041]", // 敏感文字左上角坐标
        "bottomright": "[497, 2079]" // 敏感文字右下角坐标
      },
      {
        "image_content_id": "9907396b9550f247849686842620a637",
        "text": "/scrape/site Scrape Site",
        "is_sensitive": 1,
        "sensitive_words": "['rape', 'rape']",
        "topleft": "[298, 1962]",
        "bottomright": "[889, 2007]"
      },
      {
        "image_content_id": "9907396b9550f247849686842620a637",
        "text": "/scrape/site Scrape Site",
        "is_sensitive": 1,
        "sensitive_words": "['rape', 'rape']",
        "topleft": "[287, 1900]",
        "bottomright": "[451, 1938]"
      }
    ]
  }
}

```


