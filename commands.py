import discord 
import sys
import traceback
from music import Music
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


class fun(commands.Cog):
    
    #litterally pastes boobah game to chat
    @commands.command
    async def boobah(self, ctx):
        await ctx.send("Boobah. <http://danryckert.eu/>")
    
    #horny jail command
    @commands.command(aliases=["hjail", "hornyjail"])
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def horny(self, ctx, user : discord.Member):
        if user == ctx.message.author:
            await ctx.channel.send(f"{ctx.message.author.mention} thank you for doing your part and acknowledging your hornyness, your time in horny jail has been lessened :chikaspin:.")
        else:
            await ctx.channel.send(f"{user.mention} has been banished to horny jail by {ctx.message.author.mention}! Think about what you did {user.mention}.",delete_after=10800)
    
    #kill command
    @commands.command(aliases=["gun"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def kill(self, ctx, user : discord.Member):
        killer = ctx.message.author.id
        if user == ctx.message.author:
            await ctx.channel.send(f"<@{killer}> commited suicide :weary:")
        if user.id == "675120283677622312":
            await ctx.channel.send(f"Shame on you <@{killer}> you cannont kill me!")
        if user != ctx.message.author:
            await ctx.channel.send(f"<@{killer}> killed {user.mention}", delete_after=10800 )
    
    #8Ball Command
    @commands.command(aliases=["8ball", "8ofcircles"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def _8ball(self, ctx, *, question): #responses - Seems to only like to reply positvly but it will work for now
        responses = ['It is certain', 
                    'It is decidedly so', 
                    'Without a doubt', 
                    'Yes, definitely',
                    'You may rely on it', 
                    'As I see it, yes', 
                    'Most likely',
                    'Outlook good',
                    'All Signs point to yes', 
                    'Hmm, I think so', 
                    'Stop mishandling me!', 
                    'Ask again later',
                    'I dont think im going to tell you.', 
                    'I honestly dont know', 
                    'Eh.. It seems that you have met a-a horrible demise my friend. But.. uh.. you know these.. These things happen in - in life. Life goes on. Not for you obviously uh youre dead but uh.. It reminds me of a time. I was - I was having a conversation with my friend Orville. We were uh.. we were.. - the river. We were sitting by the river watching the fish leap over the falls and I said to Orville: Sometimes I feel like a fish leaping over and over again always trying to get somewhere. No I dont know where...or only to find to find myself in the jaws of a beast. He of course looked at me.. eh.. surprised you know? Have you been in the jaws of a beast friend? To which I said No of course not Orville. I said No no no no no. I simply meant that life can seem like a relentless endeavor... Overcome meaningless obstacles only to meet an equally meaningless fate regardless of your efforts. Regardless of the obstacles youve passed. And.. uh.. Orville he stood and proceeded to drape me with a picnic cloth to which I asked him I said Friend what - what are you doing? He looked at me... very concerned really. I feel like youve gotten too much sun. Indeed heh. Indeed I had. He proceeded to pour me a glass of... just… ice-cold lemonade... Ooh. Ever mix it with iced tea? I do like... little half-lemonade half-...oh its so - you should try it someti- oh wait. You cant because youre dead. But anyways...So you may be asking yourself How did I go from sitting by the falls to drinking lemonade to being wedged in the air duct? Not only with Orville but with an entire assortment of fruity colored friends. Well theres.. uh.. Theres really no good answer to that but perhaps Ive met a demise of my own at some point and this is my afterlife or my dream - whatever it might be. I honestly dont know... Or... Maybe it doesnt mean anything at all. Maybe it doesnt mean anything at all.',
                    "Don't bet on it", 
                    'gun.', 
                    'My sources say no', 
                    'Outlook not so good',
                    'Very doubtful']
        await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}\nAsked by {ctx.message.author.mention}", delete_after=10800)

    #copypasta command
    @commands.command(aliases=["givemesomepasta"])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def copypasta(self, ctx,):
    #possible responses
    #list can be extended
        responses = [ 'Eh.. It seems that you have met a-a horrible demise my friend. But.. uh.. you know these.. These things happen in - in life. Life goes on. Not for you obviously uh youre dead but uh.. It reminds me of a time. I was - I was having a conversation with my friend Orville. We were uh.. we were.. - the river. We were sitting by the river watching the fish leap over the falls and I said to Orville: Sometimes I feel like a fish leaping over and over again always trying to get somewhere. No I dont know where...or only to find to find myself in the jaws of a beast. He of course looked at me.. eh.. surprised you know? Have you been in the jaws of a beast friend? To which I said No of course not Orville. I said No no no no no. I simply meant that life can seem like a relentless endeavor... Overcome meaningless obstacles only to meet an equally meaningless fate regardless of your efforts. Regardless of the obstacles youve passed. And.. uh.. Orville he stood and proceeded to drape me with a picnic cloth to which I asked him I said Friend what - what are you doing? He looked at me... very concerned really. I feel like youve gotten too much sun. Indeed heh. Indeed I had. He proceeded to pour me a glass of... just… ice-cold lemonade... Ooh. Ever mix it with iced tea? I do like... little half-lemonade half-...oh its so - you should try it someti- oh wait. You cant because youre dead. But anyways...So you may be asking yourself How did I go from sitting by the falls to drinking lemonade to being wedged in the air duct? Not only with Orville but with an entire assortment of fruity colored friends. Well theres.. uh.. Theres really no good answer to that but perhaps Ive met a demise of my own at some point and this is my afterlife or my dream - whatever it might be. I honestly dont know... Or... Maybe it doesnt mean anything at all. Maybe it doesnt mean anything at all.',
                    "Son.. son come closer. Sure sure what is it dad hmmmm? I just wanted to tell you that the secret to my long life is this gem *shocking thump sound effect* and if you touch it i will die so **dont** touch it i just i just wanted to tell you that. Alright. *touches gem* *melts*",
                    "Based? Based on what? In your dick? Please shut the fuck up and use words properly you fuckin troglodyte, do you think God gave us a freedom of speech just to spew random words that have no meaning that doesn't even correllate to the topic of the conversation? Like please you always complain about why no one talks to you or no one expresses their opinions on you because you're always spewing random shit like poggers based cringe and when you try to explain what it is and you just say that it's funny like what? What the fuck is funny about that do you think you'll just become a stand-up comedian that will get a standing ovation just because you said cum in the stage? HELL NO YOU FUCKIN IDIOT, so please shut the fuck up and use words properly you dumb bitch",
                    "I will end your life, career, and testicles, dont talk to me like that I came from the streets of the park you dumb bitch, I got peopleand gorrilas, geese, pigeons , and frogs these are people you dont wanna mess with okay. They will heck you up you stupid whore they will steal your money, clothes, and signifigant other Ok dont talk shit about my grapes my child is undergoing chemotherapy and the last thing he wanted was some grapes that was what he asked the make a wish foundation to do but you dont care all you care about is your 9-5 deadend job that will only feed into your miserable life so you can go home to your small house and small penis so let me have some motherfucking grapes jerry or I will take your spleen and eat it",
                    "I, evax humbly submit a toast to Nicholas Alexander, for successfully managing to pirate Warcraft 3, so that he may play defense of the ancients, congratulations nick, enjoy your dota. ***Big sip***",
                    "你是內內個 內內 內個內個 內內 nǐ shì nèi nèi gè nèi nèi nèi gè nèi gè nèi nèi 內內個 內內 內個內個 內內 nèi nèi gè nèi nèi nèi gè nèi gè nèi nèi 陽光彩虹小白馬 滴滴噠滴滴噠 yángguāng cǎihóng xiǎo báimǎ dī dī dā dī dī dā",
                    "Sometimes, when I close my eyes in bed, I see apes flash for like a split second. They are not spoopy or anything. Just a random monkey that I've never seen before. Sometimes it's not just the ape but like a whole scene with bananas and big honkin worms and stuff. Like a screenshot from King Kong (2005) except it can be a gibbon or a macaque and often playing big coconut bongos. The fuck is that all about?",
                    "Oh it's that time again So grab your tablet pen I said what's with you She said shut up and osu! with me This woman has my melody She said Ooh~ Shut up and osu! with me We were victims of Peppy Way that dude codes this game is just too sweet Helpless to the circles and the groovy beat Oh may this game live on forever! May osu! live on forever! She took my hand My God I felt so lewd We jumped to multi and she said Just let the beat sink in And grab your tablet pen I said you're full of hacks She said shut up and osu! with me This woman has my melody She said Ooh~ Shut up and osu! with me A tablet playing chick who could follow the beat My bride to be anime waifu dream I felt something lewd when she looked at me Ohh we were bound to play together Bound to osu! forever She took my hand My God I felt so lewd We jumped to multi and she said Just let the beat sink in And grab your tablet pen I said you're full of hacks She said shut up and osu! with me This woman has my melody She said Ooh~ Shut up and osu! with me Cursor dance! This can't be right I think I've fallen for her Must be a lie But my heart screams yes She took my hand My God I felt so lewd We jumped to multi and she said Just let the beat sink in And grab your tablet pen I said you're full of hacks She said shut up and osu! with me This woman has my melody She said Ooh~ Shut up and osu! Let the beat sink in And grab your tablet pen I said you're full of hacks She said shut up and osu! with me This woman has my melody She said Ooh~ Shut up and osu! with me Ooh~ Shut up and osu! with me Ooh~ Shut up and osu! with me",
                    "This is infuriating. Everyone stop. This conversation, it serves no purpose therefore this conversation is useless. No one cares whatever the fuck is going on here, I know that I certainly don't."]
        await ctx.channel.purge(limit=1)
        await ctx.send(f"Here is your delicious pasta {ctx.message.author.mention}.\n{random.choice(responses)}", delete_after=10800 )


