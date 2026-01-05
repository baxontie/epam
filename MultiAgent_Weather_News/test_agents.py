from agents.weather_agent import WeatherAgent
from agents.news_agent import NewsAgent

weather_agent = WeatherAgent()
news_agent = NewsAgent()

print(weather_agent.run("What's the weather in Astana?"))
print()
print(news_agent.run("Latest news about technology"))
