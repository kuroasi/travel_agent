import os
import asyncio
import uuid
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langgraph_supervisor import create_supervisor
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore

# Import agent creation functions
from agents.travel_schedule_agent import create_travel_schedule_agent
from agents.flight_agent import create_flight_agent
from agents.hotel_agent import create_hotel_agent
from agents.budget_agent import create_budget_agent

import pprint

# Load environment variables
load_dotenv()

# Create model instance
model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.3,
    max_tokens=2048,
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)

# Memory management - Using InMemorySaver and InMemoryStore for short-term and long-term memory management
checkpointer = InMemorySaver()
store = InMemoryStore()

# Create and run multi-agent system
async def main():
    # Create agents
    print("Initializing Travel Agent system...")
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

    # Define supervisor
    system_prompt = (
        "You are a travel planning agent responsible for breaking down user questions into tasks and assigning them to the following staff members:"
        f"{members}. Choose the next staff member to act based on the user's request."
        "Each staff member will complete their task and reply with their results and status."
        "Integrate staff results to complete the task."
        "You must let staff members complete their tasks before responding to the user, instead of telling the user 'processing' or 'will provide detailed results later' type of waiting messages."
        "Here are the names and descriptions of each staff member:"
        "travel_schedule_agent: helps users to make a travel plan"
        "flight_agent: helps users to search flight information and book flight tickets."
        "hotel_agent: helps users to search hotel information and book hotel rooms."
        "budget_agent: helps users to manage their travel budget."
    )

    supervisor = create_supervisor(
        agents=[travel_schedule_agent, flight_agent, hotel_agent, budget_agent],
        model=model,
        prompt=system_prompt,
    )

    # 编译图 - 使用checkpointer和store进行内存管理
    multi_agent_graph = supervisor.compile(
        checkpointer=checkpointer,
        store=store
    )

    # Create a unique session ID for conversation continuity
    session_id = str(uuid.uuid4())

    # Start interactive session
    print("\n" + "="*50)
    print("🌍 Travel Assistant is ready! Enter your travel question, or type 'exit' to quit.")
    print(f"📝 Session ID: {session_id}")
    print("="*50 + "\n")

    # Track conversation messages for display
    conversation_messages = []

    # Track conversation state
    is_first_message = True

    while True:
        # Get user input
        user_input = input("🧑‍💻 You: ")

        # Check if exit
        if user_input.lower() in ['exit', 'quit', '退出', '结束']:
            print("\nThank you for using Travel Assistant, goodbye! 👋")
            break

        # Create current user message
        current_message = {"role": "user", "content": user_input}

        # Add to display message list
        conversation_messages.append(current_message)

        print("\n🤖 Assistant thinking...\n")

        # Configure - Use consistent thread_id to ensure memory continuity
        config = {"configurable": {"thread_id": session_id}}

        # If first message, initialize new state; otherwise use existing state
        if is_first_message:
            # First conversation, initialize state
            input_data = {"messages": [current_message]}
            is_first_message = False
        else:
            # Continue existing conversation, automatically associate with existing state using configurable.thread_id
            input_data = {"messages": [current_message]}

        # Use streaming output to process response
        response_content = None
        async for stream_mode, chunk in multi_agent_graph.astream(
            input_data,
            config,
            stream_mode=["updates","custom"]
            ):
            if stream_mode == "updates":
                print("\n===== Execution Steps =====")
                pprint.pprint(chunk)
                # If AI message, save for display
                if hasattr(chunk, 'messages') and chunk.messages and chunk.messages[-1].role == 'assistant':
                    response_content = chunk.messages[-1].content
            elif stream_mode == "custom":
                print("\n===== Tool Calls =====")
                pprint.pprint(chunk)

        # Display final response
        if response_content:
            # Add to display message list
            conversation_messages.append({"role": "assistant", "content": response_content})
            print("\n" + "="*50)
            print("🤖 Assistant: " + response_content)
            print("="*50 + "\n")

        # Limit displayed conversation history length to avoid terminal clutter
        if len(conversation_messages) > 10:
            # Only keep the most recent 10 messages for display
            conversation_messages = conversation_messages[-10:]

        # Note: No need to manually manage actual conversation state, LangGraph's checkpointer handles it automatically

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Thank you for using Travel Assistant, goodbye! 👋")
