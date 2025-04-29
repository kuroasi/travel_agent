from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

async def create_budget_agent(model):
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
            prompt="You are a budget agent. You can help users to manage their travel budget.",
            name="budget_agent"
        )
        
        return agent