import feedparser

def get_apt_news():

    feeds = [
        "https://www.cisa.gov/cybersecurity-advisories/all.xml",
        "https://feeds.feedburner.com/TheHackersNews"
    ]

    results = []

    for f in feeds:

        data = feedparser.parse(f)

        for entry in data.entries[:3]:

            results.append({
                "title": entry.title,
                "link": entry.link
            })

    return results
