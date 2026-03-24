import requests

def get_iocs():

    results = []

    try:
        data = requests.get(
            "https://feodotracker.abuse.ch/downloads/ipblocklist_recommended.json",
            timeout=10
        ).json()

        for item in data.get("data", [])[:10]:

            results.append({
                "ip": item.get("ip_address"),
                "port": item.get("port"),
                "malware": item.get("malware"),
                "status": item.get("status")
            })

    except:
        return []

    return results
