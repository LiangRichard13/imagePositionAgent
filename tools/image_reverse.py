import yaml
import http.client
import json
from pydantic import BaseModel, HttpUrl
from langchain.tools import Tool

# 读取配置文件
with open("config/config.yaml", "r",encoding="utf-8") as file:
    config = yaml.safe_load(file)

# 获取到serpapi_key
serpapi_key = config["serpapi"]["serpapi_key"]
image_url=config["image"]["image_url"]

# 定义工具的输入参数 schema
class ImageReverseSearchInput(BaseModel):
    image_url: HttpUrl  # 使用 Pydantic 的 HttpUrl 类型，确保是一个合法的 URL

# 定义工具的主功能
def image_reverse_search(query:str)->str:
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
        "url": image_url,
        "gl": "cn",
        "hl": "zh-cn"
    })
    headers = {
        'X-API-KEY': serpapi_key,
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/lens", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")  # 将返回数据解码为字符串
    parsed_data = json.loads(data)  # 使用 json.loads 解析字符串
    # 仅保留最相关的前五个结果
    parsed_data["organic"] = parsed_data.get("organic", [])[:5]
    return json.dumps(parsed_data, indent=2, ensure_ascii=False)

image_reverse_tool = Tool(
    name="ImageReverseSearch",
    func=image_reverse_search,
    description="仅输入图片的url,搜索该图片的相似图片以及对应在互联网上的相关内容",
    args_schema=ImageReverseSearchInput
)