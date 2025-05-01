import os
import asyncio
import uuid
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langgraph_swarm import create_swarm, create_handoff_tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from IPython.display import Image, display
import datetime

# Load environment variables
load_dotenv()

# Create model instance
model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.3,
    max_tokens=2048,
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)

transfer_to_travel_schedule_agent = create_handoff_tool(
    agent_name="travel_schedule_agent",
    description="Transfer user to the travel-schedule assistant.",
)

transfer_to_hotel_agent = create_handoff_tool(
    agent_name="hotel_agent",
    description="Transfer user to the hotel-booking assistant.",
)

transfer_to_flight_agent = create_handoff_tool(
    agent_name="flight_agent",
    description="Transfer user to the flight-booking assistant.",
)

transfer_to_budget_agent = create_handoff_tool(
    agent_name="budget_agent",
    description="Transfer user to the budget-management assistant.",
)



travel_schedule_agent = create_react_agent(
    model,
    prompt="you are a travel schedule agent, you are responsible for planning the travel schedule based on the user's request",
    name="travel_schedule_agent",
    tools=[transfer_to_flight_agent, transfer_to_hotel_agent, transfer_to_budget_agent],
    )

flight_agent = create_react_agent(
    model,
    prompt="you are a flight agent, you are responsible for booking the flight tickets based on the user's request",
    name="flight_agent",
    tools=[transfer_to_travel_schedule_agent, transfer_to_budget_agent, transfer_to_hotel_agent],
    )

hotel_agent = create_react_agent(
    model,
    prompt="you are a hotel agent, you are responsible for booking the hotel rooms based on the user's request",
    name="hotel_agent",
    tools=[transfer_to_travel_schedule_agent, transfer_to_budget_agent, transfer_to_flight_agent],
    )

budget_agent = create_react_agent(
    model,
    prompt="you are a budget agent, you are responsible for managing the travel budget based on the user's request",
    name="budget_agent",
    tools=[transfer_to_travel_schedule_agent, transfer_to_flight_agent, transfer_to_hotel_agent],
    )   

swarm = create_swarm(
    agents=[travel_schedule_agent, flight_agent, hotel_agent, budget_agent],
    default_active_agent="travel_schedule_agent"
    )

graph = swarm.compile()

# Save the graph as PNG to root directory
try:
    # Get PNG data
    png_data = graph.get_graph().draw_mermaid_png()
    
    # Define filename with timestamp to avoid overwriting
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"travel_agent_graph_{timestamp}.png"
    
    # Save PNG to file in root directory
    with open(filename, "wb") as f:
        f.write(png_data)
    
    print(f"Graph saved as {filename} in the project root directory")
    
    # Also display in IPython if running in notebook
    try:
        display(Image(png_data))
    except:
        pass
        
except Exception as e:
    print(f"Error saving graph: {e}")
    # This requires some extra dependencies and is optional
    pass