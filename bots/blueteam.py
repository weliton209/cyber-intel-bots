import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

from modules.blue.cve import get_cves
from modules.blue.malware import get_malware
from modules.blue.ioc import get_iocs
from modules.core.history import load_history, save_history, gen_id

# Tokens e chat do Telegram
TOKEN = os.getenv("BLUE_TOKEN")
CHAT = os.getenv("BLUE_CHAT")
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def send(msg):
    """Envia mensagem para Telegram"""
    try:
        requests.post(url, data={"chat_id": CHAT, "text": msg}, timeout=10)
    except Exception as e:
        print(f"[!] Falha ao enviar msg: {e}")

# Carrega histórico
history = load_history()
send("🔵 Blue Team Radar ON")

# -------------------
# 🚨 CVEs
# -------------------
for c in get_cves():
    uid = gen_id(c["id"])
    if uid in history:
        continue

    msg = f"""🚨 CVE Alert

ID: {c['id']}
Description: {c['desc']}
CVSS: {c.get('cvss', 'N/A')}
Published: {c.get('published', 'N/A')}
"""
    send(msg)
    save_history(uid)

# -------------------
# 🦠 Malware
# -------------------
for m in get_malware():
    uid = gen_id(m["hash"])
    if uid in history:
        continue

    msg = f"""🦠 Malware Alert

Family: {m['family']}
Hash: {m['hash']}
Type: {m.get('type','N/A')}
"""
    send(msg)
    save_history(uid)

# -------------------
# ⚠️ IOCs Detalhados
# -------------------
for i in get_iocs():
    # UID único usando IP + hash ou domínio
    uid = gen_id(i.get("ip","") + str(i.get("hash","")) + str(i.get("domain","")) )
    if uid in history:
        continue

    msg = f"""⚠️ IOC Detected

IP: {i.get('ip', 'N/A')}
Port: {i.get('port', 'N/A')}
Country: {i.get('country', 'N/A')}
Type: {i.get('type', 'N/A')}
Malware Family: {i.get('family', 'N/A')}
Hash: {i.get('hash', 'N/A')}
Domain: {i.get('domain', 'N/A')}
ASN: {i.get('asn', 'N/A')}
"""
    send(msg)
    save_history(uid)
