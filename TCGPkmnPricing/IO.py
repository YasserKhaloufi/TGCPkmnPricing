# Author: Yasser Khaloufi

# Summary: Gestisce le interazioni con l'utente (per non scrivere tutto nel main)

from card import *
from tabulate import tabulate
from PIL import Image
from requests import *
from io import BytesIO

# TERMINALE
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
    
# DISCORD
def getCardsDisplayInfo(cards) -> str:
    str = tabulate([[card.name, card.id, card.set['releaseDate']] for card in cards], headers=['Name', 'ID', 'Release Date'])
    return str
    
# Per gestione limite 2000 caratteri per messaggio
def fragmentResponse(response) -> list[str]:
    # Suddividi il messaggio in righe
    lines = response.split('\n')
    
    # Crea una lista per contenere i vari messaggi
    messages = []
    message = "```" # Inizia ogni messaggio con backticks
    
    # Aggiungi righe al messaggio corrente finché non raggiungi il limite di 2000 caratteri
    for line in lines:
        # Se aggiungendo una nuova riga al messaggio superi i 2000 caratteri
        if len(message) + len(line) + 4 > 2000:  # (+1 per il carattere '\n', + 3 per il backticks)
            # Allora fermati e inizia a costruire il prossimo
            message += "```" # Chiudi il messaggio corrente
            messages.append(message) 
            message = "```"
        message += line + "\n"

    # Aggiungi l'ultima parte del messaggio se non è vuota (per quando sono finite le linee, ma l'ultima rimane fuori)
    if message:
        message += "```"  # Chiudi l'ultimo messaggio con backticks
        messages.append(message)
        
    return messages
            
    """ 
        Perchè i backticks?
        Discord utilizza un font monospazio per il testo formattato come codice (racchiuso tra backticks), ma per il testo normale utilizza un font proporzionale, in cui diversi caratteri possono avere larghezze diverse, questo mi dava problemi con l'allineamento del testo (gli spazi vuoti apparivano su discord meno larghi rispetto a come li vedevo in debugging) in sintesi, in una normale chat di discord era praticamente illeggibile (i vari campi erano sfasati).
        Il workaround è l'uso del formato di codice di Discord, abilitato nel momento in cui il messaggio è racchiuso tra ```.
    """