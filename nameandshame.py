import os 
import random
import discord
from discord.ext import commands
from keepalive import keepAlive
from discord import Spotify
import time

intents = discord.Intents.all()
intents.members = True


client = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    print("Ready!")
    print(client.guilds)
    # await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.guilds)}"))
    members = 0
    
    for guild in client.guilds:
        for member in guild.members:
            members += 1

    with open("members.txt", "w") as f:
        f.write(str(members))

@client.event
async def on_member_update(before, after):
    # await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=random.choice(status)))
    channel = client.get_channel()

    leagueMsgs = [ f"HEY {after.mention}, NICE GAME YOU'RE PLAYING THERE, LEAGUE. ",
    f"**LEAGUE ALERT**: {after.mention}",
    f"**ATTENTION CLIQUE**: {after.mention} IS CURRENTLY PLAYING LEAGUE OF LEGENDS. THAT IS ALL.",
    f"LEAGUE???? {after.mention} YOU COULD PLAY ANY GAME BUT YOU CHOOSE LEAGUE. GET EM BOYS",
    f"{after.mention} <- STUPID",
    f"{after.mention} NICE GAME IDIOT",
    f"YOU HAVE TEN SECONDS TO CLOSE LEAGUE OF LEGENDS OR YOU WILL BE BANNED. THE COUNTDOWN BEGINS NOW. {after.mention}."
    ]
    
    # small head mode
    if after.activity != None:
        print(after.activities)

        if str(after.activities) == '(<Game name=\'League of Legends\'>,)':
            print("BIG INFRACTION")
            try:
                with open("hall-of-shame.txt", "a+") as f:
                    f.write(after.name)

                await channel.send(random.choice(leagueMsgs))

            except discord.errors.Forbidden:
                print("Not valid permissions")
                after.send("")

    for activity in after.activities:

        if isinstance(activity, Spotify) and after.id == '' and activity.artist == 'Caravan Palace':
            messages = [ f"ATTENTION : **{after.mention}** IS CURRENTLY LISTENING TO {activity.artist}. MAKE FUN OF {after.mention}",
                f"HEY YOU ABSOLUTE BAFFOON **{after.mention}**, STOP LISTENING TO {activity.artist}",
                f"PLAY A BETTER SONG {after.mention}, {activity.artist.upper()}",
                f"ATTENTION CLIQUE. {after.mention} IS NOW LISTENING TO CARAVAN PALACE. HAVE A NICE DAY."
            ]

            print("INFRACTION")
            with open("mcjobCounter.txt", "a+") as f:
                f.write(1)
            
            await channel.send(random.choice(messages))



keepAlive()
client.run(os.environ['TOKEN']) 
