import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

from modules.recon.subdomains import get_subdomains, filter_subdomains
from modules.recon.passive_js import get_js_passive
from modules.recon.endpoints import extract_endpoints

from modules.core.filtering import is_high_value
from modules.core.history import load_history, save_history, gen_id

TOKEN = os.getenv("RED_TOKEN")
CHAT = os.getenv("RED_CHAT")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send(msg):
    try:
        requests.post(url, data={"chat_id": CHAT, "text": msg}, timeout=15)
    except:
        pass


history = load_history()

send("🕶️ Passive Recon ON")


with open("targets.txt") as f:
    targets = [
        line.strip()
        for line in f
        if line.strip() and not line.startswith("#")
    ]


for t in targets:

    subs = get_subdomains(t)
    subs = filter_subdomains(subs)

    subs = [s for s in subs if "@" not in s and "." in s]

    if not subs:
        continue

    # 🔥 PRIORIZA SEM FAZER REQUISIÇÃO
    high_value_targets = [s for s in subs if is_high_value(s)]

    if not high_value_targets:
        high_value_targets = subs[:10]

    # 🔥 JS PASSIVO
    js_files = get_js_passive(t)

    endpoints = []

    if js_files:
        endpoints = extract_endpoints(js_files)[:10]

    uid = gen_id(t + "passive")

    if uid in history:
        continue

    save_history(uid)

    msg = f"🎯 TARGET: {t}\n\n"

    msg += "🔥 Potential Targets:\n"
    for h in high_value_targets[:5]:
        msg += f"- {h}\n"

    if js_files:
        msg += "\n🧪 JS (Passive):\n"
        for j in js_files[:5]:
            msg += f"- {j}\n"

    if endpoints:
        msg += "\n🔗 API Endpoints:\n"
        for e in endpoints:
            msg += f"- {e}\n"

    send(msg)
