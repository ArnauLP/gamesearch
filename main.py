#!/usr/bin/env python3
# pyright: reportUnusedParameter=false, reportUnknownArgumentType=false, reportUnusedCallResult=false, reportAny=false

import argparse
import signal, sys, types
from termcolor import colored
from scraper import fetch

def def_handler(sig: int, frame: types.FrameType | None) -> None:
    print(colored("Exiting...\n", "red"))
    sys.exit(1)


_ = signal.signal(signal.SIGINT, def_handler)

if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(
        description="Search game prices fast through your terminal.\n"
    )
    parser.add_argument("query", help="Game title to search")
    parser.add_argument(
        "--plataform",
        choices=["steam", "epic", "gog"],
        help="Filter by plataform (steam, epic, gog...)",
        default=None,
    )

    args = parser.parse_args()

    print(f"Searching for: {args.query.capitalize()}\n")

    offers = fetch(args.query)

    if offers is None:
        print(colored("[-] Game not found or request failed.", "red"))
        sys.exit(1)

    for offer in offers:
        print(offer)


