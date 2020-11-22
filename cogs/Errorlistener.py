import discord 
import sys
import traceback
import asyncio
from async_timeout import timeout
from discord.ext import commands
from discord import message
from discord import Member
from discord import permissions
from discord.ext.commands import has_permissions, MissingPermissions, Cog, BucketType
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown)
from asyncio import sleep

class CommandErrorHandler(commands.Cog):
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
             msg = '**✘** Sorry, you are on cooldown! Please try again in {:.2f} seconds'.format(error.retry_after)
             await ctx.send(msg, delete_after=10)
        if isinstance(error, commands.MissingRequiredArgument):
            msg = '**✘** One or more of the required arguments for that command are missing! There is probably a cooldown (nothing I can do about that)'
            await ctx.send(msg, delete_after=10)
        if isinstance(error, commands.MissingPermissions):
            msg = "Sorry but you are not a moderator on this server and cannot use this command!"
            await ctx.send(msg)
        if isinstance(error, commands.BadArgument):
            msg = "**☠** Bad argument. Ill be honest I dont know what a \"bad argument\" is. Its just a thing that popped up in autocomplete so I added it. You probably messed *something* up."
            await ctx.send(msg, delete_after=10)
        if isinstance(error, commands.CommandNotFound):
            print("Error Raised: Invalid Command Called. No Matching Commands Found. This is most likely not a problem.")