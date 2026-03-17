import feedparser

def get_apt_campaigns():

    feed="https://www.cisa.gov/cybersecurity-advisories/all.xml"

    data=feedparser.parse(feed)

    campaigns=[]

    for entry in data.entries[:5]:

        campaigns.append({
            "title":entry.title,
            "link":entry.link
        })

    return campaigns
