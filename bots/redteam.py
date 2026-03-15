import requests
import os

TOKEN = os.getenv("RED_TOKEN")
CHAT = os.getenv("RED_CHAT")

msg = "🔥 Red Team Update\nNova ferramenta ofensiva detectada no GitHub"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

requests.post(url,data={
    "chat_id": CHAT,
    "text": msg
})
