import os
import requests

from modules.cve_exploit import get_exploitable_cves
from modules.pentest_tools import get_new_tools
from modules.apt_campaigns import get_apt_campaigns
from modules.credential_leaks import get_leaks
from modules.malware_c2 import get_c2

TOKEN=os.getenv("INTEL_TOKEN")
CHAT=os.getenv("INTEL_CHAT")

url=f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def send(msg):

    requests.post(url,data={
        "chat_id":CHAT,
        "text":msg
    })


# CVE

for c in get_exploitable_cves():

    send(f"""
🚨 CVE Critical

{c['id']}

{c['desc']}
""")


# Tools

for t in get_new_tools():

    send(f"""
🛠 New Pentest Tool

{t['name']}

{t['url']}
""")


# APT

for a in get_apt_campaigns():

    send(f"""
🎯 APT Campaign

{a['title']}

{a['link']}
""")


# Leaks

for l in get_leaks():

    send(f"""
🔓 Data Breach

{l['name']}

Domain: {l['domain']}
""")


# Malware

for m in get_c2():

    send(f"""
🦠 Malware C2

Family: {m['family']}

Hash: {m['hash']}
""")
