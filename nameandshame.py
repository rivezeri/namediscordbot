import os 
import random
import discord
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
    # if str(message.author.id) == '138214725715623936' and message.channel.id != "849730083434135614":
    with open("redditMode.txt") as f:
        find = f.read()

        if find == 'On':
            print(find == 'On')
            with open("users.txt") as g:
                g = g.read()
                h = g.split()
                for i in h:
                    if str(message.author.id) == str(i) and message.channel.id != "849730083434135614":
                        await message.add_reaction('<:upvote:385300941118898176>')
                        await message.add_reaction('<:downvote:385300951139090434>')
        
    # adds image to directory
    if message.content.startswith('/addMcJob'):

        if message.attachments:

            for attach in message.attachments:

                storage = f"{str(random.randint(1,1000))}{str(random.randint(1,10000))}{attach.filename}"

                await attach.save(f"/home/rive/bot/exploitables/tba/{storage}")

            await message.channel.send(f'Your exploitable has been added. Filename: {storage}.')
            
        else:
            await message.channel.send('Please add an attachment.')
    
    # returns said image from directory.
    if message.content.startswith('/exploitable'):
        dirListing = os.listdir('/home/rive/bot/exploitables/tba/')

        if len(dirListing) == 0:
            await message.channel.send('The exploitable directory is currently empty.')
            return
        
        with open(str('/home/rive/bot/exploitables/tba/' + random.choice(dirListing)),'rb') as f:

            picture = discord.File(f)
            await message.channel.send('Here is your exploitable:')
            await message.channel.send(file=picture)
    
    # will add the afflicted user to the unfun list
    if message.content.startswith('/addUser'):

       try:
           if str(message.mentions[0].id) == str(client.user.id):
                await message.channel.send('Don\'t even think about it.')
                return
            
           with open("users.txt", 'r+') as f:
                a = f.read()
                b = a.split()
                for i in b:
                    print(i)
                    if str(i) == str(message.mentions[0].id):
                        await message.channel.send('User already added.')
                        return

                f.write(f"{str(message.mentions[0].id)}\n")

           await message.channel.send(f"The user {message.mentions[0]} Added.")

       except IndexError:
           await message.channel.send('Please @ mention the user.')

    if message.content.startswith('/removeUser'):
        
        try:            
            with open("users.txt", "r") as f:
                lines = f.readlines()
            
            with open("users.txt", "w") as f:
                check = False
                for line in lines:
                    if line.strip("\n") != str(message.mentions[0].id):
                        f.write(line)
                    else:
                        check = True

                if check:
                    await message.channel.send(f'The user {message.mentions[0]} has been removed.')
                else:
                    await message.channel.send('Please remove a valid user.')
            
            # HOLY CRAP! only do this on small servers

        except IndexError:
            await message.channel.send('Please @ mention the user to remove.')

keepAlive()
client.run(os.getenv('TOKEN'))
