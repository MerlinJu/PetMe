import discord 
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from typing import Final
from pymongo import MongoClient


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


# create MONGO DB Client instance 
CLIENT = MongoClient(os.getenv('MONGO_DB_URI'))
DB = CLIENT['User_Pets'] # Database instance
COLLECTION = DB['Pets'] # Collection instance inside the Database instance


# Database connection Confirmation 
try:
    CLIENT.admin.command('ping')
    print('Pinged your deployment. Succesfully connected to the database!')
except Exception as e:
    print(e)




# command to pick a pet for user ( Will be saved in DB )
@bot.command(name = 'pickmypet')
async def pickmypet(ctx):
    # Send a message asking the user to pick a pet
    await ctx.send('Pick your Pet, Dog or Cat?  ')

    # check if the message is valid = same channel and same author of command send a message
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    
    # try picking a pet
    try:
        # wait for user response for 30sec
        msg = await bot.wait_for('message', timeout=30.0, check=check)
        user_pet_choice = msg.content.lower()

        # pet choices
        PETS = ['dog', 'cat']

        if user_pet_choice in PETS:
            COLLECTION.update_one(
                {'user_id': ctx.author.id}, # find the User by his ID 
                {'$set': {'user_name': ctx.author.name, 'user_pet': user_pet_choice}},
                upsert=True # if the user document wasnt found or there is none a new one will be created, otherwise updated
            )
            await ctx.send(f'You picked {user_pet_choice.capitalize()} as your own Pet!')
        else:
            ctx.send('Invalid pet choice, please choose between Dog or Cat.')

    except asyncio.TimeoutError: # Took too long to pick ( >30 seconds )
        await ctx.send('You took too long to pick a pet. Please try again!')
    except Exception as e: #Other Exceptions
        print(e)


    


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