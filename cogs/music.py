from discord.ext import commands
from utils.default import lib
from utils import default
import youtube_dl
import asyncio
import discord
import datetime

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': './data/music/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

players = {}
queues = {}

def check_queues(ctx, id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #@commands.command()
    #async def dmusic(self, ctx):
        #channel = ctx.author.voice.channel
        #await channel.connect()
        #await ctx.voice_client.disconnect()

    @commands.command()
    async def summon(self, ctx):
        try:
            member = ctx.author
            if member.voice is None:
                await ctx.send(embed=tools.Editable('Error', 'You arent in a voice channel!', 'Music'))
            else:
                channel = ctx.author.voice.channel
                await channel.connect()
        except Exception as error:
            await ctx.send(embed=tools.Editable('Error', 'Something went wrong, try again!', 'Music'))

    @commands.command()
    async def play(self, ctx, *, url=None):
        author = ctx.author
        avatar = ctx.author.avatar_url
        server = ctx.guild
        if author.voice is None:
            await ctx.send(embed=tools.Editable('Error', 'You arent in a voice channel!', 'Music'))
        else:
            if url is None:
                await ctx.send(embed=tools.Editable('Error', 'Please enter a song name to play', 'Music'))
            else:
                try:
                    channel = ctx.author.voice.channel
                    if self.bot.user in channel.members:
                        async with ctx.typing():
                            player = await YTDLSource.from_url(url, loop=self.bot.loop)
                            players[server.id] = player
                            ctx.voice_client.play(player, after=lambda: check_queue(server.id))
                            ctx.voice_client.source.volume = 10 / 100
                            e = discord.Embed(
                                description = 'Now playing {}'.format(player.title),
                                colour = 0x9bf442,
                                timestamp=datetime.datetime.utcnow()
                                )
                            e.set_footer(text='Devolution | Music', icon_url="https://i.imgur.com/BS6YRcT.jpg")
                            e.set_author(name=author.name + ' requested a song!', icon_url=avatar)
                            await ctx.send(embed=e)
                except Exception as e:
                        print('There was an error with your song request, {}'.format(e), 'Error')
                else:
                    if url is None:
                        await ctx.send(embed=tools.Editable('Error', 'Please enter a song name to play', 'Music'))
                    else:
                        try:
                            channel = ctx.author.voice.channel
                            await channel.connect()
                            async with ctx.typing():
                                player = await YTDLSource.from_url(url, loop=self.bot.loop)
                                players[server.id] = player
                                ctx.voice_client.play(player, after=lambda: check_queue(server.id))
                                ctx.voice_client.source.volume = 10 / 100
                                e = discord.Embed(
                                    description = 'Now playing {}'.format(player.title),
                                    colour = 0x9bf442,
                                    timestamp=datetime.datetime.utcnow()
                                    )
                                e.set_footer(text='Devolution | Music', icon_url="https://i.imgur.com/BS6YRcT.jpg")
                                e.set_author(name=author.name + ' requested a song!', icon_url=avatar)
                                await ctx.send(embed=e)
                        except Exception as e:
                            print('There was an error with your song request, {}'.format(e), 'Error')

    @commands.command()
    async def pause(self, ctx):
        author = ctx.author
        avatar = ctx.author.avatar_url
        if ctx.voice_client is None:
            return await ctx.send(embed=tools.Editable('Error', 'Im not in a voice channel!', 'Music'))
        if author.voice is None:
            await ctx.send(embed=tools.Editable('Error', 'You arent in a voice channel!', 'Music'))
        else:
            ctx.voice_client.pause()
            e = discord.Embed(
                description =  'The current track has been paused!',
                colour = 0x9bf442,
                timestamp=datetime.datetime.utcnow()
                )
            e.set_footer(text='Devolution | Music', icon_url="https://i.imgur.com/BS6YRcT.jpg")
            e.set_author(name=author.name + ' paused the music!', icon_url=avatar)
            await ctx.send(embed=e)

    @commands.command()
    async def resume(self, ctx):
        author = ctx.author
        avatar = ctx.author.avatar_url
        if ctx.voice_client is None:
            return await ctx.send(embed=tools.Editable('Error', 'Im not in a voice channel!', 'Music'))
        if author.voice is None:
            await ctx.send(embed=tools.Editable('Error', 'You arent in a voice channel!', 'Music'))
        else:
            ctx.voice_client.resume()
            e = discord.Embed(
                description =  'The current track has been resumed!',
                colour = 0x9bf442,
                timestamp=datetime.datetime.utcnow()
                )
            e.set_footer(text='Devolution | Music', icon_url="https://i.imgur.com/BS6YRcT.jpg")
            e.set_author(name=author.name + ' resumed the music!', icon_url=avatar)
            await ctx.send(embed=e)

    @commands.command()
    async def volume(self, ctx, volume:int):
        author = ctx.author
        avatar = ctx.author.avatar_url

        if ctx.voice_client is None:
            return await ctx.send(embed=tools.Editable('Error', 'Im not in a voice channel!', 'Music'))
        if author.voice is None:
            return await ctx.send(embed=tools.Editable('Error', 'You arent in a voice channel!', 'Music'))

        if volume > 100:
            return await ctx.send(embed=tools.Editable('Error', 'Please enter a volume between 0 and 100!', 'Music'))
        if volume < 0:
            return await ctx.send(embed=tools.Editable('Error', 'Please enter a volume between 0 and 100!', 'Music'))
            ctx.voice_client.source.volume = volume / 100
            e = discord.Embed(
                description = 'The volume is now {}'.format(volume),
                colour = 0x9bf442,
                timestamp=datetime.datetime.utcnow()
                )
            e.set_footer(text='Devolution | Music', icon_url="https://i.imgur.com/BS6YRcT.jpg")
            e.set_author(name=author.name + ' changed the volume!', icon_url=avatar)
            await ctx.send(embed=e)

    @commands.command()
    async def stop(self, ctx):
        author = ctx.author
        if ctx.voice_client is None:
            return await ctx.send(embed=tools.Editable('Error', 'Im not in a voice channel!', 'Music'))
        if author.voice is None:
            return await ctx.send(embed=tools.Editable('Error', 'You arent in a voice channel!', 'Music'))
        await ctx.voice_client.disconnect()

    #@commands.command()
    #async def skip(self, ctx):
    #    author = ctx.author
    #    avatar = author.avatar_url
    #    server = ctx.guild
    #    ctx.voice_client.stop()
    #    e = discord.Embed(
    #        description = 'The previous song was skipped!',
    #        colour = 0x9bf442,
    #        timestamp=datetime.datetime.utcnow()
    #        )
    #    e.set_footer(text='Devolution | Music', icon_url="https://i.imgur.com/BS6YRcT.jpg")
    #    e.set_author(name=author.name + ' skipped the song!', icon_url=avatar)
    #    await ctx.send(embed=e)
    #    url = lambda: check_queue(server.id)
    #    player = await YTDLSource.from_url(url, loop=self.bot.loop)
    #    players[server.id] = player
    #    ctx.voice_client.play(player, after=lambda: check_queue(server.id))

    #@commands.command()
    #async def queue(self, ctx, url):
    #    server = ctx.guild
    #    author = ctx.author
    #    avatar = author.avatar_url
    #    player = await YTDLSource.from_url(url, loop=self.bot.loop)
    #    if server.id in queues:
    #        queues[server.id].append(player)
    #    else:
    #        queues[server.id] = [player]
    #        e = discord.Embed(
    #            description = 'Enqueud {}'.format(player.title),
    #            colour = 0x9bf442,
    #            timestamp=datetime.datetime.utcnow()
    #            )
    #        e.set_footer(text='Devolution | Music', icon_url="https://i.imgur.com/BS6YRcT.jpg")
    #        e.set_author(name=author.name + ' enqueued a song!', icon_url=avatar)
    #        await ctx.send(embed=e)

    #@commands.command()
    #async def enqueue(self,ctx):
    #    await ctx.send(queues)



def setup(bot):
    bot.add_cog(Music(bot))
    print('Music - Initialized')
