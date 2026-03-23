import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

from modules.intel.news import get_news
from modules.intel.apt import get_apt_campaigns
from modules.intel.ioc import get_iocs
from modules.core.history import load_history, save_history, gen_id

TOKEN = os.getenv("INTEL_TOKEN")
CHAT = os.getenv("INTEL_CHAT")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def send(msg):
    try:
        requests.post(url, data={"chat_id": CHAT, "text": msg}, timeout=10)
    except Exception as e:
        print("Telegram error:", e)


history = load_history()

send("🧠 Threat Intel Briefing ON")


# -------------------
# 🎯 APT
# -------------------
for a in get_apt_campaigns():

    uid = gen_id(a["title"])

    if uid in history:
        continue

    send(f"""🎯 APT Campaign

{a['title']}
{a['link']}
""")

    save_history(uid)


# -------------------
# ⚠️ IOC
# -------------------
for i in get_iocs():

    uid = gen_id(i["ip"])

    if uid in history:
        continue

    send(f"""⚠️ IOC Detected

IP: {i['ip']}
""")

    save_history(uid)


# -------------------
# 📰 NEWS
# -------------------
for n in get_news():

    uid = gen_id(n["title"])

    if uid in history:
        continue

    send(f"""📰 Cyber Attack News

{n['title']}
{n['link']}
""")

    save_history(uid)
