import requests

def get_news():

    feeds = [
        "https://www.cisa.gov/news.xml",
        "https://feeds.feedburner.com/TheHackersNews",
    ]

    results = []

    for feed in feeds:
        try:
            r = requests.get(feed, timeout=10).text

            # parse simples
            items = r.split("<item>")[1:5]

            for i in items:
                try:
                    title = i.split("<title>")[1].split("</title>")[0]
                    link = i.split("<link>")[1].split("</link>")[0]

                    results.append({
                        "title": title,
                        "link": link
                    })

                except:
                    continue

        except:
            continue

    return results[:5]
