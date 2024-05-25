# Date: 07/02/24
# Author: Yasser Khaloufi

# Summary: Gestisce le interazioni con l'utente (per non scrivere tutto nel main)

from card import *
from tabulate import tabulate
from PIL import Image
from requests import *
from io import BytesIO

def askForPkmnName() -> str:
    return input("Insert Pokemon name:")

def askForID() -> str:
    return input("Insert the ID of the card you want:")

def printCards(cards) -> None:
    [print(card) for card in cards]
        
def printCardsDisplayInfo(cards) -> None:
    print(tabulate([[card.name, card.id, card.set['releaseDate']] for card in cards], headers=['Name', 'ID', 'Release Date']))
    # [print(f"Name:{getattr(card, 'name')} ID:{getattr(card, 'id')}\n") for card in cards]
    
def getCardFromListByID(cards, ID) -> Card:
    for card in cards:
        if card.id == ID:
            return card
        
def displayImage(URL) -> None:
    # Mostro l'immagine con una finestra veloce
    response = get(URL)
    img = Image.open(BytesIO(response.content))
    img.show()