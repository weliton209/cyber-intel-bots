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

        # ❌ remove chunks inúteis (Next.js)
        if "chunks" in js or "_next" in js:
            continue

        results.append(js)

    return results
