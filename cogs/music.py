import youtube_dl
import asyncio
import discord
import datetime
import json

from utils import default
from discord import Spotify
from utils.default import lib
from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ""

ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "./data/music/%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0" # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    "options": "-vn"
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if "entries" in data:
            # take first item from a playlist
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("utils/cfg.json")
        song_requester = None
        with open("./data/settings/deltimer.json") as f:
            self.deltimer = json.load(f)

    @commands.command()
    async def spotify(self, ctx, user: discord.Member = None):
        global song_requester
        if user:
            if user.activities:
                for activity in user.activities:
                    if isinstance(activity, Spotify):
                        song = f"{activity.title} by {activity.artist}"
                        try:
                            channel = ctx.author.voice.channel
                            if self.bot.user in channel.members:
                                if ctx.voice_client.is_playing():
                                    await ctx.send('Im playing')
                                else:
                                    player = await YTDLSource.from_url(song, loop=self.bot.loop)
                                    ctx.voice_client.play(player)
                                    ctx.voice_client.source.volume = 10 / 100
                                    await ctx.send(embed=lib.Editable(self, f"{ctx.author.name} Requested {user.name}'s Spotify Song", f"Now Playing {song}", "Music"))
                                    song_requester = ctx.author
                            else:
                                await channel.connect()
                                await ctx.reinvoke()
                        except Exception as e:
                            return
                    else:
                        await ctx.send(embed=lib.Editable(self, "Uh oh", "That user isnt listening to Spotify!", "Errors"))
            else:
                await ctx.send(embed=lib.Editable(self, "Uh oh", "That user isnt listening to Spotify!", "Errors"))
        else:
            await ctx.send(embed=lib.Editable(self, "Uh oh", f"Type `{ctx.prefix}spotify @user` to play the song someone is currently listening to on Spotify!", "Errors"))


    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def summon(self, ctx):
        try:
            member = ctx.author
            if member.voice is None:
                e = await ctx.send(embed=lib.Editable(self, "Error", "You arent in a voice channel!", "Music"))
                await lib.eraset(self, ctx, e)
            else:
                channel = ctx.author.voice.channel
                await channel.connect()
                await asyncio.sleep(5)
                await ctx.message.delete()
        except Exception as error:
            e1 = await ctx.send(embed=lib.Editable(self, "Error", "Something went wrong, try again!", "Music"))
            await lib.eraset(self, ctx, e1)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def play(self, ctx, *, url=None):
        global song_requester
        author = ctx.author
        avatar = ctx.author.avatar_url
        server = ctx.guild
        if author.voice is None:
            e = await ctx.send(embed=lib.Editable(self, "Error", "You arent in a voice channel!", "Music"))
            await lib.eraset(self, ctx, e)
        else:
            if url is None:
                e1 = await ctx.send(embed=lib.Editable(self, "Error", "Please enter a song name to play", "Music"))
                await lib.eraset(self, ctx, e1)
            else:
                try:
                    channel = ctx.author.voice.channel
                    if self.bot.user in channel.members:
                        if ctx.voice_client.is_playing():
                            await ctx.send('Im playing')
                        else:
                            player = await YTDLSource.from_url(url, loop=self.bot.loop)
                            ctx.voice_client.play(player)
                            ctx.voice_client.source.volume = 10 / 100
                            e = discord.Embed(
                                description = "Now playing {}".format(player.title),
                                colour = 0x9bf442,
                                timestamp=datetime.datetime.utcnow()
                                )
                            e.set_footer(text="Devolution | Music", icon_url="https://i.imgur.com/BS6YRcT.jpg")
                            e.set_author(name=author.name + " requested a song!", icon_url=avatar)
                            np = await ctx.send(embed=e)
                            song_requester = author
                            await lib.eraset(self, ctx, np)
                    else:
                        await channel.connect()
                        await ctx.reinvoke()
                except Exception as e:
                    return

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def pause(self, ctx):
        author = ctx.author
        avatar = ctx.author.avatar_url
        if ctx.voice_client is None:
            e = await ctx.send(embed=lib.Editable(self, "Error", "Im not in a voice channel!", "Music"))
            await lib.eraset(self, ctx, e)
        else:
            if author.voice is None:
                e1 = await ctx.send(embed=lib.Editable(self, "Error", "You arent in a voice channel!", "Music"))
                await lib.eraset(self, ctx, e1)
            else:
                ctx.voice_client.pause()
                e = discord.Embed(
                    description =  "The current track has been paused!",
                    colour = 0x9bf442,
                    timestamp=datetime.datetime.utcnow()
                    )
                e.set_footer(text="Devolution | Music", icon_url="https://i.imgur.com/BS6YRcT.jpg")
                e.set_author(name=author.name + " paused the music!", icon_url=avatar)
                p = await ctx.send(embed=e)
                await lib.eraset(self, ctx, p)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def resume(self, ctx):
        author = ctx.author
        avatar = ctx.author.avatar_url
        if ctx.voice_client is None:
            await ctx.send(embed=lib.Editable(self, "Error", "Im not in a voice channel!", "Music"))
        else:
            if author.voice is None:
                await ctx.send(embed=lib.Editable(self, "Error", "You arent in a voice channel!", "Music"))
            else:
                ctx.voice_client.resume()
                e = discord.Embed(
                    description =  "The current track has been resumed!",
                    colour = 0x9bf442,
                    timestamp=datetime.datetime.utcnow()
                    )
                e.set_footer(text="Devolution | Music", icon_url="https://i.imgur.com/BS6YRcT.jpg")
                e.set_author(name=author.name + " resumed the music!", icon_url=avatar)
                r = await ctx.send(embed=e)
                await lib.eraset(self, ctx, r)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def volume(self, ctx, volume: int):
        author = ctx.author
        avatar = ctx.author.avatar_url
        if ctx.voice_client is None:
            e = await ctx.send(embed=lib.Editable(self, "Error", "Im not in a voice channel!", "Music"))
            await lib.eraset(self, ctx, e)
        else:
            if author.voice is None:
                e1 = ctx.send(embed=lib.Editable(self, "Error", "You arent in a voice channel!", "Music"))
                await lib.eraset(self, ctx, e1)
            else:
                if volume > 100:
                    e2 = await ctx.send(embed=lib.Editable(self, "Error", "Please enter a volume between 0 and 100!", "Music"))
                    await lib.eraset(self, ctx, e2)
                else:
                    if volume < 0:
                        e3 = await ctx.send(embed=lib.Editable(self, "Error", "Please enter a volume between 0 and 100!", "Music"))
                        await lib.eraset(self, ctx, e3)
                    else:
                        ctx.voice_client.source.volume = volume / 100
                        s = await ctx.send(embed=lib.AvatarEdit(self, author.name, avatar, " ", f"The volume is now {volume}", Music))
                        await lib.eraset(self, ctx, s)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def stop(self, ctx):
        global song_requester
        author = ctx.author
        if ctx.voice_client is None:
            e = await ctx.send(embed=lib.Editable(self, "Error", "Im not in a voice channel!", "Music"))
            await lib.eraset(self, ctx, e)
        else:
            if author.voice is None:
                e1 = await ctx.send(embed=lib.Editable(self, "Error", "You arent in a voice channel!", "Music"))
                await lib.eraset(self, ctx, e1)
            else:
                if author is song_requester:
                    await ctx.voice_client.disconnect()
                    await asyncio.sleep(5)
                    await ctx.message.delete()
                else:
                    e2 = await ctx.send(embed=lib.Editable(self, "Error", "Only the song requester can stop the current track!", "Music"))
                    await lib.eraset(self, ctx, e2)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def sstop(self, ctx):
        if ctx.author.guild_permissions.manage_roles:
            author = ctx.author
            if ctx.voice_client is None:
                e = await ctx.send(embed=lib.Editable(self, "Error", "Im not in a voice channel!", "Music"))
                await lib.eraset(self, ctx, e)
            else:
                if author.voice is None:
                    e1 = await ctx.send(embed=lib.Editable(self, "Error", "You arent in a voice channel!", "Music"))
                    await lib.eraset(self, ctx, e1)
                else:
                    await ctx.voice_client.disconnect()
                    await asyncio.sleep(5)
                    await ctx.message.delete()
        else:
            await ctx.send(embed=lib.NoPerm(self))


def setup(bot):
    bot.add_cog(Music(bot))
