def detect_intent(query: str) -> str:
    q = query.lower()

    weather_keywords = ["weather", "temperature", "rain", "forecast"]
    news_keywords = ["news", "headline", "headlines"]

    is_weather = any(k in q for k in weather_keywords)
    is_news = any(k in q for k in news_keywords)

    if is_weather and is_news:
        return "both"
    if is_weather:
        return "weather"
    if is_news:
        return "news"

    return "unknown"
