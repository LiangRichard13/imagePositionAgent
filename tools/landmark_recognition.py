import requests
import base64
import yaml
from langchain.tools import Tool


with open("config/config.yaml", "r",encoding="utf-8") as file:
    config = yaml.safe_load(file)

access_token = config["baidu"]["landmark_access_token"]
image_path=config["image"]["image_path"]

'''
地标识别
'''

def landmark_recognition(query:str):
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/landmark"
    # 二进制方式打开图片文件
    f = open(image_path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        # print (response.json())
        return response.json()

landmark_recognition_tool = Tool(
    name="LandMarkRecognition",
    func=landmark_recognition,
    description="用于识别图片中的全球著名地标、热门景点"
)