from scraper import run_all_parsers
from bot import run_bot
import threading
import time

def scheduler():
    while True:
        try:
            run_all_parsers()
        except Exception as e:
            print("Parser error:", e)
        time.sleep(60 * 60 * 6)  # раз в 6 часов

if __name__ == "__main__":
    threading.Thread(target=scheduler, daemon=True).start()
    run_bot()
