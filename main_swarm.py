import os
import asyncio
import uuid
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langgraph_swarm import create_swarm, create_handoff_tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore

# 导入各个agent创建函数
from travel_schedule_agent import create_travel_schedule_agent
from flight_agent import create_flight_agent
from hotel_agent import create_hotel_agent
from budget_agent import create_budget_agent

import pprint

# 加载环境变量
load_dotenv()

# 创建模型实例
model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.3,
    max_tokens=2048,
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)

# 内存管理 - 使用InMemorySaver和InMemoryStore进行短期和长期记忆管理
checkpointer = InMemorySaver()
store = InMemoryStore()

# 创建并运行多agent系统
async def main():
    # 创建各个agent
    print("正在初始化Travel Agent系统...")
    travel_schedule_agent = await create_travel_schedule_agent(model)
    flight_agent = await create_flight_agent(model)
    hotel_agent = await create_hotel_agent(model)
    budget_agent = await create_budget_agent(model)
    
    members = [
        "travel_schedule_agent",
        "flight_agent",
        "hotel_agent",
        "budget_agent",
    ]
    
    # # 定义supervisor
    # system_prompt = (
    #     "您是一个旅行规划代理，负责将用户的问题拆解成任务，并分配给以下工作人员："
    #     f"{members}。根据用户请求，选择下一个要行动的工作人员。"
    #     "每个工作人员将执行任务并回复他们的结果和状态。"
    #     "整合工作人员的结果来完成任务。"
    #     "你必须让工作人员完成任务后，再回复用户，而不是回复用户“正在处理”“稍后将为您提供详细结果”之类的等待消息"
    #     "以下是各个工作人员的名称和介绍："
    #     "travel_schedule_agent: help users to make a travel plan"
    #     "flight_agent: help users to search flight information and book flight tickets."
    #     "hotel_agent: help users to search hotel information and book hotel rooms."
    #     "budget_agent: help users to manage their travel budget."
    # )
    
    groupchat = create_swarm(
        agents=[travel_schedule_agent, flight_agent, hotel_agent, budget_agent],
        default_active_agent="travel_schedule_agent",
    )
    
    # 编译图 - 使用checkpointer和store进行内存管理
    multi_agent_graph = groupchat.compile(
        checkpointer=checkpointer,
        store=store
    )
    
    # 创建一个唯一的会话ID用于保持对话连续性
    session_id = str(uuid.uuid4())
    
    # 启动交互式会话
    print("\n" + "="*50)
    print("🌍 旅行助手已启动! 输入您的旅行问题，或输入 'exit' 退出。")
    print(f"📝 会话ID: {session_id}")
    print("="*50 + "\n")
    
    # 跟踪对话消息，便于显示
    conversation_messages = []
    
    # 追踪对话状态
    is_first_message = True
    
    while True:
        # 获取用户输入
        user_input = input("🧑‍💻 您: ")
        
        # 检查是否退出
        if user_input.lower() in ['exit', 'quit', '退出', '结束']:
            print("\n感谢使用旅行助手，再见！👋")
            break
        
        # 创建当前用户消息
        current_message = {"role": "user", "content": user_input}
        
        # 添加到显示用的消息列表
        conversation_messages.append(current_message)
        
        print("\n🤖 助手思考中...\n")
        
        # 配置 - 使用一致的thread_id确保内存连续性
        config = {"configurable": {"thread_id": session_id}}
        
        # 如果是首次消息，初始化新状态；否则使用现有状态
        if is_first_message:
            # 首次对话，初始化状态
            input_data = {"messages": [current_message]}
            is_first_message = False
        else:
            # 继续现有对话，使用configurable.thread_id自动关联现有状态
            input_data = {"messages": [current_message]}
        
        # 使用流式输出处理响应
        response_content = None
        async for stream_mode, chunk in multi_agent_graph.astream(
            input_data,
            config, 
            stream_mode=["updates","custom"]
            ):
            if stream_mode == "updates":
                print("\n===== 执行步骤 =====")
                pprint.pprint(chunk)
                # 如果是AI消息，保存以便显示
                if hasattr(chunk, 'messages') and chunk.messages and chunk.messages[-1].role == 'assistant':
                    response_content = chunk.messages[-1].content
            elif stream_mode == "custom":
                print("\n===== 工具调用 =====")
                pprint.pprint(chunk)
        
        # 显示最终响应
        if response_content:
            # 添加到显示用的消息列表
            conversation_messages.append({"role": "assistant", "content": response_content})
            print("\n" + "="*50)
            print("🤖 助手: " + response_content)
            print("="*50 + "\n")
        
        # 限制显示的对话历史长度，避免终端过于混乱
        if len(conversation_messages) > 10:
            # 只保留最近的10条消息用于显示
            conversation_messages = conversation_messages[-10:]
        
        # 注意：无需手动管理实际的对话状态，LangGraph的checkpointer已经自动处理

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n程序被用户中断。感谢使用旅行助手，再见！👋")
