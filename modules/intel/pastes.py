import requests
import re


def get_paste_leaks(targets):

    url = "https://psbdmp.ws/api/search/recent"

    results = []

    try:
        data = requests.get(url, timeout=10).json()

        for item in data.get("data", [])[:20]:

            paste_id = item.get("id")
            paste_url = f"https://psbdmp.ws/api/dump/{paste_id}"

            try:
                content = requests.get(paste_url, timeout=10).text.lower()

                for t in targets:

                    base = t.split(".")[0].lower()

                    if base in content:

                        matches = re.findall(
                            r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+[:|].{4,20}",
                            content
                        )

                        results.append({
                            "target": t,
                            "snippet": matches[:3],
                            "url": paste_url
                        })

                        break

            except:
                continue

    except:
        return []

    return results[:5]
