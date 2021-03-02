import discord 
import sys
import traceback
from cogs.listeners import filter
from cogs.music import Music
from cogs.moderation import moderationtools
from cogs.commands import fun
from cogs.Errorlistener import CommandErrorHandler
import asyncio
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
import time
import DiscordUtils
from cogs.listeners import infodictdefine
import datetime
import asyncio
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils import manage_commands 
from discord import CategoryChannel
class bcolors: #funny colors
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
#Change Bot Status
async def status_task():
    file = open("swagstatus.txt", "r+")
    statuschoiceorig = file.readlines()
    controller = True
    while controller == True:
      statuschoice = random.choice(statuschoiceorig)
      await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f"{statuschoice}"))
      statuschoiceorig = [x for x in statuschoiceorig if x != statuschoice] #list comprehension and removes the statuses as it needs too
      print(statuschoice)
      if len(statuschoiceorig) == 0: #Refils the list if its empty
        file = open("swagstatus.txt", "r+")
        statuschoiceorig = file.readlines()
      await asyncio.sleep(21600)

def get_prefix(client, message):  ##first we define get_prefix
  with open('prefixes.json', 'r') as f:  ##we open and read the prefixes.json, assuming it's in the same file
    prefixes = json.load(f)  #load the json as prefixes
    try:
      return prefixes[str(message.author.id)]  #recieve the prefix for the guild id given
    except:
      if message.guild.id == 664264869717213225:
        return "swag!"
      else:
        return "."

async def reset_keys():
  while True:
      now = time.localtime()
      current_time = time.strftime("%H:%M:%S", now)
      infodictdefine.inforeset()
      print(f"[{bcolors.WARNING}LISTENER INFO{bcolors.ENDC}] [{bcolors.HEADER}{current_time}{bcolors.ENDC}] Info Dictionary has been reset!")
      await asyncio.sleep(21600) 

#initial startup
bot = commands.Bot(command_prefix=get_prefix,status=discord.Status.dnd,activity=discord.Game(name="Getting Ready..."), intents=discord.Intents.all())
bot.remove_command("help")
slash = slash = SlashCommand(bot, sync_commands=True)
guild_ids=[807777602633728011, 577904583213449237, 664264869717213225]
#ready
@bot.event
async def on_ready():
  now = time.localtime()
  current_time = time.strftime("%H:%M:%S", now)
  print(f"[{bcolors.OKBLUE}SYSTEM INFO{bcolors.ENDC}] [{bcolors.HEADER}{current_time}{bcolors.ENDC}] Bot Ready! Logged in as De Fan")
  print(f"[{bcolors.WARNING}LISTENER INFO{bcolors.ENDC}] [{bcolors.HEADER}{current_time}{bcolors.ENDC}] Info Dictionary has been reset!")
  bot.loop.create_task(status_task())
  bot.loop.create_task(reset_keys())


#new help command
@bot.command(aliases=["h", "i", "info"])
async def help(ctx):
    with open('prefixes.json', 'r') as f:  ##we open and read the prefixes.json, assuming it's in the same file
      prefixes = json.load(f)  #load the json as prefixes
    try:
      user_prefix = prefixes[str(ctx.message.author.id)]  #recieve the prefix for the guild id given
    except:
      user_prefix = "."
    ping_ = bot.latency
    ping = round(ping_ * 1000) #convert to ms
    embed=discord.Embed(title="Help", description=f"Commands and Usage for {ctx.guild.me.display_name}", color=0x00ff75)
    embed.add_field(name="Prefixes", value="Default is `.`\nUse the `mp` command to set your own custom prefix!", inline=False)
    embed.add_field(name="Your Prefix:", value=f"`{user_prefix}`", inline=True)
    embed.add_field(name="Current Bot Latency:", value=f"**{ping}** ms", inline=True)
    embed2=discord.Embed(title="General Commands", description="Commands everyone can use!", color=0x00ff75)
    embed2.add_field(name="__***Commands***__", value="`help/h` - Displays this help message\n`ping` - Fetches the Latency of this bot\n`mp {new prefix}` - Changes *your* custom prefix. Can be anything\n`hjail @user` - sends a user to horny jail\n`kill @user` - kills a user\n`8ball {question}` - magic 8 ball\n`copypasta` - prints a random copypasta to chat\n`hug @user` - hugs a user\n`kiss @user` - kisses a user\n`uwu` - idek man\n`coin` - Flips a coin. Pretty simple\n`credits` - Credit to Team!\n`swagscale @user percent(optional)` - Rates a user on the swag meter:tm:\n`boobah` - gives you the link to the boobah game", inline=True)
    embed2.add_field(name="** **", value="`poll {time} \"{question, must be in quotation marks}\" \"{options, must be in quotation marks. Up to 27 options allowed}\"` - Creates a poll based on time. Quotation marks **MUST** be around all options besides the time.\n```diff\n+Yes: .poll 1 \"Test Poll\" \"option 1\"... (Up to 27 options)\n\n-No: .poll 1 question 1 option1 option 2 etc.\n```")
    embed3=discord.Embed(title="Administrator Commands", description="Modz only!! :sunglasses:", color=0x00ff75)
    embed3.add_field(name="__***Commands***__", value="\n`lockdown/lock {time}` - locks a channel for a specified amount of time\n`clear/purge {number}` - Clears specified number of messages from the channel. Only works for messages younger than two weeks.", inline=True)
    musicembed=discord.Embed(title="Music Commands", description=f"{ctx.guild.me.display_name} supports a music player! This is how to use it.", color=0x00ff75)
    musicembed.add_field(name="__***Commands***__", value="`p/play {song name/link}` - Plays the specified song\n`queue/q` - Show upcoming songs\n`skip/s` - Skips the current song\n`v/setvol/volume {number}` - Sets volume client side\n`loop` - Toggles the loop on the current song\n`eq/equalize {mode}` - Its an equalizer. Supported presets are:\n```diff\nflat - resets the equalizer\nboost - bass booster\nmetal - For rock songs\npiano - For piano songs\n```", inline=False)
    musicembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/710232673976582215.gif?v=1")
    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, timeout=30, auto_footer=True, remove_reactions=True)
    paginator.add_reaction('⏮️', 'first')
    paginator.add_reaction('⬅️', 'back')
    paginator.add_reaction('➡️', 'next')
    paginator.add_reaction('⏭️', 'last')
    embeds = [embed, embed2, embed3, musicembed]
    await paginator.run(embeds)


@slash.slash(
  name="Help",
  description="Need help? Use this command to see the Help Menu",
  options=None,
  guild_ids=guild_ids
)
async def help(ctx: SlashContext):
    with open('prefixes.json', 'r') as f:  ##we open and read the prefixes.json, assuming it's in the same file
      prefixes = json.load(f)  #load the json as prefixes
    try:
      user_prefix = prefixes[str(ctx.author.id)]  #recieve the prefix for the guild id given
    except:
      user_prefix = "."
    ping_ = bot.latency
    ping = round(ping_ * 1000) #convert to ms
    embed=discord.Embed(title="Help", description="Commands and Usage for De Fan", color=0x00ff75)
    embed.add_field(name="Prefixes", value="Default is `.`\nUse the `mp` command to set your own custom prefix!", inline=False)
    embed.add_field(name="Your Prefix:", value=f"`{user_prefix}`", inline=True)
    embed.add_field(name="Current Bot Latency:", value=f"**{ping}** ms", inline=True)
    embed2=discord.Embed(title="General Commands", description="Commands everyone can use!", color=0x00ff75)
    embed2.add_field(name="__***Commands***__", value="`help/h` - Displays this help message\n`ping` - Fetches the Latency of this bot\n`mp {new prefix}` - Changes *your* custom prefix. Can be anything\n`hjail @user` - sends a user to horny jail\n`kill @user` - kills a user\n`8ball {question}` - magic 8 ball\n`copypasta` - prints a random copypasta to chat\n`hug @user` - hugs a user\n`kiss @user` - kisses a user\n`uwu` - idek man\n`coin` - Flips a coin. Pretty simple\n`credits` - Credit to Team!\n`swagscale @user percent(optional)` - Rates a user on the swag meter:tm:\n`boobah` - gives you the link to the boobah game", inline=True)
    embed2.add_field(name="** **", value="`poll {time} \"{question, must be in quotation marks}\" \"{options, must be in quotation marks. Up to 27 options allowed}\"` - Creates a poll based on time. Quotation marks **MUST** be around all options besides the time.\n```diff\n+Yes: .poll 1 \"Test Poll\" \"option 1\"... (Up to 27 options)\n\n-No: .poll 1 question 1 option1 option 2 etc.\n```")
    embed3=discord.Embed(title="Administrator Commands", description="Modz only!! :sunglasses:", color=0x00ff75)
    embed3.add_field(name="__***Commands***__", value="\n`lockdown/lock {time}` - locks a channel for a specified amount of time\n`clear/purge {number}` - Clears specified number of messages from the channel. Only works for messages younger than two weeks.", inline=True)
    musicembed=discord.Embed(title="Music Commands", description="Defan now supports a music player! This is how to use it.", color=0x00ff75)
    musicembed.add_field(name="__***Commands***__", value="`p/play {song name/link}` - Plays the specified song\n`queue/q` - Show upcoming songs\n`skip/s` - Skips the current song\n`v/setvol/volume {number}` - Sets volume client side\n`loop` - Toggles the loop on the current song\n`eq/equalize {mode}` - Its an equalizer. Supported presets are:\n```diff\nflat - resets the equalizer\nboost - bass booster\nmetal - For rock songs\npiano - For piano songs\n```", inline=False)
    musicembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/710232673976582215.gif?v=1")
    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, timeout=30, auto_footer=True, remove_reactions=True)
    paginator.add_reaction('⏮️', 'first')
    paginator.add_reaction('⬅️', 'back')
    paginator.add_reaction('➡️', 'next')
    paginator.add_reaction('⏭️', 'last')
    embeds = [embed, embed2, embed3, musicembed]
    await paginator.run(embeds)

@bot.command(aliases=["prefix", "mp"])
async def myprefix(ctx, prefix):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  prefixes[str(ctx.message.author.id)] = prefix

  with open('prefixes.json','w') as f:  #writes the new prefix into the .json
    json.dump(prefixes, f, indent=4)

  now = time.localtime()
  current_time = time.strftime("%H:%M:%S", now)
  print(f"[{bcolors.WARNING}NON-CRITICAL ALERT{bcolors.ENDC}] [{bcolors.HEADER}{current_time}{bcolors.ENDC}] User {ctx.message.author.display_name} changed their prefix to [{bcolors.FAIL}{prefix}{bcolors.ENDC}]")
  await ctx.send(f'{ctx.message.author.mention} Your prefix was changed to: {prefix}') #confirms the prefix it's been changed to

@slash.slash(
  name="NewPrefix",
  description="Set your own custom prefix!",
  options=[manage_commands.create_option(
    name = "Prefix",
    description = "Prefix you want",
    option_type = 3,
    required = True
  )],
  guild_ids=guild_ids
)
async def myprefix(ctx: SlashContext, prefix): #ignore already defined warning, ide is a bitch
  author_id = ctx.author
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  prefixes[str(author_id)] = prefix

  with open('prefixes.json','w') as f:  #writes the new prefix into the .json
    json.dump(prefixes, f, indent=4)

  now = time.localtime()
  current_time = time.strftime("%H:%M:%S", now)
  print(f"[{bcolors.WARNING}NON-CRITICAL ALERT{bcolors.ENDC}] [{bcolors.HEADER}{current_time}{bcolors.ENDC}] User {ctx.message.author.display_name} changed their prefix to [{bcolors.FAIL}{prefix}{bcolors.ENDC}]")
  await ctx.send(f'{ctx.message.author.mention} Your prefix was changed to: {prefix}') #confirms the prefix it's been changed to


#fetch latency
@bot.command(aliases=["pong"])
@commands.cooldown(1, 2, commands.BucketType.user)
async def ping(ctx):
    ping_ = bot.latency
    ping = round(ping_ * 1000) #convert to ms
    now = time.localtime()
    current_time = time.strftime("%H:%M:%S", now)
    await ctx.channel.send(f"***✓*** Pong! The current ping of De Fan is {ping} ms")
    print(f"[{bcolors.OKBLUE}SYSTEM INFO{bcolors.ENDC}] [{bcolors.HEADER}{current_time}{bcolors.ENDC}] Ping requested.\nThe current latency is {ping} ms.")

@bot.listen('on_member_join')
async def newmember(member):#SW
    if member.guild.id == 664264869717213225:
        XXI = discord.utils.get(member.guild.categories, id=664264870656475156)    
        channel = bot.get_channel(XXI.channels.pop(0).id)    
        introduce = bot.get_channel(667178772381827072)
        roles = bot.get_channel(721462151184646254)
        await channel.send(f"Hey {member.mention}!" + f" Welcome to da swag house :fire: :sunglasses: Go to the pinned messages in {roles.mention} to give yourself pronoun, color, and other roles, and don't forget to introduce yourself in {introduce.mention}")
        await member.send(f"Hey {member.mention}!" + f" Welcome to da swag house :fire: :sunglasses: Go to the pinned messages in {roles.mention} to give yourself pronoun, color, and other roles, and don't forget to introduce yourself in {introduce.mention}")
    elif member.guild.id == 577904583213449237:#CC
      channel = bot.get_channel(577906129133109259)
      await channel.send(f"Welcome To {member.guild.name} {member.mention}. Feel free to say hi and poke around. Check the reaction roles channel to get some cool roles!")
    else:
      await member.send(f"Welcome To {member.guild.name} {member.mention}. Feel free to say hi and poke around.")

emojiLetters = [
            "\N{REGIONAL INDICATOR SYMBOL LETTER A}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER B}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER C}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER D}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER E}", 
            "\N{REGIONAL INDICATOR SYMBOL LETTER F}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER G}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER H}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER I}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER J}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER K}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER L}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER M}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER N}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER O}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER P}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Q}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER R}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER S}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER T}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER U}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER V}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER W}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER X}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Y}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Z}"]

@bot.command() #Simple polling command
async def poll(ctx, timeout_opt: int, question, *args):
  #poll init
  voters = []
  vote_counts = {}
  votecountpub = 0
  options = []
  react_to_option = {}
  description = ""
  for i, arg in enumerate(args): #this works because if you have 
    description += f"React with {emojiLetters[i]} + to cast your vote for ** {arg} **\n" #Enumerate through the options passed through the *arg argument.
    options.append(arg)
    react_to_option[emojiLetters[i]] = arg
  print(react_to_option)
  #Vote counter
  for option in options:
    vote_counts[option] = 0
  my_poll = discord.Embed(
    title = question,
    description = f"Hosted by {ctx.author.display_name}\n\n{description}",
    color=ctx.author.color,
    timestamp=datetime.datetime.utcnow()
    ) #embed creation. The timestamp will update on every vote effectively telling you when the last vote was cast.
  message = await ctx.send(embed = my_poll)
  start_time = datetime.datetime.now()

  for i, option in enumerate(options):
    await message.add_reaction(emojiLetters[i])
  # Get votes
  reaction = None
  # Ensure reaction is to the poll message and the reactor is not the bot
  def check(reaction, user): 
    return reaction.message.id == message.id and user.id != 763576957618618428 #THIS IS THE BOT ID, switch this out for 

  while True: # Exit after a certain time
    try:
      reaction, user = await bot.wait_for('reaction_add', timeout = 0.5, check = check)
      await message.remove_reaction(reaction, user)
      #Checks if the user has already voted
      if user not in voters:
        voters.append(user)
        votecountpub += 1
        vote_counts[react_to_option[reaction.emoji]] += 1
        my_poll.set_footer(text=f"Total votes: {votecountpub}")
        await message.edit(embed=my_poll)
      elif user in voters:
        await user.send("I appreciate the enthusiasm but you have already voted for that poll!")
    except asyncio.TimeoutError:
      if datetime.datetime.now() >= start_time + datetime.timedelta(seconds = timeout_opt): #checks for if the poll time has been reached
        break		
    
  # Send messages of results 
  print("done")
  results = ""
  for option in vote_counts:
    results += option + " - " + "**" + str(vote_counts[option]) +"**" + " Votes" + "\n"
  results_message = discord.Embed(
    title = f"Poll Ended!\n{question}",
    description = f"Hosted by {ctx.author.display_name}\n\n__**Results**__\n{results}",
    color=ctx.author.color,
    timestamp=datetime.datetime.utcnow()
    )
  await message.clear_reactions()
  await message.delete()
  await ctx.send(embed = results_message)

#More commands in COG FOLDER
#ATTACH COGS
bot.add_cog(CommandErrorHandler(bot)) #errorlistener.py
bot.add_cog(fun(bot)) #Commands.py
bot.add_cog(moderationtools(bot)) #moderation.py
bot.add_cog(filter(bot)) #This is not really a filter in all honesty
bot.add_cog(Music(bot))
###IMPORTANT####
bot.run("NzYzNTc2OTU3NjE4NjE4NDI4.X35udQ.g6S7RTkoVIKV4vIOHEW8X1_hj9E") #Keep this token private, discord will freak if you dont
###IMPORTANT###
