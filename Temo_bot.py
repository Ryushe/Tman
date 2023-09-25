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
    if choice == "ar": # done
        
        if ',' in args:
            values = ''.join(args).split(',')
        else:
            values = ','.join(args).split(',')
        
        deEncodedValue = f"<{values[2]}>"
        try:
            cook_book.addRecepies(values[0].lower(), values[1], deEncodedValue) # should be (category, recipe, link)
            await ctx.channel.send("Recipe added")
        except(IndexError)as e:
            await ctx.channel.send(f"Give me 3 args dumbass <category> <Recipename> <link>\nTo see categories use:\n`!cook lr`")

    elif choice == "rr":
        recipe = args
        await cook_book.delRecipies(ctx, bot, recipe[0])




        # if ',' in args:
        #     values = ''.join(args).split(',')
        # else:
        #     values = ','.join(args).split(',')

        
        # try:
        #     cook_book.delRecipies(values[0], values[1]) #(category, recipe)
        #     await ctx.channel.send("Recipe deleted")
        # except(IndexError)as e:
        #     await ctx.channel.send(f"Error occured")

    elif choice == "er":
        return 0
    
    elif choice == "lr": # done
        category = ''.join(args)

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
        categories = cook_book.listCategories()
        await ctx.channel.send(f"Categories:\n{categories}")

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

@bot.command()
async def game(ctx):
    await ctx.send(f"""
Enter an option:
list - list all recipies
<recipe name>
exit or e
""")

    while True:
        # Wait for a message from the same user who triggered the game
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        userInput = await bot.wait_for('message', check=check)

        if userInput.content.lower() == 'list':
            await ctx.send("list")
    
        # Process the user's input (you can add your game logic here)
        response = f'You said: {userInput.content}'
        await ctx.send(response)

bot.run(TOKEN)