import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

from modules.recon_subdomains import get_subdomains
from modules.recon_alive import check_alive
from modules.recon_scan import run_scan
from modules.history import load_history, save_history, gen_id

TOKEN = os.getenv("RED_TOKEN")
CHAT = os.getenv("RED_CHAT")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send(msg):
    requests.post(url, data={"chat_id": CHAT, "text": msg}, timeout=15)


history = load_history()

send("🔴 Recon + Scan ON")


with open("targets.txt") as f:
    targets = [line.strip() for line in f]


for t in targets:

    # -------------------
    # SUBDOMAIN DISCOVERY
    # -------------------
    subs = get_subdomains(t)

    if not subs:
        continue

    # -------------------
    # ALIVE CHECK
    # -------------------
    alive = check_alive(subs[:30])  # limita

    if not alive:
        continue

    # -------------------
    # SCAN
    # -------------------
    findings = run_scan(alive[:10])  # limita pra não travar

    new_findings = []

    for fnd in findings:

        uid = gen_id(fnd)

        if uid in history:
            continue

        new_findings.append(fnd)
        save_history(uid)

    # -------------------
    # OUTPUT
    # -------------------
    if not new_findings:
        continue

    msg = f"🎯 TARGET: {t}\n\n"
    msg += "🚨 Findings:\n"

    for fnd in new_findings[:5]:
        msg += f"- {fnd}\n"

    send(msg)
