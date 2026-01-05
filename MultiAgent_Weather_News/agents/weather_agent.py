from mcp_config.weather_mcp import WeatherMCP

class WeatherAgent:
    def __init__(self):
        self.weather_mcp = WeatherMCP()

    def extract_city(self, query: str) -> str:
        return query.strip().split()[-1].strip("?.!,").title()

    def run(self, query: str) -> str:
        q = query.lower()
        city = self.extract_city(query)

        try:
            if "tomorrow" in q and "rain" in q:
                will_rain = self.weather_mcp.will_rain_tomorrow(city)
                if will_rain:
                    return f"Yes, it is expected to rain tomorrow in {city}."
                else:
                    return f"No, rain is not expected tomorrow in {city}."

            data = self.weather_mcp.get_current_weather(city)
            return (
                f"Weather in {city}:\n"
                f"- Temperature: {data['temperature']} °C\n"
                f"- Wind speed: {data['windspeed']} km/h"
            )

        except Exception as e:
            return f"Weather service error: {str(e)}"
