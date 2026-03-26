import os
import json

FILE = "recon_history.json"


def load_recon_history():
    if not os.path.exists(FILE):
        return {
            "subs": [],
            "js": [],
            "endpoints": []
        }

    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "subs": [],
            "js": [],
            "endpoints": []
        }


def save_recon_history(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)
