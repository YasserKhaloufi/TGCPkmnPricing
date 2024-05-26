import discord
from discord.ext import commands
from tcgAPI_Interface import getCardByPkmnName
from IO import getCardsDisplayInfo
from secret import DISCORD_KEY

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
    pokeName = ctx.message.content[len(ctx.prefix + ctx.command.name):] # Rimuovi il prefisso del comando dal messaggio (con l'operatore ":" prendo tutta la stringa dopo l'indice indicato)
    cards = getCardByPkmnName(pokeName.strip())
    
    response = "No card found with that name"
    
    if cards != []:
        response = getCardsDisplayInfo(cards)
        
        # Suddividi il messaggio in parti di 4000 caratteri
        message_parts = [response[i:i+2000] for i in range(0, len(response), 2000)]

        # Invia ogni parte come un messaggio separato
        for part in message_parts:
            await ctx.send(part)
    else:
        await ctx.send(response)

# Esegui il bot
bot.run(DISCORD_KEY)
