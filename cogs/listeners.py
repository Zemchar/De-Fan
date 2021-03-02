import discord 
import asyncio
from discord.ext import commands
from discord import message
from discord import Member as member
from discord import permissions
from discord import client
from discord.ext.commands import has_permissions, MissingPermissions, Cog, BucketType
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown)
from asyncio import sleep
import json
import aiohttp
import io
import datetime as dt
import time
import random
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class infodictdefine:
    
    def inforeset(self=None, yes=True):
        global info
        info = {}

    def colorpicker(self=None, yes=True):
        choices = [0x330033, 0x00ff00, 0xff80ff, 0x330066, 0x281e68, 0x470093]
        global colorpicked
        colorpicked = random.choice(choices)

class filter(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        infodictdefine.inforeset()
        global e
        global pollstarted
        pollstarted = False
    
    @commands.Cog.listener()
    async def on_ready(self):
        now = time.localtime()
        current_time = time.strftime("%H:%M:%S", now)
        print(f"[{bcolors.WARNING}LISTENER INFO{bcolors.ENDC}] [{bcolors.HEADER}{current_time}{bcolors.ENDC}] Info Dictionary has been reset!") 

    @commands.Cog.listener()
    async def on_message(self, message):
        global info
        global e
#SO THIS IS SUPER FUCKING DUMB BUT MY FREINDS WANTED ME TO DO IT SO HERE I AM
#Cringe/Meta/Satire scores on any image posted in a certain channel 
        infodictdefine.colorpicker()
        e = discord.Embed(title="Scores!", color=colorpicked, timestamp=dt.datetime.utcnow())
        e.add_field(name="Cringe Score:", value="Unrated", inline=True)
        e.add_field(name="Meta Score:", value="Unrated", inline=True)
        e.add_field(name="Satire Score:", value="Unrated", inline=True)
        now = time.localtime()
        current_time = time.strftime("%H:%M:%S", now)
        cringechannelid = self.bot.get_channel(801594194887704596)
        bannedwords = ["BadWords","Badword2","Bad word"] #Can be anything. Dont set it to filter something like "the"
        newcringescore = "Unrated"
        newmetascore = "Unrated"
        newsatscore = "Unrated"
        e.set_field_at(1, name="Meta Score:", value=f"{newmetascore}")
        e.set_field_at(0, name="Cringe Score:", value=f"{newcringescore}")
        e.set_field_at(2, name="Satire Score:", value=f"{newsatscore}")
        reddit = ["reddit", "r/"]
        if any(word in message.content.lower() for word in bannedwords): #Filter
            member = message.author
            modrole = message.guild.get_role(793711872313917450) 
            await message.channel.purge(limit=1)
            await message.channel.send(f"{modrole.mention}\n{message.author.mention} Said a bad word!")
        elif message.content == "<@!763576957618618428>": #idfk why this has to be this way but it does.
            with open('prefixes.json', 'r') as f:  #this function will return the current prefix if its been defined by the user or return one of the defaults if the user mentions the bot and only the bot in the message 
                prefixes = json.load(f)  #load the json as prefixes
            try:
                prefix = prefixes[str(message.author.id)]  #recieve the prefix for the guild id given
            except:
                prefix = "."
            embed=discord.Embed(title=f"Dont worry, its not a problem!\nUse `{prefix}mp <newprefix>` to change it :)\n", color=message.author.color)
            embed.set_author(name="You forgot your prefix didn't you?")
            embed.add_field(name="Your Current Prefix:", value=f"`{prefix}`", inline=True)
            await message.channel.send(embed=embed)
        elif any(word in message.content.lower() for word in reddit):
            await message.channel.send(file=discord.File('redditor.png'))
        elif message.channel == cringechannelid:
            if message.author.bot:
                pass
            else:
                if message.attachments:
                    if message.attachments[0].url.endswith('PNG') or message.attachments[0].url.endswith('JPG') or message.attachments[0].url.endswith('JPEG') or message.attachments[0].url.endswith('png') or message.attachments[0].url.endswith('jpg') or message.attachments[0].url.endswith('jpeg'):
                        cringeemoji = discord.utils.get(message.guild.emojis, name='cringe')
                        satireemoji = discord.utils.get(message.guild.emojis, name='satire')
                        metaemoji = discord.utils.get(message.guild.emojis, name='meta')
                        FurlList = message.attachments[0]
                        Furl = FurlList.url
                        OP = message.author
                        async with aiohttp.ClientSession() as session:
                            async with session.get(Furl) as resp:
                                if resp.status != 200:
                                    return await message.channel.send('Could not download file...')
                                data = io.BytesIO(await resp.read())
                                await message.channel.purge(limit=1)
                                if message.content == "":
                                    try:
                                        file=discord.File(data, filename='coolimage.png')
                                    except:
                                        file=discord.File('Failure.png')
                                    msg = await message.channel.send(f"OP: {OP.mention}", file=file, embed=e)
                                else:
                                    try:
                                        file=discord.File(data, filename='coolimage.png')
                                    except discord.errors.HTTPException:
                                        file=discord.File('Failure.png')
                                        e.set_image(url="attachment://Failure.png")
                                    e.add_field(name="Message:", value=f"{message.clean_content}")
                                    msg = await message.channel.send(f"OP: {OP.mention}", file=file, embed=e)
                        id = msg.id
                        info.update({id: {"cringe": 0, "satire": 0, "meta": 0}})
                        await msg.add_reaction(cringeemoji)
                        await msg.add_reaction(metaemoji)
                        await msg.add_reaction(satireemoji)
                        print(f"[{bcolors.OKCYAN}LISTENER INFO{bcolors.ENDC}] [{bcolors.HEADER}{current_time}{bcolors.ENDC}] New Post In Cringe Channel.\n{bcolors.WARNING}Assignments:{bcolors.ENDC} {info}")
                    if message.attachments[0].url.endswith("GIF") or message.attachments[0].url.endswith("gif"):
                        cringeemoji = discord.utils.get(message.guild.emojis, name='cringe')
                        satireemoji = discord.utils.get(message.guild.emojis, name='satire')
                        metaemoji = discord.utils.get(message.guild.emojis, name='meta')
                        FurlList = message.attachments[0]
                        Furl = FurlList.url
                        OP = message.author
                        async with aiohttp.ClientSession() as session:
                            async with session.get(Furl) as resp:
                                if resp.status != 200:
                                    return await message.channel.send('Could not download file...')
                                data = io.BytesIO(await resp.read())
                                await message.channel.purge(limit=1)
                                if message.content == "":
                                    try:
                                        file=discord.File(data, filename='coolimage.gif')
                                    except:
                                        file=discord.File('Failure.png')
                                    msg = await message.channel.send(f"OP: {OP.mention}", file=file, embed=e)
                                else:
                                    try:
                                        file=discord.File(data, filename='coolimage.gif')
                                    except discord.errors.HTTPException:
                                        file=discord.File('Failure.png')
                                    e.add_field(name="Message:", value=f"{message.clean_content}")
                                    msg = await message.channel.send(f"OP: {OP.mention}", file=file, embed=e)
                        id = msg.id
                        info.update({id: {"cringe": 0, "satire": 0, "meta": 0}})
                        await msg.add_reaction(cringeemoji)
                        await msg.add_reaction(metaemoji)
                        await msg.add_reaction(satireemoji)
                        print(f"[{bcolors.OKCYAN}LISTENER INFO{bcolors.ENDC}] [{bcolors.HEADER}{current_time}{bcolors.ENDC}] New Post In Cringe Channel. (GIF TYPE)\n{bcolors.WARNING}Assignments:{bcolors.ENDC} {info}")
                    elif message.attachments[0].url.endswith('MOV') or message.attachments[0].url.endswith('mov') or message.attachments[0].url.endswith('MP4') or message.attachments[0].url.endswith('webm') or message.attachments[0].url.endswith('avi') or message.attachments[0].url.endswith('mp4') or message.attachments[0].url.endswith('AVI') or message.attachments[0].url.endswith('WEBM'):
                        cringeemoji = discord.utils.get(message.guild.emojis, name='cringe')
                        satireemoji = discord.utils.get(message.guild.emojis, name='satire')
                        metaemoji = discord.utils.get(message.guild.emojis, name='meta')
                        FurlList = message.attachments[0]
                        Furl = FurlList.url
                        OP = message.author
                        async with aiohttp.ClientSession() as session:
                            async with session.get(Furl) as resp:
                                if resp.status != 200:
                                    return await message.channel.send('Could not download file...')
                                data = io.BytesIO(await resp.read())
                                await message.channel.purge(limit=1)
                                if message.content == "":
                                    try:
                                        file=discord.File(data, filename='coolimage.mp4')
                                    except:
                                        file=discord.File('Failure.png')
                                        e.set_image(url="attachment://Failure.png")
                                    msg = await message.channel.send(f"OP: {OP.mention}", file=file, embed=e)
                                else:
                                    try:
                                        file=discord.File(data, filename='coolimage.mp4')
                                    except discord.errors.HTTPException:
                                        file=discord.File('Failure.png')
                                    e.add_field(name="Message:", value=f"{message.clean_content}")
                                    msg = await message.channel.send(f"OP: {OP.mention}", file=file, embed=e)
                        id = msg.id
                        info.update({id: {"cringe": 0, "satire": 0, "meta": 0}})
                        await msg.add_reaction(cringeemoji)
                        await msg.add_reaction(metaemoji)
                        await msg.add_reaction(satireemoji)
                        print(f"[{bcolors.OKCYAN}LISTENER INFO{bcolors.ENDC}] [{bcolors.HEADER}{current_time}{bcolors.ENDC}] New Post In Cringe Channel. (GIF TYPE)\n{bcolors.WARNING}Assignments:{bcolors.ENDC} {info}")
                elif message.content != "":
                    OP = message.author
                    await message.channel.purge(limit=1)
                    await OP.send(f"Messages are not allowed in {message.channel.mention}! Please post an image next time!")
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        global info
        global e
        guild = discord.utils.find(lambda g : g.id == payload.guild_id, self.bot.guilds)
        cringeemoji = discord.utils.get(guild.emojis, name="cringe")
        satireemoji = discord.utils.get(guild.emojis, name='satire')
        metaemoji = discord.utils.get(guild.emojis, name='meta')
        if payload.channel_id == 801594194887704596: #Change this to fit whatever channel you want
            if payload.member.id != 763576957618618428: #change this to the id of your bot 
                if payload.emoji == cringeemoji:#cringe emoji
                    cid = payload.channel_id
                    channel = self.bot.get_channel(cid)
                    id = payload.message_id
                    msg = await channel.fetch_message(id)
                    info[id]['cringe'] += 1
                if payload.emoji == metaemoji:#Meta emoji
                    cid = payload.channel_id
                    channel = self.bot.get_channel(cid)
                    id = payload.message_id
                    msg = await channel.fetch_message(id)
                    info[id]['meta'] += 1
                if payload.emoji == satireemoji:#Meta emoji
                    cid = payload.channel_id
                    channel = self.bot.get_channel(cid)
                    id = payload.message_id
                    msg = await channel.fetch_message(id)
                    info[id]['satire'] += 1
                try:           
                    cid = payload.channel_id
                    channel = self.bot.get_channel(cid)
                    id = payload.message_id
                    msg = await channel.fetch_message(id)
                    newcringescore = round(100.0 * (info[id]["cringe"] / (info[id]["cringe"] + info[id]["satire"] + info[id]["meta"])))
                    newmetascore = round(100.0 * (info[id]["meta"] / (info[id]["cringe"] + info[id]["satire"] + info[id]["meta"])))
                    newsatscore = round(100.0 * (info[id]["satire"] / (info[id]["cringe"] + info[id]["satire"] + info[id]["meta"])))
                    e.set_field_at(1, name="Meta Score:", value=f"{newmetascore}%")
                    e.set_field_at(0, name="Cringe Score:", value=f"{newcringescore}%")
                    e.set_field_at(2, name="Satire Score:", value=f"{newsatscore}%")
                    await msg.edit(embed=e)
                except ZeroDivisionError:
                    newcringescore = "Unrated"
                    newmetascore = "Unrated"
                    newsatscore = "Unrated"
                    e.set_field_at(1, name="Meta Score:", value=f"{newmetascore}")
                    e.set_field_at(0, name="Cringe Score:", value=f"{newcringescore}")
                    e.set_field_at(2, name="Satire Score:", value=f"{newsatscore}")
                    await msg.edit(embed=e)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        global info
        global e
        guild = discord.utils.find(lambda g : g.id == payload.guild_id, self.bot.guilds)
        cringeemoji = discord.utils.get(guild.emojis, name="cringe")
        satireemoji = discord.utils.get(guild.emojis, name='satire')
        metaemoji = discord.utils.get(guild.emojis, name='meta')
        if payload.channel_id == 801594194887704596: #change these things according to above
            if payload.member != self.bot.get_user(763576957618618428): #Apperently this has to be here cause of a dumb nonetype error otherwise
                if payload.emoji == cringeemoji:#cringe emoji
                    cid = payload.channel_id
                    channel = self.bot.get_channel(cid)
                    id = payload.message_id
                    msg = await channel.fetch_message(id)
                    info[id]['cringe'] -= 1
                if payload.emoji == metaemoji:#Meta emoji
                    cid = payload.channel_id
                    channel = self.bot.get_channel(cid)
                    id = payload.message_id
                    msg = await channel.fetch_message(id)
                    info[id]['meta'] -= 1
                if payload.emoji == satireemoji:#Meta emoji
                    cid = payload.channel_id
                    channel = self.bot.get_channel(cid)
                    id = payload.message_id
                    msg = await channel.fetch_message(id)
                    info[id]['satire'] -= 1
                try:         
                    cid = payload.channel_id
                    channel = self.bot.get_channel(cid)
                    id = payload.message_id
                    msg = await channel.fetch_message(id)  
                    newcringescore = round(100.0 * (info[id]["cringe"] / (info[id]["cringe"] + info[id]["satire"] + info[id]["meta"])))
                    newmetascore = round(100.0 * (info[id]["meta"] / (info[id]["cringe"] + info[id]["satire"] + info[id]["meta"])))
                    newsatscore = round(100.0 * (info[id]["satire"] / (info[id]["cringe"] + info[id]["satire"] + info[id]["meta"])))
                    e.set_field_at(1, name="Meta Score:", value=f"{newmetascore}%")
                    e.set_field_at(0, name="Cringe Score:", value=f"{newcringescore}%")
                    e.set_field_at(2, name="Satire Score:", value=f"{newsatscore}%")
                    await msg.edit(embed=e)
                except ZeroDivisionError:
                    newcringescore = "Unrated"
                    newmetascore = "Unrated"
                    newsatscore = "Unrated"
                    e.set_field_at(1, name="Meta Score:", value=f"{newmetascore}")
                    e.set_field_at(0, name="Cringe Score:", value=f"{newcringescore}")
                    e.set_field_at(2, name="Satire Score:", value=f"{newsatscore}")
                    await msg.edit(embed=e)
# ''''