# ext
import discord
from discord.ext import commands
import asyncio

# personali
from tcgAPI_Interface import getCardByPkmnName
from secret import DISCORD_KEY
from IO import getCardsDisplayInfo
from IO import fragmentResponse


# il bot deve ricevere eventi relativi ai contenuti dei messaggi.
intents = discord.Intents.default()
intents.message_content = True 

# Creo il bot e ne imposto il prefisso per i comandi a "!"
bot = commands.Bot(command_prefix='!', intents=intents) 

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
            
        # Chiedi all'utente di scegliere una carta
        await ctx.send("Insert the ID of the card you want")
        
        def check(received):
            # Si assicura che l'utente sia quello che ha iniziato l'interazione e che il messaggio provenga dal medesimo canale e che la risposta contenga effettivamente l'ID di una delle carte
            return received.author == ctx.author and received.channel == ctx.channel and received.content in [card.id for card in cards]
        
        try:
            # Aspetta il messaggio che soddisfa le condizioni sopra, con un timeout di 120 secondi
            cardID = await bot.wait_for('message', check=check, timeout=120.0)
        except asyncio.TimeoutError:
            await ctx.send('Sorry, you took too long to choose a card.')
        else:
            # Trova la carta scelta dall'utente
            chosen_card = next(card for card in cards if card.id == cardID.content)
            
            # Invia l'immagine della carta ed i prezzi di mercato
            await ctx.send(chosen_card.images['large'])
            await ctx.send("```" + chosen_card.returnTabulatedPricesString() + "```")
    else:
        await ctx.send(response)
        
@bot.command()
async def Help(ctx):
    help_message = """
    Hello! I’m your Pokemon card bot. Here’s what I can do:

    - `Get <Pokemon name>`: Search for all cards of the specified Pokemon. After showing the cards, I will ask you to choose a card by entering its ID. Finally, I will post the image and market prices of the chosen card.
    If you do not choose a card within 120 seconds, the conversation will be closed and you will need to send a Get command again

    - Show this help message.

    The commands are case-sensitive and make sure to write the names of the Pokemon correctly!
    """

    await ctx.send(help_message)

# Esegui il bot
bot.run(DISCORD_KEY)
