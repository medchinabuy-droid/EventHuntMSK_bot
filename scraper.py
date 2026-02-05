import requests
from bs4 import BeautifulSoup
from sheets import append_event

def determine_status(text):
    t = text.lower()
    if "бесплат" in t:
        return "Бесплатно"
    if "промо" in t or "promo" in t:
        return "Промо"
    return "Платно"

def parse_example():
    url = "https://example.com/events"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")

    for e in soup.select(".event"):
        title = e.select_one(".title").text.strip()
        date = e.select_one(".date").text.strip()
        price = e.select_one(".price").text.strip()
        link = e.select_one("a")["href"]
        status = determine_status(price)

        append_event([date, title, "Москва", status, price, link, "example.com"])
