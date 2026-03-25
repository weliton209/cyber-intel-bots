import requests
from datetime import datetime


def is_recent(date_str):

    try:
        breach_date = datetime.strptime(date_str, "%Y-%m-%d")
        return breach_date.year >= 2022
    except:
        return False


def get_leaks(limit=10):

    url = "https://haveibeenpwned.com/api/v3/breaches"

    headers = {
        "User-Agent": "intel-bot"
    }

    results = []

    try:
        data = requests.get(url, headers=headers, timeout=10).json()

        for item in data:

            name = item.get("Name")
            domain = item.get("Domain")
            date = item.get("BreachDate")
            data_classes = item.get("DataClasses", [])

            # 🔥 FILTRO: só recentes
            if not is_recent(date):
                continue

            # 🔥 SCORE DE IMPACTO
            score = 0

            if "Passwords" in data_classes:
                score += 3

            if "Email addresses" in data_classes:
                score += 2

            if "Usernames" in data_classes:
                score += 1

            # 🔥 TAG DE RISCO
            if score >= 4:
                risk = "🔥 HIGH"
            elif score >= 2:
                risk = "⚠️ MED"
            else:
                risk = "ℹ️ LOW"

            results.append({
                "name": name,
                "domain": domain,
                "date": date,
                "data": ", ".join(data_classes[:3]),
                "risk": risk
            })

            if len(results) >= limit:
                break

    except:
        return []

    return results
