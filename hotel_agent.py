from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

async def create_hotel_agent(model):
    # 创建MCP客户端连接
    mcp_servers = {
        "airbnb": {
            "command": "npx",
            "args": [
                "-y",
                "@openbnb/mcp-server-airbnb"
                ]
        }
    }
    
    async with MultiServerMCPClient(mcp_servers) as client:
        # 获取MCP工具
        mcp_tools = client.get_tools()
        
        # 创建agent
        agent = create_react_agent(
            model=model,
            tools=mcp_tools,
            prompt="You are a hotel agent. You can help users to search hotel information and book hotel rooms.",
            name="hotel_agent"
        )
        
        return agent