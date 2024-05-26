# Author: Yasser Khaloufi

# Summary: Business class carta pokemon, utilizza un dizionario per gli attributi

# ext
from tabulate import tabulate

class Card:
    
    # Costruttore (il presupposto è che le info della carta arrivino come JSON)
    # Siccome non sempre le chiavi nel JSON sono uguali per ogni città, baso la conservazione degli attributi su un dizionario dinamico
    def __init__(self, data):
        [setattr(self, key, value) for key, value in data.items()]

    def getAllCardMarketPrices(self) -> dict:
        # self.cardmarket['prices'] contiene tutti i prezzi
        # Controlla se 'cardmarket' esiste prima di cercare di accedervi
        if hasattr(self, 'cardmarket'):
            return self.cardmarket['prices']
        else:
            return {}

    def returnTabulatedPricesString(self) -> str:
        """
          La funzione tabulate prende i valori e le intestazioni, ma non accetta direttamente i singoli valori,
          ma ogni una lista di liste, quindi per ogni valore di v devo creare una lista con un solo valore,
          dopodichè inserire tutte queste liste in una lista più grande (infatti uso le quadre per v).
        """
        # .keys e .values restituiscono delle view sul dizionario, non sapendo esattamente come funzionino, converto in liste
        # (la conversione non è esplicita tramite un cast, ma la faccio con una comprehension)
        prices = self.getAllCardMarketPrices()
        if prices != {}:
            headers = [keys for keys, values in prices.items() if values != 0]
            values = [f"{values}$" for values in prices.values() if values != 0]
            return tabulate([values], headers=headers)
        else:
            return "No prices found for this card"
    
        """
            Me del futuro, ricordati di sta roba che ci stavi smattando sopra: 
            quando hai un dizionario puoi ottenere direttamente la lista di valori con .values() e le chiavi con .keys()
        """

    def largeImageURL(self) -> str:
        return self.images['large']

    def __str__(self) -> str:
        str = ''
        for key, value in self.__dict__.items():
            str += f"\t{key}: {value}\n"
        return str