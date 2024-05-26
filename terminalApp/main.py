# Author: Yasser Khaloufi

# Summary: Applicazione da terminale per esplorare velocemente le funzionalità dell'interfaccia all'API

# personali
from ..APIs.tcgAPI_Interface import getCardByPkmnName
from ..terminalApp.terminal_IO import *

while 1:
    # Clear console
    print("\033c")
    cards = getCardByPkmnName(askForPkmnName())
    found = False # Sentinella

    if cards == []:
        print("No cards found with that name")
    else:
        found = True
        printCardsDisplayInfo(cards)
        
    while found:    
        while 1:
            print("\n")
            card = getCardFromListByID(cards, askForID())
            print("\n")
            
            if card == None:
                print("\nNo card found with that ID\n")
            else:
                break
            
        print(card.returnTabulatedPricesString())
        displayImage(card.largeImageURL())
        
        if(input("\nWanna continue checking on the same pkmn? (y/n): ") != 'y'):
            break
        
    if(input("\nContinue? (y/n):") != 'y'):
        break
