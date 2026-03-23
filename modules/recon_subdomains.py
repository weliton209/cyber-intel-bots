import requests

def get_subdomains(domain):

    import requests

    url = f"https://crt.sh/?q=%25.{domain}&output=json"

    try:
        data = requests.get(url, timeout=10).json()
    except:
        return []

    results = set()

    for entry in data:

        name = entry["name_value"]

        # ❌ remove wildcard
        if "*" in name:
            continue

        if domain in name:
            results.add(name.strip())

    return list(results)
