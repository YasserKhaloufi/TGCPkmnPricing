# Author: Yasser Khaloufi

# Summary: Gestisce le interazioni con l'utente discord (per non scrivere tutto in bot.py)

# ext
from tabulate import tabulate
from requests import *
import asyncio

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
    
async def getInput(bot, ctx, timeout, admittedValues, request, error):
    await ctx.send(request)
    
    def check(received):
        return received.author == ctx.author and received.channel == ctx.channel and received.content in admittedValues

    try:
        user_input = await bot.wait_for('message', check=check, timeout=timeout)
        return user_input.content
    except asyncio.TimeoutError:
        await ctx.send(error)
        return None    