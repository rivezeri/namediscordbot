import os 
import random
import time
import discord
import uuid
import requests
import shutil
from dotenv import load_dotenv
from discord.ext import commands
from keepalive import keepAlive
from discord import Spotify


load_dotenv()
intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='/', intents=intents)


@client.event
async def on_ready():
    print("Ready!")
    print(client.guilds)
    members = 0
    
    for guild in client.guilds:
        for member in guild.members:
            
            members += 1

    with open("members.txt", "w") as f:

        f.write(str(members))

@client.event
async def on_member_update(before, after):
    
    with open("defaultChannel.txt") as f:

        find = f.readline()
        channel = client.get_channel(find)

    leagueMsgs = [
    
    f"HEY {after.mention}, NICE GAME YOU'RE PLAYING THERE, LEAGUE. ",
    f"**LEAGUE ALERT**: {after.mention}",
    f"**ATTENTION CLIQUE**: {after.mention} IS CURRENTLY PLAYING LEAGUE OF LEGENDS. THAT IS ALL.",
    f"LEAGUE???? {after.mention} YOU COULD PLAY ANY GAME BUT YOU CHOOSE LEAGUE. GET EM BOYS",
    f"{after.mention} <- STUPID",
    f"{after.mention} NICE GAME IDIOT",
    f"YOU HAVE TEN SECONDS TO CLOSE LEAGUE OF LEGENDS OR YOU WILL BE BANNED. THE COUNTDOWN BEGINS NOW. {after.mention}."
    
    ]
    
    # small head mode, checks if playing league
    if after.activity != None:
        print(after.activities)

        if str(after.activities) == '(<Game name=\'League of Legends\'>,)':
            
            print("BIG INFRACTION")

            with open("hall-of-shame.txt", "w+") as f:
                f.write(after.name)

            await channel.send(random.choice(leagueMsgs))
    
    # checks if playing 'caravan palace' on spotify
    for activity in after.activities:

        if isinstance(activity, Spotify) and after.id == '138214725715623936' and activity.artist == 'Caravan Palace':
            
            print("INFRACTION")

            messages = [
                f"ATTENTION : **{after.mention}** IS CURRENTLY LISTENING TO {activity.artist}. MAKE FUN OF {after.mention}",
                f"HEY YOU ABSOLUTE BAFFOON **{after.mention}**, STOP LISTENING TO {activity.artist}",
                f"PLAY A BETTER SONG {after.mention}, {activity.artist.upper()}",
                f"ATTENTION CLIQUE. {after.mention} IS NOW LISTENING TO CARAVAN PALACE. HAVE A NICE DAY."
            ]

            await channel.send(random.choice(messages))

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    # enables / disables reddit mode
    if message.content.startswith('/reddit'):
        if message.author.id == '138214725715623936':

            await message.channel.send("""Sorry. You don\'t have permission to edit this mode.
            \nPlease say \"The dollar delicacy is real\" to disable.'""")
            
            return

        with open("redditMode.txt", "r+") as f:
            
            find = f.read()

            if find == 'On':
                f.seek(0)
                f.truncate(0)
                f.write('Off')
                
                await message.channel.send('Reddit mode has been *disabled*.')

            else:
                f.seek(0)
                f.truncate(0)
                f.write('On')
                
                await message.channel.send('Reddit mode has been *enabled*.')

    # sets a directory where the bot announces
    if message.content.startswith('/setmain'):

        with open("defaultChannel.txt", "w") as f:
            f.write(str(message.channel.id))

        await message.channel.send('Broadcasts will now be sent in this channel.')

    # checks if reddit mode is enabled, if enabled will automatically add upvote/downvote functionality
    if str(message.author.id) == '138214725715623936' and message.channel.id != "849730083434135614":

        with open("redditMode.txt") as f:

            find = f.read()
            print(find == 'On')

            if find == 'On':
                await message.add_reaction('<:upvote:385300941118898176>')
                await message.add_reaction('<:downvote:385300951139090434>')
    
    # adds image to directory
    if message.content.startswith('/addMcJob'):

        rand = random.randint(1,1000000)
        if message.attachments:

            for attach in message.attachments:

                await attach.save(f"/home/rive/bot/exploitables/tba/{str(rand)} {attach.filename}")

            await message.channel.send('Your exploitable has been added.')
            
        else:
            await message.channel.send('Please add an attachment.')
    
    # returns said image from directory.
    if message.content.startswith('/exploitable'):

        dirListing = os.listdir('/home/rive/bot/exploitables/tba/')
    
        with open(str('/home/rive/bot/exploitables/tba/' + random.choice(dirListing)),'rb') as f:

            picture = discord.File(f)
            await message.channel.send(file=picture)
            


keepAlive()
client.run(os.getenv('TOKEN'))