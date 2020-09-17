import discord 
import sys
import traceback
from cogs.commands import fun
from cogs.Errorlistener import CommandErrorHandler
from cogs.music import Music
from discord import Spotify
import asyncio
import functools
import itertools
import youtube_dl
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

async def status_task():
    while True:
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=".help | Carribean way is best way"))
        await sleep(10)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Oh it's that time again So grab your tablet pen I said what's with you She said shut up and osu! with me..."))
        await sleep(10)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="And what can you do my effeminate fellow?"))
        await sleep(10)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="I can suck ya [REDACTED]"))
        await sleep(10)
        

#initial startup
bot = commands.Bot(command_prefix=".", status=discord.Status.dnd, activity=discord.Game(name="starting lol"))
bot.remove_command("help")
#ready presance change
@bot.event
async def on_ready():
   print("Ready")
   bot.loop.create_task(status_task())


#help command
@bot.command()
async def help(ctx):
    await ctx.channel.send(f"***Current Commands***\nHelp - Displays this Help message \nPing - Fetches latency of bot (Aliases: Pong) \nKill - kills a member (Aliases: gun) \n8ball - Magic 8 ball (Aliases: _8ball, 8ofcircles)\nCopypasta - gets a random copypasta \nhorny - banishes a user to horny jail (Aliases: hjail, jail) \n-------------------------------------------------\nThe code is open source and avalible on https://github.com/N3utr1n0/DiscordBotButBad")

#fetch latency
@bot.command(aliases=["pong"])
@commands.cooldown(1, 2, commands.BucketType.user)
async def ping(ctx):
    ping_ = bot.latency
    ping = round(ping_ * 1000) #convert to ms
    await ctx.channel.send(f"***✓*** Pong! The current ping of this bot is {ping} ms")


#More commands in COG FILE COMMANDS.PY

##############################ADMIN COMMANDS#################################
@bot.command(aliases=["purge"])
async def clear(ctx, ammount=1):
    if ctx.message.author.guild_permissions.administrator:
        counter = ammount
        ammount = ammount + 1
        await ctx.channel.purge(limit=ammount)
        await ctx.send(f"***✓*** Deleted {counter} messages!", delete_after=5)
    else: 
        embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        await ctx.send(embed=embed)


@bot.command(aliases=["banish"])
@commands.has_any_role("ALL POWERFUL GAMER","God Teir Gamer (Mod)")
async def ban(ctx, member : discord.Member, reason=None):
    if reason == None:
        await ctx.send(f"{member.mention} has been banned from {ctx.guild.name} for no reason whatsoever")
    else:
        messageok = f"{member.mention} has been banned from {ctx.guild.name} for {reason}"
        await member.send(messageok)
        await member.ban(reason=reason)

@bot.command(aliases=["goodbye"])
@commands.has_any_role("ALL POWERFUL GAMER","God Teir Gamer (Mod)")
async def kick(ctx, member : discord.Member, reason=None):
    if reason == None:
        await ctx.send(f"{member.mention} has been kicked from {ctx.guild.name} for no reason whatsoever")
    else:
        messageok = f"{member.mention} has been kicked from {ctx.guild.name} for {reason}"
        await member.send(messageok)
        await member.kick(reason=reason)

# This prevents staff members from being punished 
class Sinner(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument) # gets a member object
        permission = argument.guild_permissions.administrator # can change into any permission
        if not permission: # checks if user has the permission
            return argument # returns user object
        else:
            raise commands.BadArgument("You cannot punish other staff members") # tells user that target is a staff member

# Checks if you have a muted role
class Redeemed(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument) # gets member object
        muted = discord.utils.get(ctx.guild.roles, name="Muted") # gets role object
        if muted in argument.roles: # checks if user has muted role
            return argument # returns member object if there is muted role
        else:
            raise commands.BadArgument("The user was not muted.") # self-explainatory
            
# Checks if there is a muted role on the server and creates one if there isn't
async def mute(ctx, user, reason):
    role = discord.utils.get(ctx.guild.roles, name="Muted") # retrieves muted role returns none if there isn't 
    hell = discord.utils.get(ctx.guild.text_channels, name="hell") # retrieves channel named hell returns none if there isn't
    if not role: # checks if there is muted role
        try: # creates muted role 
            muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")
            for channel in ctx.guild.channels: # removes permission to view and send in the channels 
                await channel.set_permissions(muted, send_messages=False,
                                              read_message_history=False,
                                              read_messages=False)
        except discord.Forbidden:
            return await ctx.send("I have no permissions to make a muted role") # self-explainatory
        await user.add_roles(muted) # adds newly created muted role
        await ctx.send(f"{user.mention} has been sent to hell for {reason}")
    else:
        await user.add_roles(role) # adds already existing muted role
        await ctx.send(f"{user.mention} has been sent to hell for {reason}")
       
    if not hell: # checks if there is a channel named hell
        overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_message_history=False),
                      ctx.guild.me: discord.PermissionOverwrite(send_messages=True),
                      muted: discord.PermissionOverwrite(read_message_history=True)} # permissions for the channel
        try: # creates the channel and sends a message
            channel = await ctx.create_channel('hell', overwrites=overwrites)
            await channel.send("Welcome to hell.. You will spend your time here until you get unmuted. Enjoy the silence.")
        except discord.Forbidden:
            return await ctx.send("I have no permissions to make #hell")
            
            
class Moderation(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    async def __error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(error)
            
    @commands.command()
    async def mute(self, ctx, user: Sinner, reason=None):
        if ctx.message.author.guild_permissions.administrator:
            await mute(ctx, user, reason or "treason") # uses the mute function
    
    
    @commands.command()
    async def unmute(self, ctx, user: Redeemed):
        if ctx.message.author.guild_permissions.administrator:
            await user.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted")) # removes muted role
            await ctx.send(f"{user.mention} has been unmuted")


    

#Music command
###SEE COGS FOLDER###
bot.add_cog(fun(bot))
bot.add_cog(Music(bot)) #Closed source, sorry
bot.add_cog(CommandErrorHandler(bot))
bot.add_cog(Moderation(bot))

###IMPORTANT####
bot.run("TOKEN")
###IMPORTANT###
