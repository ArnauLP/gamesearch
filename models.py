#!/usr/bin/env python3

from dataclasses import dataclass

@dataclass
class GameOffer:
    title: str
    price: str
    store: str
    link: str


