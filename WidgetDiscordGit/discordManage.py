import requests # type: ignore
import time
from config import (
    DISCORD_APP_ID,
    DISCORD_USER_ID,
    DISCORD_TOKEN
)
from logger import log

URL = (
    f"https://discord.com/api/v9/applications/"
    f"{DISCORD_APP_ID}/users/{DISCORD_USER_ID}/identities/0/profile"
)
HEADERS = {
    "Authorization": f"Bot {DISCORD_TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "DiscordBot"
}

# Etat Discord
last_discord_call = 0
pending_update = None
retry_after = 0

def safe_discord_patch(body):
    global last_discord_call
    global pending_update
    global retry_after
    now = time.time()
    if now < retry_after:
        pending_update = body
        return

    try:
        r = requests.patch(
            URL,
            headers=HEADERS,
            json=body
        )
        if r.status_code == 429:
            retry = r.json().get(
                "retry_after",
                5
            )
            log(
                f"⚠️ 429 Discord → retry dans {retry}s"
            )
            retry_after = now + retry
            pending_update = body
            return
        last_discord_call = now
    except Exception as e:
        log(
            f"Erreur Discord : {e}"
        )
        pending_update = body

def update_discord(game):
    body = {
        "data": {
            "dynamic": [
                {
                    "type": 1,
                    "name": "CurrentGame",
                    "value": game["name"]
                },
                {
                    "type": 1,
                    "name": "Platform",
                    "value": game["platform"]
                },
                {
                    "type": 2,
                    "name": "GameTrophy",
                    "value": game["current"]
                },
                {
                    "type": 2,
                    "name": "MaxGameTrophy",
                    "value": game["total"]
                },
                {
                    "type": 3,
                    "name": "gameImg",
                    "value": {
                        "url": game["image"]
                    }
                },
                {
                    "type": 1,
                    "name": "desc",
                    "value": "In game"
                }
            ]
        }
    }
    safe_discord_patch(body)

def update_idle():
    body = {
        "data": {
            "dynamic": [
                {
                    "type": 1,
                    "name": "CurrentGame",
                    "value": "Waiting for game"
                },
                {
                    "type": 1,
                    "name": "Platform",
                    "value": "None"
                },
                {
                    "type": 2,
                    "name": "GameTrophy",
                    "value": 1
                },
                {
                    "type": 2,
                    "name": "MaxGameTrophy",
                    "value": 1
                },
                {
                    "type": 3,
                    "name": "gameImg",
                    "value": {
                        "url":
                        "https://i.pinimg.com/736x/0e/ce/9f/0ece9f5c572c6015a518f9f4b79b10ee.jpg"
                    }
                },
                {
                    "type": 1,
                    "name": "desc",
                    "value": "Not in game"
                }
            ]
        }
    }
    safe_discord_patch(body)

def retry_pending():
    global pending_update
    global retry_after
    if pending_update and time.time() >= retry_after:
        body = pending_update
        pending_update = None
        safe_discord_patch(body)
