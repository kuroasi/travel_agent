from langgraph_swarm import create_swarm, create_handoff_tool

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

transfer_to_travel_schedule_agent = create_handoff_tool(
    agent_name="travel_schedule_agent",
    description="Transfer user to the travel-planning assistant.",
)




