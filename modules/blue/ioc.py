import requests

def get_iocs():

    urls = [
        "https://feodotracker.abuse.ch/downloads/ipblocklist.txt",
        "https://raw.githubusercontent.com/stamparm/ipsum/master/ipsum.txt"
    ]

    results = []

    for url in urls:
        try:
            data = requests.get(url, timeout=10).text.splitlines()

            for line in data:

                if not line or line.startswith("#"):
                    continue

                ip = line.split()[0]

                results.append({
                    "ip": ip
                })

        except:
            continue

return list(set([r["ip"] for r in results]))[:10]
