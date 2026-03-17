
import requests

def get_leaks():

    url="https://haveibeenpwned.com/api/v3/breaches"

    headers={
        "user-agent":"intel-bot"
    }

    r=requests.get(url,headers=headers)

    data=r.json()

    leaks=[]

    for breach in data[:5]:

        leaks.append({
            "name":breach["Name"],
            "domain":breach["Domain"]
        })

    return leaks
