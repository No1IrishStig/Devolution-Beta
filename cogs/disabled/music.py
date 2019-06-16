import asyncio
import discord
from discord.ext import commands
import datetime
from cogs.tools import tools
if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')

def __init__(self, bot):
        self.bot = bot

class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = ' {0.title} uploaded by {0.uploader} and requested by {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set() # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            self.current.player.start()
            await self.play_next_song.wait()
class Music:
    """Voice related commands.
    Works in multiple servers at once.
    """
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    @commands.command(pass_context=True, no_pm=True)
    async def join(self, ctx, *, channel : discord.Channel):
        """Joins a voice channel."""
        try:
            await self.create_voice_client(channel)
        except discord.ClientException:
            await self.bot.say('Already in a voice channel...')
        except discord.InvalidArgument:
            await self.bot.say('This is not a voice channel...')
        else:
            await self.bot.say('Ready to play audio in **' + channel.name)

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        """Summons the bot to join your voice channel."""
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.bot.say(embed=tools.Editable('Error!', 'Please join a voice channel!', 'Error'))
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song : str):
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            name = ctx.message.author.name
            avatar = ctx.message.author.avatar_url
            title = player.title
            uploader = player.uploader
            update = player.upload_date
            duration = player.duration
            views = player.views
            player.volume = 0.2
            entry = VoiceEntry(ctx.message, player)
            embed = discord.Embed(
                title = '{} with a duration of {}'.format(title, str(datetime.timedelta(seconds=duration))),
                colour = 0x9bf442,
                timestamp=datetime.datetime.utcnow()
                )
            embed.set_footer(text='Devolution | Music', icon_url='https://i.imgur.com/BS6YRcT.jpg')
            embed.set_author(name=name + ' requested Song:', icon_url=avatar)
            embed.add_field(name="Uploader", value=uploader, inline=True)
            embed.add_field(name="Upload Date", value=update, inline=True)
            embed.add_field(name="Views", value="{:,}".format(views), inline=True)
            await self.bot.say(embed=embed)
            await state.songs.put(entry)

    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value : int):
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            if value > 200:
                await self.bot.say(embed=tools.Editable('Error!', 'Try set the volume between 0 - 200!', 'Error'))
            else:
                if value < 0:
                    await self.bot.say(embed=tools.Editable('Error!', 'Try set the volume between 0 - 200!', 'Error'))
                else:
                    player.volume = value / 100
                    name = ctx.message.author.name
                    avatar = ctx.message.author.avatar_url
                    embed = discord.Embed(
                        title = 'Volume',
                        description = 'The volume has been set to {:.0%}'.format(player.volume, limit=int(value)),
                        colour = 0x9bf442,
                        timestamp=datetime.datetime.utcnow()
                        )
                    embed.set_footer(text='Devolution | Music')
                    embed.set_author(name=name + ' set the volume!', icon_url=avatar)
                    await self.bot.say(embed=embed)
        else:
                    await self.bot.say(embed=tools.Editable('Error!', 'Nothing is playing', 'Error'))

    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        """Resumes the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()
            name = ctx.message.author.name
            avatar = ctx.message.author.avatar_url
            embed = discord.Embed(
                title = '',
                description = 'Requested Song Has Been Paused!',
                colour = 0x9bf442,
                timestamp=datetime.datetime.utcnow()
                )
            embed.set_footer(icon_url='https://i.imgur.com/BS6YRcT.jpg', text='Devolution | Music')
            embed.set_author(name=name + ' paused the music!', icon_url=avatar)
            await self.bot.say(embed=embed)
        else:
            await self.bot.say(embed=tools.Editable('Error!', 'Nothing to pause', 'Error'))

    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        """Resumes the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()
            name = ctx.message.author.name
            avatar = ctx.message.author.avatar_url
            embed = discord.Embed(
                title = '',
                description = 'Requested Song Has Been Resumed!',
                colour = 0x9bf442,
                timestamp=datetime.datetime.utcnow()
                )
            embed.set_footer(icon_url='https://i.imgur.com/BS6YRcT.jpg', text='Devolution | Music')
            embed.set_author(name=name + ' resumed the music!', icon_url=avatar)
            await self.bot.say(embed=embed)
        else:
            await self.bot.say(embed=tools.Editable('Error!', 'Nothing to resume', 'Error'))

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        server = ctx.message.server
        state = self.get_voice_state(server)
        name = ctx.message.author.name
        avatar = ctx.message.author.avatar_url
        server = ctx.message.server
        await state.voice.disconnect()
        embed = discord.Embed(
            title = '',
            description = 'Requested Song Has Been Stopped!',
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        embed.set_footer(icon_url='https://i.imgur.com/BS6YRcT.jpg', text='Devolution | Music')
        embed.set_author(name=name + ' stopped the music!', icon_url=avatar)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await self.bot.say(embed=tools.Editable('Error!', 'No music is playing.', 'Error'))
            return
        name = ctx.message.author.name
        avatar = ctx.message.author.avatar_url
        voter = ctx.message.author
        if ctx.message.author.id == '439327545557778433':
            state.skip()
            embed = discord.Embed(
                title = '',
                description = 'The Song Has Been Stopped!',
                colour = 0x9bf442,
                timestamp=datetime.datetime.utcnow()
                )
            embed.set_footer(icon_url='https://i.imgur.com/BS6YRcT.jpg', text='Devolution | Music')
            embed.set_author(name=name + ' skipped the song using magic!', icon_url=avatar)
            await self.bot.say(embed=embed)
        else:
            if voter == state.current.requester:
                name = ctx.message.author.name
                avatar = ctx.message.author.avatar_url
                embed = discord.Embed(
                    description = 'Requester has skipped the song!',
                    colour = 0x9bf442,
                    timestamp=datetime.datetime.utcnow()
                    )
                embed.set_footer(icon_url='https://i.imgur.com/BS6YRcT.jpg', text='Devolution | Music')
                embed.set_author(name=name + ' skipped the Song!', icon_url=avatar)
                await self.bot.say(embed=embed)
            elif voter.id not in state.skip_votes:
                state.skip_votes.add(voter.id)
                total_votes = len(state.skip_votes)
                if total_votes > 3:
                    await self.bot.say(embed=tools.Editable('Song Skipped!', 'Vote passed, skipping song!.', 'Music'))
                    state.skip()
                else:
                    await self.bot.say(embed=tools.Editable('Vote Added!', 'Skip vote added, there are now [{}/3] votes!!'.format(total_votes), 'Music'))
            else:
                await self.bot.say(embed=tools.Editable('Error', 'You have already voted to skip this song!', 'Error'))

def setup(bot):
    bot.add_cog(Music(bot))
    print('Music Cog has been loaded.')
