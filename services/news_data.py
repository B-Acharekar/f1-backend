import feedparser

def get_f1_stories():
    feed = feedparser.parse("https://www.autosport.com/rss/f1/news")
    articles = [
        {
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "summary": entry.summary,
        }
        for entry in feed.entries[:5]
    ]
    return {"stories": articles}