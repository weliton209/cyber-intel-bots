import requests

def get_subdomains(domain):

    url = f"https://crt.sh/?q=%25.{domain}&output=json"

    try:
        data = requests.get(url, timeout=10).json()
    except:
        return []

    results = set()

    for entry in data:

        name = entry["name_value"]

        if domain in name:
            results.add(name)

    return list(results)
