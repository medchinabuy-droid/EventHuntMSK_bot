import requests
from bs4 import BeautifulSoup
from sheets import append_event, get_all_uids
from dedup import make_uid

HEADERS = {"User-Agent": "Mozilla/5.0"}

def determine_status(text):
    t = text.lower()
    if "бесплат" in t or "free" in t:
        return "Бесплатно"
    if "промо" in t or "promo" in t or "скид" in t:
        return "Промо"
    return "Платно"

def save_event(date, title, link, source, tags=""):
    uid = make_uid(title, date, link)
    existing = get_all_uids()
    if uid in existing:
        return

    append_event([
        date, "", title, "событие", "Москва", "",
        determine_status(title), "", "", link,
        source, tags, "нет", uid
    ])

def parse_generic(url, source, card_selector, title_sel, link_sel):
    r = requests.get(url, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    cards = soup.select(card_selector)
    for c in cards:
        try:
            title = c.select_one(title_sel).text.strip()
            link = c.select_one(link_sel)["href"]
            save_event("", title, link, source)
        except:
            pass

def parse_timepad():
    parse_generic(
        url="https://timepad.ru/events/moscow/",
        source="timepad",
        card_selector=".event-card",
        title_sel=".event-card__title",
        link_sel="a"
    )

def run_all_parsers():
    parse_timepad()
    # сюда легко добавлять новые источники
