import discord
from discord.ext import commands
from secret import DISCORD_KEY

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Evento on_ready
@bot.event
async def on_ready():
    print(f'Bot connesso come {bot.user}')

# Mapping comando-funzione stile switch-case
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

# Esegui il bot
bot.run(DISCORD_KEY)
