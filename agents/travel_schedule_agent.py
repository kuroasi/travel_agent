from langchain_deepseek import ChatDeepSeek
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_community.tools.tavily_search import TavilySearchResults

from tools.transfer_tool import *

# Define MCP server configuration for external use
def get_mcp_servers_config():
    return {
        "amap-amap-sse": {
            "url": "https://mcp.amap.com/sse?key=e21e37c0efc968877fe633a4f76a0ff7",
            "transport": "sse"
        }
    }

async def create_travel_schedule_agent(model, mcp_client=None):
    """
    Create a travel schedule agent
    
    Args:
        model: The language model to use
        mcp_client: External MCP client, if provided it will be used, otherwise a temporary client will be created
    
    Returns:
        Travel schedule agent
    """
    # Create tavily search tool
    tavily_tool = TavilySearchResults(max_results=10)

    # Determine whether to use the external client or create a temporary one
    client_to_use = mcp_client
    needs_temporary_client = client_to_use is None
    
    # If no client provided, create a temporary one
    if needs_temporary_client:
        client_to_use = MultiServerMCPClient(get_mcp_servers_config())
        await client_to_use.connect()
    
    # Get MCP tools
    mcp_tools = client_to_use.get_tools()
    transfer_tools = [transfer_to_flight_agent, transfer_to_hotel_agent, transfer_to_budget_agent]
    
    # Create agent
    agent = create_react_agent(
        model=model,
        tools= [tavily_tool] + mcp_tools + transfer_tools,
        prompt=
        "You are a travel schedule agent. You can help users to make a travel plan."
        "Use tools to answer questions, never rely on your own knowledge."
        #"When users ask questions about China, please use tools provided by Amap MCP or Baidu MCP. For other countries or regions, use Tavily for searching."
        "When users ask about geographic information and travel plan, please use map tools provided by MCP services."
        "When users ask about other information, please use Tavily for searching."
        "When using tools, please ensure you use the correct parameters. For example:"
        "- When searching for restaurants, you can use maps_text_search, providing keywords and city"
        "- When planning routes, you can use maps_distance to calculate distances"
        "- When searching for places nearby, you can use maps_around_search"
        ,
        name="travel_schedule_agent"
    )
    
    # If using a temporary client, close it before returning
    if needs_temporary_client:
        await client_to_use.close()
    
    return agent
