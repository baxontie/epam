from agents.intent_parser import detect_intent
from agents.weather_agent import WeatherAgent
from agents.news_agent import NewsAgent

class Orchestrator:
    def __init__(self):
        self.weather_agent = WeatherAgent()
        self.news_agent = NewsAgent()

    def handle(self, query: str) -> str:
        intent = detect_intent(query)

        if intent == "weather":
            return self.weather_agent.run(query)

        if intent == "news":
            return self.news_agent.run(query)

        if intent == "both":
            weather_response = self.weather_agent.run(query)
            news_response = self.news_agent.run(query)
            return f"{weather_response}\n\n{news_response}"

        return (
            "Sorry, I couldn't understand your request.\n"
            "You can ask about weather, news, or both."
        )
