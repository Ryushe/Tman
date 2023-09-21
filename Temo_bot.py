import os 
import discord
from discord.ext import commands
from dotenv import load_dotenv
import bother_temo
import anime_updates
import time

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