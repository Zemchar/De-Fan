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
import random
from random import choice
import math
import os
import datetime
from datetime import timezone, tzinfo, timedelta
import time


class fun(commands.Cog):
    #litterally pastes boobah game to chat
    @commands.command(aliases=["Boobah"])
    async def boobah(self, ctx):
        await ctx.send("Boobah.\n<http://danryckert.eu/>")

    #horny jail command
    @commands.command(aliases=["hjail", "hornyjail"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def horny(self, ctx, user : discord.Member):
        if user == ctx.message.author:
            await ctx.channel.send(f"{ctx.message.author.mention} thank you for doing your part and acknowledging your hornyness, your time in horny jail has been lessened.")
        else:
            await ctx.channel.send(f"{user.mention} has been banished to horny jail by {ctx.message.author.mention}! Stop being horny {user.mention}.")
    
    #kill command
    @commands.command(aliases=["murder"])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def kill(self, ctx, user : discord.Member):
        if user == ctx.message.author:
            await ctx.channel.send(f"{ctx.message.author.mention} commited suicide :weary:")
        if user.id == 763576957618618428:
            await ctx.channel.send(f"No.")
        if user != ctx.message.author:
            await ctx.channel.send(f"{ctx.message.author.mention} killed {user.mention}")
    
    @commands.command(aliases=["Shoot"])
    async def gun(self, ctx, user : discord.Member):
        if user == ctx.message.author:
            await ctx.channel.send(f"{ctx.message.author.mention} gunned themselves :banned::pensive:")
        if user.id == 763576957618618428:
            await ctx.channel.send(f":menacing:                                                            :menacing:\n:menacing: I wouldnt do that If I were you... :menacing:\n:menacing:                                                            :menacing:")
        if user != ctx.message.author:
            await ctx.channel.send(f"{ctx.message.author.mention} gunned {user.mention}")
    
    #8Ball Command
    @commands.command(aliases=["8ball", "8ofcircles"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _8ball(self, ctx, *, question): #responses - Seems to only like to reply positvly but it will work for now
        responses = ['It is certain', 
                    'It is decidedly so', 
                    "no", 
                    'Yes, definitely',
                    'You may rely on it', 
                    'As I see it, yes', 
                    'Most likely',
                    'Outlook good',
                    'All Signs point to yes', 
                    'Hmm, I think so', 
                    'So fuck you and fuck off, and leave me to my lotions. **SMACKS TABLE** oop the floor just cracked i belive i might fa-', 
                    'Ask again later',
                    'I dont think im going to tell you.', 
                    'I honestly dont know', 
                    'Eh.. It seems that you have met a-a horrible demise my friend. But.. uh.. you know these.. These things happen in - in life. Life goes on. Not for you obviously uh youre dead but uh.. It reminds me of a time. I was - I was having a conversation with my friend Orville. We were uh.. we were.. - the river. We were sitting by the river watching the fish leap over the falls and I said to Orville: Sometimes I feel like a fish leaping over and over again always trying to get somewhere. No I dont know where...or only to find to find myself in the jaws of a beast. He of course looked at me.. eh.. surprised you know? Have you been in the jaws of a beast friend? To which I said No of course not Orville. I said No no no no no. I simply meant that life can seem like a relentless endeavor... Overcome meaningless obstacles only to meet an equally meaningless fate regardless of your efforts. Regardless of the obstacles youve passed. And.. uh.. Orville he stood and proceeded to drape me with a picnic cloth to which I asked him I said Friend what - what are you doing? He looked at me... very concerned really. I feel like youve gotten too much sun. Indeed heh. Indeed I had. He proceeded to pour me a glass of... just… ice-cold lemonade... Ooh. Ever mix it with iced tea? I do like... little half-lemonade half-...oh its so - you should try it someti- oh wait. You cant because youre dead. But anyways...So you may be asking yourself How did I go from sitting by the falls to drinking lemonade to being wedged in the air duct? Not only with Orville but with an entire assortment of fruity colored friends. Well theres.. uh.. Theres really no good answer to that but perhaps Ive met a demise of my own at some point and this is my afterlife or my dream - whatever it might be. I honestly dont know... Or... Maybe it doesnt mean anything at all. Maybe it doesnt mean anything at all.',
                    "Don't bet on it", 
                    'gun.', 
                    'My sources say no', 
                    'Outlook not so good',
                    'Very doubtful',
                    'troll',
                    "Uh probably",]
        await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}\nAsked by {ctx.message.author.mention}")

    #copypasta command
    @commands.command(aliases=["givemesomepasta"])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def copypasta(self, ctx):
    #possible responses
    #list can be extended
        responses = [ 'Eh.. It seems that you have met a-a horrible demise my friend. But.. uh.. you know these.. These things happen in - in life. Life goes on. Not for you obviously uh youre dead but uh.. It reminds me of a time. I was - I was having a conversation with my friend Orville. We were uh.. we were.. - the river. We were sitting by the river watching the fish leap over the falls and I said to Orville: Sometimes I feel like a fish leaping over and over again always trying to get somewhere. No I dont know where...or only to find to find myself in the jaws of a beast. He of course looked at me.. eh.. surprised you know? Have you been in the jaws of a beast friend? To which I said No of course not Orville. I said No no no no no. I simply meant that life can seem like a relentless endeavor... Overcome meaningless obstacles only to meet an equally meaningless fate regardless of your efforts. Regardless of the obstacles youve passed. And.. uh.. Orville he stood and proceeded to drape me with a picnic cloth to which I asked him I said Friend what - what are you doing? He looked at me... very concerned really. I feel like youve gotten too much sun. Indeed heh. Indeed I had. He proceeded to pour me a glass of... just… ice-cold lemonade... Ooh. Ever mix it with iced tea? I do like... little half-lemonade half-...oh its so - you should try it someti- oh wait. You cant because youre dead. But anyways...So you may be asking yourself How did I go from sitting by the falls to drinking lemonade to being wedged in the air duct? Not only with Orville but with an entire assortment of fruity colored friends. Well theres.. uh.. Theres really no good answer to that but perhaps Ive met a demise of my own at some point and this is my afterlife or my dream - whatever it might be. I honestly dont know... Or... Maybe it doesnt mean anything at all. Maybe it doesnt mean anything at all.',
                    "Son.. son come closer. Sure sure what is it dad hmmmm? I just wanted to tell you that the secret to my long life is this gem *shocking thump sound effect* and if you touch it i will die so **dont** touch it i just i just wanted to tell you that. Alright. *touches gem* *melts*",
                    "Based? Based on what? In your dick? Please shut the fuck up and use words properly you fuckin troglodyte, do you think God gave us a freedom of speech just to spew random words that have no meaning that doesn't even correllate to the topic of the conversation? Like please you always complain about why no one talks to you or no one expresses their opinions on you because you're always spewing random shit like poggers based cringe and when you try to explain what it is and you just say that it's funny like what? What the fuck is funny about that do you think you'll just become a stand-up comedian that will get a standing ovation just because you said cum in the stage? HELL NO YOU FUCKIN IDIOT, so please shut the fuck up and use words properly you dumb bitch",
                    "I will end your life, career, and testicles, dont talk to me like that I came from the streets of the park you dumb bitch, I got peopleand gorrilas, geese, pigeons , and frogs these are people you dont wanna mess with okay. They will heck you up you stupid whore they will steal your money, clothes, and signifigant other Ok dont talk shit about my grapes my child is undergoing chemotherapy and the last thing he wanted was some grapes that was what he asked the make a wish foundation to do but you dont care all you care about is your 9-5 deadend job that will only feed into your miserable life so you can go home to your small house and small penis so let me have some motherfucking grapes jerry or I will take your spleen and eat it",
                    "I, evax humbly submit a toast to Nicholas Alexander, for successfully managing to pirate Warcraft 3, so that he may play defense of the ancients, congratulations nick, enjoy your dota. ***Big sip***",
                    "Sometimes, when I close my eyes in bed, I see apes flash for like a split second. They are not spoopy or anything. Just a random monkey that I've never seen before. Sometimes it's not just the ape but like a whole scene with bananas and big honkin worms and stuff. Like a screenshot from King Kong (2005) except it can be a gibbon or a macaque and often playing big coconut bongos. The fuck is that all about?",
                    "Oh it's that time again So grab your tablet pen I said what's with you She said shut up and osu! with me This woman has my melody She said Ooh~ Shut up and osu! with me We were victims of Peppy Way that dude codes this game is just too sweet Helpless to the circles and the groovy beat Oh may this game live on forever! May osu! live on forever! She took my hand My God I felt so lewd We jumped to multi and she said Just let the beat sink in And grab your tablet pen I said you're full of hacks She said shut up and osu! with me This woman has my melody She said Ooh~ Shut up and osu! with me A tablet playing chick who could follow the beat My bride to be anime waifu dream I felt something lewd when she looked at me Ohh we were bound to play together Bound to osu! forever She took my hand My God I felt so lewd We jumped to multi and she said Just let the beat sink in And grab your tablet pen I said you're full of hacks She said shut up and osu! with me This woman has my melody She said Ooh~ Shut up and osu! with me Cursor dance! This can't be right I think I've fallen for her Must be a lie But my heart screams yes She took my hand My God I felt so lewd We jumped to multi and she said Just let the beat sink in And grab your tablet pen I said you're full of hacks She said shut up and osu! with me This woman has my melody She said Ooh~ Shut up and osu! Let the beat sink in And grab your tablet pen I said you're full of hacks She said shut up and osu! with me This woman has my melody She said Ooh~ Shut up and osu! with me Ooh~ Shut up and osu! with me Ooh~ Shut up and osu! with me",
                    "This is infuriating. Everyone stop. This conversation, it serves no purpose therefore this conversation is useless. No one cares whatever the fuck is going on here, I know that I certainly don't."]
        await ctx.send(f"Here is your delicious pasta {ctx.message.author.mention}.\n{random.choice(responses)}",)
    
    @commands.command(aliases=["Hug"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def hug(self, ctx, user : discord.Member):
        if user != ctx.message.author:
            await ctx.channel.send(f"{ctx.message.author.mention} gives you hugs {user.mention}（っ・∀・）っ ⊂(・ヮ・⊂)")
        if user == ctx.message.author:
            await ctx.channel.send(f"{ctx.message.author.mention} hugs themself.")
    @commands.command(aliases=["muah"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def kiss(self, ctx, user : discord.Member):
        if user != ctx.message.author:
            await ctx.channel.send(f"{ctx.message.author.mention} kisses {user.mention} :eyes:!")
        if user == ctx.message.author:
            await ctx.channel.send(f"{ctx.message.author.mention} kisses themself. What a lonely chap. Everybody laugh at this idot")
    
    @commands.command(aliases=["fuck", "seks"]) #I dont know what this is. Someone sent me a code snippet and i just put it in
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def uwu(self, ctx):
        responses =  ["*Looks away nervously*\nY-you want to take this to the dms??",
                        "No dont start",
                        "owo",
                        "{",
                        "Perish",
                        "elfl",
                        "is a furry",
                        "Im not into you like that... sorry.",
                        "are you really *that* into bots?"]
        await ctx.send(f"{ctx.message.author.mention} {random.choice(responses)}")

    @commands.command(aliases=["gamble"])
    @commands.cooldown(1,10, commands.BucketType.user)
    async def coin(self, ctx):
        #The reason for all these responses is to create a weighted chance without actually creating weighted chance
        responses = ["Heads", "Tails", "Heads", "Tails", "Heads", "Tails", "Heads", "Tails", "Heads", "Tails", "Heads", "Tails", "Heads", "Tails", "Heads", "Tails", "Heads", "Tails", "Heads", "Tails", "Heads", "Tails", "Heads", "Tails", "Heads", "Tails", "Heads", "Tails", "Heads", "Tails", "Heads", "Tails", "Heads", "Tails", "Heads", "Tails", "Singularity", "Edge", "Heads", "Tails", "Heads", "Tails", "Heads", "Tails", "Heads", "Tails", ]
        response = random.choice(responses)
        embed=discord.Embed(title=":coin: Coin Flip :coin:", description=f"{response}", color=ctx.message.author.top_role.colour)
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["credit2team", "c2t", "ctwot"])
    async def credits(self, ctx):
        embed=discord.Embed(title="The creators of De Fan Of De Way", color=0xff68b9)
        embed.set_author(name="Credits!")
        embed.add_field(name="<:4407_New_verified:799696049119428638>CoronerInArkansas#3639: ", value="Name Creator", inline=True)
        embed.add_field(name="<:4407_New_verified:799696049119428638>ℑ𝔰𝔞𝔟𝔢𝔩𝔩𝔞#0116:", value="Command Ideas", inline=False)
        embed.add_field(name="<:4407_New_verified:799696049119428638>just_bellis#5024", value="Command Ideas", inline=False)
        embed.add_field(name="<:6520_devNew:799695876050124830>N3#6494", value="Programming ", inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["swagscale", "meter"])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def rate(self, ctx, user : discord.Member, *, percent=None):
        print(percent)
        responses = ["is not very swag. step up your game", "is extremely swag :smiling_imp:", "is only a little bit swag... smh", "is sort of swag, they could do better tho", "has average swagness levels", "is pretty mf swag! hella", "is literally in the negative swagness levels. perish", "is so fukcingn swag.... awooga", "is barely swag enough to even be on this server.. ur on thin ice my guy", "is the physical embodiment of swag. they live, breathe, and eat pure swag. swag courses through their veins and pumps out of their heart. bow down", "is swag enough to say poggers unironically and not get the death penalty"]
        if percent is None:
            await ctx.send(f"{user.mention} {random.choice(responses)}")
        else:
            await ctx.send(f"{user.mention} is {random.randint(0, 100)}% swag")

    @commands.command(aliases=["aisgdjha"])
    async def say(self, ctx, *, words):
        await ctx.message.delete()
        await ctx.send(f"{words}")