# Date: 07/02/24
# Author: Yasser Khaloufi

from pokemontcg import *
from IO import *

while 1:
    # Clear console
    print("\033c")
    cards = getCardByPkmnName(askForPkmnName())

    if cards == []:
        print("No cards found with that name")
    else:
        printCardsDisplayInfo(cards)
        
    while 1:    
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
        
    input("\n--Press Enter to continue...")
