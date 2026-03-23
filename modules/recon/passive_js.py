import requests

def get_js_passive(domain):

    url = f"http://web.archive.org/cdx/search/cdx?url=*.{domain}/*.js&output=json&fl=original"

    try:
        data = requests.get(url, timeout=10).json()
    except:
        return []

    results = set()

    # pula o header (linha 0)
    for row in data[1:]:
        if isinstance(row, list) and row:
            results.add(row[0])

    return list(results)[:10]
