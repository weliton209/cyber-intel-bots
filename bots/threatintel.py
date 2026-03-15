import requests
import os

TOKEN=os.getenv("INTEL_TOKEN")
CHAT=os.getenv("INTEL_CHAT")

msg="🌎 Threat Intelligence Update\nNova campanha APT detectada"

requests.post(
f"https://api.telegram.org/bot{TOKEN}/sendMessage",
data={"chat_id":CHAT,"text":msg}
)
