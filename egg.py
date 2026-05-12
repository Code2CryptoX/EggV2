#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
══════════════════════════════════════
        Code2Crypto - Egg Hatch Bot
         Developed By Anaik_Dev
══════════════════════════════════════
"""

import requests
import time
import os
from datetime import datetime

# ==========================================
# COLORS
# ==========================================
C = "\033[96m"   # Cyan
G = "\033[92m"   # Green
W = "\033[97m"   # White
B = "\033[94m"   # Blue
R = "\033[91m"   # Red
X = "\033[0m"    # Reset

# ==========================================
# SIMPLE BANNER
# ==========================================
BANNER = f"""{G}
╔══════════════════════════════════════╗
║         CODE2CRYPTO OFFICIAL        ║
║            EGG HATCH BOT            ║
║         Developed By Anaik_Dev      ║
╚══════════════════════════════════════╝
{X}"""

# ==========================================
# UTILITIES
# ==========================================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def log(msg, color=W):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"{C}[{now}] {color}{msg}{X}")

def line():
    print(f"{B}══════════════════════════════════════════════{X}")

# ==========================================
# ACCOUNT SUMMARY
# ==========================================
def get_summary(token):

    url = "https://forum-defend-expiration-holdem.trycloudflare.com/api/eggs/summary"

    headers = {
        "authorization": f"Bearer {token}",
        "user-agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            return False

        data = response.json()

        if data.get("ok"):

            balance = data.get("balance", 0)

            print(f"""
{G}╔══════════════════════════════════════╗
║         ACCOUNT INFORMATION          ║
╠══════════════════════════════════════╣
║   🥚 Balance : {balance} Eggs
╚══════════════════════════════════════╝{X}
""")

            return True

        return False

    except Exception as e:

        log(f"Summary Error : {e}", R)
        return False

# ==========================================
# TASK RUNNER
# ==========================================
def run_task_batch(token, provider):

    url = "https://forum-defend-expiration-holdem.trycloudflare.com/api/tasks/claim-ad"

    headers = {
        "authorization": f"Bearer {token}",
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0"
    }

    line()
    log(f"Starting {provider.upper()} Tasks", G)
    line()

    for slot in range(20):

        watch_start = int(time.time() * 1000)

        log(f"Watching Ad Slot {slot}", W)

        time.sleep(17)

        payload = {
            "type": provider,
            "clicked": True,
            "slot_index": slot
        }

        if provider == "adsgram":
            payload["watch_start_ms"] = watch_start

        try:

            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=20
            )

            data = response.json()

            if data.get("ok"):

                balance = data.get("balance", "Unknown")

                print(f"{G}✔ Slot {slot} Completed | Balance : {balance}{X}")

            elif data.get("code") == "SLOT_ALREADY_CLAIMED":

                print(f"{B}➜ Slot {slot} Already Claimed{X}")

            else:

                print(f"{R}❌ Failed Slot {slot}{X}")

        except Exception as e:

            print(f"{R}❌ Connection Error On Slot {slot}{X}")

        time.sleep(1)

# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":

    clear()
    print(BANNER)

    line()

    auth_input = input(f"{C}➤ Paste Authorization Token : {X}").strip()

    if auth_input.startswith("Bearer "):
        auth_input = auth_input.replace("Bearer ", "")

    line()

    if get_summary(auth_input):

        run_task_batch(auth_input, "adsgram")
        run_task_batch(auth_input, "monetag")

        line()
        print(f"{G}✔ ALL TASKS COMPLETED SUCCESSFULLY{X}")
        line()

    else:

        print(f"{R}❌ Invalid Token!{X}")

    input(f"\n{W}Press Enter To Exit...{X}")
