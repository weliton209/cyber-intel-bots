import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

from modules.intel.apt import get_apt_campaigns
from modules.intel.leaks import get_leaks
from modules.intel.news import get_news
from modules.intel.ioc import get_iocs

from modules.intel.correlation import correlate_ioc_news
from modules.intel.prioritization import is_target_related

from modules.core.history import load_history, save_history, gen_id


TOKEN = os.getenv("INTEL_TOKEN")
CHAT = os.getenv("INTEL_CHAT")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send(msg):
    try:
        requests.post(url, data={"chat_id": CHAT, "text": msg}, timeout=10)
    except:
        pass


history = load_history()

send("🧠 Threat Intel Radar ON")


# -------------------
# 🎯 LOAD TARGETS
# -------------------
with open("targets.txt") as f:
    targets = [t.strip() for t in f if t.strip()]


# -------------------
# 📦 COLETA DE DADOS (UMA VEZ)
# -------------------
iocs = get_iocs()
news = get_news()
leaks = get_leaks()
apts = get_apt_campaigns()


# -------------------
# 🚨 CORRELAÇÃO (ATAQUE ATIVO)
# -------------------
alerts = correlate_ioc_news(iocs, news)

for a in alerts:

    uid = gen_id(a["ioc"].get("ip", "") + a["news"]["title"])

    if uid in history:
        continue

    send(f"""🚨 POSSIBLE ACTIVE ATTACK

Malware: {a['ioc'].get('malware')}
IP: {a['ioc'].get('ip')}

News:
{a['news']['title']}
{a['news']['link']}
""")

    save_history(uid)


# -------------------
# 🎯 APT
# -------------------
for a in apts:

    uid = gen_id(a["title"])

    if uid in history:
        continue

    send(f"""🎯 APT Campaign

{a['title']}
{a['link']}
""")

    save_history(uid)


# -------------------
# 🔓 LEAKS (PRIORIZADO)
# -------------------
for l in leaks:

    if not is_target_related(l.get("domain", ""), targets):
        continue

    uid = gen_id(l["name"])

    if uid in history:
        continue

    send(f"""🔓 TARGET BREACH

{l['name']}
Domain: {l['domain']}
Date: {l.get('date')}
""")

    save_history(uid)


# -------------------
# 📰 NEWS (PRIORIZADO)
# -------------------
for n in news:

    if not is_target_related(n["title"], targets):
        continue

    uid = gen_id(n["title"])

    if uid in history:
        continue

    send(f"""🎯 TARGET NEWS

{n['title']}
{n['link']}
""")

    save_history(uid)


# -------------------
# ⚠️ IOC (MELHORADO)
# -------------------
for i in iocs:

    uid = gen_id(i.get("ip", ""))

    if uid in history:
        continue

    send(f"""⚠️ IOC

IP: {i.get('ip')}
Malware: {i.get('malware')}
Port: {i.get('port')}
""")

    save_history(uid)
