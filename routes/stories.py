from fastapi import APIRouter
import feedparser

stories_router = APIRouter()

@stories_router.get("/stories")
def get_f1_stories():
    feed_url = "https://www.autosport.com/rss/f1/news"
    feed = feedparser.parse(feed_url)

    if not feed.entries:
        return {"stories": []}

    stories = [
        {
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "summary": entry.summary,
        }
        for entry in feed.entries[:10]
    ]
    return {"stories": stories}
