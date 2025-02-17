import base64
from openai import OpenAI
import yaml
import requests
from config.prompt import information_extraction_prompt

with open("config/config.yaml", "r",encoding="utf-8") as file:
    config = yaml.safe_load(file)

words_access_token = config["baidu"]["words_access_token"]
image_path=config["image"]["image_path"]


def call_gpt4o_vision(prompt):
    print("开始进行图片的识别")
    try:
        # openai.api_key = self.apikey
        with open(image_path, "rb") as img_file:
            base64_string = base64.b64encode(img_file.read()).decode('utf-8')
        client = OpenAI()
        response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text":prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_string}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        result=response.choices[0].message.content
        return result
    except Exception as e:
        return f"API Problem: {e}"
    
def words_recognition():
    print("开始进行文字提取")
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
        return response.json()

def information_extract():
    recognition_result=words_recognition()
    print("*****文字识别结果*****:\n",recognition_result)
    prompt="以下是对该图的文字精确提取，请你使用提取结果执行下面的指令:\n\n"+str(recognition_result)+"\n\n"+information_extraction_prompt
    extracted_information=call_gpt4o_vision(prompt=prompt)
    print("*****信息提取结果*****:\n",extracted_information)
    return extracted_information
