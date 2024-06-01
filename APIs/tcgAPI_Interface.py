# Author: Yasser Khaloufi

# Summary: Funzioni statiche che fanno da interfaccia con l'API pokemontcg

# ext
import os
import sys
from requests import get
# personali
# ricavo il path della cartella superiore allo script corrente e lo aggiungo a sys
dir_path = os.path.dirname(os.path.realpath(__file__))+"\.."
sys.path.append(dir_path)
from classes.card import Card
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