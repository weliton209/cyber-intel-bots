import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

from modules.recon_subdomains import get_subdomains
from modules.recon_js import get_js_files
from modules.cve_exploit import get_exploitable_cves
from modules.credential_leaks import get_leaks
from modules.history import load_history, save_history, gen_id

TOKEN = os.getenv("RED_TOKEN")
CHAT = os.getenv("RED_CHAT")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send(msg):
    requests.post(url, data={"chat_id": CHAT, "text": msg}, timeout=10)


history = load_history()

send("🔴 Recon Bot ON")

# -------------------
# LOAD TARGETS
# -------------------

with open("targets.txt") as f:
    targets = [line.strip() for line in f]


# -------------------
# SUBDOMAINS
# -------------------

for t in targets:

    subs = get_subdomains(t)

    for s in subs[:10]:

        uid = gen_id(s)

        if uid in history:
            continue

        send(f"🌐 New Subdomain\n{s}")
        save_history(uid)


# -------------------
# JS FILES
# -------------------

for t in targets:

    js_files = get_js_files(t)

    for js in js_files:

        uid = gen_id(js)

        if uid in history:
            continue

        send(f"🧪 JS Found\n{js}")
        save_history(uid)


# -------------------
# CVE
# -------------------

for c in get_exploitable_cves():

    uid = gen_id(c["id"])

    if uid in history:
        continue

    send(f"🔥 CVE Exploitable\n{c['id']}")
    save_history(uid)


# -------------------
# LEAKS
# -------------------

for l in get_leaks():

    uid = gen_id(l["name"])

    if uid in history:
        continue

    send(f"🔓 Leak Target\n{l['name']}\n{l['domain']}")
    save_history(uid)
