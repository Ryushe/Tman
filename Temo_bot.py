import os 
import discord
from discord.ext import commands
from dotenv import load_dotenv
import bother_temo
import anime_updates
import cook_book
import time
import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} is in your servers')

@bot.command()
async def hello(ctx):
    if ctx.author == bot.user:
        return

    response = 'Leave me tf alone'
    await ctx.channel.send(response)
    print('sent')
    

@bot.command()
async def commands(ctx):
    await ctx.channel.send("""
Available commands:
!hello - say hi to the bot :)
!update - update on any important anime info 
!sendate @___ - update specific person on info
!pfp @__ - gets user pfp / if left empty gives the user's pfp
!cook <choice(optional)> <option(optional)>
    "h" = help
    """)

@bot.command()
async def pfp(ctx, user: discord.User=None):
    if user:
        pic = user.display_avatar.url
        await ctx.channel.send(pic)
    else: 
        user = ctx.author
        pic = user.display_avatar.url
        await ctx.channel.send(pic)


@bot.command()
async def cook(ctx, choice, *args):
    choices = """
empty(anything thats not an option) - help

ar - add recepies <category>, <recipe>, <link> (comma seperated or whitespace seperated) if 2 words use _ instead of whitespace
rr - remove recepies
er - edit recepies
lr - list recepies

ac - add categories
rc - remove categories
ec - edit categories
lc - list categories
    """
    if choice == "ar":
        
        if ',' in args:
            values = ''.join(args).split(',')
        else:
            values = ','.join(args).split(',')


        print(values)
#         try:
#             cook_book.addRecepies(values[0].lower(), values[1], values[2]) # should be (category, recipe, link)
#             await ctx.channel.send("Recipe added)")
#         except(ValueError)as e:
#             await ctx.channel.send(f"""
# Didnt work lol
# """)

    elif choice == "rr":
        return 0
    elif choice == "er":
        return 0
    
    elif choice == "lr":
        category = args

        if args:
            recipe = cook_book.listRecepies(category.lower())
        else: 
            recipe = cook_book.listAllRecepies()

        await ctx.channel.send(f"Recepies are: \n{recipe}")

    elif choice == "ac":
        return 0
    elif choice == "rc":
        return 0
    elif choice == "ec":
        return 0
    elif choice == "lc":
        return 0
    else:
        await ctx.channel.send(f"your choices are: {choices}")
    
@bot.command()
async def pcook(ctx, choice, *args): # personal cook instead of global
    return 0



@bot.command()
async def nigger(ctx, quantity=1, word="nigger"):
    i = 0
    while i != quantity:
        await ctx.channel.send(f"{word}")
        i += 1


@bot.command()
async def botherTemo(ctx, user: discord.User=None, message='bbw'):
    image_links = bother_temo.get_google_images(message)
    
    if user:
        for link in image_links:
            time.sleep(.2)
            await user.send(link)
    else:
        for link in image_links:
            time.sleep(.2)
            await ctx.channel.send(link)


@bot.command()
async def update(ctx):
    episode_list = anime_updates.get_episode_list()
    name_list = anime_updates.get_name_list()

    name_episode_list = anime_updates.get_full_list()

    for value in name_episode_list:
        await ctx.channel.send(f'{value}')

# send list to people
@bot.command()
async def sendate(ctx, user: discord.User):

    name_episode_list = anime_updates.get_full_list()

    for value in name_episode_list:
        await user.send(f'{value}')
    
#commands for imports

def get_bot():
    return bot

bot.run(TOKEN)