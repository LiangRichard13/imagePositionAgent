import http.client
import json
from langchain.tools import Tool
# 引入能够读取yaml配置文件的工具
import yaml

with open("config/config.yaml", "r",encoding="utf-8") as file:
    config = yaml.safe_load(file)

serpapi_key = config["serpapi"]["serpapi_key"]

# 定义自定义函数来查询 Serper.dev API
def places_search(query: str) -> str:
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
    "q": query,
    "gl": "cn",
    "hl": "zh-cn"
    })
    headers = {
    'X-API-KEY': serpapi_key,
    'Content-Type': 'application/json'
    }
    conn.request("POST", "/places", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

# 使用 langchain 的 Tool 包装自定义函数
places_search_tool = Tool(
    name="PlacesSearch",
    func=places_search,
    description="使用谷歌地图服务，输入地点名称(如店铺、医院、酒店、公交站、景点、街道名等等)用于得到某个地点的最精确位置"
)
