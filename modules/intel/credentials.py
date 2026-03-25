def is_target_related_loose(text, targets):

    text = (text or "").lower()

    for t in targets:
        t = t.lower()

        if t in text:
            return True

        base = t.split(".")[0]

        if len(base) > 4 and base in text:
            return True

    return False


def is_exploitable(leak):

    data = (leak.get("data") or "").lower()

    if "password" in data:
        return True

    if "hash" in data:
        return True

    return False


def analyze_credential_leak(leak, targets):

    domain = leak.get("domain", "")
    name = leak.get("name", "")

    related = (
        is_target_related_loose(domain, targets)
        or is_target_related_loose(name, targets)
    )

    exploitable = is_exploitable(leak)

    if related and exploitable:
        level = "🔥 CRITICAL"
    elif exploitable:
        level = "⚠️ HIGH"
    elif related:
        level = "🎯 TARGET"
    else:
        level = "ℹ️ LOW"

    return {
        "related": related,
        "exploitable": exploitable,
        "level": level
    }
