import os
import asyncio
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
import uuid
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.types import Command
from typing import TypedDict, Literal, Union
from typing_extensions import TypedDict

# Load environment variables from .env file
load_dotenv()

# use deepseek v3 model, or define your own model
model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.7,
    max_tokens=1024,
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)

#short term and long term memory
checkpointer = InMemorySaver()
store = InMemoryStore()

#define the tools



#add tavily search tool
tavily_tool = TavilySearchResults(max_results=5)


#build the team and the supervisor
members = ["travel_schedule_agent", "flight_agent", "hotel_agent", "budget_agent"]
# Our team supervisor is an LLM node. It just picks the next agent to process
# and decides when the work is completed
options = members + ["FINISH"]

# system_prompt = """
# You are a supervisor, you can help users to make a travel plan.
# You can assign the work to the agents.
# You can also collect the works from the agents.
# You can also decide when the work is completed.
# """

system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    f" following workers: {members}. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. When finished,"
    " respond with FINISH."
)

class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""
    next: Literal[*options]  # 使用元组替代解包

class State(MessagesState):
    next: str

def supervisor_node(state: State) -> Command[Literal[*members, "__end__"]]:  # 使用元组替代解包
    messages = [
        {"role": "system", "content": system_prompt},
    ] + state["messages"]
    response = model.with_structured_output(Router).invoke(messages)
    goto = response["next"]
    if goto == "FINISH":
        goto = END

    return Command(goto=goto, update={"next": goto})




#create the agents
travel_schedule_agent = create_react_agent(
    model=model,
    tools=[tavily_tool],#行程搜索、天气查询
    prompt="you are a travel aschedule  agent, you can help users to make a travel plan.",
    #name="travel_schedule_agent"
)

flight_agent = create_react_agent(
    model=model,
    tools=[],#航班查询、机票预订
    prompt="you are a flight agent, you can help users to search flight information and book flight tickets.",
    # name="flight_agent"
)

hotel_agent = create_react_agent(
    model=model,
    tools=[],#酒店查询、预订
    prompt="you are a hotel agent, you can help users to search hotel information and book hotel rooms.",
    # name="hotel_agent"
)

budget_agent = create_react_agent(
    model=model,
    tools=[],#预算管理
    prompt="you are a budget agent, you can help users to manage their travel budget.",
    # name="budget_agent"
)

def travel_schedule_node(state: State) -> Command[Literal["supervisor"]]:
    result = travel_schedule_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="travel_schedule_agent")
            ]
        },
        goto="supervisor",
    )

def flight_node(state: State) -> Command[Literal["supervisor"]]:
    result = flight_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="flight_agent")
            ]
        },
        goto="supervisor",
    )

def hotel_node(state: State) -> Command[Literal["supervisor"]]:
    result = hotel_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="hotel_agent")
            ]
        },
        goto="supervisor",
    )

def budget_node(state: State) -> Command[Literal["supervisor"]]:
    result = budget_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="budget_agent")
            ]
        },
        goto="supervisor",
    )


#construct the graph

builder = StateGraph(State)
builder.add_edge(START, "supervisor")
builder.add_node("supervisor", supervisor_node)
builder.add_node("travel_schedule_agent", travel_schedule_node)
builder.add_node("flight_agent", flight_node)
builder.add_node("hotel_agent", hotel_node)
builder.add_node("budget_agent", budget_node)

graph = builder.compile(
    checkpointer=checkpointer,
    store=store
)

# # Show the architecture diagram
# current_dir = os.path.dirname(os.path.abspath(__file__))
# graph_path = os.path.join(current_dir, "travel_agent_graph.png")
# print(f"Saving the graph to: {graph_path}")

# graph.get_graph().draw_mermaid_png()
# with open(graph_path, "wb") as f:
#     f.write(graph.get_graph().draw_mermaid_png())

# print("Graph saved successfully!")
# print(f"Please check the file: {graph_path}")

# 定义交互式异步主函数
async def interactive_chat():
    print("="*50)
    print("Travel assistant has started! Input 'exit' to exit the program.")
    print("Please tell me your travel plan or requirements...")
    print("="*50)
    
    # API密钥检查
    print(f"DeepSeek API Key: {'Set' if os.getenv('DEEPSEEK_API_KEY') else 'Not Set'}")
    print(f"Tavily API Key: {'Set' if os.getenv('TAVILY_API_KEY') else 'Not Set'}")
    
    # 创建线程ID
    thread_id = f"thread_{uuid.uuid4()}"
    
    # 初始化状态
    state = {"messages": [], "next": "supervisor"}
    
    while True:
        # 获取用户输入
        user_input = input("\nYou: ")
        
        # 检查是否退出
        if user_input.lower() == 'exit':
            print("Thank you for using the travel assistant, goodbye!")
            break
        
        # 添加用户消息到历史
        state["messages"].append(HumanMessage(content=user_input))
        
        try:
            print("Thinking...")
            print(f"Initial state: {state}")
            
            # 使用普通调用方式替代流式输出
            result = await graph.ainvoke(
                state,
                {"configurable": {"thread_id": thread_id}}
            )
            
            print(f"Result: {result}")
            
            # 处理结果
            if "messages" in result and len(result["messages"]) > 0:
                # 获取最新的消息
                last_message = result["messages"][-1]
                print(f"Message type: {type(last_message)}")
                
                if isinstance(last_message, AIMessage):
                    print(f"\nTravel assistant: {last_message.content}")
                else:
                    print(f"\nTravel assistant: {last_message}")
            else:
                print("\nTravel assistant: No response generated.")
            
            # 更新状态
            state = result
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"\nTravel assistant: Error processing your request: {str(e)}")

# 运行交互式异步主函数
if __name__ == "__main__":
    asyncio.run(interactive_chat())