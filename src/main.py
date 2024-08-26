import discord 
from discord.ext import commands

# correct intents to send and read messages
intents = discord.Intents.default()
intents.messae_content = True
intents.guilds = True


# command prefix as '!'
bot = commands.Bot(command_prefix='!', intents=intents)