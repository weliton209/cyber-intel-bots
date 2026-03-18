import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

from modules.pentest_tools import get_new_tools
from modules.cve_exploit import get_exploitable_cves
from modules.credential_leaks import get_leaks
from modules.history import load_history, save_history, gen_id

TOKEN = os.getenv("RED_TOKEN")
CHAT = os.getenv("RED_CHAT")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send(msg):
    requests.post(url, data={"chat_id": CHAT, "text": msg}, timeout=10)


history = load_history()

send("🔴 Red Team Radar ON")

# TOOLS
for t in get_new_tools():
    uid = gen_id(t["url"])

    if uid in history:
        continue

    send(f"🛠 Tool\n{t['name']}\n{t['url']}")
    save_history(uid)

# CVE
for c in get_exploitable_cves():
    uid = gen_id(c["id"])

    if uid in history:
        continue

    send(f"🔥 Exploitable CVE\n{c['id']}")
    save_history(uid)

# LEAKS (foco ofensivo)
for l in get_leaks():
    uid = gen_id(l["name"])

    if uid in history:
        continue

    send(f"🔓 Possible Credential Leak\n{l['name']}\n{l['domain']}")
    save_history(uid)
