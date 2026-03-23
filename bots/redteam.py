import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

from modules.recon_subdomains import get_subdomains
from modules.recon_alive import check_alive
from modules.recon_scan import run_scan
from modules.recon_js import get_js_files
from modules.recon_endpoints import extract_endpoints
from modules.filtering import is_valid_finding, is_high_value
from modules.history import load_history, save_history, gen_id

TOKEN = os.getenv("RED_TOKEN")
CHAT = os.getenv("RED_CHAT")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send(msg):
    requests.post(url, data={"chat_id": CHAT, "text": msg}, timeout=15)


history = load_history()

send("🔴 Smart Recon + Fallback ON")


with open("targets.txt") as f:
    targets = [line.strip() for line in f]


for t in targets:

    subs = get_subdomains(t)
    subs = filter_subdomains(subs)

    if not subs:
        continue

    alive = check_alive(subs[:30])

    if not alive:
        continue

    high_value_targets = [a for a in alive if is_high_value(a)]

    if not high_value_targets:
        continue

    # -------------------
    # SCAN
    # -------------------
    findings = run_scan(high_value_targets[:10])

    valid_findings = []

    for fnd in findings:

        if not is_valid_finding(fnd):
            continue

        uid = gen_id(fnd)

        if uid in history:
            continue

        valid_findings.append(fnd)
        save_history(uid)

    # -------------------
    # SE TEM VULN → PRIORIDADE
    # -------------------
    if valid_findings:

        msg = f"🎯 TARGET: {t}\n\n🚨 HIGH VALUE FINDINGS:\n\n"

        for fnd in valid_findings[:5]:
            msg += f"- {fnd}\n"

        send(msg)
        continue

    # -------------------
    # 🔥 FALLBACK (SEM VULN)
    # -------------------

    js_files = []
    endpoints = []

    for h in high_value_targets[:5]:
        js = get_js_files(h)
        js_files.extend(js)

    js_files = list(set(js_files))[:5]

    if js_files:
        endpoints = extract_endpoints(js_files)[:5]

    # evita repetir fallback
    uid = gen_id(t + "fallback")

    if uid in history:
        continue

    save_history(uid)

    msg = f"🎯 TARGET: {t}\n\n"
    msg += "⚠️ No vuln found — Recon data:\n\n"

    msg += "🔥 High Value Targets:\n"
    for h in high_value_targets[:5]:
        msg += f"- {h}\n"

    if js_files:
        msg += "\n🧪 JS Files:\n"
        for j in js_files:
            msg += f"- {j}\n"

    if endpoints:
        msg += "\n🔗 API Endpoints:\n"
        for e in endpoints:
            msg += f"- {e}\n"

    send(msg)
