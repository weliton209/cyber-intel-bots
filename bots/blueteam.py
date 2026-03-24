import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

from modules.blue.cve import get_cves
from modules.blue.malware import get_malware
from modules.blue.ioc import get_iocs

from modules.core.history import load_history, save_history, gen_id

TOKEN = os.getenv("BLUE_TOKEN")
CHAT = os.getenv("BLUE_CHAT")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send(msg):
    try:
        requests.post(url, data={"chat_id": CHAT, "text": msg}, timeout=10)
    except:
        pass


history = load_history()

send("🔵 Blue Team Radar ON")


# 🚨 CVE
for c in get_cves():

    uid = gen_id(c["id"])

    if uid in history:
        continue

    send(f"""🚨 CVE Alert

{c['id']}
{c['desc']}
""")

    save_history(uid)


# 🦠 Malware
for m in get_malware():

    uid = gen_id(m["hash"])

    if uid in history:
        continue

    send(f"""🦠 Malware

Family: {m['family']}
Hash: {m['hash']}
""")

    save_history(uid)


# ⚠️ IOC
for i in get_iocs():

    uid = gen_id(i["ip"])

    if uid in history:
        continue

    send(f"""⚠️ IOC

IP: {i['ip']}
""")

    save_history(uid)
