import discord 
import os
from discord.ext import commands
from dotenv import load_dotenv
from typing import Final


# load Bot Token from .env file
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# correct intents to send and read messages
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# command prefix as '!'
bot = commands.Bot(command_prefix='!', intents=intents)

#GLOBALS 

PETS = ['Dog', 'Cat']


# command to pick a pet for user ( Will be saved in DB )
@bot.command(name = 'pickmypet')
async def pickmypet(ctx):
    pass


# command to call users own pet 
@bot.command(name='mypet')
async def mypet(ctx):
    pass





# RUNTIME BELOW

# event when the bot is ready 
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

# Start the bot if script is manually run
if __name__ == '__main__':
    if TOKEN:
        bot.run(TOKEN)
    else:
        print('Discord Token not found')