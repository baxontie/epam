from mcp_config.news_mcp import NewsMCP

class NewsAgent:
    def __init__(self):
        self.news_mcp = NewsMCP()

    def extract_topic(self, query: str) -> str | None:
        q = query.lower()

        if "about" in q:
            return q.split("about", 1)[1].strip(" ?.!,")

        if " in " in q:
            return q.split(" in ", 1)[1].strip(" ?.!,")

        return None

    def run(self, query: str) -> str:
        topic = self.extract_topic(query)

        try:
            articles = self.news_mcp.get_top_news(topic)
        except Exception as e:
            return f"News service error: {str(e)}"

        if not articles:
            return "No news articles found."

        header = "Latest news"
        if topic:
            header += f" about {topic.title()}"

        response = header + ":\n"
        for a in articles:
            response += f"- {a['title']}\n"

        return response
