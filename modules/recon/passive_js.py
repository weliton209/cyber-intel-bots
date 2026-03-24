import requests

def get_passive_js(domain):
    """
    Busca arquivos JS de forma passiva via CRT.sh.
    """
    results = []

    url = f"https://crt.sh/?q={domain}&output=json"

    try:
        r = requests.get(url, timeout=10).json()
        for entry in r[:50]:
            name = entry.get("name_value", "")
            if ".js" in name:
                if not name.startswith("http"):
                    name = "https://" + name
                results.append(name)
    except:
        pass

    return list(set(results))[:10]
