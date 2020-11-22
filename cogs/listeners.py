import discord 
import sys
import traceback
import asyncio
from async_timeout import timeout
from discord.ext import commands
from discord import message
from discord import Member
from discord import permissions
from discord import client
from discord.ext.commands import has_permissions, MissingPermissions, Cog, BucketType
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown)
from asyncio import sleep
import random
from random import choice
import math
import os
import datetime
from datetime import timezone, tzinfo, timedelta
import time


class filter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, ctx, message): #NOT FUNCTIONAL
        bannedwords = ["word1","word2","word3"] #Can be anything. Dont set it to filter something like "the"
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if any(word in message.content.lower() for word in bannedwords):
            await ctx.channel.send(f"__***One (1) message deleted for violating rule number one.***__\n{ctx.message.author.mention} has been muted.\nIf you find it so integral to your identity to be able to use slurs please note that its against the rules here. There is no immunity based of your sex, orintation, race, etc. If you dont like it feel free to leave.\n.**If this is a repeat offense expect to be banned or kicked.**")
            await ctx.message.author.add_roles(role)
            await message.delete(message)