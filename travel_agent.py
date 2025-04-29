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


#create the agents
travel_schedule_agent = create_react_agent(
    model=model,
    tools=[tavily_tool],#行程搜索、天气查询
    prompt="you are a travel aschedule  agent, you can help users to make a travel plan.",
    name="travel_schedule_agent"
)

flight_agent = create_react_agent(
    model=model,
    tools=[],#航班查询、机票预订
    prompt="you are a flight agent, you can help users to search flight information and book flight tickets.",
    name="flight_agent"
)

hotel_agent = create_react_agent(
    model=model,
    tools=[],#酒店查询、预订
    prompt="you are a hotel agent, you can help users to search hotel information and book hotel rooms.",
    name="hotel_agent"
)

budget_agent = create_react_agent(
    model=model,
    tools=[],#预算管理
    prompt="you are a budget agent, you can help users to manage their travel budget.",
    name="budget_agent"
)

members = [
    "travel_schedule_agent",
    "flight_agent",
    "hotel_agent",
    "budget_agent",
]

#define the supervisor
system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    f" following workers: {members}. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. "
    "Integrate with the workers' results to complete the task."
)

supervisor = create_supervisor(
    agents=[travel_schedule_agent, flight_agent, hotel_agent, budget_agent],
    model=model,
    prompt=system_prompt,
    #output_mode="full_history"
)


# Define graph
multi_agent_graph = supervisor.compile(
    checkpointer=checkpointer,
    store=store
)


# Run the multi-agent graph
config = {"configurable": {"thread_id": "1"}}
input_message = {"role": "user", "content": "the most 5 famous places in paris"}
for chunk in multi_agent_graph.stream({"messages": [input_message]}, config, stream_mode="values"):
    chunk["messages"][-1].pretty_print()



# # Show the architecture diagram
# current_dir = os.path.dirname(os.path.abspath(__file__))
# graph_path = os.path.join(current_dir, "travel_agent_graph.png")
# print(f"Saving the graph to: {graph_path}")

# multi_agent_graph.get_graph().draw_mermaid_png()
# with open(graph_path, "wb") as f:
#     f.write(multi_agent_graph.get_graph().draw_mermaid_png())

# print("Graph saved successfully!")
# print(f"Please check the file: {graph_path}")
