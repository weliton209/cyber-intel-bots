import requests

def get_leaks():

    url = "https://haveibeenpwned.com/api/v3/breaches"

    headers = {
        "User-Agent": "intel-bot"
    }

    results = []

    try:
        data = requests.get(url, headers=headers, timeout=10).json()

        for item in data[:10]:

            results.append({
                "name": item.get("Name"),
                "domain": item.get("Domain")
            })

    except:
        return []

    return results[:5]
