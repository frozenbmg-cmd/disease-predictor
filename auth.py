import json
import os

USERS_FILE = "users.json"
HISTORY_FILE = "history.json"

# ---------------- CREATE FILES ----------------
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump({}, f)

# ---------------- REGISTER ----------------
def register(username, password):

    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    if username in users:
        return False

    users[username] = password

    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

    return True

# ---------------- LOGIN ----------------
def login(username, password):

    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    return users.get(username) == password

# ---------------- SAVE HISTORY ----------------
def save_history(username, data):

    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)

    if username not in history:
        history[username] = []

    history[username].append(data)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

# ---------------- GET HISTORY ----------------
def get_history(username):

    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)

    return history.get(username, [])
