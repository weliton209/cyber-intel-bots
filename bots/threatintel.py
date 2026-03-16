import requests
import os

from feeds.apt_feed import get_apt_news
from feeds.exploit_feed import get_exploits
from feeds.malware_feed import get_malware

TOKEN=os.getenv("INTEL_TOKEN")
CHAT=os.getenv("INTEL_CHAT")

url=f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def send(msg):

    requests.post(url,data={
        "chat_id":CHAT,
        "text":msg
    })


# APT / CISA
for news in get_apt_news():

    msg=f"""
🌎 Threat Intel

{news['title']}

{news['link']}
"""
    send(msg)


# Exploits
for e in get_exploits():

    msg=f"""
💣 New Exploit

{e['title']}

{e['link']}
"""
    send(msg)


# Malware
for m in get_malware():

    msg=f"""
🦠 Malware Sample

Family: {m['family']}
Hash: {m['hash']}
"""

    send(msg)
