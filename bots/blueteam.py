import requests
import os

TOKEN = os.getenv("BLUE_TOKEN")
CHAT = os.getenv("BLUE_CHAT")

url_cve="https://services.nvd.nist.gov/rest/json/cves/2.0?cvssV3Severity=CRITICAL"

data=requests.get(url_cve).json()

for cve in data["vulnerabilities"][:3]:

    cve_id=cve["cve"]["id"]

    msg=f"🚨 Nova CVE crítica\n{cve_id}"

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id":CHAT,"text":msg}
    )
