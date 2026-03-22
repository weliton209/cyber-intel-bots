import requests
import re

def get_js_files(domain):

    try:
        r = requests.get(f"https://{domain}", timeout=10).text
    except:
        return []

    js_files = re.findall(r'src="(.*?\.js)"', r)

    return js_files
