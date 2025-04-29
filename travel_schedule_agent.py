from langchain_deepseek import ChatDeepSeek
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_community.tools.tavily_search import TavilySearchResults

async def create_travel_schedule_agent(model):
    # 创建MCP客户端连接
    mcp_servers = {

    }
    
    # 创建tavily搜索工具
    tavily_tool = TavilySearchResults(max_results=5)
    
    async with MultiServerMCPClient(mcp_servers) as client:
        # 获取MCP工具
        mcp_tools = client.get_tools()
        
        # 创建agent
        agent = create_react_agent(
            model=model,
            tools=[tavily_tool] + mcp_tools,
            prompt="You are a travel schedule agent. You can help users to make a travel plan.",
            name="travel_schedule_agent"
        )
        
        return agent
