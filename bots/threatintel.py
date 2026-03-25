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
from modules.intel.credentials import analyze_credential_leak
from modules.intel.pastes import get_paste_leaks

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

send("🧠 Threat Intel PRO MAX ON")


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
leaks = get_leaks(targets)  # 🔥 AGORA USANDO TARGETS
apts = get_apt_campaigns()


# -------------------
# 🚨 CORRELATION (HIGH PRIORITY)
# -------------------
alerts = correlate_ioc_news(iocs, news)

for a in alerts:

    risk = "🔥 HIGH" if a["ioc"].get("malware") else "⚠️ MED"

    uid = gen_id(
        str(a["ioc"].get("ip", "")) +
        str(a["ioc"].get("hash", "")) +
        a["news"]["title"]
    )

    if uid in history:
        continue

    send(f"""🚨 POSSIBLE ACTIVE ATTACK {risk}

🔥 Malware: {a['ioc'].get('malware', 'unknown')}
🌐 IP: {a['ioc'].get('ip')}
🏳️ Country: {a['ioc'].get('country', 'N/A')}

📰 News:
{a['news']['title']}
{a['news']['link']}

🛠 Action:
- Block IOC
- Investigate logs
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
# 🔓 LEAKS (CRED INTEL)
# -------------------
for l in leaks:

    analysis = analyze_credential_leak(l, targets)

    level = analysis["level"]

    # 🔥 ANTI RUÍDO
    if level not in ["🔥 CRITICAL", "⚠️ HIGH"]:
        continue

    uid = gen_id(l["name"] + str(l.get("domain")))

    if uid in history:
        continue

    send(f"""🔓 Credential Leak {level}

🏢 Name: {l['name']}
🌐 Domain: {l.get('domain', 'N/A')}
📅 Date: {l.get('date')}
📦 Data: {l.get('data')}

🎯 Related to Target: {analysis['related']}
🔑 Exploitable: {analysis['exploitable']}

🛠 Attack Paths:
- Credential stuffing
- Password reuse
- Account takeover
""")

    save_history(uid)


# -------------------
# 🔥 LIVE CREDENTIAL LEAKS
# -------------------
pastes = get_paste_leaks(targets)

for p in pastes:

    uid = gen_id(p["url"])

    if uid in history:
        continue

    send(f"""🔥 LIVE CREDENTIAL LEAK

🎯 Target: {p['target']}

🧾 Sample:
{chr(10).join(p['snippet'])}

🔗 Source:
{p['url']}

🛠 Risk:
- Active credential exposure
- Immediate takeover risk
""")

    save_history(uid)


# -------------------
# 📰 NEWS (SMART FILTER)
# -------------------
for n in news:

    is_target = is_target_related(n["title"], targets)

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
# ⚠️ IOC (SMART)
# -------------------
for i in iocs:

    score = 0

    if i.get("malware"): score += 2
    if i.get("port"): score += 1
    if i.get("asn"): score += 1

    if score < 2:
        continue

    if score >= 3:
        level = "🔥 HIGH"
    else:
        level = "⚠️ MED"

    uid = gen_id(
        str(i.get("ip", "")) +
        str(i.get("hash", "")) +
        str(i.get("domain", ""))
    )

    if uid in history:
        continue

    send(f"""⚠️ IOC {level}

🌐 IP: {i.get('ip', 'N/A')}
🏳️ Country: {i.get('country', 'N/A')}
🔌 Port: {i.get('port', 'N/A')}
🦠 Malware: {i.get('malware', 'unknown')}
🔑 Hash: {i.get('hash', 'N/A')}
🌍 Domain: {i.get('domain', 'N/A')}

🛠 Action:
- Block IOC
- Hunt in SIEM
""")

    save_history(uid)
