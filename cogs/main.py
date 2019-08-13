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
from utils.default import lib
from discord.ext import commands
from random import choice as randchoice

start_time = time.time()

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = shelve.open("./data/db/data.db", writeback=True)
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

    @commands.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx):
        await ctx.message.add_reaction("📄")
        author = ctx.author
        embed = discord.Embed(
            title = "Help",
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        embed.set_author(name="Devolution", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        embed.set_footer(text="Devolution | Help", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        embed.add_field(name="Information", value="**help** - Gives help!\n**help permissions** - Gives a list of permissions the bot requires to function\n**bug** - Use it to report bugs.\n**suggest** - Suggest something to the dev\n**sinfo** - Displays guild information.\n**uinfo** - Displays user information\n**uptime** - Displays the bots uptime\n**about** - Displays stuff about the bot\n**changelog** - Displays the entire bots changelog\n**github** - Provides github link", inline=False)
        embed.add_field(name="Fun", value="**coinflip** - Flip a coin\n**space** - Get live information about the ISS\n**colour** - Get a random colour\n**roll** - Roles a dice\n**insult** - Insult people you dislike!\n**boobs** - See some melons!\n**ass** - See some peaches!\n**gif** - Search up a gif on giphy by name\n**gifr** - Gives a random gif from giphy\n**owo** - Get random responses", inline=False)
        embed.add_field(name="Economy", value="**bank**\n\n**register** - Creates a bank account at Devo Bank\n**balance** - Returns your balance\n**transfer** - Send credits to your friends\n**set** - Set the credits of an account\n**economyset** - Change economy values\n**slot** - Play the slot machine\n**blackjack** - Gives details on how to play (Updated Soon)", inline=False)
        embed.add_field(name="Useful", value="**say** - Speak as the bot\n**rename** - Change a users nickname\n**invite** - Gives usage details\n**embed** - Creates an embed message\n**role** - Gives role options\n**music** - Gives music help", inline=False)
        embed.add_field(name="Moderation", value="**kick** - Kick a mentioned user\n**ban** - Ban a mentioned user\n**hackban** - Allows you to ban a UserID\n**punish** - Gives mute options\n**cleanup** - Gives message moderation options\n**clean** - Deletes the last 100 command messages and bot messages\n**logs** - Get logs on nearly everything\n**deltimer** - Change the timer at which the bot auto deletes its messages\n**warn** - Warnings System", inline=False)
        embed.add_field(name="Admin", value="**leave** - Makes the bot leave the guild\n**leaveid** - Leaves a server by ID\n**setpresence(sp)** - Change the playing status of the bot.\n**shutdown** - Sends the bot into a deep sleep ...\n**cog** - Displays list of Cog Options\n**todo** - Displays List of shit todo\n**pm** - PMs Target user as bot\n**pmid** - PMs target ID as bot\n**amiadmin** - Tells you if your UserID is inside the cfg file.\n**admin** - Add and remove admins\n**leveling** - Enable leveling system", inline=False)
        await author.send(embed=embed)
        await asyncio.sleep(10)
        await ctx.message.delete()

    @help.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def permissions(self, ctx):
        await ctx.message.add_reaction("📄")
        author = ctx.author
        embed = discord.Embed(
            title = "Help",
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        embed.set_author(name="Devolution", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        embed.set_footer(text="Devolution | Bot Permission Help", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        embed.add_field(name="Permission Requirements", value="Manage Roles\nManage Channels\nKick Members\n Ban Members\nManage Nicknames\nRead Channels\nSend Messages\nManage Messages\nAdd Reactions\nConnect\nSpeak", inline=False)
        await author.send(embed=embed)
        await asyncio.sleep(10)
        await ctx.message.delete()

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def prefix(self, ctx, prefix:str=None):
        if ctx.author.guild_permissions.administrator:
            if prefix:
                self.config["prefix"] = prefix
                with open("./utils/cfg.json", "w") as f:
                    json.dump(self.config, f)
                await ctx.send(f"Your prefix has been set to {ctx.prefix}\n\nYour bot will need a full restart for this to apply :frowning:. Using {ctx.prefix}restart will not work.")
            else:
                await ctx.send(embed=lib.Editable("Uh oh", "You need to give me a prefix to use", "Prefix"))

        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def changelog(self, ctx):
        user = ctx.author
        await ctx.message.add_reaction("📄")
        e = discord.Embed(
            description = "__**Changelog (15/12/2018) v0.0.1 Beta 1**__\n+ Added Help command\n+ Added Ping command\n+ Added Music Cog\n\n__**Changelog (16/12/2018) v0.0.2 Beta 2**__\n+ Added shutdown command\n\n- Changed some Music messages to embeds\n\n__**Changelog (18/12/2018) v0.0.3 Beta 3**__\n- Finished changing all music embeds\n- Updated help command\n\n__**Changelog (21/12/2018) v0.0.4 Beta 4**__\n+ Added sinfo command\n\n- Edited many embed messages in music commands\n- Updated Help command\n- Music Cog Work\n\n__**Changelog (21/12/2018  v0.0.5 Beta 5**__\n+ Added Uptime command\n+ Added Kick command\n\n- Fixed all timestamps to make them actually work\n- Changed set presence command to an embed\n- Updated Help command\n\n__**Changelog (22/12/2018) v0.1**__\n+ Added Cog check, if you arent me, goodluck using that one\n+ Added Cog commands Load, Unload and List\n+ Added Set Presence command (Alias sp)\n\n- Updated Help command\n\n__**Changelog (23/12/2018) v0.1.1**__\n+ Added Avatar command\n+ Added Avatar command\n+ Added purge command\n+ Added uinfo command\n+ Added ban command\n+ Added say command\n+ Added about command\n+ Added pm Command\n\n- Changed kick embed message, bot sends embed to kicked user {server} {kicked_by} {reason (if there was one)}\n- Kick command now accepts reasons\n- Updated Help command\n\n__**Changelog (29/12/2018) v0.1.2**__\n+ Added rename command\n+ Added coinflip command\n\n- Updated Help command\n\n__**Changelog (04/01/2019) v0.1.3**__\n- Changed music play embed again",
            colour = 0x9bf442,
            )
        e.set_author(name="Stig#1337 - The developer of Devolution", icon_url="https://cdn.discordapp.com/avatars/439327545557778433/a_09b7d5d0f8ecbd826fe3f7b15ee2fb93.gif")
        await user.send(embed=e)
        ee = discord.Embed(
            description = "__**Changelog (04/01/2019) v0.2**__\n+ Added Colour command\n+ Added Meme command\n+ Added Space command\n\n- Updated Help command\n\n__**Changelog (14/01/2019) v0.2.1**__\n+ Added Prefix command\n+ Added Leave command\n\n- Reworked Invite command\n- Updated Help command\n\n__**Changelog (24/01/2019) v0.2.2**__\n+ Added spp command (Set punish permissions)\n+ Added punish & unpunish commands\n\n- Updated Help command\n\n__**Changelog (26/01/2019) v0.3 **__\n- Major code overhaul\n- File sizes cut in half, bot should now run smoother\n\n__**Changelog (26/01/2019) v0.3.1**__\n+ Added lspunish command\n+ Added Embed command\n\n- Updated Punish command to give usage details\n- Updated Help command\n\n__**Changelog (27/01/2019) v0.4 **__\n+ Added role commands\n+ Added Bug command\n\n- Updated Help command\n\n__**Changelog (02/03/2019) v0.5 **__\n+ Added changelog command (So you can see all this)\n+ Added new cog for tournaments\n+ Added Tournament commands\n\n- Updated bots default playing status\n- Updated Help command\n\n__**Changelog (09/03/2019) v0.5.1**__\n+ Added volume min and max 0 - 200\n\n - Fixed anyone being able to skip on the fist vote\n - Fixed Embed Messages not sending\n- Fixed Music failing to play\n\n__**Changelog (16/06/2019) v1.0 **__\n- Rewrote the entire bot into the newest version of Python and Discordpy\n- Updated Todo Command and made it public\n- Reworked Bug report command\n- Reworked help command\n\n__**Changelog (17/06/2019) v1.0.1 **__\n+ Added a command to list all roles in a server\n+ Added github issue link to bug command\n+ Reintroduced the beloved data folder!\n+ Added Boobs & Ass command\n+ Added Insult command\n+ Added roll command\n+ Added bot launcher\n+ Added Cleanup\n\n- Huge amounts of optimization with the cogs\n- Removed meme api as it was broken\n- Removed unnecessary json loading\n- Squashed a **lot** of nasty bugs\n- Removed Purge command\n- Removed prefix command\n- Removed tournament cog",
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        await user.send(embed=ee)
        eee = discord.Embed(
            description = "__**Changelog (17/06/2019) v1.0.2**__\nAdded music command!(Play, Pause, Resume, volume, Stop)\n+ Added gif and gifr commands\n+ Added Hackban!\n+ Added pmid\n\n- Reworked the changelog command and put it in size order (iiCarelessness)\n- Reworked and updated Help command\n- Planted logos everywhere!\n\n__**Changelog (18/06/2019) v1.1**__\n+ Added a launcher gui with a few features\n+ Added Set Activity command\n+ Created a new admin cog\n+ Added amiadmin command\n+ Added utils folder\n+ Added config file\n\n- Merged lib into a new file named default inside util\n- Music now creates a folder for songs\n- Updated help command\n- Fixed some music bugs\n\n__**Changelog (18/06/2019) v1.1.1**__\n+ Added owo command (944)\n\n- Fixed Punish not setting channel permissions\n- Finished Cleanup command\n- Fixed volume command\n- Updated help command\n- Added clean command\n- Bug Fixes\n\n__**Changelog (21/06/2019) v1.2**__\n+ Added Error handler (catches and resolves errors automatically)\n+ Added help command for bot required permissions\n+ Added self delete function to every command\n+ Added 'role exist' check to remove and add\n+ Added sstop command (Force stop song)\n+ Added command cooldowns\n\n- Updated 'Forgot Something' errors to add more detail and to give a similar appearance\n- Reworked invite command (Invite ClientID is now based on the bots ID)\n- Changed stop command so only the song player can stop the song\n- Rewrote every command and optimized a lot of code\n- Rearranged and removed unused imports\n- Tweaked and tidied changelog output\n- Reverted and updated help command\n- Placed all commands into cogs\n- Reworked Cog loading system\n- Removed todo command\n- Reworked every cog\n- Reworked bot.py file\n- Bug Fixes\n\n__**Changelog (21/06/2019) v1.3**__\n+ Added customcommands\n+ Added leaveid\n+ Added logs\n\n- Added permission check to spp\n- Updated help command\n- Updated changelog\n- Bug fixes\n\n__**Changelog (23/06/2019) v1.3.1**__\n- Fixed cleanup after\n- Bug fixes",
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        await user.send(embed=eee)
        eeee = discord.Embed(
            description = "__**Changelog (04/07/2019) v1.4**__\n+ Added !deltimer\n\n- Fixed time being off in logs\n- Bug Fixes\n- Updated help command\n\n__**Changelog (05/07/2019) v1.5**__\n+ Added !admin\n\n- Bug fixes\n\n__**Changelog (05/07/2019) v1.5**__\n+ Added !admin\n\n- Changed !amiadmin to incorperate the new admin command\n- Updated error handler\n- Bug fixes\n\n__**Changelog (06/07/2019) v1.5.1\n\n- Bug fixes\n\n__**Changelog (03/08/2019) v1.6**__\n+ Added custom prefix support\n+ Added economy update\n+ Added slots\n\n- Optimized code and remove unnecessary checks.\n- Added Economy to help command\n- Bug Fixes\n\n__**Changelog (03/08/2019) v1.6.1**__\n- Made each server have its own bank\n- Many code optimizations\n- Began work on blackjack\n- Bug fixes\n\n__**Changelog (05/08/2019) v1.6.3**__\n+ Added a restart command (This only restarts the connection, wont apply any file changes)\n+ Added checks to bank balance, bank register, bank transfer, bank set, benefits and top\n+ Added blackjack\n\n- Removed unnecessary checks\n- Code optimization\n- Many bug fixes\n\n__**Changelog (05/08/2019) v1.6.4**__\n+ Added check to !blackjack command and more information\n+ Added a message to show if the house hit or stood\n+ Added a Tie Check to blackjack\n\n- Fixed a bug when losing after standing where all cards are shown\n- Fixed bank balance\n\n__**Changelog (11/08/2019) v1.6.6**__\n+ Began work on leveling system\n\n- Began work on changing the way data is stored\n- Completely reworked the blackjack logic\n- Reworked and removed cogs\n\n__**Changelog (12/08/2019) v1.7**__\n+ Added check if punished users try rejoin\n+ Added some new folders\n+ Added Database Check\n+ Added Timer to Punish\n\n- Reworked Economy and Admins to use Database\n- Removed some checks from bot.py\n- Removed checks from default.py\n- Removed a lot of the json files\n- Remove customcommand\n- Updated Help Command\n- Added cmd_data folder\n- Added Settings folder\n- Cleaned up imports\n\n__**Changelog (13/08/2019) v1.7.2**__\n+ Added Warnings System\n+ Added Leveling System\n\n- Bug Fixes and Improvements\n- Updated JSON Check\n- Updated Help",
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        eeee.set_footer(text="Devolution | Changelogs", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        await user.send(embed=eeee)
        await asyncio.sleep(10)
        await ctx.message.delete()

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
        embed.set_author(name="Devolution", icon_url="https://i.imgur.com/BS6YRcT.jpg")
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
        ques = await ctx.channel.send("What would you like to say?")
        msg = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout = 120)
        user = ctx.author
        userid = ctx.author.id
        guild = ctx.message.guild.name
        guildid = ctx.message.guild.id
        me = await self.bot.fetch_user("439327545557778433")
        embed = discord.Embed(
            title = f"You've recieved a bug report from {user}",
            colour = 0x9bf442,
            )
        embed.add_field(name="User ID", value=userid, inline=True)
        embed.add_field(name="Server Name", value=guild, inline=True)
        embed.add_field(name="Server ID", value=guildid, inline=True)
        embed.add_field(name="Message", value=msg.content, inline=True)
        await me.send(embed=embed)
        f = await ctx.send(embed=lib.Editable("Success", f"Thanks to you another bug is about to be squished! Thank you for your feedback **{ctx.author.name}** :smile:", "Bug Report"))
        await lib.eraset(self, ctx, f)
        await ques.delete()
        await msg.delete()

    @commands.command(no_pm=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def suggest(self, ctx):
        ques = await ctx.channel.send("What would you like to say?")
        msg = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout = 120)
        user = ctx.author
        userid = ctx.author.id
        guild = ctx.message.guild.name
        guildid = ctx.message.guild.id
        me = await self.bot.fetch_user("439327545557778433")
        embed = discord.Embed(
            title = f"You've recieved a suggestion from {user}",
            colour = 0x9bf442,
            )
        embed.add_field(name="User ID", value=userid, inline=True)
        embed.add_field(name="Server Name", value=guild, inline=True)
        embed.add_field(name="Server ID", value=guildid, inline=True)
        embed.add_field(name="Message", value=msg.content, inline=True)
        await me.send(embed=embed)
        f = await ctx.send(embed=lib.Editable("Success", f"Thank you for your suggestion! It's been sent to our dev, **{ctx.author.name}** :smile:", "Suggestion"))
        await lib.eraset(self, ctx, f)
        await ques.delete()
        await msg.delete()

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
            p = await ctx.send(embed=lib.Editable("Setting Permissions", "This may take a while, Ill tell you when im done.", "Moderation"))
            await asyncio.sleep(5)
            msg2 = await ctx.send(embed=lib.Editable("Im Finished!", "All permissions should be set.", "Moderation"))
            await lib.erase(ctx, 5, p)
            await asyncio.sleep(10)
            await msg2.delete()
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def music(self, ctx):
        m = await ctx.send(embed=lib.Editable("Music Usage", f"**{ctx.prefix}play (song/link)** - Plays a song by name or url from youtube\n**{ctx.prefix}pause** - Pauses the current song\n**{ctx.prefix}resume** - Resumes the current song\n**{ctx.prefix}volume (number)** - Change the volume of the bot\n**{ctx.prefix}stop** - Disconnects the bot\n**{ctx.prefix}sstop** - Force disconnects the bot ", "Todo"))
        await lib.eraset(self, ctx, m)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def github(self, ctx):
        user = ctx.author
        await ctx.message.add_reaction("📄")
        await user.send(embed=lib.Editable("Github", "https://github.com/No1IrishStig/Devolution-Beta/", "Github"))
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
        embed.set_author(name=f"Devolution                                                                              ID: {ctx.guild.id}", icon_url="https://i.imgur.com/BS6YRcT.jpg", )
        embed.set_footer(icon_url="https://i.imgur.com/BS6YRcT.jpg", text="Devolution | Info")
        e = await ctx.send(embed=embed)
        await lib.eraset(self, ctx, e)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def uinfo(self, ctx, user:discord.User=None):
        if user is None:
            embed = discord.Embed(
                title = "User Information",
                colour = 0x9bf442,
                timestamp=datetime.datetime.utcnow()
                )
            embed.add_field(name="Status", value=ctx.author.status, inline=True)
            embed.add_field(name="Playing", value=ctx.author.activity, inline=True)
            embed.add_field(name="Nickname", value=ctx.author.nick, inline=True)
            embed.add_field(name="Role Count", value=len(ctx.author.roles), inline=True)
            embed.add_field(name="Account Creation", value=ctx.author.created_at.strftime("Since %d/%m/%Y"), inline=True)
            embed.add_field(name="Joined guild", value=ctx.author.joined_at.strftime("Since %d/%m/%Y"), inline=True)
            embed.set_author(name=ctx.author.name + "s User Information", icon_url=ctx.author.avatar_url)
            embed.set_footer(icon_url="https://i.imgur.com/BS6YRcT.jpg", text="Devolution | Info")
            e = await ctx.send(embed=embed)
            await lib.eraset(self, ctx, e)
        else:
            embed = discord.Embed(
                title = "User Information",
                colour = 0x9bf442,
                timestamp=datetime.datetime.utcnow()
                )
            embed.add_field(name="Status", value=user.status, inline=True)
            embed.add_field(name="Playing", value=user.activity, inline=True)
            embed.add_field(name="Nickname", value=user.nick, inline=True)
            embed.add_field(name="Role Count", value=len(user.roles), inline=True)
            embed.add_field(name="Account Creation", value=user.created_at.strftime("Since %d/%m/%Y"), inline=True)
            embed.add_field(name="Joined guild", value=user.joined_at.strftime("Since %d/%m/%Y"), inline=True)
            embed.set_author(name=user.name + "s User Information", icon_url=user.avatar_url)
            embed.set_footer(icon_url="https://i.imgur.com/BS6YRcT.jpg", text="Devolution | Info")
            ee = await ctx.send(embed=embed)
            await lib.eraset(self, ctx, ee)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, user:discord.User=None):
        if user is None:
            embed = discord.Embed(
                title = "Avatar Stealer",
                description = ctx.author.avatar_url,
                colour = 0x9bf442,
                timestamp=datetime.datetime.utcnow()
                )
            embed.set_image(url=ctx.author.avatar_url)
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_footer(icon_url="https://i.imgur.com/BS6YRcT.jpg", text="Devolution | Info")
            e = await ctx.send(embed=embed)
            await lib.eraset(self, ctx, e)
        else:
            embed = discord.Embed(
                title = "Avatar Stealer",
                description = user.avatar_url,
                colour = 0x9bf442,
                timestamp=datetime.datetime.utcnow()
                )
            embed.set_image(url=user.avatar_url)
            embed.set_thumbnail(url=user.avatar_url)
            embed.set_author(name=user.name, icon_url=user.avatar_url)
            embed.set_footer(icon_url="https://i.imgur.com/BS6YRcT.jpg", text="Devolution | Info")
            e = await ctx.send(embed=embed)
            await lib.eraset(self, ctx, e)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def embed(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            ques = await ctx.send("What title?")
            msg = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout = 120)
            ques1 = await ctx.send("What would you like to say?")
            title = msg.content
            msg1 = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout = 120)
            ques2 = await ctx.send("Ok.. What footer text?")
            desc = msg1.content
            msgg = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout = 120)
            ans = await ctx.send("Generating Embed...")
            footer = msgg.content
            await asyncio.sleep(2)
            r = await ctx.send(embed=lib.Editable(title, desc, footer))
            await ques.delete()
            await msg.delete()
            await ques1.delete()
            await msg1.delete()
            await ques2.delete()
            await msgg.delete()
            await ans.delete()
            await lib.eraset(self, ctx, r)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @commands.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def role(self, ctx):
        if ctx.author.guild_permissions.manage_roles:
            u = await ctx.send(embed=lib.Editable("Role Usage!", f"**{ctx.prefix}add** - Adds a user to a role.\n**{ctx.prefix}list** - List all roles in the server\n**{ctx.prefix}remove** - Removes a user from a role\n**{ctx.prefix}create** - Creates a role\n**{ctx.prefix}delete** - Deletes a role", "Role Usage"))
            await lib.eraset(self, ctx, u)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @role.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def list(self, ctx):
        if ctx.author.guild_permissions.manage_roles:
            roles = []
            for role in ctx.guild.roles:
                roles.append(role.name)
            roles.remove("@everyone")
            l = await ctx.send(embed=lib.Editable("Role List", "{}".format(", ".join(roles)), "Roles"))
            await lib.eraset(self, ctx, l)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @role.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def add(self, ctx, rolename=None, member: discord.Member=None):
        if ctx.author.guild_permissions.manage_roles:
            if rolename and member:
                role = discord.utils.get(ctx.message.guild.roles, name=rolename)
                if role in ctx.guild.roles:
                    if role in member.roles:
                        e = await ctx.send(embed=lib.Editable("Error", f"**{member.name}** already has the role **{role}**", "Roles"))
                        await lib.eraset(self, ctx, e)
                    else:
                        await member.add_roles(role)
                        d = await ctx.send(embed=lib.Editable("Role Added", f"The role **{role}** was added to **{member.name}**", "Roles"))
                        await lib.eraset(self, ctx, d)
                else:
                    e = await ctx.send(embed=lib.Editable("Error", f"The role **{rolename}** doesnt exist!", "Roles"))
                    await lib.eraset(self, ctx, e)
            else:
                u = await ctx.send(embed=lib.Editable("Oops!", f"You forgot something!\n\n{ctx.prefix}role add (role) (@user)\n\n This will add the role to the user.", "Role Usage"))
                await lib.eraset(self, ctx, u)
        else:
            p = await ctx.send(embed=lib.NoPerm())
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
                        d = await ctx.send(embed=lib.Editable("Role Removed", f"The role **{role}** was removed from **{member.name}**", "Roles"))
                        await lib.eraset(self, ctx, d)
                    else:
                        e = await ctx.send(embed=lib.Editable("Error", f"**{member.name}** does not have the role **{role}**", "Roles"))
                        await lib.eraset(self, ctx, e)
                else:
                    e = await ctx.send(embed=lib.Editable("Error", f"The role **{rolename}** doesnt exist!", "Roles"))
                    await lib.eraset(self, ctx, e)
            else:
                u = await ctx.send(embed=lib.Editable("Oops!", f"You forgot something!\n\n{ctx.prefix}role remove (role) (@user)\n\n This will remove the role from the user.", "Roles"))
                await lib.eraset(self, ctx, u)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @role.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def create(self, ctx, rolename=None):
        if ctx.author.guild_permissions.manage_roles:
            if rolename:
                role = discord.utils.get(ctx.message.guild.roles, name=rolename)
                if role in ctx.message.guild.roles:
                    e = await ctx.send(embed=lib.Editable("Error", f"The role **{rolename}** already exists!", "Roles"))
                    await lib.eraset(self, ctx, e)
                else:
                    await ctx.guild.create_role(name=rolename)
                    d = await ctx.send(embed=lib.Editable("Role Created", f"The role **{rolename}** has been created!", "Roles"))
                    await lib.eraset(self, ctx, d)
            else:
                u = await ctx.send(embed=lib.Editable("Oops!", f"You forgot something!\n\n{ctx.prefix}role create (role)\n\n This will create a role with the specified name.", "Role Usage"))
                await lib.eraset(self, ctx, u)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @role.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def delete(self, ctx, rolename=None):
        if ctx.author.guild_permissions.manage_roles:
            if rolename:
                role = discord.utils.get(ctx.message.guild.roles, name=rolename)
                if role in ctx.message.guild.roles:
                    await role.delete()
                    d = await ctx.send(embed=lib.Editable("Role Deleted", f"The role **{rolename}** has been deleted!", "Roles"))
                    await lib.eraset(self, ctx, d)
                else:
                    e = await ctx.send(embed=lib.Editable("Error", f"The role **{rolename}** doesnt exist!", "Roles"))
                    await lib.eraset(self, ctx, e)
            else:
                u = await ctx.send(embed=lib.Editable("Oops!", f"You forgot something!\n\n{ctx.prefix}role delete (role)\n\n This will delete the role with the specified name.", "Role Usage"))
                await lib.eraset(self, ctx, u)
        else:
            p = await ctx.send(embed=lib.NoPerm())
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
                        e = await ctx.send(embed=lib.Editable("Error", "No search results found", "Giphy"))
                        await lib.eraset(self, ctx, e)
                else:
                    ee = await ctx.send(embed=lib.Editable("Error", f"There was an error contacting the API! Report this with {ctx.prefix}bug", "Giphy"))
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
                        e = await ctx.send(embed=lib.Editable("Error", "No search results found", "Giphy"))
                        await lib.eraset(self, ctx, e)
                else:
                    ee = await ctx.send(embed=lib.Editable("Error", f"There was an error contacting the API! Report this with {ctx.prefix}bug", "Giphy"))
                    await lib.eraset(self, ctx, ee)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def owo(self, ctx, user : discord.Member=None):
        o = await ctx.send(ctx.author.mention + " " + randchoice(self.owo))

# Fun End --------------------------------------------------------------------------------

# Leveling System Start ------------------------------------------------------------------


    @commands.group(invoke_without_command=True)
    async def leveling(self, ctx):
        await ctx.send(embed=lib.Editable("Uh oh", f"Looks like you forgot something.\n\n`{ctx.prefix}leaderboard - To show the highest rankers in the server\n`{ctx.prefix}leveling toggle` - To enable the leveling system\n`{ctx.prefix}leaderboard - To show the highest rankers in the server\n`{ctx.prefix}leveling toggle messages` - Disables level up messages for the guild", "Leveling"))

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
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @commands.command()
    async def leaderboard(self, ctx):
        GID = str(ctx.guild.id)
        if "Levels" in self.db and GID in self.db["Levels"]:
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
            await ctx.send(embed=lib.Editable(f"Top 10", f"{highscore}", "Leveling"))
        else:
            ctx.send("There was an error")

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
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @commands.Cog.listener(name="on_message")
    async def on_message_(self, message):
        GID = str(message.guild.id)
        UID = str(message.author.id)
        if self.levels[GID]["Enabled"] is True:
            if message.author != self.bot.user:
                if "Levels" in self.db and GID in self.db["Levels"]:
                    if UID in self.db["Levels"][GID]:
                        await self.add_xp(message, 1)
                        await self.level_up(message)
                        self.db.sync()
                    else:
                        await self.setup(message)
                        self.db.sync()
                else:
                    await self.setup(message)
                    self.db.sync()
            else:
                return
        else:
            return

    async def add_xp(self, message, exp):
        GID = str(message.guild.id)
        UID = str(message.author.id)
        self.db["Levels"][GID][UID]["xp"] += int(exp)

    async def setup(self, message):
        GID = str(message.guild.id)
        user = message.author
        UID = str(user.id)
        if "Levels" not in self.db and GID not in self.db["Levels"]:
            self.db["Levels"] = {}
            self.db["Levels"] = {GID :{UID: {"name": user.name, "level": 0, "xp": 0}}}
        else:
            self.db["Levels"][GID][UID] = {"name": user.name, "level": 0, "xp": 0}

    async def level_up(self, message):
        GID = str(message.guild.id)
        UID = str(message.author.id)
        xp = self.db["Levels"][GID][UID]["xp"]
        level = self.db["Levels"][GID][UID]["level"]
        required_xp = 10 * level
        if level == 0:
            required_xp = 10 * 1
        if xp >= required_xp:
            self.db["Levels"][GID][UID]["level"] += 1
            self.db["Levels"][GID][UID]["xp"] = 0
            if self.levels[GID]["Messages"] is True:
                newlevel = self.db["Levels"][GID][UID]["level"]
                await message.channel.send(embed=lib.Editable("Level Up!", f"{message.author.name} Leveled up to {newlevel}", "Leveling"))
            else:
                return

def setup(bot):
    bot.add_cog(Core(bot))
