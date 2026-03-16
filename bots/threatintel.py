import requests
import os
import feedparser

TOKEN = os.getenv("INTEL_TOKEN")
CHAT = os.getenv("INTEL_CHAT")

def send(msg):

    url=f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(url,data={
        "chat_id":CHAT,
        "text":msg
    })


# -------------------
# APT / Threat News
# -------------------

feeds=[
"https://www.cisa.gov/cybersecurity-advisories/all.xml",
"https://feeds.feedburner.com/TheHackersNews"
]

for f in feeds:

    data=feedparser.parse(f)

    for entry in data.entries[:3]:

        msg=f"""
🌎 Threat Intel

{entry.title}

{entry.link}
"""

        send(msg)


# -------------------
# Exploits
# -------------------

exp=feedparser.parse("https://www.exploit-db.com/rss.xml")

for e in exp.entries[:3]:

    msg=f"""
💣 New Exploit

{e.title}

{e.link}
"""

    send(msg)


# -------------------
# Malware
# -------------------

try:

    url="https://mb-api.abuse.ch/api/v1/"

    payload={"query":"get_recent"}

    r=requests.post(url,data=payload)

    data=r.json()

    for sample in data["data"][:3]:

        msg=f"""
🦠 Malware Sample

Family: {sample["signature"]}
Hash: {sample["sha256_hash"]}
"""

        send(msg)

except:

    send("⚠ Malware feed error")
