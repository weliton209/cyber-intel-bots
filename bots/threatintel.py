import feedparser
import requests
import os

TOKEN = os.getenv("INTEL_TOKEN")
CHAT = os.getenv("INTEL_CHAT")

feed = feedparser.parse("https://feeds.feedburner.com/TheHackersNews")

for entry in feed.entries[:5]:

    title = entry.title
    link = entry.link

    msg = f"""
🌎 Threat Intelligence

{title}

Read more:
{link}
"""

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT, "text": msg}
    )
