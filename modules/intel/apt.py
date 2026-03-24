import requests

def get_apt_campaigns():

    url = "https://www.cisa.gov/news.xml"

    results = []

    try:
        r = requests.get(url, timeout=10).text

        items = r.split("<item>")[1:6]

        for i in items:
            try:
                title = i.split("<title>")[1].split("</title>")[0]
                link = i.split("<link>")[1].split("</link>")[0]

                if "APT" not in title and "threat" not in title.lower():
                    continue

                results.append({
                    "title": title,
                    "link": link
                })

            except:
                continue

    except:
        return []

    return results[:5]
