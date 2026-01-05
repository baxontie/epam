import requests

class WeatherMCP:
    BASE_GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
    BASE_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

    def get_coordinates(self, city: str):
        response = requests.get(
            self.BASE_GEOCODE_URL,
            params={"name": city, "count": 1}
        )
        response.raise_for_status()
        data = response.json()

        if "results" not in data:
            raise ValueError("City not found")

        result = data["results"][0]
        return result["latitude"], result["longitude"]

    def get_current_weather(self, city: str):
        lat, lon = self.get_coordinates(city)

        response = requests.get(
            self.BASE_WEATHER_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": True
            }
        )
        response.raise_for_status()
        data = response.json()

        weather = data.get("current_weather", {})
        return {
            "temperature": weather.get("temperature"),
            "windspeed": weather.get("windspeed")
        }

    def will_rain_tomorrow(self, city: str) -> bool:
        lat, lon = self.get_coordinates(city)

        response = requests.get(
            self.BASE_WEATHER_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "daily": "precipitation_sum",
                "timezone": "auto"
            }
        )
        response.raise_for_status()
        data = response.json()

        precipitation = data["daily"]["precipitation_sum"][1]
        return precipitation > 0
