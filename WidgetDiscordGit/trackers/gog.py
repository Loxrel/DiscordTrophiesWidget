import sqlite3
import os
import psutil # type: ignore
import json
from logger import log

# Find GOG database
def find_gog_database():
    paths = [
        r"C:\ProgramData\GOG.com\Galaxy\storage\galaxy-2.0.db",
        r"C:\ProgramData\GOG.com\Galaxy\storage\galaxy.db"
    ]
    for path in paths:
        if os.path.exists(path):
            log(
                f"GOG database found : {path}"
            )
            return path
    log(
        "GOG database not found"
    )
    return None
GOG_DB = find_gog_database()

# Get installed GOG executables
def get_gog_executables():
    if not GOG_DB:
        return []
    games = []
    try:
        conn = sqlite3.connect(GOG_DB)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 
                GameFiles.installPath,
                LimitedDetails.title,
                LimitedDetails.images,
                GameFiles.productId,
                'gog_' || GameFiles.productId
            FROM GameFiles
            JOIN LimitedDetails
            ON GameFiles.productId = LimitedDetails.productId
            WHERE GameFiles.installPath LIKE '%.exe'
            """
        )
        for path, title, images, product_id, release_key in cursor.fetchall():
            image_url = ""
            try:
                data = json.loads(images)
                image_url = data.get(
                    "background",
                    ""
                )
            except Exception:
                pass
            games.append({
                "exe": os.path.basename(path).lower(),
                "name": title,
                "productId": product_id,
                "releaseKey": release_key,
                "image": image_url
            })
        conn.close()
    except Exception as e:
        log(
            f"GOG database error : {e}"
        )
    return games

# Get running processes
def get_running_processes():
    processes = []
    for process in psutil.process_iter(
        ["name"]
    ):
        try:
            if process.info["name"]:
                processes.append(
                    process.info["name"].lower()
                )
        except:
            pass
    return processes

# Get GOG achievements
def get_achievements(game_release_key):
    if not GOG_DB:
        return 0, 0
    try:
        conn = sqlite3.connect(GOG_DB)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM Achievements
            WHERE gameReleaseKey = ?
            """,
            (game_release_key,)
        )
        total = cursor.fetchone()[0]
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM UserAchievements
            WHERE gameReleaseKey = ?
            AND isUnlocked = 1
            """,
            (game_release_key,)
        )
        unlocked = cursor.fetchone()[0]
        conn.close()
        return unlocked, total
    except Exception as e:
        log(
            f"GOG achievement error : {e}"
        )
        return 0, 0

# Detect current GOG game
def get_game():
    games = get_gog_executables()
    running = get_running_processes()
    for game in games:
        if game["exe"] in running:
            current, total = get_achievements(
                game["releaseKey"]
            )
            return {
                "platform": "GOG",
                "name": game["name"],
                "current": current,
                "total": total,
                "image": game["image"]
            }
    return None
