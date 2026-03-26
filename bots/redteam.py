import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

from modules.recon.subdomains import get_subdomains
from modules.recon.recon_js import get_js_files
from modules.recon.endpoints import extract_endpoints
from modules.recon.passive_js import get_passive_js

from modules.core.history import load_history, save_history, gen_id


TOKEN = os.getenv("RED_TOKEN")
CHAT = os.getenv("RED_CHAT")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send(msg):
    try:
        requests.post(url, data={"chat_id": CHAT, "text": msg}, timeout=15)
    except:
        pass


# -------------------
# 📂 LOAD HISTORY
# -------------------
history = load_history()

seen_subs = set(history.get("subs", []))
seen_js = set(history.get("js", []))
seen_endpoints = set(history.get("endpoints", []))

send("🔴 Smart Recon DELTA ON")


# -------------------
# 📂 LOAD TARGETS
# -------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
targets_path = os.path.join(BASE_DIR, "targets.txt")

with open(targets_path) as f:
    targets = [t.strip() for t in f if t.strip()]


# -------------------
# 🔥 HIGH VALUE FILTER
# -------------------
def is_high_value(sub):
    keywords = ["api", "admin", "dev", "stage", "internal", "auth"]
    return any(k in sub.lower() for k in keywords)


# -------------------
# 🔁 LOOP TARGETS
# -------------------
for t in targets:

    subs = get_subdomains(t)
    subs = list(set(subs))[:30]

    if not subs:
        continue

    # 🔥 prioriza high value
    high_value = [s for s in subs if is_high_value(s)]

    if high_value:
        targets_to_use = high_value[:10]
        tag = "🔥 HIGH VALUE"
    else:
        targets_to_use = subs[:10]
        tag = "🌐 RECON"

    # -------------------
    # 🆕 FILTRO NOVOS SUBS
    # -------------------
    new_subs = [s for s in targets_to_use if s not in seen_subs]

    # -------------------
    # 🧪 JS
    # -------------------
    js_files = []

    for h in targets_to_use[:5]:
        js = get_js_files(h)
        js_files.extend(js)

    if not js_files:
        js_files = get_passive_js(t)

    js_files = list(set(js_files))[:20]

    new_js = [j for j in js_files if j not in seen_js]

    # -------------------
    # 🔗 ENDPOINTS
    # -------------------
    endpoints = extract_endpoints(js_files)
    endpoints = list(set(endpoints))[:20]

    # 🔥 filtra só endpoints interessantes
    interesting = ["api", "login", "admin", "auth", "v1", "v2"]

    endpoints = [
        e for e in endpoints
        if any(k in e.lower() for k in interesting)
    ]

    new_endpoints = [e for e in endpoints if e not in seen_endpoints]

    # -------------------
    # 🚫 SE NÃO TEM NOVIDADE → SKIP
    # -------------------
    if not new_subs and not new_js and not new_endpoints:
        continue

    # -------------------
    # 🧠 UPDATE HISTORY
    # -------------------
    seen_subs.update(new_subs)
    seen_js.update(new_js)
    seen_endpoints.update(new_endpoints)

    save_history({
        "subs": list(seen_subs),
        "js": list(seen_js),
        "endpoints": list(seen_endpoints)
    })

    # -------------------
    # 📤 OUTPUT LIMPO
    # -------------------
    msg = f"🎯 TARGET: {t}\n\n"
    msg += f"{tag}\n\n"

    if new_subs:
        msg += "🌐 New Subdomains:\n"
        for s in new_subs[:5]:
            msg += f"- {s}\n"

    if new_js:
        msg += "\n🧪 New JS Files:\n"
        for j in new_js[:5]:
            msg += f"- {j}\n"

    if new_endpoints:
        msg += "\n🔗 New Endpoints:\n"
        for e in new_endpoints[:5]:
            msg += f"- {e}\n"

    send(msg)
