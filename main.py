from scraper import run_all_parsers
from bot import run_bot
import threading, time

def scheduler():
    while True:
        run_all_parsers()
        time.sleep(60 * 60 * 4)  # каждые 4 часа

if __name__ == "__main__":
    threading.Thread(target=scheduler, daemon=True).start()
    run_bot()
