import discord 
import sys
import traceback
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



##############################ADMIN COMMANDS################################ 
class moderationtools(commands.Cog):    
    def __init__(self, bot):
        self.bot = bot
    
    async def __error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(error)
    
    #Clears specified ammount of messages from the channel it was invoked in
    @commands.command(aliases=["purge"])
    async def clear(self, ctx, ammount=1):
        if ctx.message.author.guild_permissions.administrator: #Permission check
            counter = ammount
            ammount = ammount + 1
            await ctx.channel.purge(limit=ammount)
            await ctx.send(f"***✓*** Deleted {counter} messages!", delete_after=5)

    # kicks user specified
    @commands.command(aliases=["goodbye"])
    async def kick(self, ctx, member : discord.Member):
        if ctx.message.author.guild_permissions.administrator: #Permission check
            await member.send(f"{member.mention}, you have been kicked from {ctx.guild.name}. A moderator will contact you shortly with more details")
            await ctx.channel.send(f"{member.mention} has been kicked from {ctx.guild.name} by {ctx.message.author.mention}.")
            await member.kick(reason=None)   

    #Bans user specified
    @commands.command(aliases=["banish"])
    async def ban(self, ctx, member : discord.Member):
        if ctx.message.author.guild_permissions.administrator: #Permission check
            await member.send(f"{member.mention}, you have been banned from {ctx.guild.name}. A moderator will contact you shortly with more details.")
            await ctx.channel.send(f"{member.mention} has been kicked from {ctx.guild.name} by {ctx.message.author.mention}.")
            await member.ban(reason=None)

    #Gives muted role to specified user
    @commands.command(aliases=["shutup"])
    async def mute(self, ctx, user: discord.Member): #Permission check
        channel = discord.utils.get_channel(610172526395392011)
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        user = discord.utils.get_user(user)
        if ctx.message.author.guild_permissions.administrator:
            await user.add_roles(role)
            await user.send(f"You have been muted. Please read the rules, you will be receiving a DM from one of the moderators containing the reason you were muted as well as how long (if applicable). Thanks for not fighting with the mods!")
            await ctx.channel.send(f"{ctx.user.mention} Has been muted by {ctx.message.author.mention}")
            await channel.send(f"This is an automated message to the other moderators so they know that {ctx.user} has been muted by {ctx.message.author.mention}. Please discuss why and actions to take.")

    #Removes muted role from specified user
    @commands.command(aliases=["unshutup"])
    async def unmute(self, ctx, user: discord.Member): #Permission check
        if ctx.message.author.guild_permissions.administrator:
            await user.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted")) # removes muted role
            await ctx.send(f"{user.mention} has been unmuted")

    #locks channel that it was invoked in
    @commands.command(aliases=["lock", "toohorny"])
    async def lockdown(self, ctx, time):
        if ctx.message.author.guild_permissions.administrator: #Permission check
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
            await ctx.channel.send(f"***✓*** Locked channel for {time} seconds!")
            await asyncio.sleep(time)
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
#################################END OF ADMIN COG######################################