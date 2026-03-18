import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from modules.malware_c2 import get_c2
from modules.apt_campaigns import get_apt_campaigns

TOKEN = os.getenv("BLUE_TOKEN")
CHAT = os.getenv("BLUE_CHAT")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def send(msg):
    requests.post(url, data={"chat_id": CHAT, "text": msg}, timeout=10)

send("🔵 Blue Team Radar ON")

# Malware
for m in get_c2()[:5]:
    send(f"🦠 Threat\n{m['family']}\n{m['hash']}")

# APT
for a in get_apt_campaigns()[:5]:
    send(f"🎯 APT\n{a['title']}")
