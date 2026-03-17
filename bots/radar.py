import os
import requests

from modules.cve_exploit import get_exploitable_cves
from modules.pentest_tools import get_new_tools
from modules.apt_campaigns import get_apt_campaigns
from modules.credential_leaks import get_leaks
from modules.malware_c2 import get_c2


TOKEN = os.getenv("INTEL_TOKEN")
CHAT = os.getenv("INTEL_CHAT")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

HISTORY_FILE = "sent_alerts.txt"


# -------------------
# TELEGRAM SEND
# -------------------

def send(msg):

    try:

        requests.post(
            url,
            data={
                "chat_id": CHAT,
                "text": msg
            },
            timeout=10
        )

    except Exception as e:

        print("Telegram error:", e)


# -------------------
# HISTORY SYSTEM
# -------------------

def load_history():

    if not os.path.exists(HISTORY_FILE):
        return set()

    with open(HISTORY_FILE, "r") as f:
        return set(f.read().splitlines())


def save_history(item):

    with open(HISTORY_FILE, "a") as f:
        f.write(item + "\n")


history = load_history()


# TEST MESSAGE

send("✅ Radar started")


# -------------------
# CVE ALERTS
# -------------------

try:

    for c in get_exploitable_cves():

        if c["id"] in history:
            continue

        send(f"""
🚨 CVE Critical

{c['id']}

{c['desc']}
""")

        save_history(c["id"])

except Exception as e:

    print("CVE module error:", e)


# -------------------
# NEW PENTEST TOOLS
# -------------------

try:

    for t in get_new_tools():

        if t["url"] in history:
            continue

        send(f"""
🛠 New Pentest Tool

{t['name']}

{t['url']}
""")

        save_history(t["url"])

except Exception as e:

    print("Tools module error:", e)


# -------------------
# APT CAMPAIGNS
# -------------------

try:

    for a in get_apt_campaigns():

        if a["title"] in history:
            continue

        send(f"""
🎯 APT Campaign

{a['title']}

{a['link']}
""")

        save_history(a["title"])

except Exception as e:

    print("APT module error:", e)


# -------------------
# DATA BREACHES
# -------------------

try:

    for l in get_leaks():

        if l["name"] in history:
            continue

        send(f"""
🔓 Data Breach

{l['name']}

Domain: {l['domain']}
""")

        save_history(l["name"])

except Exception as e:

    print("Leak module error:", e)


# -------------------
# MALWARE C2
# -------------------

try:

    for m in get_c2():

        if m["hash"] in history:
            continue

        send(f"""
🦠 Malware C2

Family: {m['family']}

Hash: {m['hash']}
""")

        save_history(m["hash"])

except Exception as e:

    print("Malware module error:", e)
