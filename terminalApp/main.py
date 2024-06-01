# Author: Yasser Khaloufi

# Summary: Applicazione da terminale per esplorare velocemente le funzionalità dell'interfaccia all'API

# ext
import os
import sys
import random

# personali
# ricavo il path della cartella superiore allo script corrente e lo aggiungo a sys
dir_path = os.path.dirname(os.path.realpath(__file__))+"\.."
sys.path.append(dir_path)
from APIs.tcgAPI_Interface import *
from terminalApp.terminal_IO import *

# Predispongo la seguente variabile globale per non dover fetchare tutte la carte da capo ogni volta che il comando random viene usato (fino alla prossima esecuzione), viene inizializzata una volta e poi riciclata (una sorta di singleton)
all_cards = None

while 1:
    # Clear console
    print("\033c")
    
    choice = None
    while choice not in ['0', '1']:
        choice = input("0 - Search for card by Pokemon name and ID\n1 - Get Random card\n")
    
    if(choice == '0'):
    
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
    else:        
        # Fetcha tutte le carte solo se non lo sono già state
        if all_cards is None:
            all_cards = getCards()
            
        index = random.randint(0, len(all_cards))
        picked_card = all_cards[index]
        
        print(picked_card.returnTabulatedPricesString())
        displayImage(picked_card.largeImageURL())

        
    if(input("\nContinue? (y/n):") != 'y'):
        break
