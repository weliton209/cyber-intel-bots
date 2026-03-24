import requests

def get_exploitable_cves():

    url = "https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=20"

    results = []

    try:
        r = requests.get(url, timeout=10).json()

        for item in r.get("vulnerabilities", []):

            cve = item.get("cve", {})
            cve_id = cve.get("id")

            desc = ""

            descriptions = cve.get("descriptions", [])
            if descriptions:
                desc = descriptions[0].get("value", "")

            # 🔥 filtro básico (prioriza coisa relevante)
            if not any(word in desc.lower() for word in [
                "remote", "rce", "execution", "auth bypass", "deserialization"
            ]):
                continue

            results.append({
                "id": cve_id,
                "desc": desc[:200]
            })

    except:
        return []

    return results[:5]
