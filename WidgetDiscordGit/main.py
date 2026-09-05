import time

from logger import log

from trackers import steam, gog

from discordManage import (
    update_discord,
    update_idle,
    retry_pending
)


trackers = [
    steam,
    gog
]


last_game = None
last_progress = None
is_idle = False


log("Starting Game Tracker...")


while True:

    current_game = None

    for tracker in trackers:

        game = tracker.get_game()

        if game:

            current_game = game

            break

    # IDLE

    if current_game is None:

        if not is_idle:

            log(
                "No Game Detected → idle"
            )
            log(
                "Sending Idle profile to Discord"
            )

            update_idle()

            is_idle = True

            last_game = None

            last_progress = None

    # GAME

    else:

        is_idle = False

        progress = (
            f"{current_game['current']}/"
            f"{current_game['total']}"
        )

        if (

            current_game["name"] != last_game

            or progress != last_progress

        ):

            log(

                f"{current_game['platform']} : "
                f"{current_game['name']} "
                f"- {progress}"

            )

            log(
                f"Sending Discord update : {game['name']}"
            )

            update_discord(
                current_game
            )

            last_game = current_game["name"]

            last_progress = progress

    retry_pending()

    time.sleep(0.5)
