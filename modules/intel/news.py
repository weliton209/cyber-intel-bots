import requests
import re


def clean(text):
    if not text:
        return ""

    # remove CDATA
    text = re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", text)

    return text.strip()


def get_news():

    feeds = [
        "https://feeds.feedburner.com/TheHackersNews",
        "https://www.bleepingcomputer.com/feed/",
        "https://www.darkreading.com/rss.xml",
        "https://www.cisa.gov/news.xml",
        "https://boletimsec.com/feed/"
    ]

    keywords = [
        "ransomware",
        "data breach",
        "cyberattack",
        "hacked",
        "zero-day",
        "exploit",
        "leak",
        "vazamento",
        "ataque"
    ]

    results = []

    for feed in feeds:
        try:
            r = requests.get(feed, timeout=10).text

            items = r.split("<item>")[1:8]

            for i in items:
                try:
                    title = clean(i.split("<title>")[1].split("</title>")[0])
                    link = clean(i.split("<link>")[1].split("</link>")[0])

                    title_lower = title.lower()

                    if not any(k in title_lower for k in keywords):
                        continue

                    # 🔥 TAG DE PRIORIDADE
                    if any(x in title_lower for x in ["ransomware", "zero-day", "exploit"]):
                        tag = "🔥 HIGH"
                    elif any(x in title_lower for x in ["breach", "leak", "vazamento"]):
                        tag = "⚠️ MED"
                    else:
                        tag = "ℹ️ LOW"

                    results.append({
                        "title": title,
                        "link": link,
                        "tag": tag
                    })

                except:
                    continue

        except:
            continue

    return results[:10]
