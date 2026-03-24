import requests

def get_news():

    feeds = [
        "https://feeds.feedburner.com/TheHackersNews",
        "https://www.cisa.gov/news.xml"
    ]

    keywords = [
        "ransomware",
        "breach",
        "leak",
        "hacked",
        "cyber attack",
        "data exposed"
    ]

    results = []

    for feed in feeds:
        try:
            r = requests.get(feed, timeout=10).text

            items = r.split("<item>")[1:6]

            for i in items:
                try:
                    title = i.split("<title>")[1].split("</title>")[0]
                    link = i.split("<link>")[1].split("</link>")[0]

                    if not any(k in title.lower() for k in keywords):
                        continue

                    results.append({
                        "title": title,
                        "link": link
                    })

                except:
                    continue

        except:
            continue

    return results[:5]
