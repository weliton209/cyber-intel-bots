import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from modules.pentest_tools import get_new_tools
from modules.cve_exploit import get_exploitable_cves

TOKEN = os.getenv("RED_TOKEN")
CHAT = os.getenv("RED_CHAT")
send("🚀 TESTE RED TEAM OK")
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def send(msg):
    requests.post(url, data={"chat_id": CHAT, "text": msg}, timeout=10)

send("🔴 Red Team Radar ON")

# Tools
for t in get_new_tools()[:5]:
    send(f"🛠 Tool\n{t['name']}\n{t['url']}")

# CVE
for c in get_exploitable_cves()[:5]:
    send(f"🔥 Exploitable CVE\n{c['id']}")
