import requests

def get_iocs():

    urls = [
        "https://feodotracker.abuse.ch/downloads/ipblocklist.txt",
        "https://raw.githubusercontent.com/stamparm/ipsum/master/ipsum.txt"
    ]

    ips = set()

    for url in urls:
        try:
            data = requests.get(url, timeout=10).text.splitlines()

            for line in data:

                if not line or line.startswith("#"):
                    continue

                ip = line.split()[0]
                ips.add(ip)

        except:
            continue

    return [{"ip": ip} for ip in list(ips)[:10]]
