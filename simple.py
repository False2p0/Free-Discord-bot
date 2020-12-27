import discord
from discord.ext import commands, tasks
import asyncio
import datetime
import os
import json

with open("setting.0", "r") as settings:
    infos = settings.read()


def get_prefix(client, message):
    with open('prefixes.json', 'r')as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

version = "0.1 Alpha"

Token = infos
client = commands.Bot(command_prefix=get_prefix, case_insensitive=True)


# Events
# on_ready
@client.event
async def on_ready():
    print(" ____                _ \n|  _ \ ___  __ _  __| |_   _\n| |_) / _ \/ _` |/ _` | | | |\n|  _ <  __/ (_| | (_| | |_| |\n|_| \_\___|\__,_|\__,_|\__, |\n                       |___/ ")
    print("---")
    print(F"Bot account : {client.user.name}")
    print("---")
    print(F"Discord server : {client.guilds.pop()} ")
    print("---")
    print(F"Discord.py Version {discord.__version__}")
    print("---")
    print(version)


@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r')as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '*'

    with open('prefixes.json', 'w')as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r')as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    prefixes[str(guild.id)] = '*'
    with open('prefixes.json', 'w')as f:
        json.dump(prefixes, f, indent=4)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.message.delete()
        fehler = discord.Embed(title="\n",
                               description="Error.\n \n You dont have enough roles",
                               color=0xff0000)
        await ctx.send(embed=fehler)

    if isinstance(error, commands.CommandNotFound):
        fehler = discord.Embed(title="\n",
                               description="Error.\n \n The command dont exist please use *help to find the right command",
                               color=0xff0000)
        await ctx.send(embed=fehler)

    if isinstance(error, commands.NoPrivateMessage):
        fehler = discord.Embed(title="\n",
                               description="Error.\n \n You don't can use this command in the dm´s",
                               color=0xff0000)
        await ctx.send(embed=fehler)

    if isinstance(error, commands.MissingRequiredArgument):
        fehler = discord.Embed(title="\n",
                               description="Error.\n \n it miss a Argument",
                               color=0xff0000)
        await ctx.send(embed=fehler)

@client.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, prefix):
    with open('prefixes.json', 'r')as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w')as f:
        json.dump(prefixes, f, indent=4)

    embed = discord.Embed(title="\n", description=F"prefix change to {prefix}", color=discord.colour.Color.red())
    await ctx.send(embed=embed)

@client.command()
@commands.guild_only()
async def embed(ctx):

    embed = discord.Embed(title="Create a Embed \n Please enter the titel", description="||End in 1 min ||")
    Titel = await ctx.send(embed=embed)
    try:
        msg = await client.wait_for(
            "message",
            timeout=60,
            check=lambda message: message.author == ctx.author
                                  and message.channel == ctx.channel)
        if msg:
            Name = discord.Embed(title="Please enter a description", description="|| End in 1 min ||")
            await Titel.delete()
            await msg.delete()
            test = await ctx.send(embed=Name)

        msg2 = await client.wait_for(
            "message",
            timeout=60,
            check=lambda message: message.author == ctx.author
                                  and message.channel == ctx.channel)

        if msg2:
            embed2 = discord.Embed(title=msg.content, description=msg2.content)
            await test.delete()
            await msg2.delete()
            await ctx.send(embed=embed2)



    except asyncio.TimeoutError:
        await Titel.delete()
        await ctx.send("Chancelling due to timeout.", delete_after=60)


@client.command()
async def announce(ctx):

    embed = discord.Embed(title="Create a Embed \n Please enter the channel id", description="||End in 1 min ||")
    Titel = await ctx.send(embed=embed)
    try:
        msg = await client.wait_for(
            "message",
            timeout=60,
            check=lambda message: message.author == ctx.author
                                  and message.channel == ctx.channel)
        if msg:
            Name = discord.Embed(title="Please enter a description", description="|| End in 1 min ||")
            await Titel.delete()
            await msg.delete()
            test = await ctx.send(embed=Name)

        msg2 = await client.wait_for(
            "message",
            timeout=60,
            check=lambda message: message.author == ctx.author
                                  and message.channel == ctx.channel)

        if msg2:
            embed2 = discord.Embed(title="\n", description=msg2.content, timestamp=datetime.datetime.utcnow())
            embed2.set_thumbnail(url=ctx.guild.icon_url)
            embed2.set_footer(text=ctx.guild.name)

            await test.delete()
            await msg2.delete()
            await client.get_channel(int(msg.content)).send(embed=embed2)

    except asyncio.TimeoutError:
        await Titel.delete()
        await ctx.send("Chancelling due to timeout.", delete_after=60)

client.run(Token)
