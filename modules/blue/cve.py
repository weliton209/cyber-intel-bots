import requests

def get_cves():

    url = "https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=30"

    results = []

    try:
        data = requests.get(url, timeout=10).json()

        for item in data.get("vulnerabilities", []):

            cve = item.get("cve", {})
            cve_id = cve.get("id")

            desc = ""
            descriptions = cve.get("descriptions", [])
            if descriptions:
                desc = descriptions[0].get("value", "")

            # 🔥 filtro Blue Team (só coisa séria)
            keywords = [
                "remote", "rce", "execution",
                "privilege escalation",
                "authentication bypass",
                "deserialization"
            ]

            if not any(k in desc.lower() for k in keywords):
                continue

            results.append({
                "id": cve_id,
                "desc": desc[:200]
            })

    except:
        return []

return list(set([r["ip"] for r in results]))[:10]
