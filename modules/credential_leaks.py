import feedparser

# 🔥 SEUS ALVOS (bug bounty / interesse)
TARGETS = [
    "portoseguro",
    "azulseguros",
    "redbull",
    "nba",
    "btg"
]

KEYWORDS = [
    "breach",
    "leak",
    "database",
    "dump",
    "credentials",
    "exposed"
]

FEEDS = [
    "https://www.bleepingcomputer.com/feed/",
    "https://feeds.feedburner.com/TheHackersNews"
]

def get_leaks():

    results = []

    for feed in FEEDS:

        f = feedparser.parse(feed)

        for entry in f.entries[:10]:

            title = entry.title.lower()

            # 🔎 filtro de leak
            if not any(k in title for k in KEYWORDS):
                continue

            # 🎯 filtro de TARGET
            if not any(t in title for t in TARGETS):
                continue

            results.append({
                "name": entry.title,
                "domain": entry.link
            })

    return results
