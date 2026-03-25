import feedparser


def get_news(limit=5):

    feeds = [
        "https://feeds.feedburner.com/TheHackersNews",
        "https://www.bleepingcomputer.com/feed/",
        "https://www.darkreading.com/rss.xml",
        "https://www.cisa.gov/news.xml"
    ]

    # 🔥 palavras mais fortes (peso maior)
    high_keywords = [
        "ransomware",
        "data breach",
        "zero-day",
        "exploit",
        "leak",
        "critical vulnerability"
    ]

    # ⚠️ palavras médias
    medium_keywords = [
        "cyberattack",
        "hacked",
        "security flaw",
        "malware",
        "phishing"
    ]

    results = []
    seen = set()

    for feed in feeds:
        try:
            parsed = feedparser.parse(feed)

            for entry in parsed.entries[:10]:

                title = entry.title
                link = entry.link

                title_lower = title.lower()

                # 🔥 SCORING
                score = 0

                if any(k in title_lower for k in high_keywords):
                    score += 2

                if any(k in title_lower for k in medium_keywords):
                    score += 1

                # ignora notícia irrelevante
                if score == 0:
                    continue

                # remove duplicados
                uid = title.strip()
                if uid in seen:
                    continue

                seen.add(uid)

                # prioridade visual
                if score >= 2:
                    tag = "🔥 HIGH"
                else:
                    tag = "⚠️ MED"

                results.append({
                    "title": title,
                    "link": link,
                    "tag": tag
                })

        except:
            continue

    return results[:limit]
