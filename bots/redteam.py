import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

from modules.recon.subdomains import get_subdomains
from modules.recon.recon_js import get_js_files
from modules.recon.endpoints import extract_endpoints
from modules.recon.passive_js import get_passive_js

from modules.recon.analyzer import (
    classify_endpoint,
    extract_params,
    is_sensitive,
    score_endpoint
)

from modules.core.history import load_history, save_history, gen_id
from modules.core.filtering import is_high_value


TOKEN = os.getenv("RED_TOKEN")
CHAT = os.getenv("RED_CHAT")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send(msg):
    try:
        requests.post(url, data={"chat_id": CHAT, "text": msg}, timeout=15)
    except:
        pass


history = load_history()

send("🔴 Smart Recon PRO ON")


# -------------------
# 📂 TARGETS
# -------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
targets_path = os.path.join(BASE_DIR, "targets.txt")

with open(targets_path) as f:
    targets = [t.strip() for t in f if t.strip()]


# -------------------
# 🔁 LOOP
# -------------------
for t in targets:

    subs = get_subdomains(t)
    subs = list(set(subs))[:20]

    if not subs:
        continue

    high_value = [s for s in subs if is_high_value(s)]

    if high_value:
        targets_to_use = high_value[:10]
        tag = "🔥 HIGH VALUE"
    else:
        targets_to_use = subs[:10]
        tag = "🌐 RECON"

    js_files = []
    endpoints = []

    # JS
    for h in targets_to_use[:5]:
        js = get_js_files(h)
        js_files.extend(js)

    # fallback passivo
    if not js_files:
        js_files = get_passive_js(t)

    js_files = list(set(js_files))[:10]

    if js_files:
        endpoints = extract_endpoints(js_files)[:20]

    # -------------------
    # 🔥 ANALYSIS
    # -------------------
    classified = []
    sensitive = []
    scored = []
    params = extract_params(endpoints)

    for e in endpoints:
        c = classify_endpoint(e)
        s = score_endpoint(e)

        classified.append(f"{c} → {e}")
        scored.append(f"{s} → {c} → {e}")

        if is_sensitive(e):
            sensitive.append(e)

    # -------------------
    # 🧠 HISTORY
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

    if scored:
        msg += "\n🔗 Endpoints (Scored):\n"
        for e in scored[:5]:
            msg += f"- {e}\n"

    if params:
        msg += "\n⚠️ Possible Inputs:\n"
        for p in params[:5]:
            msg += f"- {p}\n"

    if sensitive:
        msg += "\n🚨 Sensitive:\n"
        for s in sensitive[:5]:
            msg += f"- {s}\n"

    send(msg)
