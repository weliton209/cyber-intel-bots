import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

from modules.intel.news import get_news
from modules.intel.apt import get_apt_campaigns
from modules.intel.ioc import get_iocs
from modules.intel.malware import get_c2
from modules.intel.leaks import get_leaks
from modules.cve_exploit import get_exploitable_cves

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

send("🧠 Threat Intel PRO ON")


# -------------------
# 🚨 CVE (PRIORIDADE)
# -------------------
for c in get_exploitable_cves():

    uid = gen_id(c["id"])

    if uid in history:
        continue

    send(f"""🚨 Exploitable CVE

{c['id']}
{c['desc']}
""")

    save_history(uid)


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
# 🦠 MALWARE C2
# -------------------
for m in get_c2():

    uid = gen_id(m["hash"])

    if uid in history:
        continue

    send(f"""🦠 Malware C2

Family: {m['family']}
Hash: {m['hash']}
""")

    save_history(uid)


# -------------------
# 🔓 DATA BREACH
# -------------------
for l in get_leaks():

    uid = gen_id(l["name"])

    if uid in history:
        continue

    send(f"""🔓 Data Breach

{l['name']}
Domain: {l['domain']}
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
