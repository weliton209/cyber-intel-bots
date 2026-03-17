import sys
import os

# adiciona raiz do projeto no path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

TOKEN = os.getenv("INTEL_TOKEN")
CHAT = os.getenv("INTEL_CHAT")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send(msg):

    requests.post(
        url,
        data={
            "chat_id": CHAT,
            "text": msg
        },
        timeout=10
    )


send("🚀 Radar started")


# -------------------
# TESTE CVE
# -------------------

try:

    from modules.cve_exploit import get_exploitable_cves

    send("Testing CVE module")

    for c in get_exploitable_cves()[:2]:

        send(f"CVE test: {c['id']}")

except Exception as e:

    send(f"CVE ERROR: {e}")


# -------------------
# TESTE APT
# -------------------

try:

    from modules.apt_campaigns import get_apt_campaigns

    send("Testing APT module")

    for a in get_apt_campaigns()[:2]:

        send(f"APT: {a['title']}")

except Exception as e:

    send(f"APT ERROR: {e}")
