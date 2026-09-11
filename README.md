# Multi-Agent Travel Planning System

An AI-powered travel planning system built with LangGraph, featuring multiple specialized agents, MCP integrations, guardrails, and human-in-the-loop approval.

## Architecture

<img src="graph.png" alt="">
<br/>


```
User Request
    │
    ▼
[Guardrail Agent] ─── PII cleaning + content moderation
    ├── (not travel-related) ──▶ END (reject)
    └── (travel-related) ──▶ [Supervisor Agent]
                                    │
                                    ▼
                            [Supervisor Agent] ─── LLM selects needed agents + extracts constraints
                                    │
                                    ▼
                            [Flight Agent] ─── AviationStack MCP (live airport/airline data)
                                    │
                                    ▼
                            [Hotel Agent] ─── Tavily MCP (web search)
                                    │
                                    ▼
                            [Weather Agent] ─── Custom Weather MCP (OpenWeatherMap)
                                    │
                                    ▼
                            [Budget Agent] ─── LLM cost analysis
                                    │
                                    ▼
                            [Itinerary Agent] ─── LLM creates draft itinerary
                                    │
                                    ▼
                            [Human Approval] ─── INTERRUPT (pause for review)
                                    ├── approve ──▶ [Final Agent] ──▶ polish ──▶ END
                                    └── reject  ──▶ [Final Agent] ──▶ revise ──▶ END
```


## Key Features

- **Guardrails**: Every request passes through PII cleaning and content moderation before processing
- **Dynamic agent selection**: The supervisor LLM determines which specialist agents are needed per request
- **Human-in-the-loop**: System pauses at the itinerary draft stage for human review and approval
- **MCP tool integration**: External services (flights, hotels, weather) accessed via Model Context Protocol
- **Conversation persistence**: LangGraph checkpoints state to PostgreSQL, enabling multi-turn conversations
- **Structured output**: Key decisions use Pydantic models for reliable LLM output parsing


## Getting Started


### Installation

```bash
# Clone the repository
git clone <repo-url>
cd Multi-Agent-Travel-Planning-System

# Create virtual environment
uv sync
source .venv/bin/activate
```

### Configuration

Create a `.env` file with the following variables:

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key
TAVILY_API_KEY=your_tavily_key
SOVEREIGN_EG_API_KEY=your_sovereign_eg_key
AVIATION_STACK_KEY=your_aviation_stack_key
OPENWEATHER_API_KEY=your_openweather_key
DATABASE_URL=postgresql://user:password@host:port/dbname
```

### Running

```bash
# without docker
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# or using Docker
docker build -t travel-planner .
docker run -p 8000:8000 --env-file .env travel-planner
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Web UI (Jinja2 template) |
| `POST` | `/api/travel` | Submit a travel planning request |
| `POST` | `/api/travel/approve` | Approve or reject a draft itinerary |
| `GET` | `/health` | Health check |

### Example Requests

**Start a travel plan:**
```bash
curl -X POST http://localhost:8000/api/travel \
  -H "Content-Type: application/json" \
  -d '{"message": "Plan a 7-day trip to Tokyo for 2 people with a $3000 budget"}'
```

**Approve a draft itinerary:**
```bash
curl -X POST http://localhost:8000/api/travel/approve \
  -H "Content-Type: application/json" \
  -d '{"thread_id": "<thread-id>", "approved": true, "feedback": ""}'