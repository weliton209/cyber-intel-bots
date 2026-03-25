import re

def classify_endpoint(e):

    e = e.lower()

    if any(x in e for x in ["login", "auth", "token"]):
        return "🔐 AUTH"

    if any(x in e for x in ["admin", "dashboard"]):
        return "👑 ADMIN"

    if any(x in e for x in ["user", "account", "profile"]):
        return "👤 USER"

    if any(x in e for x in ["log", "debug"]):
        return "📜 LOGS"

    if any(x in e for x in ["metric", "health", "status"]):
        return "📊 METRICS"

    if any(x in e for x in ["api", "v1", "v2"]):
        return "🔗 API"

    return "🌐 OTHER"


def extract_params(endpoints):

    params = []

    for e in endpoints:
        if re.search(r"(id=|user=|token=|auth=|key=|email=)", e.lower()):
            params.append(e)

    return list(set(params))


def is_sensitive(e):

    keywords = [
        "admin", "internal", "debug", "test",
        "dev", "staging", "private", "backup"
    ]

    return any(k in e.lower() for k in keywords)


def score_endpoint(e):

    e = e.lower()
    score = 0

    if "admin" in e: score += 3
    if "auth" in e: score += 3
    if "user" in e: score += 2
    if "api" in e: score += 1
    if "log" in e: score += 2

    if score >= 5:
        return "🔥 HIGH"
    elif score >= 3:
        return "⚠️ MED"
    else:
        return "ℹ️ LOW"
