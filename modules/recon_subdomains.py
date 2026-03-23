import requests
import re

def from_crtsh(domain):

    url = f"https://crt.sh/?q=%25.{domain}&output=json"

    try:
        data = requests.get(url, timeout=10).json()
    except:
        return []

    results = set()

    for entry in data:
        name = entry["name_value"]

        if "*" in name:
            continue

        results.add(name.strip())

    return results


def from_hackertarget(domain):

    url = f"https://api.hackertarget.com/hostsearch/?q={domain}"

    try:
        r = requests.get(url, timeout=10).text
    except:
        return []

    results = set()

    for line in r.splitlines():
        if "," in line:
            sub = line.split(",")[0]
            results.add(sub)

    return results


def from_rapiddns(domain):

    url = f"https://rapiddns.io/subdomain/{domain}?full=1"

    try:
        r = requests.get(url, timeout=10).text
    except:
        return []

    results = set()

    matches = re.findall(r'<td>(.*?)</td>', r)

    for m in matches:
        if domain in m and "*" not in m:
            results.add(m.strip())

    return results


def get_subdomains(domain):

    results = set()

    results.update(from_crtsh(domain))
    results.update(from_hackertarget(domain))
    results.update(from_rapiddns(domain))

    return list(results)
