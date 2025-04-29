import os
import asyncio
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langgraph_supervisor import create_supervisor
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore

# 导入各个agent创建函数
from travel_schedule_agent import create_travel_schedule_agent
from flight_agent import create_flight_agent
from hotel_agent import create_hotel_agent
from budget_agent import create_budget_agent

# 加载环境变量
load_dotenv()

# 创建模型实例
model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.7,
    max_tokens=1024,
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)

# 内存管理
checkpointer = InMemorySaver()
store = InMemoryStore()

# 创建并运行多agent系统
async def main():
    # 创建各个agent
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
    
    # 定义supervisor
    system_prompt = (
        "您是一个管理员，负责管理以下工作人员之间的对话："
        f"{members}。根据用户请求，选择下一个要行动的工作人员。"
        "每个工作人员将执行任务并回复他们的结果和状态。"
        "整合工作人员的结果来完成任务。"
    )
    
    supervisor = create_supervisor(
        agents=[travel_schedule_agent, flight_agent, hotel_agent, budget_agent],
        model=model,
        prompt=system_prompt,
    )
    
    # 编译图
    multi_agent_graph = supervisor.compile(
        checkpointer=checkpointer,
        store=store
    )
    
    # 运行图
    config = {"configurable": {"thread_id": "1"}}
    input_message = {"role": "user", "content": "我想计划一次巴黎的5天旅行"}
    for chunk in multi_agent_graph.stream({"messages": [input_message]}, config, stream_mode="values"):
        chunk["messages"][-1].pretty_print()

if __name__ == "__main__":
    asyncio.run(main())
