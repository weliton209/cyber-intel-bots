import requests
import os

TOKEN = os.getenv("BLUE_TOKEN")
CHAT = os.getenv("BLUE_CHAT")

url = "https://services.nvd.nist.gov/rest/json/cves/2.0?cvssV3Severity=CRITICAL"

data = requests.get(url).json()

for cve in data["vulnerabilities"][:5]:

    cve_id = cve["cve"]["id"]

    desc = cve["cve"]["descriptions"][0]["value"]

    msg = f"""
🚨 Critical CVE

ID: {cve_id}

Description:
{desc[:200]}
"""

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT, "text": msg}
    )
