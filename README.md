# Travel Agent System

> [中文版](./README_CN.md)

## Overview

Travel Agent System is an intelligent multi-agent travel planning platform that helps users plan their trips, search for flights and hotels, manage budgets, and create comprehensive travel itineraries. The system utilizes advanced language models and a multi-agent architecture to provide personalized travel recommendations and services.

## Features

- **Intelligent Trip Planning**: Generate customized travel plans based on user preferences
- **Flight Booking**: Search and book flights with detailed information
- **Hotel Reservation**: Find and book suitable hotels based on location, amenities, and budget
- **Budget Management**: Estimate, track, and analyze travel expenses
- **Interactive Interface**: Natural language conversation for all travel planning needs
- **Memory Management**: Maintain conversation context throughout the planning process
- **Real-Time Information**: Integrated search functionality for up-to-date travel information
- **Map Services**: Access to location and route planning through Amap MCP services

## Tech Stack

- **Languages**: Python 3.11+
- **Framework**: 
  - LangGraph (for agent orchestration)
  - LangGraph Swarm (for multi-agent collaboration)
  - LangChain (for LLM interactions)
- **Models**: DeepSeek Chat API
- **Memory**: LangGraph Memory Store and Checkpointer
- **External Services**:
  - Tavily API (for real-time information search)
  - Amap API (for location and mapping services)
- **Data**: Simulated travel data for development and testing

## System Architecture

The system is built around a groupchat architecture with specialized agents:

- **Travel Schedule Agent**: Coordinates the overall trip planning process, integrated with Tavily search for real-time travel information and Amap MCP services for location data and route planning
- **Flight Agent**: Manages flight search and booking operations
- **Hotel Agent**: Handles hotel search and reservation services
- **Budget Agent**: Provides financial planning and expense tracking

These agents communicate and collaborate using the LangGraph Swarm framework, enabling efficient task delegation and information sharing.

## Project Structure

```
travel_agent/
│
├── main_swarm.py         # Main entry point (swarm-based implementation)
├── transfer_tool.py      # Tool for transferring information between agents
│
├── Agents:
│   ├── flight_agent.py   # Flight search and booking agent
│   ├── hotel_agent.py    # Hotel search and booking agent
│   ├── budget_agent.py   # Budget management agent
│   └── travel_schedule_agent.py # Travel planning coordinator with search and map services
│
├── Tools and Data:
│   ├── flight_tools.py   # Flight-related utilities
│   ├── flight_data.py    # Flight database
│   ├── hotel_tools.py    # Hotel-related utilities
│   ├── hotel_data.py     # Hotel database
│   └── budget_tools.py   # Budget management utilities
│
└── requirements.txt      # Python dependencies
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/travel_agent.git
   cd travel_agent
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

4. Setup environment variables:
   ```bash
   # Create .env file with API keys
   echo "DEEPSEEK_API_KEY=your_api_key_here" > .env
   echo "TAVILY_API_KEY=your_tavily_api_key_here" >> .env
   echo "AMAP_API_KEY=your_amap_api_key_here" >> .env
   ```

## Usage

Run the main application:

```bash
python main_swarm.py
```

The system will start an interactive session where you can input your travel queries in natural language. Examples of queries include:

- "I want to plan a 5-day trip to Tokyo for 2 people."
- "Find flights from Beijing to Shanghai on May 15th."
- "Show me hotels in Shanghai with swimming pools."
- "Can you help me estimate a budget for a 7-day trip to Paris?"
- "What are the main attractions in Beijing?"
- "How do I get from the airport to downtown in Shanghai?"

## Example Session

```
🌍 Travel Assistant is ready! Enter your travel question, or type 'exit' to quit.
📝 Session ID: 3f7b9a1c-8d24-4e61-9d7b-2a6fc98a5c7f

🧑‍💻 You: I want to plan a 3-day trip to Shanghai next month. Can you help me with flights and hotels?

🤖 Assistant: I'd be happy to help you plan your 3-day trip to Shanghai!

Let me first find some flight options for you. Could you please tell me:
1. Where will you be departing from?
2. What are your preferred travel dates?
3. How many people will be traveling?

Once I have this information, I can search for flights and then find suitable hotels in Shanghai for your stay.
```

## Future Plans

- Integration with real-world travel APIs for live data
- Mobile application interface
- Multi-language support
- Trip sharing and collaboration features
- Automated itinerary optimization

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or feedback, please contact: [1302278835@qq.com](mailto:1302278835@qq.com) 