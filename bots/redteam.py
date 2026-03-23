import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

from modules.recon_subdomains import get_subdomains
from modules.recon_js import get_js_files
from modules.history import load_history, save_history, gen_id

TOKEN = os.getenv("RED_TOKEN")
CHAT = os.getenv("RED_CHAT")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send(msg):
    requests.post(url, data={"chat_id": CHAT, "text": msg}, timeout=10)


history = load_history()

send("🔴 Recon Bot ON")


with open("targets.txt") as f:
    targets = [line.strip() for line in f]


for t in targets:

    subs = get_subdomains(t)
    js_files = get_js_files(t)

    new_subs = []
    new_js = []

    # -------------------
    # SUBDOMAINS
    # -------------------
    for s in subs:

        uid = gen_id(s)

        if uid in history:
            continue

        new_subs.append(s)
        save_history(uid)

    # -------------------
    # JS
    # -------------------
    for js in js_files:

        uid = gen_id(js)

        if uid in history:
            continue

        new_js.append(js)
        save_history(uid)

    # -------------------
    # OUTPUT ORGANIZADO
    # -------------------

    if not new_subs and not new_js:
        continue

    msg = f"🎯 TARGET: {t}\n\n"

    if new_subs:
        msg += f"🌐 Subdomains ({len(new_subs)} novos)\n"
        for s in new_subs[:5]:
            msg += f"- {s}\n"

    if new_js:
        msg += f"\n🧪 JS ({len(new_js)} encontrados)\n"
        for j in new_js[:5]:
            msg += f"- {j}\n"

    send(msg)
