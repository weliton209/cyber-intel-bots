import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

from modules.malware_c2 import get_c2
from modules.apt_campaigns import get_apt_campaigns
from modules.history import load_history, save_history, gen_id

TOKEN = os.getenv("BLUE_TOKEN")
CHAT = os.getenv("BLUE_CHAT")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send(msg):
    requests.post(url, data={"chat_id": CHAT, "text": msg}, timeout=10)


history = load_history()

send("🔵 Blue Team Radar ON")

# MALWARE
for m in get_c2():
    uid = gen_id(m["hash"])

    if uid in history:
        continue

    send(f"🦠 Threat\n{m['family']}\n{m['hash']}")
    save_history(uid)

# APT
for a in get_apt_campaigns():
    uid = gen_id(a["title"])

    if uid in history:
        continue

    send(f"🎯 APT\n{a['title']}")
    save_history(uid)
