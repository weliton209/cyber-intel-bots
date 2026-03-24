def correlate_ioc_news(iocs, news):

    alerts = []

    keywords_map = {
        "emotet": ["bank", "financial"],
        "trickbot": ["enterprise", "windows"],
        "ransomware": ["ransomware", "attack", "breach"]
    }

    for i in iocs:

        malware = str(i.get("malware", "")).lower()

        for n in news:

            title = n["title"].lower()

            for key, words in keywords_map.items():

                if key in malware and any(w in title for w in words):

                    alerts.append({
                        "ioc": i,
                        "news": n
                    })

    return alerts
