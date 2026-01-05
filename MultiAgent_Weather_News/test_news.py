from mcp_config.news_mcp import NewsMCP

news = NewsMCP()
articles = news.get_top_news()

for a in articles:
    print("-", a["title"])
