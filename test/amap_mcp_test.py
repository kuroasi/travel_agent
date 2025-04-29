import asyncio
import os
import json
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_deepseek import ChatDeepSeek 
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langgraph.config import get_stream_writer

# 加载环境变量
load_dotenv()

# 配置模型
def create_model():
    return ChatDeepSeek(
        model="deepseek-chat", 
        api_key=os.getenv("DEEPSEEK_API_KEY")
    )

# 创建带有监控功能的工具包装器
def create_monitored_tools(tools):
    monitored_tools = []
    
    for tool in tools:
        original_func = tool.func
        
        async def monitored_func(*args, **kwargs):
            tool_name = tool.name
            print(f"\n🛠️ 调用高德地图工具: {tool_name}")
            print(f"📤 输入参数: {json.dumps(kwargs, ensure_ascii=False, indent=2)}")
            try:
                result = await original_func(*args, **kwargs)
                result_str = str(result)
                if len(result_str) > 300:
                    print(f"📥 返回结果: (截取前300字符)\n{result_str[:300]}...")
                else:
                    print(f"📥 返回结果:\n{result_str}")
                return result
            except Exception as e:
                print(f"❌ 调用失败: {str(e)}")
                raise
        
        # 复制原始工具并更新函数
        monitored_tool = tool.copy()
        monitored_tool.func = monitored_func
        monitored_tools.append(monitored_tool)
    
    return monitored_tools

async def main():
    # 配置MCP服务器
    mcp_servers = {
        "amap-amap-sse": {
                "url": "https://mcp.amap.com/sse?key=e21e37c0efc968877fe633a4f76a0ff7",
                "transport": "sse"
        }
    }
    
    # 创建MCP客户端
    async with MultiServerMCPClient(mcp_servers) as client:
        # 获取MCP工具
        mcp_tools = client.get_tools()
        print(f"可用MCP工具: {[tool.name for tool in mcp_tools]}")
        
        # 创建带有MCP工具的Agent - 使用流式调试方式
        agent = create_react_agent(
            model=create_model(),
            tools=mcp_tools,
            prompt="""你是一个助手，可以调用高德地图的工具完成任务。请尽可能使用工具来回答问题，而不是依赖自己的知识。
            
当需要使用工具时，请确保使用正确的参数。例如：
- 在查询餐厅时，可以使用maps_text_search，提供关键词和城市
- 在规划路线时，可以使用maps_direction_transit_integrated获取公共交通路线
- 在查询天气时，可以使用maps_weather，提供城市名称
            """
        )
        
        # 发送测试查询 - 使用更明确的查询促使工具调用
        test_query = """请执行以下任务：
1. 查询北京天安门附近的3家热门餐厅，使用maps_text_search工具
2. 查找从北京站到北京故宫的公共交通路线，使用maps_direction_transit_integrated工具
3. 获取北京的当前天气，使用maps_weather工具

请一步一步执行，每执行一步都告诉我你调用了什么工具和结果。"""
        
        print(f"\n发送查询: '{test_query}'")
        
        # 使用流式输出
        print("\n开始获取响应...")
        async for stream_mode, chunk in agent.astream(
            {"messages": [HumanMessage(content=test_query)]},
            stream_mode=["updates", "custom"]
        ):
            # 根据不同的流类型处理响应
            if stream_mode == "updates":
                print(f"\n===== 执行状态更新 =====")
                chunk_str = str(chunk)
                if "tool_calls" in chunk_str:
                    print(f"检测到工具调用: {chunk_str}")
                elif "tool_call" in chunk_str:
                    print(f"检测到工具调用: {chunk_str}")
                else:
                    print(f"状态: {type(chunk).__name__}")
            elif stream_mode == "custom":
                print(f"\n===== 自定义输出 =====")
                print(f"{chunk}")
        
        print("\n\n响应完成!")

if __name__ == "__main__":
    asyncio.run(main()) 