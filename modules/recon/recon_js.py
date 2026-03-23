import requests
import re

def get_js_files(domain):

    try:
        r = requests.get(f"https://{domain}", timeout=10).text
    except:
        return []

    js_files = re.findall(r'src="(.*?\.js)"', r)

    results = []

    for js in js_files:

        if "chunk" in js or "_next" in js:
            continue

        if js.startswith("/"):
            js = f"https://{domain}{js}"

        results.append(js)

    return list(set(results))
