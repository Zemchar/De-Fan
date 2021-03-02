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
    
    #Clears specified ammount of messages from the channel it was invoked in
    @commands.command(aliases=["purge"])
    @commands.has_guild_permissions(manage_guild=True)
    async def clear(self, ctx, ammount=1):
            counter = ammount
            ammount = ammount + 1
            await ctx.channel.purge(limit=ammount)
            await ctx.send(f"***✓*** Deleted {counter} messages!", delete_after=5)

    #locks channel that it was invoked in
    @commands.command(aliases=["lock", "toohorny"])
    @commands.has_guild_permissions(manage_guild=True)
    async def lockdown(self, ctx, time: int):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.channel.send(f"***✓*** Locked channel for {time} seconds!")
        await asyncio.sleep(time)
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)

#################################END OF ADMIN COG#####################################