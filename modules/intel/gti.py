import requests
import os

API_KEY = os.getenv("GTI_API_KEY")


def enrich_ip(ip):

    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"

    headers = {
        "x-apikey": API_KEY
    }

    try:
        r = requests.get(url, headers=headers, timeout=10).json()

        attr = r.get("data", {}).get("attributes", {})

        stats = attr.get("last_analysis_stats", {})

        return {
            "malicious": stats.get("malicious", 0),
            "suspicious": stats.get("suspicious", 0),
            "country": attr.get("country"),
            "asn": attr.get("asn"),
            "owner": attr.get("as_owner")
        }

    except:
        return None
