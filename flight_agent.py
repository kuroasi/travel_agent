from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

async def create_flight_agent(model):
    # 创建MCP客户端连接
    mcp_servers = {

    }
    
    async with MultiServerMCPClient(mcp_servers) as client:
        # 获取MCP工具
        mcp_tools = client.get_tools()
        
        # 创建agent
        agent = create_react_agent(
            model=model,
            tools=mcp_tools,
            prompt="You are a flight agent. You can help users to search flight information and book flight tickets.",
            name="flight_agent"
        )
        
        return agent
