import os
import hashlib

HISTORY_FILE = "sent_alerts.txt"


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return set()

    with open(HISTORY_FILE, "r") as f:
        return set(f.read().splitlines())


def save_history(item):
    with open(HISTORY_FILE, "a") as f:
        f.write(item + "\n")


def gen_id(text):
    return hashlib.md5(text.encode()).hexdigest()
