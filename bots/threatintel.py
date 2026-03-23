import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

from modules.intel.news import get_news
from modules.intel.apt import get_apt_campaigns

from modules.core.history import load_history, save_history, gen_id

TOKEN = os.getenv("INTEL_TOKEN")
CHAT = os.getenv("INTEL_CHAT")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def send(msg):
    requests.post(url, data={"chat_id": CHAT, "text": msg}, timeout=10)


history = load_history()

send("🧠 Threat Intel Briefing ON")

# -------------------
# APT
# -------------------
for a in get_apt_campaigns():

    uid = gen_id(a["title"])

    if uid in history:
        continue

    send(f"🎯 APT Campaign\n{a['title']}\n{a['link']}")
    save_history(uid)


# -------------------
# IOC
# -------------------
for i in get_iocs():

    uid = gen_id(i["hash"])

    if uid in history:
        continue

    send(f"🦠 IOC Detected\nFamily: {i['family']}\nHash: {i['hash']}")
    save_history(uid)


# -------------------
# NEWS
# -------------------
for n in get_attack_news():

    uid = gen_id(n["title"])

    if uid in history:
        continue

    send(f"📰 Cyber Attack News\n{n['title']}\n{n['link']}")
    save_history(uid)
