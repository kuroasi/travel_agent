from langchain_deepseek import ChatDeepSeek
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_community.tools.tavily_search import TavilySearchResults

from transfer_tool import *

async def create_travel_schedule_agent(model):
    # 创建MCP客户端连接
    mcp_servers = {
        "amap-amap-sse": {
                "url": "https://mcp.amap.com/sse?key=e21e37c0efc968877fe633a4f76a0ff7",
                "transport": "sse"
        }
    }
    
    # 创建tavily搜索工具
    tavily_tool = TavilySearchResults(max_results=10)
    
    async with MultiServerMCPClient(mcp_servers) as client:
        # 获取MCP工具
        mcp_tools = client.get_tools()
        transfer_tools = [transfer_to_flight_agent, transfer_to_hotel_agent, transfer_to_budget_agent]
        # 创建agent
        agent = create_react_agent(
            model=model,
            tools= [tavily_tool] + mcp_tools + transfer_tools,
            prompt=
            "You are a travel schedule agent. You can help users to make a travel plan."
            "请尽可能使用工具来回答问题，而不是依赖自己的知识。"
            "当用户询问中国相关的问题请使用amap mcp提供的工具，其他国家或地区问题使用tavily进行搜索"
            "当需要使用工具时，请确保使用正确的参数。例如："
            "- 在查询餐厅时，可以使用maps_text_search，提供关键词和城市"
            "- 在规划路线时，可以使用maps_direction_transit_integrated获取公共交通路线"
            "- 在查询天气时，可以使用maps_weather，提供城市名称"
            ,
            name="travel_schedule_agent"
        )
        
        return agent
