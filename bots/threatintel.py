import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

from modules.cve_exploit import get_exploitable_cves
from modules.apt_campaigns import get_apt_campaigns
from modules.credential_leaks import get_leaks
from modules.malware_c2 import get_c2

TOKEN = os.getenv("INTEL_TOKEN")
CHAT = os.getenv("INTEL_CHAT")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def send(msg):
    requests.post(url, data={"chat_id": CHAT, "text": msg}, timeout=10)

send("🧠 Threat Intel Radar ON")

# CVE
for c in get_exploitable_cves()[:5]:
    send(f"🚨 CVE Exploited\n{c['id']}\n{c['desc']}")

# APT
for a in get_apt_campaigns()[:5]:
    send(f"🎯 APT Campaign\n{a['title']}\n{a['link']}")

# Leaks
for l in get_leaks():
    send(f"🔓 Data Leak\n{l['name']}\nDomain: {l['domain']}")

# Malware
for m in get_c2()[:5]:
    send(f"🦠 Malware C2\nFamily: {m['family']}\nHash: {m['hash']}")
