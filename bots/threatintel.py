import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

from modules.cve_exploit import get_exploitable_cves
from modules.apt_campaigns import get_apt_campaigns
from modules.credential_leaks import get_leaks
from modules.malware_c2 import get_c2
from modules.history import load_history, save_history, gen_id

TOKEN = os.getenv("INTEL_TOKEN")
CHAT = os.getenv("INTEL_CHAT")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send(msg):
    requests.post(url, data={"chat_id": CHAT, "text": msg}, timeout=10)


history = load_history()

send("🧠 Threat Intel Radar ON")

# CVE
for c in get_exploitable_cves():
    uid = gen_id(c["id"] + c["desc"])

    if uid in history:
        continue

    send(f"🚨 CVE Exploited\n{c['id']}\n{c['desc']}")
    save_history(uid)

# APT
for a in get_apt_campaigns():
    uid = gen_id(a["title"])

    if uid in history:
        continue

    send(f"🎯 APT Campaign\n{a['title']}\n{a['link']}")
    save_history(uid)

# LEAKS
for l in get_leaks():
    uid = gen_id(l["name"])

    if uid in history:
        continue

    send(f"🔓 Data Leak\n{l['name']}\n{l['domain']}")
    save_history(uid)

# MALWARE
for m in get_c2():
    uid = gen_id(m["hash"])

    if uid in history:
        continue

    send(f"🦠 Malware C2\n{m['family']}\n{m['hash']}")
    save_history(uid)
