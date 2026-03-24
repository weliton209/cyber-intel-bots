import requests

def get_iocs(limit=10):
    """
    Retorna uma lista de IOCs recentes com informações detalhadas:
    - IP
    - Porta (se disponível)
    - País (geolocalização)
    - Hash / Família de malware
    - Tipo de ameaça
    """
    results = []

    # API Abuse.ch para malware & C2
    try:
        r = requests.post(
            "https://mb-api.abuse.ch/api/v1/",
            data={"query": "get_recent"},
            timeout=15
        ).json()

        for item in r.get("data", [])[:limit]:
            sha256 = item.get("sha256_hash")
            family = item.get("signature", "unknown")
            ip = item.get("host")
            country = item.get("country")
            port = item.get("port")
            threat_type = item.get("threat_type", "malware")

            results.append({
                "ip": ip,
                "port": port,
                "country": country,
                "family": family,
                "hash": sha256,
                "type": threat_type
            })
    except Exception:
        pass

    # Aqui você pode adicionar mais feeds, como MalwareBazaar, etc.
    # Exemplo:
    # try:
    #     r = requests.get("https://mb-api.abuse.ch/api/v1/get_recent", timeout=15).json()
    #     ...
    # except:
    #     pass

    # Remove duplicados e limita
    seen = set()
    clean_results = []
    for r in results:
        uid = f"{r['ip']}-{r.get('hash','')}"
        if uid not in seen:
            seen.add(uid)
            clean_results.append(r)

    return clean_results[:limit]
