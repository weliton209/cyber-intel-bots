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
    except Exception as e:
        print(f"[!] Falha ao enviar msg: {e}")


history = load_history()

send("🔵 Blue Team PRO ON")


# -------------------
# 🚨 CVE (PRIORIZADO)
# -------------------
for c in get_cves():

    cvss = float(c.get("cvss", 0))

    # 🔥 filtra só relevante
    if cvss < 7:
        continue

    if cvss >= 9:
        severity = "🔥 CRITICAL"
    elif cvss >= 7:
        severity = "⚠️ HIGH"

    uid = gen_id(c["id"])

    if uid in history:
        continue

    send(f"""🚨 {severity} CVE

ID: {c['id']}
CVSS: {cvss}
Published: {c.get('published', 'N/A')}

📝 {c['desc'][:200]}

🛠 Action:
- Check affected systems
- Apply patch ASAP
- Monitor exploitation attempts
""")

    save_history(uid)


# -------------------
# 🦠 MALWARE (COM CONTEXTO)
# -------------------
for m in get_malware():

    uid = gen_id(m["hash"])

    if uid in history:
        continue

    send(f"""🦠 Malware Detected

Family: {m['family']}
Hash: {m['hash']}
Type: {m.get('type','N/A')}

🛠 Action:
- Block hash in EDR
- Search in SIEM
- Isolate infected host if found
""")

    save_history(uid)


# -------------------
# ⚠️ IOC (PRIORIZADO)
# -------------------
for i in get_iocs():

    uid = gen_id(
        i.get("ip","") +
        str(i.get("hash","")) +
        str(i.get("domain",""))
    )

    if uid in history:
        continue

    # 🔥 SCORE SIMPLES
    score = 0

    if i.get("malware"): score += 2
    if i.get("port"): score += 1
    if i.get("asn"): score += 1

    if score >= 3:
        severity = "🔥 HIGH"
    elif score >= 2:
        severity = "⚠️ MED"
    else:
        severity = "ℹ️ LOW"

    send(f"""⚠️ IOC {severity}

🌐 IP: {i.get('ip', 'N/A')}
🌍 Country: {i.get('country', 'N/A')}
🔌 Port: {i.get('port', 'N/A')}
🦠 Malware: {i.get('family', 'N/A')}
🔑 Hash: {i.get('hash', 'N/A')}
🌐 Domain: {i.get('domain', 'N/A')}
🏢 ASN: {i.get('asn', 'N/A')}

🛠 Action:
- Block IP/Domain on firewall
- Search logs (SIEM)
- Check outbound connections
""")

    save_history(uid)
