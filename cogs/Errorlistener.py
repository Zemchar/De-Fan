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
             msg = '**✘** You are on cooldown! Please try again in {:.2f} seconds'.format(error.retry_after)
             await ctx.send(msg)
        if isinstance(error, commands.MissingRequiredArgument):
            msg = '**✘** One or more of the required arguments for that command are missing! Please resolve this and try again.'
            await ctx.send(msg, delete_after=10)
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
            await ctx.send(embed=embed)
        if isinstance(error, commands.BadArgument):
            msg = "**☠** Bad argument. You probably tried to punish a moderator or simply didnt format the argument correctly."
            await ctx.send(msg)
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(title="That command doesnt exist!", color=0xff0000)
