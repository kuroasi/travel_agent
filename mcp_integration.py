"""
MCP Tools Integration with Travel Agent
This module demonstrates how to integrate MCP tools with the travel agent.
"""

import os
from dotenv import load_dotenv
from mcp_tools import get_mcp_tools, airbnb_search, airbnb_listing_details
from langchain_deepseek import ChatDeepSeek
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage, AIMessage

# Load environment variables
load_dotenv()

# Initialize the model
model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.7,
    max_tokens=1024,
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)

# Create a specialized accommodation agent with MCP tools
accommodation_agent = create_react_agent(
    model=model,
    tools=[airbnb_search, airbnb_listing_details],
    prompt="""You are an accommodation agent specializing in finding and booking accommodations.
You can search for Airbnb listings and provide detailed information about specific listings.
Help users find the perfect place to stay based on their preferences and requirements.
Always provide clear information about prices, amenities, and location.""",
    name="accommodation_agent"
)

# Example of how to use the accommodation agent
def test_accommodation_agent():
    """Test the accommodation agent with a sample query."""
    # Sample query
    query = "I'm looking for an Airbnb in San Francisco for 2 adults from 2023-12-15 to 2023-12-20 with a budget of $300 per night."
    
    # Create a state with the query
    state = {"messages": [HumanMessage(content=query)]}
    
    # Invoke the agent
    result = accommodation_agent.invoke(state)
    
    # Print the result
    print("\nAccommodation Agent Response:")
    print("-" * 50)
    for message in result["messages"]:
        if isinstance(message, AIMessage):
            print(f"AI: {message.content}")
        else:
            print(f"Human: {message.content}")

# Example of how to integrate with the main travel agent
def integrate_with_travel_agent():
    """
    Example of how to integrate MCP tools with the main travel agent.
    
    This is a template - you would need to modify your travel_agent.py file
    to include these tools.
    """
    print("\nIntegration Instructions:")
    print("-" * 50)
    print("To integrate the MCP tools with your travel agent:")
    print("1. Import the MCP tools in your travel_agent.py:")
    print("   from mcp_tools import get_mcp_tools, airbnb_search, airbnb_listing_details")
    print("\n2. Add the tools to your hotel_agent:")
    print("   hotel_agent = create_react_agent(")
    print("       model=model,")
    print("       tools=[airbnb_search, airbnb_listing_details],  # Add MCP tools here")
    print("       prompt=\"you are a hotel agent, you can help users to search hotel information and book hotel rooms.\"")
    print("   )")
    print("\n3. Make sure to handle any exceptions from the MCP tools in your agent's error handling.")

if __name__ == "__main__":
    # Test the accommodation agent
    test_accommodation_agent()
    
    # Show integration instructions
    integrate_with_travel_agent()
