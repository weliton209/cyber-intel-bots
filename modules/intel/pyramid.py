def classify_intel(item):

    text = str(item).lower()

    # 🔺 TTP (TOP - mais importante)
    if any(k in text for k in [
        "privilege escalation",
        "lateral movement",
        "credential dumping",
        "cobalt strike",
        "exploitation",
        "rce",
        "zero-day"
    ]):
        return "🔺 TTP", 5

    # 🔺 TOOLS
    if any(k in text for k in [
        "mimikatz",
        "metasploit",
        "cobalt strike",
        "empire",
        "sliver"
    ]):
        return "🛠 TOOL", 4

    # 🔺 APT / CAMPAIGN
    if any(k in text for k in [
        "apt",
        "campaign",
        "threat actor"
    ]):
        return "🎯 APT", 4

    # ⚠️ DOMAIN
    if "http" in text or "domain" in text:
        return "🌐 DOMAIN", 2

    # ⚠️ IP
    if "ip" in text:
        return "🌐 IP", 1

    # ⚠️ HASH
    if "hash" in text:
        return "🧬 HASH", 1

    return "ℹ️ LOW", 0
