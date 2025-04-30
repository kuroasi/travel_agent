from langchain_deepseek import ChatDeepSeek
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_community.tools.tavily_search import TavilySearchResults

from tools.transfer_tool import *

async def create_travel_schedule_agent(model):
    # Create MCP client connection
    mcp_servers = {
        "amap-amap-sse": {
                "url": "https://mcp.amap.com/sse?key=e21e37c0efc968877fe633a4f76a0ff7",
                "transport": "sse"
        }
    }

    # Create tavily search tool
    tavily_tool = TavilySearchResults(max_results=10)

    async with MultiServerMCPClient(mcp_servers) as client:
        # Get MCP tools
        mcp_tools = client.get_tools()
        transfer_tools = [transfer_to_flight_agent, transfer_to_hotel_agent, transfer_to_budget_agent]
        # Create agent
        agent = create_react_agent(
            model=model,
            tools= [tavily_tool] + mcp_tools + transfer_tools,
            prompt=
            "You are a travel schedule agent. You can help users to make a travel plan."
            "Please use tools as much as possible to answer questions, rather than relying on your own knowledge."
            "When users ask questions about China, please use tools provided by Amap MCP. For other countries or regions, use Tavily for searching."
            "When using tools, please ensure you use the correct parameters. For example:"
            "- When searching for restaurants, you can use maps_text_search, providing keywords and city"
            "- When planning routes, you can use maps_direction_transit_integrated to get public transportation routes"
            "- When checking the weather, you can use maps_weather, providing the city name"
            ,
            name="travel_schedule_agent"
        )

        return agent
