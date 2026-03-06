#!/usr/bin/env python3
# pyright: reportUnusedParameter=false, reportUnknownArgumentType=false, reportUnusedCallResult=false, reportAny=false

import requests
from urllib.parse import urlencode
from termcolor import colored
import json

# Globals
APP_ID = "QKNHP8TC3Y"
API_KEY = "4813969db52fc22897f8b84bac1299ad"

URL = "https://qknhp8tc3y-dsn.algolia.net/1/indexes/produits_es_spotlighted_desc/query"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:148.0) Gecko/20100101 Firefox/148.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "Origin": "https://www.instant-gaming.com",
    "Referer": "https://www.instant-gaming.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Te": "trailers",
}

PARAMS = {
    "x-algolia-application-id": APP_ID,
    "x-algolia-api-key": API_KEY,
}


def get_payload(query: str, hits_per_page: int = 15) -> dict[str, str]:
    algolia_params = {
        "query": query,
        "hitsPerPage": hits_per_page,
    }
    return {"params": urlencode(algolia_params)}


def fetch_ig(game: str) -> dict[str, str] | None:
    payload = get_payload(game.strip().lower())

    try:
        r = requests.post(URL, headers=HEADERS, params=PARAMS, json=payload, timeout=10)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(colored(f"Instant Gaming request failed: {e}", "red"))
        return None

    try:
        data = r.json()
    except ValueError:
        print(colored("Instant Gaming returned invalid JSON", "red"))
        return None

    return data


def get_offers(data: dict[str, str], game: str):
    print()

if __name__ == "__main__":
    # FOR TESTING
    game = "Resident evil requiem"
    data = fetch_ig(game)
    print(json.dumps(data, indent=4, ensure_ascii=False))
