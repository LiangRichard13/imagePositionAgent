import http.client
import json
from langchain.tools import Tool
# 引入能够读取yaml配置文件的工具
import yaml

with open("config/config.yaml", "r",encoding="utf-8") as file:
    config = yaml.safe_load(file)

serpapi_key = config["serpapi"]["serpapi_key"]

# 定义自定义函数来查询 Serper.dev API
def web_search(query: str) -> str:
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
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")  # 将返回数据解码为字符串
    parsed_data = json.loads(data)  # 使用 json.loads 解析字符串
    # 仅保留最相关的前五个结果
    parsed_data["organic"] = parsed_data.get("organic", [])[:5]
    return json.dumps(parsed_data, indent=2, ensure_ascii=False)

# 使用 langchain 的 Tool 包装自定义函数
web_search_tool = Tool(
    name="WebSearch",
    func=web_search,
    description="用于互联网搜索，参数为一个单句或者一个单词"
)
