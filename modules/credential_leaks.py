import feedparser

FEEDS = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/",
]

def get_leaks():

    results = []

    for feed in FEEDS:

        f = feedparser.parse(feed)

        for entry in f.entries[:10]:

            title = entry.title.lower()

            # filtro focado em vazamento
            if any(word in title for word in ["breach", "leak", "data leak", "exposed"]):

                results.append({
                    "name": entry.title,
                    "domain": entry.link
                })

    return results
