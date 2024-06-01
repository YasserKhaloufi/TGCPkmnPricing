# Author: Yasser Khaloufi

# Summary: Definisce il flusso di esecuzione del bot, non che i parametri di configurazione

# ext
import os
import sys
import random
import discord
from discord.ext import commands
# personali
# ricavo il path della cartella superiore allo script corrente e lo aggiungo a sys
dir_path = os.path.dirname(os.path.realpath(__file__))+"\.."
sys.path.append(dir_path)
from APIs.tcgAPI_Interface import *
from discordBot.discordIO import *
from secret import DISCORD_KEY

# il bot deve ricevere eventi relativi ai contenuti dei messaggi.
intents = discord.Intents.default()
intents.message_content = True 

# Creo il bot e ne imposto il prefisso per i comandi a "!"
bot = commands.Bot(command_prefix='!', intents=intents) 

# Predispongo la seguente variabile globale per non dover fetchare tutte la carte da capo ogni volta che il comando random viene usato (fino alla prossima esecuzione), viene inizializzata una volta e poi riciclata (una sorta di singleton)
all_cards = None

# Evento on_ready
@bot.event
async def on_ready():
    print(f'Bot connesso come {bot.user}')

# Mapping comando-funzione stile switch-case (il comando è il nome della funzione asincrona)
# Grazie all'asincronicità il bot può gestire più interazioni contemporaneamente
@bot.command()
async def Get(ctx): # ctx sta per context e contiene tutte le info della conversazione (es. contenuto messaggio)
    pkmnName = ctx.message.content[len(ctx.prefix + ctx.command.name):] # Rimuovi il prefisso del comando dal messaggio (con l'operatore ":" prendo tutta la stringa dopo l'indice indicato)
    cards = getCardByPkmnName(pkmnName.strip())
    
    response = "No card found with that name"
    
    if cards != []:
        response = getCardsDisplayInfo(cards)
        messages = fragmentResponse(response)
        # Invia ogni parte come un messaggio separato
        for message in messages:
            await ctx.send(message)
            
        while 1:
            
            # Chiedi all'utente di scegliere una carta
            cardID = await getInput(bot, ctx, 120.0, [card.id for card in cards], "Insert the ID of the card you want", "Sorry, it took you too long to choose a card")
            
            if cardID is None: # L'utente non ha risposto in tempo, chiudi la conversazione
                break
            else:
                # Trova la carta scelta dall'utente
                chosen_card = next(card for card in cards if card.id == cardID)
                
                # Invia l'immagine della carta ed i prezzi di mercato
                await ctx.send(chosen_card.images['large'])
                await ctx.send("```" + chosen_card.returnTabulatedPricesString() + "```")
                
            # Ripeti lo stesso processo per chiedere all'utente se vuole continuare ad esplorare le carte dello stesso pokemon o meno
            choice = await getInput(bot, ctx, 120.0, ['y', 'n'], "Wanna continue checking on the same pkmn? (y/n)", "Sorry, it took you too long to respond")
            
            if choice is None or choice.lower() == 'n': # chiudi la conversazione
                break
    else:
        await ctx.send(response)
        
@bot.command()
async def Random(ctx):
    global all_cards # Se non lo facessi verrebbe creata una nuova variabile con stesso nome ma con scope limitato a questo blocco
    await ctx.send("This could take a couple seconds...")
    
    # Fetcha tutte le carte solo se non lo sono già state
    if all_cards is None:
        all_cards = getCards()
        
    index = random.randint(0, len(all_cards))
    picked_card = all_cards[index]
    await ctx.send(picked_card.images['large'])
    # Riciclo il metodo getCardsDisplayInfo (che in realtà serve per le liste di carte)
    await ctx.send("```" + getCardsDisplayInfo([picked_card]) + "\n\n" + picked_card.returnTabulatedPricesString() + "```")
    
        
@bot.command()
async def Help(ctx):
    help_message = """
    Hello! I’m your Pokemon card bot. Here’s what I can do:

    - `Get <Pokemon name>`: Search for all cards of the specified Pokemon. After showing the cards, I will ask you to choose a card by entering its ID. Finally, I will post the image and market prices of the chosen card.
    If you do not choose a card within 120 seconds, the conversation will be closed and you will need to send a Get command again
    
    - `Random`: Returns a random pokemon card

    - `Help` Show this help message.

    The commands are case-sensitive and make sure to write the names of the Pokemon correctly!
    """

    await ctx.send(help_message)

# Esegui il bot
bot.run(DISCORD_KEY)
