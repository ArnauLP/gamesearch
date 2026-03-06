#!/usr/bin/env python3
# pyright: reportUnusedParameter=false, reportUnknownArgumentType=false, reportUnusedCallResult=false, reportAny=false

import requests
from bs4 import BeautifulSoup
from models import GameOffer

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:148.0) Gecko/20100101 Firefox/148.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Cookie": "cookie_notice_accepted=false",
}


def build_url(game: str) -> str:
    slug = game.strip().lower().replace(" ", "-")
    return f"https://www.allkeyshop.com/blog/buy-{slug}-cd-key-compare-prices/"


def parse(soup: BeautifulSoup) -> list[GameOffer]:
    offers: list[GameOffer] = []
    # TODO: find html elements

    for card in soup.select("a.recomended_offers"):
        store_tag = card.find("span", class_="offers-merchant-name")
        price_tag = card.find("div", class_="offers-price")

        if not store_tag or not price_tag:
            continue

        store = store_tag.get_text(strip=True)
        price = price_tag.get_text(strip=True)
        link = str(card.get("href", ""))
        # TODO: resolve links (maybe a flag like --resolve-links ?)
        #link = resolve_link(str(card.get("href", "")))

        offers.append(GameOffer(title="", price=price, store=store, link=link))

    return offers


def resolve_link(url: str) -> str:
    try:
        r = requests.head(url, headers=HEADERS, allow_redirects=True, timeout=5)
        return r.url

    except requests.RequestException:
        return url


def fetch(game: str) -> list[GameOffer] | None:
    url = build_url(game)
    response = requests.get(url, headers=HEADERS)

    # DEBUG
    with open("debug.html", "w") as f:
        f.write(response.text)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    return parse(soup)
