import os
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import tool, AgentExecutor, create_tool_calling_agent
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Google API key not found. Make sure it's in the .env file")
if not OPENWEATHERMAP_API_KEY:
    raise ValueError("OpenWeatherMap API key not found. Make sure it's in the .env file")

@tool
def get_weather(location: str) -> str:
    """
    Gets the current weather conditions for a specific geographical location.
    Use this tool whenever the user asks about the weather, temperature,
    humidity, or general weather conditions for a city or place.
    Returns a string describing the weather.
    """
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": OPENWEATHERMAP_API_KEY,
        "units": "metric",
        "lang": "en"
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("cod") != 200:
            return f"Error getting weather: {data.get('message', 'Unknown error')}"

        main_weather = data.get("weather", [{}])[0].get("description", "Not available")
        temp = data.get("main", {}).get("temp", "Not available")
        feels_like = data.get("main", {}).get("feels_like", "Not available")
        humidity = data.get("main", {}).get("humidity", "Not available")

        return f"The weather in {location} is: {main_weather}. Temperature: {temp}°C (feels like: {feels_like}°C). Humidity: {humidity}%."

    except requests.exceptions.RequestException as e:
        return f"Network error contacting the weather API: {e}"
    except Exception as e:
        return f"An unexpected error occurred while getting the weather: {e}"


llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=GOOGLE_API_KEY)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a very helpful conversational weather assistant. "
              "Your main function is to get the current weather using the 'get_weather' tool. "
              "Carefully analyze the user's question and the CONVERSATION HISTORY. "
              "If the user's question, even a short follow-up like 'and in [city]?', "
              "asks for weather information (climate, weather, temperature, humidity) for ANY location, "
              "you MUST use the 'get_weather' tool with that location's name. "
              "Do not answer that you cannot get the weather if the 'get_weather' tool is available. "
              "Respond in a friendly manner."),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

tools = [get_weather]

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
)

if __name__ == "__main__":
    print("Conversational Weather App with Langchain and Gemini")
    print("Type 'exit' to end.")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            print("Agent: Goodbye!")
            break
        if user_input:
            try:
                response = agent_executor.invoke({"input": user_input})
                print(f"\nAgent: {response['output']}")
            except Exception as e:
                print(f"\nAgent: An error occurred: {e}")
        else:
            print("Agent: Please enter a question.") 