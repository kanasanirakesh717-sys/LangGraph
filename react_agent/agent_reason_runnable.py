from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import tool, create_react_agent
from langchain_tavily import TavilySearch
import datetime
from langchain import hub
import os

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """Returns the current date and time in the specified format."""
    current_time = datetime.datetime.now()
    return current_time.strftime(format)


# Ensure API key is set
if not os.environ.get("TAVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = input("Enter your TAVILY_API_KEY: ")

# Create updated Tavily search tool
search_tool = TavilySearch(
    max_results=5,
    topic="general",
    search_depth="basic",
    include_answer=False,
    include_raw_content=False,
    include_images=False,
)

react_prompt = hub.pull("hwchase17/react")
tools = [get_system_time, search_tool]

react_agent_runnable = create_react_agent(tools=tools, llm=llm, prompt=react_prompt)
