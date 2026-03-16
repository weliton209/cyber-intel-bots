import requests
import os

TOKEN = os.getenv("RED_TOKEN")
CHAT = os.getenv("RED_CHAT")

url = "https://api.github.com/search/repositories?q=pentesting+tool&sort=updated"

data = requests.get(url).json()

for repo in data["items"][:5]:

    name = repo["name"]
    link = repo["html_url"]
    desc = repo["description"]

    msg = f"""
🔥 Red Team Tool

Name: {name}
Desc: {desc}
Repo: {link}
"""

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT, "text": msg}
    )
