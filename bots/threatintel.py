import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

from modules.intel.apt import get_apt_campaigns
from modules.intel.leaks import get_leaks
from modules.intel.news import get_news
from modules.intel.ioc import get_iocs
from modules.intel.pastes import get_paste_leaks

from modules.intel.correlation import correlate_ioc_news
from modules.intel.prioritization import is_target_related
from modules.intel.credentials import analyze_credential_leak
from modules.intel.pyramid import classify_intel
from modules.intel.gti import enrich_ip
from modules.core.history import load_history, save_history, gen_id


TOKEN = os.getenv("INTEL_TOKEN")
CHAT = os.getenv("INTEL_CHAT")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send(msg):
    try:
        requests.post(url, data={"chat_id": CHAT, "text": msg}, timeout=10)
    except:
        pass


# -------------------
# 🧠 INIT
# -------------------
history = load_history()
send("🧠 Threat Intel PRO MAX (Pyramid Mode ON)")


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
leaks = get_leaks(targets)
apts = get_apt_campaigns()
pastes = get_paste_leaks(targets)


# -------------------
# 🚨 CORRELATION (ATAQUE ATIVO)
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
# 🎯 APT (ALTO NA PIRÂMIDE)
# -------------------
for a in apts:

    tag = "🎯 TARGET" if is_target_related(a["title"], targets) else "🌍 GLOBAL"

    uid = gen_id(a["title"])

    if uid in history:
        continue

    send(f"""🎯 {tag} APT Campaign 🔺

{a['title']}
{a['link']}
""")

    save_history(uid)


# -------------------
# 🔓 LEAKS (CREDENCIAIS)
# -------------------
for l in leaks:

    analysis = analyze_credential_leak(l, targets)

    if analysis["level"] not in ["🔥 CRITICAL", "⚠️ HIGH"]:
        continue

    tag_pyramid, _ = classify_intel(l.get("data", ""))

    uid = gen_id(l["name"] + str(l.get("domain")))

    if uid in history:
        continue

    send(f"""🔓 Credential Leak {analysis['level']} {tag_pyramid}

🏢 Name: {l['name']}
🌐 Domain: {l.get('domain', 'N/A')}
📅 Date: {l.get('date')}
📦 Data: {l.get('data')}

🎯 Related: {analysis['related']}
🔑 Exploitable: {analysis['exploitable']}

🛠 Attack Paths:
- Credential stuffing
- Account takeover
""")

    save_history(uid)


# -------------------
# 🔥 LIVE PASTE LEAKS
# -------------------
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
- Immediate account takeover
""")

    save_history(uid)


# -------------------
# 📰 NEWS (PYRAMID)
# -------------------
for n in news:

    tag_pyramid, score = classify_intel(n["title"])

    # 🔥 ignora lixo
    if score < 2:
        continue

    uid = gen_id(n["title"])

    if uid in history:
        continue

    send(f"""📰 Threat Intel {tag_pyramid} {n.get('tag','')}

{n['title']}

🧠 {n.get('summary','')}

🔗 {n['link']}
""")

    save_history(uid)


# -------------------
# ⚠️ IOC (GTI ENRICHED)
# -------------------
for i in iocs:

    ip = i.get("ip")

    if not ip:
        continue

    enriched = enrich_ip(ip)

    if not enriched:
        continue

    # 🔥 só alerta se realmente malicioso
    if enriched.get("malicious", 0) < 3:
        continue

    uid = gen_id(ip)

    if uid in history:
        continue

    send(f"""⚠️ IOC CONFIRMED 🔥

🌐 IP: {ip}
☠️ Malicious: {enriched.get('malicious')}
⚠️ Suspicious: {enriched.get('suspicious')}

🌍 Country: {enriched.get('country')}
🏢 ASN Owner: {enriched.get('owner')}

🛠 Action:
- Block IP
- Check logs
- Hunt connections
""")

    save_history(uid)
