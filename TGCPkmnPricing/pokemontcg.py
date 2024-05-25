# Author: Yasser Khaloufi

# Summary: Static functions that act as an interface to get data from the Pokemon TCG API

from requests import get
from card import *
from secret import POKEMON_KEY

BASE_URL = "https://api.pokemontcg.io/v2"
HEADERS = {"X-Api-Key": POKEMON_KEY}

def getCards() -> list[Card]:
    data = get(f"{BASE_URL}/cards", headers=HEADERS).json()["data"]
    cards = [Card(card) for card in data]
    return cards

def getCardByPkmnName(name) -> list[Card]:
    data = get(f"{BASE_URL}/cards", params={"q": f"name:{name}"}, headers=HEADERS).json()["data"]
    cards = [Card(card) for card in data]
    return cards