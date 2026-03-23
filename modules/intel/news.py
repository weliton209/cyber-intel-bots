import feedparser

KEYWORDS = [
    "cyber attack",
    "ransomware",
    "breach",
    "data leak",
    "hacked"
]

FEEDS = [
    "https://news.google.com/rss/search?q=cyber+attack",
    "https://www.bleepingcomputer.com/feed/"
]

def get_attack_news():

    results = []

    for feed in FEEDS:

        f = feedparser.parse(feed)

        for entry in f.entries[:10]:

            title = entry.title.lower()

            if any(k in title for k in KEYWORDS):

                results.append({
                    "title": entry.title,
                    "link": entry.link
                })

    return results
