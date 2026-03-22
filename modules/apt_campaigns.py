import feedparser

FEEDS = [
    "https://www.securelist.com/feed/",
    "https://unit42.paloaltonetworks.com/feed/",
    "https://www.mandiant.com/resources/blog/rss.xml"
]

def get_apt_campaigns():

    results = []

    for feed in FEEDS:

        f = feedparser.parse(feed)

        for entry in f.entries[:5]:

            results.append({
                "title": entry.title,
                "link": entry.link
            })

    return results
