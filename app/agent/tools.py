from langchain.tools import tool
import httpx
import json


@tool
def search_web(query: str) -> str:
    """Search the web for current information on a topic."""
    # Replace with Tavily or SerpAPI for real results:
    # from tavily import TavilyClient
    # client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    # return client.search(query)
    return f"Search results for: '{query}' — integrate Tavily/SerpAPI here."


@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression safely."""
    try:
        allowed = set("0123456789+-*/()., ")
        if not all(c in allowed for c in expression):
            return "Invalid expression: only numbers and basic operators allowed."
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"


@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    # Replace with real API:
    # import requests
    # r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=KEY")
    # return r.json()
    return json.dumps({
        "city": city,
        "temp": "28°C",
        "condition": "Sunny",
        "note": "Integrate OpenWeatherMap API for real data.",
    })


@tool
def summarize_url(url: str) -> str:
    """Fetch and return text content from a URL (first 2000 chars)."""
    try:
        with httpx.Client(timeout=10) as client:
            response = client.get(url, follow_redirects=True)
            response.raise_for_status()
            return response.text[:2000]
    except Exception as e:
        return f"Could not fetch URL: {str(e)}"


# Master list of tools available to the agent
TOOLS = [search_web, calculator, get_weather, summarize_url]
