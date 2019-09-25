import datetime
import aiohttp
import discord
import asyncio
import random
import shelve
import json
import time
import re


from utils import default
from discord import Spotify
from utils.default import lib
from discord.ext import commands
from random import choice as randchoice

global page_number
page_number = None
global page_num
page_num = None
start_time = time.time()

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = shelve.open("./data/db/levels/data.db", writeback=True)
        with open("./utils/cfg.json") as f:
            self.config = json.load(f)
            with open("./data/settings/deltimer.json") as f:
                self.deltimer = json.load(f)
                with open("./data/cmd_data/insults.json") as f:
                    self.insults = json.load(f)
                    with open("./data/settings/nsfw.json") as f:
                        self.settings = json.load(f)
                        with open("./data/cmd_data/owo.json") as f:
                            self.owo = json.load(f)
                            with open("./data/settings/leveling.json") as f:
                                self.levels = json.load(f)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        global page_number
        emojis = ['◀', '▶', '🗑', ':one:', ':two:', ':three:', ':four:', ':five:']
        if not user.bot:
            if str(reaction.emoji in emojis):
                if str(reaction.emoji) == '1\N{combining enclosing keycap}':
                    page_number = 1
                    await reaction.remove(user)
                elif str(reaction.emoji) == '2\N{combining enclosing keycap}':
                    page_number = 2
                    await reaction.remove(user)
                elif str(reaction.emoji) == '3\N{combining enclosing keycap}':
                    page_number = 3
                    await reaction.remove(user)
                elif str(reaction.emoji) == '4\N{combining enclosing keycap}':
                    page_number = 4
                    await reaction.remove(user)
                elif str(reaction.emoji) == '5\N{combining enclosing keycap}':
                    page_number = 5
                    await reaction.remove(user)
                elif str(reaction.emoji) == '0\N{combining enclosing keycap}':
                    page_number = 0
                    await reaction.remove(user)

                elif str(reaction.emoji) == '🗑':
                    try:
                        await changelog.delete()
                        page_number = None
                    except Exception as e:
                        return

                if page_number == 0:
                    e = lib.Editable(self, "Devolution Beta Changelogs Since 15/12/18", "**Page 0** - This Page\n**Page 1** 15/12/2018 - 04/01/2019\n**Page 2** 04/01/2019 - 17/06/2019\n**Page 3** 17/06/2019 - 23/06/2019\n**Page 4** 04/07/2019 - 26/08/2019\n**Page 5** 13/08/2019 - {}".format(datetime.datetime.utcnow().strftime("%d/%m/%Y")), "Changelogs Index")
                    await changelog.edit(embed=e)

                elif page_number == 1:
                    e = lib.Editable(self, f"Devolution Beta Changelogs Since 15/12/18", "__**Changelog (15/12/2018) v0.0.1 Beta 1**__\n+ Added Help command\n+ Added Ping command\n+ Added Music Cog\n\n__**Changelog (16/12/2018) v0.0.2 Beta 2**__\n+ Added shutdown command\n\n- Changed some Music messages to embeds\n\n__**Changelog (18/12/2018) v0.0.3 Beta 3**__\n- Finished changing all music embeds\n- Updated help command\n\n__**Changelog (21/12/2018) v0.0.4 Beta 4**__\n+ Added sinfo command\n\n- Edited many embed messages in music commands\n- Updated Help command\n- Music Cog Work\n\n__**Changelog (21/12/2018  v0.0.5 Beta 5**__\n+ Added Uptime command\n+ Added Kick command\n\n- Fixed all timestamps to make them actually work\n- Changed set presence command to an embed\n- Updated Help command\n\n__**Changelog (22/12/2018) v0.1**__\n+ Added Cog check, if you arent me, goodluck using that one\n+ Added Cog commands Load, Unload and List\n+ Added Set Presence command (Alias sp)\n\n- Updated Help command\n\n__**Changelog (23/12/2018) v0.1.1**__\n+ Added Avatar command\n+ Added Avatar command\n+ Added purge command\n+ Added uinfo command\n+ Added ban command\n+ Added say command\n+ Added about command\n+ Added pm Command\n\n- Changed kick embed message, bot sends embed to kicked user {server} {kicked_by} {reason (if there was one)}\n- Kick command now accepts reasons\n- Updated Help command\n\n__**Changelog (29/12/2018) v0.1.2**__\n+ Added rename command\n+ Added coinflip command\n\n- Updated Help command\n\n__**Changelog (04/01/2019) v0.1.3**__\n- Changed music play embed again", f"Page {page_number}")
                    await changelog.edit(embed=e)

                elif page_number == 2:
                    e = lib.Editable(self, f"Devolution Beta Changelogs Since 15/12/18", f"__**Changelog (04/01/2019) v0.2**__\n+ Added Colour command\n+ Added Meme command\n+ Added Space command\n\n- Updated Help command\n\n__**Changelog (14/01/2019) v0.2.1**__\n+ Added Prefix command\n+ Added Leave command\n\n- Reworked Invite command\n- Updated Help command\n\n__**Changelog (24/01/2019) v0.2.2**__\n+ Added spp command (Set punish permissions)\n+ Added punish & unpunish commands\n\n- Updated Help command\n\n__**Changelog (26/01/2019) v0.3 **__\n- Major code overhaul\n- File sizes cut in half, bot should now run smoother\n\n__**Changelog (26/01/2019) v0.3.1**__\n+ Added lspunish command\n+ Added Embed command\n\n- Updated Punish command to give usage details\n- Updated Help command\n\n__**Changelog (27/01/2019) v0.4 **__\n+ Added role commands\n+ Added Bug command\n\n- Updated Help command\n\n__**Changelog (02/03/2019) v0.5 **__\n+ Added changelog command (So you can see all this)\n+ Added new cog for tournaments\n+ Added Tournament commands\n\n- Updated bots default playing status\n- Updated Help command\n\n__**Changelog (09/03/2019) v0.5.1**__\n+ Added volume min and max 0 - 200\n\n - Fixed anyone being able to skip on the fist vote\n - Fixed Embed Messages not sending\n- Fixed Music failing to play\n\n__**Changelog (16/06/2019) v1.0 **__\n- Rewrote the entire bot into the newest version of Python and Discordpy\n- Updated Todo Command and made it public\n- Reworked Bug report command\n- Reworked help command\n\n__**Changelog (17/06/2019) v1.0.1 **__\n+ Added a command to list all roles in a server\n+ Added github issue link to bug command\n+ Reintroduced the beloved data folder!\n+ Added Boobs & Ass command\n+ Added Insult command\n+ Added roll command\n+ Added bot launcher\n+ Added Cleanup\n\n- Huge amounts of optimization with the cogs\n- Removed meme api as it was broken\n- Removed unnecessary json loading\n- Squashed a **lot** of nasty bugs\n- Removed Purge command\n- Removed prefix command\n- Removed tournament cog", f"Page {page_number}")
                    await changelog.edit(embed=e)

                elif page_number == 3:
                    e = lib.Editable(self, f"Devolution Beta Changelogs Since 15/12/18", f"__**Changelog (17/06/2019) v1.0.2**__\nAdded music command!(Play, Pause, Resume, volume, Stop)\n+ Added gif and gifr commands\n+ Added Hackban!\n+ Added pmid\n\n- Reworked the changelog command and put it in size order (iiCarelessness)\n- Reworked and updated Help command\n- Planted logos everywhere!\n\n__**Changelog (18/06/2019) v1.1**__\n+ Added a launcher gui with a few features\n+ Added Set Activity command\n+ Created a new admin cog\n+ Added amiadmin command\n+ Added utils folder\n+ Added config file\n\n- Merged lib into a new file named default inside util\n- Music now creates a folder for songs\n- Updated help command\n- Fixed some music bugs\n\n__**Changelog (18/06/2019) v1.1.1**__\n+ Added owo command (944)\n\n- Fixed Punish not setting channel permissions\n- Finished Cleanup command\n- Fixed volume command\n- Updated help command\n- Added clean command\n- Bug Fixes\n\n__**Changelog (21/06/2019) v1.2**__\n+ Added Error handler (catches and resolves errors automatically)\n+ Added help command for bot required permissions\n+ Added self delete function to every command\n+ Added 'role exist' check to remove and add\n+ Added sstop command (Force stop song)\n+ Added command cooldowns\n\n- Updated 'Forgot Something' errors to add more detail and to give a similar appearance\n- Reworked invite command (Invite ClientID is now based on the bots ID)\n- Changed stop command so only the song player can stop the song\n- Rewrote every command and optimized a lot of code\n- Rearranged and removed unused imports\n- Tweaked and tidied changelog output\n- Reverted and updated help command\n- Placed all commands into cogs\n- Reworked Cog loading system\n- Removed todo command\n- Reworked every cog\n- Reworked bot.py file\n- Bug Fixes\n\n__**Changelog (21/06/2019) v1.3**__\n+ Added customcommands\n+ Added leaveid\n+ Added logs\n\n- Added permission check to spp\n- Updated help command\n- Updated changelog\n- Bug fixes\n\n__**Changelog (23/06/2019) v1.3.1**__\n- Fixed cleanup after\n- Bug fixes", f"Page {page_number}")
                    await changelog.edit(embed=e)

                elif page_number == 4:
                    e = lib.Editable(self, f"Devolution Beta Changelogs Since 15/12/18", f"__**Changelog (04/07/2019) v1.4**__\n+ Added !deltimer\n\n- Fixed time being off in logs\n- Bug Fixes\n- Updated help command\n\n__**Changelog (05/07/2019) v1.5**__\n+ Added !admin\n\n- Bug fixes\n\n__**Changelog (05/07/2019) v1.5**__\n+ Added !admin\n\n- Changed !amiadmin to incorperate the new admin command\n- Updated error handler\n- Bug fixes\n\n__**Changelog (06/07/2019) v1.5.1**__\n\n- Bug fixes\n\n__**Changelog (03/08/2019) v1.6**__\n+ Added custom prefix support\n+ Added economy update\n+ Added slots\n\n- Optimized code and remove unnecessary checks.\n- Added Economy to help command\n- Bug Fixes\n\n__**Changelog (03/08/2019) v1.6.1**__\n- Made each server have its own bank\n- Many code optimizations\n- Began work on blackjack\n- Bug fixes\n\n__**Changelog (05/08/2019) v1.6.3**__\n+ Added a restart command (This only restarts the connection, wont apply any file changes)\n+ Added checks to bank balance, bank register, bank transfer, bank set, benefits and top\n+ Added blackjack\n\n- Removed unnecessary checks\n- Code optimization\n- Many bug fixes\n\n__**Changelog (05/08/2019) v1.6.4**__\n+ Added check to !blackjack command and more information\n+ Added a message to show if the house hit or stood\n+ Added a Tie Check to blackjack\n\n- Fixed a bug when losing after standing where all cards are shown\n- Fixed bank balance\n\n__**Changelog (11/08/2019) v1.6.6**__\n+ Began work on leveling system\n\n- Began work on changing the way data is stored\n- Completely reworked the blackjack logic\n- Reworked and removed cogs\n\n__**Changelog (12/08/2019) v1.7**__\n+ Added check if punished users try rejoin\n+ Added some new folders\n+ Added Database Check\n+ Added Timer to Punish\n\n- Reworked Economy and Admins to use Database\n- Removed some checks from bot.py\n- Removed checks from default.py\n- Removed a lot of the json files\n- Remove customcommand\n- Updated Help Command\n- Added cmd_data folder\n- Added Settings folder\n- Cleaned up imports", f"Page {page_number}")
                    await changelog.edit(embed=e)

                elif page_number == 5:
                    e = lib.Editable(self, f"Devolution Beta Changelogs Since 15/12/18", f"__**Changelog (13/08/2019) v1.7.2**__\n+ Added Warnings System\n+ Added Leveling System\n\n- Bug Fixes and Improvements\n- Updated JSON Check\n- Updated Help\n\n__**Changelog (26/08/2019) v1.7.5**__\n+ Added Move Commands\n\n- Fixed a check for Prefix\n- Fixed music auto delete\n- Other random bugs\n\n__**Changelog (30/08/2019) v1.7.6**__\n- Rewrote changelog command\n- Rewrote uinfo command\n- Rewrote help command\n- Bug Fixes\n\n__**Changelog (01/09/2019) v1.8**__+ Added custom userid and avatar to every embed (your bot)\n+ Added token and userid request if they arent in the cfg file\n+ Added some functions to default.py\n+ Added Spotify command\n+ Added Math command\n\n- Reworked database check, and added 3 new databases\n- Reworked entire leveling system and its functions\n- Bug fixes and stability improvements\n Removed unnecessary checks\n- Tidied up bot.py\n- Fixed deltimer", f"Page {page_number}")
                    await changelog.edit(embed=e)

            else:
                return
        else:
            return

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def changelog(self, ctx):
        global page_number
        global changelog
        await ctx.message.delete()
        page_number = 0
        changelog = await ctx.send(embed = lib.Editable(self, "Devolution Beta Changelogs Since 15/12/18", "**Page 0** - This Page\n**Page 1** 15/12/2018 - 04/01/2019\n**Page 2** 04/01/2019 - 17/06/2019\n**Page 3** 17/06/2019 - 23/06/2019\n**Page 4** 04/07/2019 - 26/08/2019\n**Page 5** 13/08/2019 - {}".format(datetime.datetime.utcnow().strftime("%d/%m/%Y")), "Changelogs Index"))

        await changelog.add_reaction("🗑")
        await changelog.add_reaction("1\N{combining enclosing keycap}")
        await changelog.add_reaction("2\N{combining enclosing keycap}")
        await changelog.add_reaction("3\N{combining enclosing keycap}")
        await changelog.add_reaction("4\N{combining enclosing keycap}")
        await changelog.add_reaction("5\N{combining enclosing keycap}")
        await changelog.add_reaction("0\N{combining enclosing keycap}")

    @commands.Cog.listener(name="on_reaction_add")
    async def reaction_add_(self, reaction, user):
        global page_num
        emojis1 = ['◀', '▶', '🇽', '🇵']
        if not user.bot:
            if str(reaction.emoji in emojis1):

                if str(reaction.emoji) == '🇽':
                    try:
                        await help.delete()
                        page_num = None
                    except Exception as e:
                        return

                elif str(reaction.emoji) == '◀':
                    if page_num > 0:
                        await help.add_reaction("◀")
                        page_num -= 1
                        await reaction.remove(user)
                        if page_num == 0:
                            try:
                                await reaction.remove(self.bot.user)
                                await reaction.remove(user)
                            except Exception as e:
                                return
                    else:
                        try:
                            await reaction.remove(self.bot.user)
                            await reaction.remove(user)
                        except Exception as e:
                            return

                elif str(reaction.emoji) == '▶':
                    if page_num <= 5:
                        page_num += 1
                        await reaction.remove(user)
                        await help.add_reaction("◀")
                    else:
                        try:
                            await reaction.remove(self.bot.user)
                            await reaction.remove(user)
                        except Exception as e:
                            return

                elif str(reaction.emoji) == '🇵':
                    await user.send(embed=lib.Editable(self, "Permission Requirements", "Manage Roles\nManage Channels\nKick Members\n Ban Members\nManage Nicknames\nRead Channels\nSend Messages\nManage Messages\nAdd Reactions\nConnect\nSpeak", "Help"))
                    await reaction.remove(user)

                if page_num == 0:
                    e = lib.Editable(self, "Devolution - Help", "**Page 0** - This Page\n**Page 1** - Information\n**Page 2** - Fun\n**Page 3** - Useful\n**Page 4** - Moderation\n**Page 5** - Admin\n**Permission Help (P)** - DM's Required Permissions", "Help Index")
                    await help.edit(embed=e)

                elif page_num == 1:
                    e = lib.Editable(self, f"Devolution Help", "**help** - Gives help!\n**about** - Displays stuff about the bot\n**changelog** - Displays the entire bots changelog\n**sinfo** - Displays guild information.\n**uinfo** - Displays user information\n**uptime** - Displays the bots uptime\n**bug** - Use it to report bugs.\n**github** - Provides github link", "Information")
                    await help.edit(embed=e)

                elif page_num == 2:
                    e = lib.Editable(self, f"Devolution Help", "**bank** - Gives usage details\n**coinflip** - Flip a coin\n**space** - Get live information about the ISS\n**colour** - Get a random colour\n**roll** - Roles a dice\n**insult** - Insult people you dislike!\n**boobs** - See some melons!\n**ass** - See some peaches!\n**gif** - Search up a gif on giphy by name\n**gifr** - Gives a random gif from giphy\n**owo** - Get random responses", "Fun Help")
                    await help.edit(embed=e)

                elif page_num == 3:
                    e = lib.Editable(self, "Devolution Help", "**say** - Speak as the bot\n**rename** - Change a users nickname\n**invite** - Sends a bot invite link\n**embed** - Creates an embed message\n**role** - Gives role options\n**music** - Gives music help\n**math** - Gives usage details", "Useful Help")
                    await help.edit(embed=e)

                elif page_num == 4:
                    e = lib.Editable(self, "Devolution Help", "**kick**- Kick a mentioned user\n**ban** - Ban a mentioned user\n**hackban** - Allows you to ban a UserID\n**punish** - Gives usage details\n**clean** - Cleans the current channel of bot messages and commands\n**cleanup** - Gives usage details\n**logs** - Gives usage details\n**warn** - Gives usage details\n**move** - Gives usage details\n**deltimer** - Change the timer at which the bot auto deletes its messages", "Moderation Help")
                    await help.edit(embed=e)

                elif page_num == 5:
                    e = lib.Editable(self, f"Devolution Help", "**leave** - Makes the bot leave the guild\n**setpresence(sp)** - Change the playing status of the bot.\n**shutdown** - Sends the bot into a deep sleep ...\n**cog** - Displays list of Cog Options\n**pm** - PMs Target user as bot\n**pmid** - PMs target ID as bot\n**amiadmin** - Tells you if your UserID is inside the cfg file.\n**admin** - Gives usage details\n**leveling** - Gives usage details", "Admin Help")
                    await help.edit(embed=e)

            else:
                return
        else:
            return

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx):
        global page_num
        global help
        await ctx.message.delete()
        page_num = 0
        help = await ctx.send(embed = lib.Editable(self, "Devolution - Help", "**Page 0** - This Page\n**Page 1** - Information\n**Page 2** - Fun\n**Page 3** - Useful\n**Page 4** - Moderation\n**Page 5** - Admin\n**Permission Help (P)** - DM's Required Permissions", "Help Index"))

        await help.add_reaction("🇽")
        await help.add_reaction("▶")
        await help.add_reaction("🇵")

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx):
        user = ctx.author
        await ctx.message.add_reaction("📄")
        await user.send(f"Heres the link to invite me to your guilds!\n\nhttps://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=8")
        await asyncio.sleep(10)
        await ctx.message.delete()

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def uptime(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        embed.add_field(name="Uptime", value=text)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.set_footer(icon_url="https://i.imgur.com/BS6YRcT.jpg", text="Devolution | Core")
        u = await ctx.send(embed=embed)
        await lib.eraset(self, ctx, u)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def about(self, ctx):
        embed=discord.Embed(
            title="About Devolution",
            description="A discord bot created for guild Administration, with plenty of commands for Admins, Moderators, games and more. For more information see below:",
            colour = 0x9bf442
            )
        embed.set_author(name="Stig", icon_url="https://cdn.discordapp.com/avatars/439327545557778433/a_09b7d5d0f8ecbd826fe3f7b15ee2fb93.gif?size=1024")
        embed.add_field(name="Discord Support", value="https://discord.gg/frcc5vF", inline=True)
        embed.add_field(name="Bot Creator", value="Stig#1337", inline=True)
        embed.add_field(name="Version & API version", value=f"Build - {default.version} & API Version {discord.__version__}", inline=True)
        embed.set_footer(text="Devolution - About - Providing Discord support since May 2018")
        await ctx.channel.send(embed=embed)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def bug(self, ctx):
        f = await ctx.send(embed=lib.Editable(self, "We've Moved!", f"We no longer take bugs directly on discord. However you are encouraged to still report these bugs, on the github!\n\nhttps://github.com/No1IrishStig/Devolution-Beta/issues", "Bug Report"))
        await lib.eraset(self, ctx, f)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def spp(self, ctx):
        if ctx.author.guild_permissions.manage_channels:
            for channel in ctx.message.guild.channels:
                role = discord.utils.get(channel.guild.roles, name="punished")
                overwrite = discord.PermissionOverwrite()
                overwrite.send_messages = False
                overwrite.send_tts_messages = False
                overwrite.add_reactions = False
                await channel.set_permissions(role, overwrite=overwrite),
            p = await ctx.send(embed=lib.Editable(self, "Setting Permissions", "This may take a while, Ill tell you when im done.", "Moderation"))
            await asyncio.sleep(5)
            msg2 = await ctx.send(embed=lib.Editable(self, "Im Finished!", "All permissions should be set.", "Moderation"))
            await lib.erase(ctx, 5, p)
            await asyncio.sleep(10)
            await msg2.delete()
        else:
            p = await ctx.send(embed=lib.NoPerm(self))
            await lib.eraset(self, ctx, p)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def music(self, ctx):
        m = await ctx.send(embed=lib.Editable(self, "Music Usage", f"**{ctx.prefix}play (song/link)** - Plays a song by name or url from youtube\n**{ctx.prefix}pause** - Pauses the current song\n**{ctx.prefix}resume** - Resumes the current song\n**{ctx.prefix}volume (number)** - Change the volume of the bot\n**{ctx.prefix}stop** - Disconnects the bot\n**{ctx.prefix}sstop** - Force disconnects the bot\n**{ctx.prefix}spotify @user** - Plays the spotify song through the bot", "Todo"))
        await lib.eraset(self, ctx, m)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def github(self, ctx):
        user = ctx.author
        await ctx.message.add_reaction("📄")
        await user.send(embed=lib.Editable(self, "Github", "https://github.com/No1IrishStig/Devolution-Beta/", "Github"))
        await asyncio.sleep(10)
        await ctx.message.delete()

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sinfo(self, ctx):
        embed = discord.Embed(
            title = "Server Information for " + ctx.guild.name,
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        embed.add_field(name="Creation Date", value=ctx.guild.created_at.strftime("%d/%m/%Y at %H:%M:%S (GMT)"), inline=False)
        embed.add_field(name="Owner", value=ctx.guild.owner.name, inline=True)
        embed.add_field(name="Region", value=ctx.guild.region, inline=True)
        embed.add_field(name="Roles", value=len(ctx.guild.roles), inline=True)
        embed.add_field(name="Users", value=ctx.guild.member_count, inline=True)
        embed.add_field(name="Channels", value=len(ctx.guild.channels), inline=True)
        embed.add_field(name="AFK Channel", value=ctx.guild.afk_channel, inline=True)
        embed.set_author(name=f"{self.bot.user.name}                                                                              ID: {ctx.guild.id}", icon_url=self.bot.user.avatar_url, )
        embed.set_footer(icon_url="https://i.imgur.com/BS6YRcT.jpg", text="Devolution | Info")
        e = await ctx.send(embed=embed)
        await lib.eraset(self, ctx, e)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def uinfo(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
            pass
        if user.voice is None:
            channel = "Not in a voice channel"
        else:
            channel = user.voice.channel.name
        if user.activities:
            for activity in user.activities:
                if isinstance(activity, Spotify):
                    title = f"Listening to {activity.title} by {activity.artist}"
                else:
                    title = f"Playing {activity.name}"
        else:
            title = "Doing Nothing"
        embed = discord.Embed(
            title = title,
            colour = 0x9bf442,
            timestamp = datetime.datetime.utcnow()
            )
        embed.set_author(name = f"{self.bot.user.name}", icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=f"{user.name}'s User Info", icon_url=user.avatar_url)
        embed.add_field(name="Joined At", value=user.joined_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="Account Created", value=user.created_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="Status", value=user.status, inline=True)
        embed.add_field(name="Role Count", value=len(user.roles), inline=True)
        embed.add_field(name="Nickname", value=user.nick, inline=True)
        embed.add_field(name="Voice", value=channel, inline=True)
        ee = await ctx.send(embed=embed)
        await lib.eraset(self, ctx, ee)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, user : discord.User=None):
        if user is None:
            user = ctx.author
            pass
        embed = discord.Embed(
            title = "Avatar Stealer",
            description = user.avatar_url,
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        embed.set_image(url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        embed.set_footer(text=f"{self.bot.user.name} - Avatar", icon_url=self.bot.user.avatar_url)
        e = await ctx.send(embed=embed)
        await lib.eraset(self, ctx, e)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def embed(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            await ctx.message.delete()
            question = await ctx.send(embed=lib.Editable(self, "Embed Generator", "Please type your title!", "Embed Generation"))
            title = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout = 120)
            await title.delete()
            e = lib.Editable(self, title.content, "Please type your footer!", "Embed Generation")
            await question.edit(embed=e)
            footer = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout = 120)
            await footer.delete()
            e = lib.Editable(self, title.content, "Please type your description!", footer.content)
            await question.edit(embed=e)
            description = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout = 120)
            await description.delete()
            e = lib.Editable(self, title.content, description.content, footer.content)
            await question.edit(embed=e)
        else:
            p = await ctx.send(embed=lib.NoPerm(self))
            await lib.eraset(self, ctx, p)

    @commands.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def role(self, ctx):
        if ctx.author.guild_permissions.manage_roles:
            u = await ctx.send(embed=lib.Editable(self, "Role Usage!", f"**{ctx.prefix}add** - Adds a user to a role.\n**{ctx.prefix}list** - List all roles in the server\n**{ctx.prefix}remove** - Removes a user from a role\n**{ctx.prefix}create** - Creates a role\n**{ctx.prefix}delete** - Deletes a role", "Role Usage"))
            await lib.eraset(self, ctx, u)
        else:
            p = await ctx.send(embed=lib.NoPerm(self))
            await lib.eraset(self, ctx, p)

    @role.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def list(self, ctx):
        if ctx.author.guild_permissions.manage_roles:
            roles = []
            for role in ctx.guild.roles:
                roles.append(role.name)
            roles.remove("@everyone")
            l = await ctx.send(embed=lib.Editable(self, "Role List", "{}".format(", ".join(roles)), "Roles"))
            await lib.eraset(self, ctx, l)
        else:
            p = await ctx.send(embed=lib.NoPerm(self))
            await lib.eraset(self, ctx, p)

    @role.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def add(self, ctx, rolename=None, member: discord.Member=None):
        if ctx.author.guild_permissions.manage_roles:
            if rolename and member:
                role = discord.utils.get(ctx.message.guild.roles, name=rolename)
                if role in ctx.guild.roles:
                    if role in member.roles:
                        e = await ctx.send(embed=lib.Editable(self, "Error", f"**{member.name}** already has the role **{role}**", "Roles"))
                        await lib.eraset(self, ctx, e)
                    else:
                        await member.add_roles(role)
                        d = await ctx.send(embed=lib.Editable(self, "Role Added", f"The role **{role}** was added to **{member.name}**", "Roles"))
                        await lib.eraset(self, ctx, d)
                else:
                    e = await ctx.send(embed=lib.Editable(self, "Error", f"The role **{rolename}** doesnt exist!", "Roles"))
                    await lib.eraset(self, ctx, e)
            else:
                u = await ctx.send(embed=lib.Editable(self, "Oops!", f"You forgot something!\n\n{ctx.prefix}role add (role) (@user)\n\n This will add the role to the user.", "Role Usage"))
                await lib.eraset(self, ctx, u)
        else:
            p = await ctx.send(embed=lib.NoPerm(self))
            await lib.eraset(self, ctx, p)

    @role.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def remove(self, ctx, rolename=None, member: discord.Member=None):
        if ctx.author.guild_permissions.manage_roles:
            if rolename and member:
                role = discord.utils.get(ctx.message.guild.roles, name=rolename)
                if role in ctx.guild.roles:
                    if role in member.roles:
                        await member.remove_roles(role)
                        d = await ctx.send(embed=lib.Editable(self, "Role Removed", f"The role **{role}** was removed from **{member.name}**", "Roles"))
                        await lib.eraset(self, ctx, d)
                    else:
                        e = await ctx.send(embed=lib.Editable(self, "Error", f"**{member.name}** does not have the role **{role}**", "Roles"))
                        await lib.eraset(self, ctx, e)
                else:
                    e = await ctx.send(embed=lib.Editable(self, "Error", f"The role **{rolename}** doesnt exist!", "Roles"))
                    await lib.eraset(self, ctx, e)
            else:
                u = await ctx.send(embed=lib.Editable(self, "Oops!", f"You forgot something!\n\n{ctx.prefix}role remove (role) (@user)\n\n This will remove the role from the user.", "Roles"))
                await lib.eraset(self, ctx, u)
        else:
            p = await ctx.send(embed=lib.NoPerm(self))
            await lib.eraset(self, ctx, p)

    @role.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def create(self, ctx, rolename=None):
        if ctx.author.guild_permissions.manage_roles:
            if rolename:
                role = discord.utils.get(ctx.message.guild.roles, name=rolename)
                if role in ctx.message.guild.roles:
                    e = await ctx.send(embed=lib.Editable(self, "Error", f"The role **{rolename}** already exists!", "Roles"))
                    await lib.eraset(self, ctx, e)
                else:
                    await ctx.guild.create_role(name=rolename)
                    d = await ctx.send(embed=lib.Editable(self, "Role Created", f"The role **{rolename}** has been created!", "Roles"))
                    await lib.eraset(self, ctx, d)
            else:
                u = await ctx.send(embed=lib.Editable(self, "Oops!", f"You forgot something!\n\n{ctx.prefix}role create (role)\n\n This will create a role with the specified name.", "Role Usage"))
                await lib.eraset(self, ctx, u)
        else:
            p = await ctx.send(embed=lib.NoPerm(self))
            await lib.eraset(self, ctx, p)

    @role.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def delete(self, ctx, rolename=None):
        if ctx.author.guild_permissions.manage_roles:
            if rolename:
                role = discord.utils.get(ctx.message.guild.roles, name=rolename)
                if role in ctx.message.guild.roles:
                    await role.delete()
                    d = await ctx.send(embed=lib.Editable(self, "Role Deleted", f"The role **{rolename}** has been deleted!", "Roles"))
                    await lib.eraset(self, ctx, d)
                else:
                    e = await ctx.send(embed=lib.Editable(self, "Error", f"The role **{rolename}** doesnt exist!", "Roles"))
                    await lib.eraset(self, ctx, e)
            else:
                u = await ctx.send(embed=lib.Editable(self, "Oops!", f"You forgot something!\n\n{ctx.prefix}role delete (role)\n\n This will delete the role with the specified name.", "Role Usage"))
                await lib.eraset(self, ctx, u)
        else:
            p = await ctx.send(embed=lib.NoPerm(self))
            await lib.eraset(self, ctx, p)

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            server = message.guild
            gid = str(server.id)
            cc = self.cc
            prefix = ctx.prefix

            if not prefix:
                return

            if gid in cc:
                cmdlist = cc[gid]
                cmd = message.content[len(prefix):]
                if cmd in cmdlist:
                    cmd = cmdlist[cmd]
                    dest = message.channel
                    await dest.send(cmd)
                elif cmd.lower() in cmdlist:
                    cmd = cmdlist[cmd.lower()]
                    cmd = self.format_cc(cmd, message)
                    dest = message.channel
                    await dest.send(cmd)
        except Exception as e:
            return

    def format_cc(self, command, message):
        results = re.findall("\{([^}]+)\}", command)
        for result in results:
            param = self.transform_parameter(result, message)
            command = command.replace("{" + result + "}", param)
        return command

# Fun Commands --------------------------------------------------------------------------------

    @commands.command(no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def ping(self, ctx):
        await ctx.send("Pong")

    @commands.command(no_pm=True, aliases=["cf"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def coinflip(self, ctx):
        await ctx.send("Flipping...")
        await asyncio.sleep(2)
        choices = ["Heads", "Tails"]
        rancoin = random.choice(choices)
        await ctx.send("You flipped a " + rancoin)

    @commands.command(aliases=["color"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def colour(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("http://www.colr.org/json/color/random") as r:
                res = await r.json(content_type=None)
                colour = res["new_color"]
                embedcolour = int(colour, 16)
                embed = discord.Embed(
                    title = "#" + colour,
                    colour = embedcolour
                    )
                await ctx.send(embed=embed)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def space(self, ctx):
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://api.open-notify.org/iss-now.json") as r:
                    res = await r.json()
                    async with cs.get("http://api.open-notify.org/astros.json") as r2:
                        res2 = await r2.json()
                        latitude = res["iss_position"]["latitude"]
                        longitude = res["iss_position"]["longitude"]
                        people = res2["number"]
                        name = ctx.author.name
                        avatar = ctx.author.avatar_url
                        embed = discord.Embed(
                            title = "International Space Station",
                            colour = 0x9bf442,
                            timestamp=datetime.datetime.utcnow()
                            )
                        embed.add_field(name="Longitude", value=f"{longitude}", inline=True)
                        embed.add_field(name="Latitude", value=f"{latitude}", inline=True)
                        embed.add_field(name="People in Space", value=f"{people}", inline=True)
                        embed.set_footer(text="Devolution | Space", icon_url="https://i.imgur.com/BS6YRcT.jpg")
                        await ctx.send(embed=embed)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def roll(self, ctx, number : int = 100):
        author = ctx.author
        if number > 1:
            n = random.randint(1, number)
            await ctx.send(f"{author.mention} :game_die: {n} :game_die:")
        else:
            number = 69
            n = random.randint(1, number)
            await ctx.send(f"{author.mention} :game_die: {n} :game_die:")

    @commands.command(no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def insult(self, ctx, user : discord.Member=None):
        author = ctx.author
        msg = " "
        if user != None:
            if user.id == self.bot.user.id:
                msg = " How original. No one else had thought of trying to get the bot to insult itself. I applaud your creativity. Yawn. Perhaps this is why you don't have friends. You don't add anything new to any conversation. You are more of a bot than me, predictable answers, and absolutely dull to have an actual conversation with."
                await ctx.send(author.mention + msg)
            else:
                await ctx.send(user.mention + msg + randchoice(self.insults))
        else:
                await ctx.send(author.mention + msg + randchoice(self.insults))

    @commands.command(no_pm=True, aliases=["tits"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def boobs(self, ctx):
        author = ctx.author
        rdm = random.randint(0, self.settings["ama_boobs"])
        search = (f"http://api.oboobs.ru/boobs/{rdm}")
        async with aiohttp.ClientSession() as cs:
            async with cs.get(search) as r:
                result = await r.json()
                boob = randchoice(result)
                boob = "http://media.oboobs.ru/{}".format(boob["preview"])
            await ctx.send(boob)

    @commands.command(no_pm=True, aliases=["booty"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def ass(self, ctx):
        author = ctx.author
        rdm = random.randint(0, self.settings["ama_ass"])
        search = (f"http://api.obutts.ru/butts/{rdm}")
        async with aiohttp.ClientSession() as cs:
            async with cs.get(search) as r:
                result = await r.json(content_type=None)
                ass = randchoice(result)
                ass = "http://media.obutts.ru/{}".format(ass["preview"])
            await ctx.send(ass)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def gif(self, ctx, *keywords):
        url = (f"http://api.giphy.com/v1/gifs/search?&api_key=dc6zaTOxFJmzC&q={keywords}")
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                result = await r.json()
                if r.status == 200:
                    if result["data"]:
                        g = await ctx.send(result["data"][0]["url"])
                    else:
                        e = await ctx.send(embed=lib.Editable(self, "Error", "No search results found", "Giphy"))
                        await lib.eraset(self, ctx, e)
                else:
                    ee = await ctx.send(embed=lib.Editable(self, "Error", f"There was an error contacting the API! Report this with {ctx.prefix}bug", "Giphy"))
                    await lib.eraset(self, ctx, ee)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def gifr(self, ctx, *keywords):
        url = (f"http://api.giphy.com/v1/gifs/random?&api_key=dc6zaTOxFJmzC&tag={keywords}")
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                result = await r.json()
                if r.status == 200:
                    if result["data"]:
                        g = await ctx.send(result["data"]["url"])
                    else:
                        e = await ctx.send(embed=lib.Editable(self, "Error", "No search results found", "Giphy"))
                        await lib.eraset(self, ctx, e)
                else:
                    ee = await ctx.send(embed=lib.Editable(self, "Error", f"There was an error contacting the API! Report this with {ctx.prefix}bug", "Giphy"))
                    await lib.eraset(self, ctx, ee)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def owo(self, ctx, user : discord.Member=None):
        o = await ctx.send(ctx.author.mention + " " + randchoice(self.owo))

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def math(self, ctx, num1 : int, op, num2 : int):
        if num1 and op and num2:
            if op == "+":
                ans = num1 + num2
            elif op == "-":
                ans = num1 - num2
            elif op == "*":
                ans = num1 * num2
            elif op == "/":
                ans = num1 / num2
            await ctx.send(embed=lib.Editable(self, f"You requested {num1} {op} {num2}", f"{num1} {op} {num2} = {ans}", "Maths"))
        else:
            await ctx.send(embed=lib.Editable(self, "Uh oh", "You need to provide a number, operator and another number.\nExamples\n\n1 + 1\n1 - 1\n 1 * 1\n 1 / 1", "Maths"))

# Fun End --------------------------------------------------------------------------------

# Leveling System Start ------------------------------------------------------------------

    @commands.Cog.listener(name="on_message")
    async def on_message_(self, message):
        try:
            GID = str(message.guild.id)
            UID = str(message.author.id)
            if GID in self.levels:
                if self.levels[GID]["Enabled"] is True:
                    if message.author != self.bot.user:
                        if self.db_exists(GID, UID):
                            if self.user_exists(GID, UID):
                                self.add_xp(GID, UID)
                                await self.level_up(message)
                                self.db.sync()
                            else:
                                self.setup(message)
                        else:
                            self.setup(message)
                    else:
                        return
                else:
                    return
            else:
                self.levels[GID] = {"Enabled": True, "Messages": True}
                with open("./data/settings/leveling.json", "w") as f:
                    json.dump(self.levels, f)
        except AttributeError:
            return

    @commands.group(invoke_without_command=True)
    async def leveling(self, ctx):
        await ctx.send(embed=lib.Editable(self, "Information", f"`{ctx.prefix}leveling progress` - Shows your progress to the next level\n`{ctx.prefix}leveling calculate (level)` - Gives you the required XP for given level\n\n**Admin Commands**\n`{ctx.prefix}leaderboard` - To show the highest rankers in the server\n`{ctx.prefix}leveling toggle` - To enable the leveling system\n`{ctx.prefix}leveling toggle messages` - Disables level up messages for the guild", "Leveling"))

    @leveling.group(invoke_without_command=True)
    async def progress(self, ctx):
        global required_xp
        GID = str(ctx.guild.id)
        UID = str(ctx.author.id)
        xp = self.db["Levels"][GID][UID]["xp"]
        level = self.db["Levels"][GID][UID]["level"]
        await ctx.send(embed=lib.Editable(self, f"{ctx.author.name}'s Level Progression Report", f"Your XP: {xp}\nYour Level: {level}\n\nLevel {level + 1} requires: {required_xp} XP\n XP To Level Up: {required_xp - xp} XP", "Leveling"))

    @leveling.group(invoke_without_command=True)
    async def calculate(self, ctx, level :int = None):
        if level:
            xp = level * 25
            await ctx.send(embed=lib.Editable(self, f"Level {level} Calculation", f"Level {level} requires {xp} XP", "Leveling"))


    @leveling.group(invoke_without_command=True)
    async def toggle(self, ctx):
        GID = str(ctx.guild.id)
        if ctx.author.guild_permissions.manage_roles:
            if GID in self.levels:
                if self.levels[GID]["Enabled"] is False:
                    self.levels[GID]["Enabled"] = True
                    with open("./data/settings/leveling.json", "w") as f:
                        json.dump(self.levels, f)
                else:
                    self.levels[GID]["Enabled"] = False
                    with open("./data/settings/leveling.json", "w") as f:
                        json.dump(self.levels, f)
            else:
                self.levels[GID] = {"Enabled": True, "Messages": True}
                with open("./data/settings/leveling.json", "w") as f:
                    json.dump(self.levels, f)
        else:
            p = await ctx.send(embed=lib.NoPerm(self))
            await lib.eraset(self, ctx, p)

    @commands.command()
    async def leaderboard(self, ctx):
        GID = str(ctx.guild.id)
        UID = str(ctx.author.id)
        if self.user_exists:
            top = 10
            level_sorted = sorted(self.db["Levels"][GID].items(), key=lambda x: x[1]["xp"], reverse=True)
            if len(level_sorted) < top:
                top = len(level_sorted)
            topten = level_sorted[:top]
            highscore = ""
            place = 1
            for id in topten:
                highscore += str(place).ljust(len(str(top))+1)
                highscore += (id[1]["name"]+ "'s XP:" + " ").ljust(23-len(str(id[1]["xp"])))
                highscore += str(id[1]["xp"]) + "\n"
                place += 1
            await ctx.send(embed=lib.Editable(self, f"Top 10", f"{highscore}", "Leveling"))
        else:
            self.setup(message)

    @toggle.group()
    async def messages(self, ctx):
        GID = str(ctx.guild.id)
        if ctx.author.guild_permissions.manage_roles:
            if GID in self.levels:
                if self.levels[GID]["Messages"] is False:
                    self.levels[GID]["Messages"] = True
                    with open("./data/settings/leveling.json", "w") as f:
                        json.dump(self.levels, f)
                else:
                    self.levels[GID]["Messages"] = False
                    with open("./data/settings/leveling.json", "w") as f:
                        json.dump(self.levels, f)

            else:
                self.levels[GID] = {"Enabled": True, "Messages": True}
        else:
            p = await ctx.send(embed=lib.NoPerm(self))
            await lib.eraset(self, ctx, p)

    def db_exists(self, GID, UID):
        GID = str(GID)
        UID = str(UID)
        if GID in self.db["Levels"]:
            return True
        else:
            return False

    def user_exists(self, GID, UID):
        GID = str(GID)
        UID = str(UID)
        if self.db_exists:
            if UID in self.db["Levels"][GID]:
                return True
            else:
                return False
        else:
            return False

    def add_xp(self, GID, UID):
        GID = str(GID)
        UID = str(UID)
        if self.user_exists(GID, UID):
            self.db["Levels"][GID][UID]["xp"] += 1

    def setup(self, message):
        GID = str(message.guild.id)
        UID = str(message.author.id)
        user = message.author
        if self.db_exists(GID, UID):
            if not self.user_exists(GID, UID):
                self.db["Levels"][GID] = {UID: {"name": user.name, "level": 0, "xp": 0}}
                self.db.sync()
        else:
            self.db["Levels"][GID] = {UID: {"name": user.name, "level": 0, "xp": 0}}
            self.db.sync()


    async def level_up(self, message):
        GID = str(message.guild.id)
        UID = str(message.author.id)
        global required_xp
        if self.user_exists:
            xp = self.db["Levels"][GID][UID]["xp"]
            level = self.db["Levels"][GID][UID]["level"]
            if level == 0:
                required_xp = 15
                pass
            else:
                required_xp = 25 * level
                pass
            if xp >= required_xp:
                self.db["Levels"][GID][UID]["level"] += 1
                if self.levels[GID]["Messages"] is True:
                    await message.channel.send(embed=lib.Editable(self, "Level Up!", f"{message.author.name} Leveled up to {level + 1}", "Leveling"))
        else:
            await self.setup(message)



def setup(bot):
    bot.add_cog(Core(bot))
