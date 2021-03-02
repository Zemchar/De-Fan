import asyncio
import datetime as dt
import random
import re
import typing as t
from enum import Enum
import time
import discord
import wavelink
from discord.ext import commands

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

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
OPTIONS = {
    "1️⃣": 0,
    "2⃣": 1,
    "3⃣": 2,
    "4⃣": 3,
    "5⃣": 4,
}

#makes python happy when your bot wants to explode
class AlreadyConnectedToChannel(commands.CommandError):
    pass
class NoVoiceChannel(commands.CommandError):
    pass
class QueueIsEmpty(commands.CommandError):
    pass
class NoTracksFound(commands.CommandError):
    pass
class PlayerIsAlreadyPaused(commands.CommandError):
    pass
class NoMoreTracks(commands.CommandError):
    pass
class NoPreviousTracks(commands.CommandError):
    pass
class InvalidRepeatMode(commands.CommandError):
    pass
class RepeatMode(Enum):
    NONE = 0
    ONE = 1
    ALL = 2


class Queue:
    def __init__(self):
        self._queue = []
        self.position = 0
        self.repeat_mode = RepeatMode.NONE

    @property
    def is_empty(self):
        return not self._queue

    @property
    def current_track(self):
        if not self._queue:
            raise QueueIsEmpty

        if self.position <= len(self._queue) - 1:
            return self._queue[self.position]

    @property
    def upcoming(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[self.position + 1:]

    @property
    def history(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[:self.position]

    @property
    def length(self):
        return len(self._queue)

    def add(self, *args):
        self._queue.extend(args)

    def get_next_track(self):
        if not self._queue:
            raise QueueIsEmpty

        self.position += 1

        if self.position < 0:
            return None
        elif self.position > len(self._queue) - 1:
            if self.repeat_mode == RepeatMode.ALL:
                self.position = 0
            else:
                return None

        return self._queue[self.position]

    def shuffle(self):
        if not self._queue:
            raise QueueIsEmpty

        upcoming = self.upcoming
        random.shuffle(upcoming)
        self._queue = self._queue[:self.position + 1]
        self._queue.extend(upcoming)

    def set_repeat_mode(self, mode):
        if mode == "none":
            self.repeat_mode = RepeatMode.NONE
        elif mode == "1":
            self.repeat_mode = RepeatMode.ONE
        elif mode == "all":
            self.repeat_mode = RepeatMode.ALL

    def empty(self):
        self._queue.clear()
        self.position = 0

#Player for wavelink, "appropriated" a bunch from the docs
class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()

    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnectedToChannel
        if (channel := getattr(ctx.author.voice, "channel", channel)) is None:
            raise NoVoiceChannel
        await super().connect(channel.id)
        return channel

    async def teardown(self): #kill
        try:
            await self.destroy()
        except KeyError:
            pass

    async def add_tracks(self, ctx, tracks):
        if not tracks:
            raise NoTracksFound
        if isinstance(tracks, wavelink.TrackPlaylist):
            self.queue.add(*tracks.tracks)
        elif len(tracks) == 1:
            self.queue.add(tracks[0])
            await ctx.send(f"Added {tracks[0].title} to the queue.")
        else:
            if (track := await self.choose_track(ctx, tracks)) is not None:
                self.queue.add(track)
                await ctx.send(f"Added {track.title} to the queue.")
        if not self.is_playing and not self.queue.is_empty:
            await self.start_playback()

    async def choose_track(self, ctx, tracks):
        def _check(r, u):
            return (
                r.emoji in OPTIONS.keys()
                and u == ctx.author
                and r.message.id == msg.id
            )

        embed = discord.Embed(
            title="Choose a song",
            description=(
                "\n".join(
                    f"**{i+1}.** {t.title} ({t.length//60000}:{str(t.length%60).zfill(2)})"
                    for i, t in enumerate(tracks[:5])
                )
            ),
            colour=ctx.author.colour,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Top 5 Songs Matching your query")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed=embed)
        for emoji in list(OPTIONS.keys())[:min(len(tracks), len(OPTIONS))]:
            await msg.add_reaction(emoji)
        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=15.0, check=_check) #Times out the message after 15 seconds
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
        else:
            await msg.delete()
            return tracks[OPTIONS[reaction.emoji]]

    async def start_playback(self):
        await self.play(self.queue.current_track)

    async def advance(self):
        try:
            if (track := self.queue.get_next_track()) is not None:
                await self.play(track)
        except QueueIsEmpty:
            pass

    async def repeat_track(self):
        await self.play(self.queue.current_track)


class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.bot = bot
        self.wavelink = wavelink.Client(bot=bot)
        self.bot.loop.create_task(self.start_nodes())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after): #Leaves when last person in call leaves
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                await self.get_player(member.guild).teardown()

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node):
        now = time.localtime()
        current_time = time.strftime("%H:%M:%S", now)
        print(f"[{bcolors.OKBLUE}WAVELINK INFO{bcolors.ENDC}] [{bcolors.HEADER}{current_time}{bcolors.ENDC}] Wavelink node `{node.identifier}` ready.")

    @wavelink.WavelinkMixin.listener("on_track_stuck")
    @wavelink.WavelinkMixin.listener("on_track_end")
    @wavelink.WavelinkMixin.listener("on_track_exception")
    async def on_player_stop(self, node, payload):
        if payload.player.queue.repeat_mode == RepeatMode.ONE:
            await payload.player.repeat_track()
        else:
            await payload.player.advance()

    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Music commands are not available in DMs.")
            return False
        return True

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        nodes = { #Set up your lavalink node with default settinsgs besides the port
            "MAIN": {
                "host": "127.0.0.1",
                "port": 5500,
                "rest_uri": "http://127.0.0.1:5500",
                "password": "youshallnotpass",
                "identifier": "MAIN",
                "region": "us-central",
            }
        }

        for node in nodes.values():
            await self.wavelink.initiate_node(**node)

    def get_player(self, obj):
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)

    @commands.command(name="connect", aliases=["join"])
    async def connect_command(self, ctx, *, channel: t.Optional[discord.VoiceChannel]):
        player = self.get_player(ctx)
        channel = await player.connect(ctx, channel)
        await ctx.send(f"Connected to {channel.name}.")

    @connect_command.error
    async def connect_command_error(self, ctx, exc):
        if isinstance(exc, AlreadyConnectedToChannel):
            await ctx.send("Already connected to a voice channel.")
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send("No suitable voice channel was provided.")

    @commands.command(name="disconnect", aliases=["leave"])
    async def disconnect_command(self, ctx):
        player = self.get_player(ctx)
        await player.teardown()
        await ctx.send("Disconnect.")

    @commands.command(name="play", aliases=["p"])
    async def play_command(self, ctx, *, query: t.Optional[str]):
        player = self.get_player(ctx)

        if not player.is_connected:
            await player.connect(ctx)
        if query is None:
            if player.queue.is_empty:
                raise QueueIsEmpty
            await player.set_pause(False)
            await ctx.send("Playback resumed.")
        else:
            query = query.strip("<>")
            if not re.match(URL_REGEX, query):
                query = f"ytsearch:{query}"
            await player.add_tracks(ctx, await self.wavelink.get_tracks(query))

    @play_command.error
    async def play_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("No songs to play as the queue is empty.")
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send("You must join a voice channel or connect me to one to use that command first!")

    @commands.command(name="pause")
    async def pause_command(self, ctx):
        player = self.get_player(ctx)
        if player.is_paused:
            raise PlayerIsAlreadyPaused
        await player.set_pause(True)
        await ctx.send("Playback paused.")

    @pause_command.error
    async def pause_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.send("Unpausing...", delete_after=10)
            await player.set_pause(False)

    @commands.command(name="stop")
    async def stop_command(self, ctx):
        player = self.get_player(ctx)
        player.queue.empty()
        await player.stop()
        await ctx.send("Playback stopped.")

    @commands.command(name="next", aliases=["skip", "s"])
    async def next_command(self, ctx):
        player = self.get_player(ctx)

        if not player.queue.upcoming:
            await player.stop()
            await ctx.send("Skipped!\n:warning: There are no more songs in the queue!")
        else:
            await player.stop()
            await ctx.send("Skipped!")

    @next_command.error
    async def next_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("Queue is empty!")

    @commands.command(name="previous", aliases=["back"])
    async def previous_command(self, ctx):
        player = self.get_player(ctx)
        if not player.queue.history:
            raise NoPreviousTracks
        player.queue.position -= 2
        await player.stop()
        await ctx.send("Playing previous track.")

    @previous_command.error
    async def previous_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("Nothing is in the queue to go back to!")
        elif isinstance(exc, NoPreviousTracks):
            await ctx.send("There are no previous tracks in the queue.")

    @commands.command(name="shuffle")
    async def shuffle_command(self, ctx):
        player = self.get_player(ctx)
        player.queue.shuffle()
        await ctx.send("Queue shuffled.")

    @shuffle_command.error
    async def shuffle_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("You cant shuffle and empty queue. Add some songs first!")

    @commands.command(name="repeat", aliases=["loop"])
    async def repeat_command(self, ctx, mode: str):
        if mode not in ("none", "1", "all"):
           await ctx.send("That is not a repeat mode!\n\n__**Please add one of the three options below to your command:**__\n`none` to disable looping\n`1` to loop the current song\n`all` to loop the entire queue")
           pass
        player = self.get_player(ctx)
        player.queue.set_repeat_mode(mode)
        await ctx.send(f"The repeat mode has been set to {mode}.")
    
    @commands.command(name="queue", aliases=["q"])
    async def queue_command(self, ctx, show: t.Optional[int] = 10):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        embed = discord.Embed(
            title="Queue",
            description=f"Showing up to next {show} tracks\nTip: You can specify the number of tracks you want to show by putting a number at the end of this command!",
            colour=ctx.author.colour,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.add_field(
            name="Currently playing",
            value=getattr(player.queue.current_track, "title", "No tracks currently playing."),
            inline=False
        )
        if upcoming := player.queue.upcoming:
            embed.add_field(
                name="Next up",
                value="\n".join(t.title for t in upcoming[:show]),
                inline=False
            )

        msg = await ctx.send(embed=embed)

    @queue_command.error
    async def queue_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("The queue is currently empty.")
    
    @commands.command(name="volume", aliases=["setvol", "v"])
    async def set_volume(self, ctx, volume: int):
        player = self.get_player(ctx)
        if volume > 200:
            await ctx.send(f"Volume requested too high! Setting to 200% instead!") #no earrape 
            await player.set_volume(200)
        else:
            await player.set_volume(volume)
            await ctx.send(f"Set volume to: {volume}%")
    
    @commands.command(name="equalizer", aliases=["eq", "equalize"])
    async def set_equalizer(self, ctx, mode: t.Optional[str] = 'flat'):
        player = self.get_player(ctx)
        eqs = {'flat': wavelink.Equalizer.flat(),
               'boost': wavelink.Equalizer.boost(),
               'metal': wavelink.Equalizer.metal(),
               'piano': wavelink.Equalizer.piano()}
        eq = eqs.get(mode.lower(), None)
        if not eq:
            joined = "\n".join(eqs.keys())
            return await ctx.send(f'Invalid EQ provided. Valid EQs:\n\n{joined}')
        elif mode.lower() == 'flat':
            await ctx.guild.get_member(self.bot.user.id).edit(nick=None)
            await player.set_eq(eq)
            await ctx.send(f"Reset Equalizer!", delete_after=15)
        else:
            await ctx.guild.get_member(self.bot.user.id).edit(nick=f"{self.bot.user.name} [{eq}]") #nicknames to tell you its effect type
            await player.set_eq(eq)
            await ctx.send(f'Successfully changed equalizer to {eq}', delete_after=15)