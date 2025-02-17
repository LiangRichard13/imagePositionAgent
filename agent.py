import os 
import yaml
from information_extract import information_extract,call_gpt4o_vision
from langchain.agents import AgentType
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent
from config.prompt import plan,agent_prompt,conclusion_prompt,helpful_tips
from tools.image_reverse import image_reverse_tool
from tools.places_search import places_search_tool
from tools.web_search import web_search_tool
from tools.landmark_recognition import landmark_recognition_tool


# 读取配置文件
with open("config/config.yaml", "r",encoding="utf-8") as file:
    config = yaml.safe_load(file)

# 设置OPENIA_API_KEY环境变量
os.environ["OPENAI_API_KEY"] = config["openai"]["openai_key"]
# 获取image_url
image_url=config["image"]["image_url"]

llm = ChatOpenAI(
    temperature=0.3,
    model="gpt-4o",
)

# 加载工具
tools = load_tools(
    ["llm-math"],
    llm=llm
    )

tools.append(image_reverse_tool)
tools.append(places_search_tool)
tools.append(web_search_tool)
# tools.append(words_recognition_tool)
tools.append(landmark_recognition_tool)
tools_information =str([{"name": tool.name, "description": tool.description} for tool in tools])

# 初始化agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)


extract_information=information_extract()
conclusion_prompt=extract_information+"\n\n"+conclusion_prompt
conclude_information=call_gpt4o_vision(conclusion_prompt)
print("*****对提取信息的总结结果*****:\n\n",conclude_information)
prompt=image_url+"\n\n"+conclude_information+agent_prompt+"\n\n"+plan+"\n\n"+helpful_tips
output=agent(prompt)
print(output)