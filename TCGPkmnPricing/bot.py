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
    pkmnName = ctx.message.content[len(ctx.prefix + ctx.command.name):] # Rimuovi il prefisso del comando dal messaggio (con l'operatore ":" prendo tutta la stringa dopo l'indice indicato)
    cards = getCardByPkmnName(pkmnName.strip())
    
    response = "No card found with that name"
    
    if cards != []:
        response = getCardsDisplayInfo(cards)
        
        # Gestione limite 2000 caratteri per messaggio
        # Suddividi il messaggio in righe
        lines = response.split('\n')
        
        # Crea una lista per contenere i vari messaggi
        messages = []
        message = ""
        
        # Aggiungi righe al messaggio corrente finché non raggiungi il limite di 2000 caratteri
        for line in lines:
            # Se aggiungendo una nuova riga al messaggio superi i 2000 caratteri
            if len(message) + len(line) + 1 > 2000:  # (+1 per il carattere '\n')
                # Allora fermati e inizia a costruire il prossimo
                messages.append(message) 
                message = ""          
            message += line + "\n"

        # Aggiungi l'ultima parte del messaggio se non è vuota (per quando sono finite le linee, ma l'ultima rimane fuori)
        if message:
            messages.append(message)

        # Invia ogni parte come un messaggio separato
        for m in messages:
            await ctx.send(m)
    else:
        await ctx.send(response)

# Esegui il bot
bot.run(DISCORD_KEY)
