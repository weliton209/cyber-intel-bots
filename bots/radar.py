import os
import requests

TOKEN = os.getenv("INTEL_TOKEN")
CHAT = os.getenv("INTEL_CHAT")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

r = requests.post(url, data={
    "chat_id": CHAT,
    "text": "🚀 Radar TESTE"
})

print(r.text)
