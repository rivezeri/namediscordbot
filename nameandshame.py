from dotenv import load_dotenv
load_dotenv()

import os 
import random
import discord
from discord.ext import commands
from keepalive import keepAlive
from discord import Spotify

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

    channel = client.get_channel(836753810965528578)

    leagueMsgs = [ f"HEY {after.mention}, NICE GAME YOU'RE PLAYING THERE, LEAGUE. ",
    f"**LEAGUE ALERT**: {after.mention}",
    F"ATTENTION CLIQUE: {after.mention} IS CURRENTLY PLAYING LEAGUE OF LEGENDS. THAT IS ALL."
    ]

    if after.activity != None:
        print(after.name)

        for activity in after.activities:
            
            messages = [ f"ATTENTION : **{after.mention}** IS CURRENTLY LISTENING TO {activity.artist.upper()}. MAKE FUN OF THEM",
            f"HEY YOU ABSOLUTE BAFFOON **{after.mention}**, STOP LISTENING TO {activity.artist.upper()}",
            f"PLAY A BETTER SONG {after.mention}, {activity.artist.upper()} REALLY?"
            ]

            if isinstance(activity, Spotify) and after.name == 'justBen' and activity.artist == 'Caravan Palace':
                print("INFRACTION")
                with open("mcjobCounter.txt", "a+") as f:
                    f.write(1)
                
                await channel.send(random.choice(messages))

        if len(after.activities) > 1:
            print(after.activities[1].name)
            if str(after.activities[1].name).lower() == "league of legends":
                print("BIG INFRACTION")
                try:
                    with open("hall-of-shame.txt", "a+") as f:
                        f.write(after.name)

                    await channel.send(random.choice(leagueMsgs))

                except discord.errors.Forbidden:
                    print("Not valid permissions")
                    after.send("")

                print(after.activities[1])

keepAlive()
client.run(os.getenv('TOKEN')) 