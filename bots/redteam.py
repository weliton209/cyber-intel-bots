import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

from modules.recon.subdomains import get_subdomains
from modules.recon.recon_js import get_js_files
from modules.recon.endpoints import extract_endpoints
from modules.recon.passive_js import get_passive_js


TOKEN = os.getenv("RED_TOKEN")
CHAT = os.getenv("RED_CHAT")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send(msg):
    try:
        requests.post(url, data={"chat_id": CHAT, "text": msg}, timeout=15)
    except:
        pass


history = load_history()

send("🔴 Smart Passive Recon ON")


# -------------------
# 📂 LOAD TARGETS
# -------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
targets_path = os.path.join(BASE_DIR, "targets.txt")

with open(targets_path) as f:
    targets = [t.strip() for t in f if t.strip()]


# -------------------
# 🔁 LOOP TARGETS
# -------------------
for t in targets:

    subs = get_subdomains(t)

    subs = list(set(subs))[:20]

    if not subs:
        continue

    # 🔥 PRIORIZA HIGH VALUE MAS NÃO BLOQUEIA
    high_value = [s for s in subs if is_high_value(s)]

    if high_value:
        targets_to_use = high_value[:10]
        tag = "🔥 HIGH VALUE"
    else:
        targets_to_use = subs[:10]
        tag = "🌐 RECON"

    js_files = []
    endpoints = []

    # -------------------
    # 🧪 JS (ATIVO LEVE)
    # -------------------
    for h in targets_to_use[:5]:
        js = get_js_files(h)
        js_files.extend(js)

    # -------------------
    # 👻 PASSIVE JS (SE NÃO ACHOU NADA)
    # -------------------
    if not js_files:
        js_files = get_passive_js(t)

    js_files = list(set(js_files))[:10]

    if js_files:
        endpoints = extract_endpoints(js_files)[:10]

    # -------------------
    # 🧠 ANTI DUPLICAÇÃO
    # -------------------
    uid = gen_id(t + "".join(targets_to_use))

    if uid in history:
        continue

    save_history(uid)

    # -------------------
    # 📤 OUTPUT
    # -------------------
    msg = f"🎯 TARGET: {t}\n\n"
    msg += f"{tag}\n\n"

    msg += "🌐 Subdomains:\n"
    for s in targets_to_use[:5]:
        msg += f"- {s}\n"

    if js_files:
        msg += "\n🧪 JS Files:\n"
        for j in js_files[:5]:
            msg += f"- {j}\n"

    if endpoints:
        msg += "\n🔗 Endpoints:\n"
        for e in endpoints[:5]:
            msg += f"- {e}\n"

    send(msg)
