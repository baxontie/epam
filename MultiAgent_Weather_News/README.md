# Multi-Agent Weather & News Application

## Overview

This project is a Python-based Streamlit application that answers user questions about
current weather conditions and the latest news.  
The application demonstrates a **multi-agent architecture** with **agent orchestration**
and **MCP-style integration** for external data sources.

The system works entirely with **free, public data sources** and does **not require any API keys**.

---

## Key Features

- Multi-agent orchestration (Weather Agent + News Agent)
- MCP-style abstraction for external tools
- Natural language intent detection
- Context-aware responses (e.g. city-specific news)
- Streamlit-based chat interface
- Multi-turn conversations
- Graceful error handling

---

## Architecture Overview

The application follows a modular, agent-oriented design:

User (Streamlit UI)  
→ Agent Orchestrator  
→ Intent Parser  
→ Weather Agent (Open-Meteo MCP)  
→ News Agent (Google News RSS MCP)  
→ Response Aggregation  
→ Streamlit Chat UI  

Each agent is responsible for a single domain and communicates through standardized,
MCP-style tool interfaces.

---

## Agents Description

### Weather Agent

- Retrieves real-time weather data
- Uses Open-Meteo APIs with built-in geocoding
- Supports queries such as:
  - "What's the weather in Berlin?"
  - "Will it rain tomorrow in Paris?"
- Returns:
  - Temperature
  - Wind speed
- No API key required

---

### News Agent

- Retrieves latest news headlines using **Google News RSS**
- Supports:
  - General news queries
  - Topic-based news (e.g. "news about AI")
  - **City-specific news when a location is detected**
- Example queries:
  - "Latest news headlines"
  - "News about technology"
  - "Weather and news in London"

If a city is mentioned in the user query, the agent automatically retrieves
**location-specific news** for that city.

---

### Agent Orchestrator

The Agent Orchestrator is the central coordination component:

- Analyzes user intent (weather / news / both)
- Routes requests to appropriate agents
- Aggregates responses when multiple agents are involved
- Ensures clean separation of responsibilities

This design demonstrates a true **multi-agent orchestration pattern**.

---

## MCP Integration

External data sources are integrated using **MCP-style wrappers**:

- Each external service is encapsulated in its own class
- Agents interact with tools through a unified interface
- This approach enables:
  - Standardized tool usage
  - Easy extensibility
  - Clear separation between agents and data providers

### MCP Tools Used

- **Open-Meteo MCP**
  - Weather and geocoding data
- **Google News RSS MCP**
  - News headlines and topic-based news

---

## User Interface

The application uses **Streamlit** with a chat-style interface:

- Text input for user questions
- Chat history preserved across turns
- Clear formatting for:
  - Weather information
  - News headlines
- Immediate feedback and error messages when services are unavailable

---

## Setup Instructions

### Requirements

- Python 3.10 or higher
- Internet connection

### Installation

python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# or
.venv\Scripts\Activate.ps1  # Windows

pip install -r requirements.txt

### Run the Application

streamlit run app.py

Then open in a browser:

http://localhost:8501

### Example Queries

- Weather:
  - "What's the weather in Berlin?"
- News:
  - "Latest news headlines"
- Combined:
  - "Weather and news in London"
- Multi-turn:
  - "What's the weather in Paris?"
  - "And the news there?"

### Error Handling & Limitations

- Graceful handling of unavailable external services
- Simple heuristic-based intent detection
- City extraction is rule-based and may not handle very complex phrasing
- News results depend on RSS feed availability

### Conclusion

This project demonstrates a practical and clean implementation of:
- Multi-agent systems
- Agent orchestration patterns
- MCP-style external tool integration
- Streamlit-based conversational applications
All requirements of the practical task are fulfilled, including:
- Weather data integration
- News data integration
- Agent routing and orchestration
- No API keys required
- Working Streamlit web application