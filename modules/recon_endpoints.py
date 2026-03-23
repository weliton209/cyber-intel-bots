import requests
import re

def extract_endpoints(js_urls):

    endpoints = set()

    for url in js_urls:

        try:
            content = requests.get(url, timeout=10).text
        except:
            continue

        found = re.findall(r'["\'](\/api\/.*?|\/v1\/.*?|\/v2\/.*?)["\']', content)

        for f in found:
            endpoints.add(f)

    return list(endpoints)
