import discord 
import sys
import traceback
from cogs.moderation import moderationtools
from cogs.commands import fun
from cogs.Errorlistener import CommandErrorHandler
from cogs.listeners import filter
from discord import Spotify
import asyncio
import functools
import itertools
from async_timeout import timeout
from discord.ext import commands
from discord import message
from discord import Member
from discord import permissions
from discord.ext.commands import has_permissions, MissingPermissions, Cog, BucketType
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown)
from asyncio import sleep
import json
import os
import random
from random import choice
import math
import datetime
from datetime import timezone, tzinfo, timedelta
import time

#Change Bot Status
async def status_task():
    while True:
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Carribean way is best way"))
        await sleep(10) #Will cycle thru these statuses
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Oh it's that time again So grab your tablet pen I said what's with you She said shut up and osu! with me..."))
        await sleep(10)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="And what can you do my effeminate fellow?"))
        await sleep(10)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="I can suck ya [REDACTED]"))
        await sleep(10)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Dont forget, you are here forever!"))
        await sleep(10)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="[insert joke here]"))
        await sleep(10)

        #Add more statuses below, do not forget to add await sleep(10) at the end of it. 


#initial startup
bot = commands.Bot(command_prefix=".", status=discord.Status.dnd, activity=discord.Game(name="Getting Ready..."))
bot.remove_command("help")

#ready
@bot.event
async def on_ready():
   print("Ready")
   bot.loop.create_task(status_task())

#new help command
@bot.command()
async def help(ctx):
    await ctx.channel.send(f"***Commands for [BOT NAME]***\nhelp - Prints this Help message\nping - Fetches the Latency of this bot\nhjail - sends a user to horny jail\nkill - kills a user\n8ball - magic 8 ball\ncopypasta - prints a random copypasta to chat\nhug - hugs a user\nkiss - kisses a user\nuwu - try it and see what happens\ncoin - Flips a coin. Pretty simple\n")
    await ctx.channel.send(f"***Command prefix is \'.\'\nThe code is open source and avalible on <https://github.com/N3utr1n0/Discord-Bot-Basic-Framework>\nCreated by N3#6494")

@bot.command()
async def ahelp(ctx, admin: discord.Member):
    if ctx.message.author.guild.has_permissions.administrator:
        await admin.send(f"***Admin commands for [BOT NAME]:***\n\nEach command is structured as follows: [prefix][command (can be replaced with the listed alias)] [arguments]\n\nclear - clears specified ammount of messaegs from the channel invoked in. Usage: .clear [number of messages to delete] Aliases: purge\nkick OR ban - kicks/bans a specified user Usage: .[kick or ban] @[Mention user you want to kick/ban] Aliases: goodbye/banish\n")
#fetch latency
@bot.command(aliases=["pong"])
@commands.cooldown(1, 2, commands.BucketType.user)
async def ping(self, ctx):
    ping_ = bot.latency
    ping = round(ping_ * 1000) #convert to ms
    await ctx.channel.send(f"***✓*** Pong! The current ping of De Fan is {ping} ms")
    print(f"Ping requested.\nThe current latency is {ping} ms.")

#More commands in COG FOLDER
#ATTACH COGS
bot.add_cog(CommandErrorHandler(bot)) #errorlistener.py
bot.add_cog(fun(bot)) #Commands.py
bot.add_cog(moderationtools(bot)) #moderation.py
bot.add_cog(filter(bot)) #listeners.py #listeners.py


###IMPORTANT####
bot.run("token") #Keep this token private, discord will freak if you dont
###IMPORTANT###
