import requests
import base64
import yaml
from langchain.tools import Tool

with open("../config/config.yaml", "r") as file:
    config = yaml.safe_load(file)

words_access_token = config["baidu"]["words_access_token"]
image_path=config["image"]["image_path"]

'''
通用文字识别（高精度版）
'''
def words_recognition():
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # 二进制方式打开图片文件
    f = open(image_path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img}
    access_token = words_access_token
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print (response.json())

words_recognition_tool = Tool(
    name="WordsRecognition",
    func=words_recognition,
    description="用于精确识别图片中所包含的全球语言文字，该工具方法不需要传递任何参数"
)