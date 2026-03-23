def is_valid_finding(finding):

    # ❌ ignora lixo comum
    blacklist = [
        "info",
        "tech-detect",
        "favicon",
        "robots.txt",
        "missing security headers"
    ]

    for b in blacklist:
        if b in finding.lower():
            return False

    return True
