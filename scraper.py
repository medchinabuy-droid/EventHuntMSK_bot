import requests
from bs4 import BeautifulSoup
from sheets import append_event
from datetime import datetime

HEADERS = {"User-Agent": "Mozilla/5.0"}

def normalize_date(date_str):
    # TODO: привести даты разных сайтов к формату YYYY-MM-DD
    return date_str

def determine_status(text):
    t = text.lower()
    if "бесплат" in t or "free" in t:
        return "Бесплатно"
    if "промо" in t or "promo" in t or "скид" in t:
        return "Промо"
    return "Платно"

def parse_timepad_moscow():
    url = "https://timepad.ru/events/moscow/"
    r = requests.get(url, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    events = soup.select(".event-card")  # селекторы нужно уточнять под реальную разметку

    for e in events:
        try:
            title = e.select_one(".event-card__title").text.strip()
            date = normalize_date(e.select_one(".event-card__date").text.strip())
            link = "https://timepad.ru" + e.select_one("a")["href"]
            price_text = e.text
            status = determine_status(price_text)

            append_event([
                date,
                "",
                title,
                "ивент",
                "Москва",
                "",
                status,
                "",
                "",
                link,
                "timepad",
                "нетворкинг",
                "нет"
            ])
        except Exception as ex:
            print("TimePad parse error:", ex)

def parse_kudago():
    url = "https://kudago.com/msk/events/"
    r = requests.get(url, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    cards = soup.select(".post-card")
    for c in cards:
        try:
            title = c.select_one(".post-card-title").text.strip()
            link = "https://kudago.com" + c.select_one("a")["href"]
            date = normalize_date(c.text)
            status = determine_status(c.text)

            append_event([
                date,
                "",
                title,
                "событие",
                "Москва",
                "",
                status,
                "",
                "",
                link,
                "kudago",
                "ивенты",
                "нет"
            ])
        except Exception as ex:
            print("KudaGo parse error:", ex)

def run_all_parsers():
    parse_timepad_moscow()
    parse_kudago()
