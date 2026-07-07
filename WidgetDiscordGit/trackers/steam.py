import requests
import time

from config import (
    STEAM_API_KEY,
    STEAM_ID
)


def get_game():


    url = (
        "https://api.steampowered.com/ISteamUser/"
        "GetPlayerSummaries/v2/"
        f"?key={STEAM_API_KEY}&steamids={STEAM_ID}"
    )


    r = requests.get(url).json()


    players = (
        r.get("response", {})
        .get("players", [])
    )


    if not players:

        return None



    player = players[0]


    if "gameid" not in player:

        return None



    appid = player["gameid"]


    unlocked, total = get_achievements(appid)



    return {

        "platform": "Steam",

        "name": player.get(
            "gameextrainfo",
            "Unknown Game"
        ),

        "current": unlocked,

        "total": total,

        "image": get_game_image(appid)

    }




def get_achievements(appid):


    url = (

        "https://api.steampowered.com/"
        "ISteamUserStats/GetPlayerAchievements/v1/"
        f"?key={STEAM_API_KEY}"
        f"&steamid={STEAM_ID}"
        f"&appid={appid}"

    )


    r = requests.get(url).json()


    achievements = (

        r.get("playerstats", {})
        .get("achievements", [])

    )


    if not achievements:

        return 0, 0



    unlocked = sum(

        1 for a in achievements

        if a.get("achieved") == 1

    )


    return unlocked, len(achievements)





def get_game_image(appid):


    return (

        "https://cdn.cloudflare.steamstatic.com/"
        f"steam/apps/{appid}/header.jpg"
        f"?t={int(time.time())}"

    )