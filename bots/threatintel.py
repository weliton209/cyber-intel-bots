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

send("🧠 Threat Intel PRO ON")


# -------------------
# 📂 TARGETS
# -------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
targets_path = os.path.join(BASE_DIR, "targets.txt")

with open(targets_path) as f:
    targets = [t.strip().lower() for t in f if t.strip()]


# -------------------
# 📦 DATA COLLECTION
# -------------------
iocs = get_iocs()
news = get_news()
leaks = get_leaks()
apts = get_apt_campaigns()


# -------------------
# 🚨 CORRELATION (HIGH PRIORITY)
# -------------------
alerts = correlate_ioc_news(iocs, news)

for a in alerts:

    uid = gen_id(
        str(a["ioc"].get("ip", "")) +
        str(a["ioc"].get("hash", "")) +
        a["news"]["title"]
    )

    if uid in history:
        continue

    send(f"""🚨 POSSIBLE ACTIVE ATTACK

🔥 Malware: {a['ioc'].get('malware', 'unknown')}
🌐 IP: {a['ioc'].get('ip')}
🏳️ Country: {a['ioc'].get('country', 'N/A')}

📰 News:
{a['news']['title']}
{a['news']['link']}
""")

    save_history(uid)


# -------------------
# 🎯 APT
# -------------------
for a in apts:

    tag = "🎯 TARGET" if is_target_related(a["title"], targets) else "🌍 GLOBAL"

    uid = gen_id(a["title"])

    if uid in history:
        continue

    send(f"""🎯 {tag} APT Campaign

{a['title']}
{a['link']}
""")

    save_history(uid)


# -------------------
# 🔓 LEAKS (SMART)
# -------------------
for l in leaks:

    is_target = l.get("target")

    # 🔥 REGRA DE OURO
    if not is_target and l.get("risk") != "🔥 HIGH":
        continue

    if is_target:
        tag = "🎯 TARGET"
    else:
        tag = "🌍 GLOBAL"

    uid = gen_id(l["name"] + str(l.get("domain")))

    if uid in history:
        continue

    send(f"""🔓 {tag} Data Breach {l['risk']}

🏢 Name: {l['name']}
🌐 Domain: {l.get('domain', 'N/A')}
📅 Date: {l.get('date')}
📦 Data: {l.get('data')}

🛠 Impact:
- Credential stuffing risk
- Password reuse attack
""")

    save_history(uid)

# -------------------
# 📰 NEWS (SMART FILTER)
# -------------------
for n in news:

    is_target = is_target_related(n["title"], targets)

    # 🔥 só manda global se HIGH
    if not is_target and "🔥" not in n.get("tag", ""):
        continue

    tag = "🎯 TARGET" if is_target else "🌍 GLOBAL"

    uid = gen_id(n["title"])

    if uid in history:
        continue

    send(f"""📰 {tag} Cyber Attack {n.get('tag','')}

{n['title']}
{n['link']}
""")

    save_history(uid)


# -------------------
# ⚠️ IOC (ENRIQUECIDO)
# -------------------
for i in iocs:

    uid = gen_id(
        str(i.get("ip", "")) +
        str(i.get("hash", "")) +
        str(i.get("domain", ""))
    )

    if uid in history:
        continue

    send(f"""⚠️ IOC Detected

🌐 IP: {i.get('ip', 'N/A')}
🏳️ Country: {i.get('country', 'N/A')}
🔌 Port: {i.get('port', 'N/A')}
🦠 Malware: {i.get('malware', 'unknown')}
🔑 Hash: {i.get('hash', 'N/A')}
🌍 Domain: {i.get('domain', 'N/A')}
""")

    save_history(uid)
