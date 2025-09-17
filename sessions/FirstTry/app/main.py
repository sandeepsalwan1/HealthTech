from typing import Dict, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from . import config as app_config

load_dotenv()

###########################
### ReAct Search Agent ####
###########################

AGENT_READY: bool = False
agent_executor = None

def _maybe_init_agent():
    global AGENT_READY, agent_executor
    if AGENT_READY:
        return
    # Only attempt to initialize if API keys likely exist
    if not app_config.OPENAI_API_KEY:
        AGENT_READY = False
        agent_executor = None
        return
    try:
        from langgraph.checkpoint.sqlite import SqliteSaver
        from langchain_openai import ChatOpenAI
        from langchain_community.tools.tavily_search import TavilySearchResults
        from langgraph.prebuilt import create_react_agent

        memory = SqliteSaver.from_conn_string(":memory:")
        model = ChatOpenAI(model="gpt-4o")
        search = TavilySearchResults(max_results=2)
        tools = [search]
        agent_executor = create_react_agent(model, tools, checkpointer=memory)
        AGENT_READY = True
    except Exception as _e:  # Libraries missing or incompatible, or keys invalid
        AGENT_READY = False
        agent_executor = None


###########################
###   Nutrition Agent  ####
###########################
# For now, provide a demo response. Can be replaced with a real agent.


###########################
###    App + Models    ####
###########################

class EventRequest(BaseModel):
    event_type: str
    location: str
    time_frame: str


class NutritionRequest(BaseModel):
    query: Optional[str] = None


app = FastAPI(title=app_config.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[app_config.FRONTEND_ORIGIN] if app_config.FRONTEND_ORIGIN != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/nutrition")
def generate_nutrition(data: NutritionRequest):
    """Demo nutrition endpoint returning a friendly placeholder."""
    query_text = data.query or "Mediterranean breakfast options"
    demo_response = (
        f"Here are three {query_text} to consider:\n"
        "- Greek yogurt with honey, walnuts, and berries\n"
        "- Avocado toast with olive oil, tomatoes, and feta\n"
        "- Chickpea omelette with spinach and herbs\n"
    )
    return {"response": demo_response}


@app.post("/event")
def generate_events(data: EventRequest):
    _maybe_init_agent()
    user_input = (
        f"Find me {data.event_type} events in {data.location} around {data.time_frame} "
        f"time frame in 2024. Return back specific events."
    )

    if AGENT_READY and agent_executor is not None:
        # Set memory for a specific user
        run_config = {"configurable": {"thread_id": app_config.AGENT_THREAD_ID}}
        response = agent_executor.invoke({"messages": [("user", user_input)]}, run_config)
        response_text = response["messages"][-1].content
        return {"response": response_text}

    # Fallback demo response if agent not available
    demo = (
        f"Here are a few {data.event_type} events near {data.location} in {data.time_frame}:\n"
        "- City Classic 10k – Central Park – Aug 10, 2024\n"
        "- Waterfront Run – Riverside – Aug 18, 2024\n"
        "- Night Lights 5k – Downtown – Aug 24, 2024\n"
    )
    return {"response": demo}