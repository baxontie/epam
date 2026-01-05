from mcp_config.weather_mcp import WeatherMCP

weather = WeatherMCP()
result = weather.get_weather("Berlin")

print(result)
