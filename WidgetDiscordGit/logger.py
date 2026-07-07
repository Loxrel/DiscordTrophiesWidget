from datetime import datetime


def log(msg):

    now = datetime.now().strftime("%H:%M:%S")

    print(f"[{now}] {msg}")