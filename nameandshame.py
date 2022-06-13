import os 
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
from keepalive import keepAlive
from discord import Spotify
from discord.utils import get


load_dotenv()
intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

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

# construction zone
@client.event
async def on_voice_state_update(member, before, after):
    with open("mainvc.txt", 'r+') as f:
        a = f.read()
        b = a.split()

        role = get(member.guild.roles, name='vc')

        if member.voice and member.voice.channel and str(member.voice.channel.id) in b:
            await member.add_roles(role)
        else:
            await member.remove_roles(role)

@client.event
async def on_member_update(before, after):
    
    '''Includes the LOL banner and Caravan Palace checker. Needed on member update for active checks.'''
    
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

# construction zone
@commands.guild_only()
@client.command()
async def setVC(ctx):
    '''Sets a main vc.'''

    try:

        with open("mainvc.txt", 'r+') as f:
            a = f.read()
            b = a.split()
            for i in b:
                if str(i) == str(ctx.author.voice.channel.id):
                    await ctx.send('Voice channel already set.')
                    return

            f.write(f"{str(ctx.author.voice.channel.id)}\n")

        await ctx.send(f"The channel '{ctx.author.voice.channel}' Added.")

    except IndexError:
        await ctx.send('Please @ mention the user.')

@commands.guild_only()
@client.command()
async def reddit(ctx):
    
    '''Reddit toggle. Enables upvote/downvote on each enabled redditor.'''
    
    with open("redditMode.txt", "r+") as f:
        find = f.read()
    
        if find == 'On':
            f.seek(0)
            f.truncate(0)
            f.write('Off')
            
            await ctx.send('Reddit mode has been *disabled*.')

        else:
            f.seek(0)
            f.truncate(0)
            f.write('On')
            
            await ctx.send('Reddit mode has been *enabled*.')

@commands.guild_only()
@client.command()
async def setMain(ctx):
    
    '''Sets the main channel to allow broadcasts.'''
    
    with open("defaultChannel.txt", "w") as f:
        f.write(str(ctx.message.channel.id))

    await ctx.send('Broadcasts will now be sent in this channel.')

@commands.guild_only()
@client.command()
async def addMcJob(ctx):
    
    '''Adds McJob exploits to the alloted directory.'''

    if ctx.message.attachments:

        for attach in ctx.message.attachments:

            storage = f"{str(random.randint(1,1000))}{str(random.randint(1,10000))}{attach.filename}"

            await attach.save(f"/home/rive/bot/exploitables/tba/{storage}")

        await ctx.send(f'Your exploitable has been added. Filename: {storage}.')
        
    else:
        await ctx.send('Please add an attachment.')


@commands.guild_only()
@client.command()
async def exploitable(ctx):
    
    '''Calls an exploit randomly from the same directory.'''
    
    dirListing = os.listdir('/home/rive/bot/exploitables/tba/')

    if len(dirListing) == 0:
        await ctx.send('The exploitable directory is currently empty.')
        return

    with open(str('/home/rive/bot/exploitables/tba/' + random.choice(dirListing)),'rb') as f:

        picture = discord.File(f)

        await ctx.send('Here is your exploitable:')
        await ctx.send(file=picture)

@commands.guild_only()
@client.command()
async def addRedditor(ctx):
    
    '''Adds your wanted Redditor to a file, works in tandem with the reddit command.'''
    
    try:
        if str(ctx.message.mentions[0].id) == str(client.user.id):
            await ctx.send('Don\'t even think about it.')
            return
        
        with open("users.txt", 'r+') as f:
            a = f.read()
            b = a.split()
            for i in b:

                if str(i) == str(ctx.message.mentions[0].id):
                    await ctx.send('User already added.')
                    return

            f.write(f"{str(ctx.message.mentions[0].id)}\n")

        await ctx.send(f"The user {ctx.message.mentions[0]} Added.")

    except IndexError:
        await ctx.send('Please @ mention the user.')


@client.command()
@commands.guild_only()
async def removeRedditor(ctx):
    
    '''Cuts the Redditor from the file. Disables the function to the user.'''
    
    try:            
        with open("users.txt", "r") as f:
            lines = f.readlines()
        
        with open("users.txt", "w") as f:
            check = False
            for line in lines:

                if line.strip("\n") != str(ctx.message.mentions[0].id):
                    f.write(line)

                else:
                    check = True

            if check:
                await ctx.send(f'The user {ctx.message.mentions[0]} has been removed.')

            else:
                await ctx.send('Please remove a valid user.')
        
        # HOLY CRAP! only do this on small servers

    except IndexError:
        await ctx.send('Please @ mention the user to remove.')

@client.command()
@commands.guild_only()
async def restrictChannel(ctx):
    
    '''Disallows reddit to run on the specific channel.'''
    
    try:
        with open("restrictedChannels.txt",'r+') as f:
            a = f.read()
            b = a.split()
            for i in b:
                if str(i) == str(ctx.message.channel.id):
                    await ctx.send('Channel already restricted.')
                    return
            
            f.write(f"{str(ctx.message.channel.id)}\n")

            await ctx.send(f'The current channel \'{ctx.message.channel}\' has been restricted.')

    except IndexError:
        await ctx.send('Please select a channel to restrict.')

@client.command()
@commands.guild_only()
async def unsetVC(ctx):
    '''Unsets the @vc role per main. Inverse of setVC.'''

    try:
        with open("mainvc.txt", "r") as f:
            lines = f.readlines()

        with open("mainvc.txt", "w") as f:
            check = False
            for line in lines:

                if line.strip("\n") != str(ctx.author.voice.channel.id):
                    f.write(line)

                else:
                    check = True

            if check:
                await ctx.send(f'The channel \'{ctx.author.voice.channel}\' has been unset.')

            else:
                await ctx.send('This voice was never set.')

    except IndexError:
        await ctx.send('Takes the current channel only.')

@client.command()
@commands.guild_only()
async def unrestrictChannel(ctx):
    
    '''Unrestricts said channel. Inverse of above.'''

    try:            
        with open("restrictedChannels.txt", "r") as f:
            lines = f.readlines()
        
        with open("restrictedChannels.txt", "w") as f:
            check = False
            for line in lines:

                if line.strip("\n") != str(ctx.message.channel.id):
                    f.write(line)

                else:
                    check = True

            if check:
                await ctx.send(f'The channel \'{ctx.message.channel}\' has been unrestricted.')

            else:
                await ctx.send('This channel was never restricted.')

    except IndexError:
        await ctx.send('Takes the current channel only.')

@client.event
async def on_message(message):
    with open("restrictedChannels.txt") as f:
        
        a = f.read()
        restricted = a.split()

    with open("redditMode.txt") as f:
        find = f.read()

        if str(find) == "On":

            with open("users.txt") as g:

                g = g.read()
                h = g.split()

                for i in h:
                    if str(message.author.id) == str(i) and str(message.channel.id) not in restricted:
                        await message.add_reaction('<:upvote:385300941118898176>')
                        await message.add_reaction('<:downvote:385300951139090434>')

    await client.process_commands(message)


keepAlive()
client.run(os.getenv('TOKEN'))
