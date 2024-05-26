import discord
from discord.ext import commands
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
@bot.command()
async def ping(ctx): # Grazie all'asincronicità il bot può gestire più interazioni contemporaneamente
    await ctx.send('Pong!')

# Esegui il bot
bot.run(DISCORD_KEY)
