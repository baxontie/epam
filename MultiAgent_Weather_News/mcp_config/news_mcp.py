import feedparser
from urllib.parse import quote

class NewsMCP:
    BASE_URL = "https://news.google.com/rss"

    def get_top_news(self, topic: str | None = None):
        if topic:
            safe_topic = quote(topic)
            url = f"{self.BASE_URL}/search?q={safe_topic}&hl=en-US&gl=US&ceid=US:en"
        else:
            url = f"{self.BASE_URL}?hl=en-US&gl=US&ceid=US:en"

        feed = feedparser.parse(url)

        articles = []
        for entry in feed.entries[:5]:
            articles.append({
                "title": entry.title,
                "description": getattr(entry, "summary", ""),
                "source": "Google News"
            })

        return articles
