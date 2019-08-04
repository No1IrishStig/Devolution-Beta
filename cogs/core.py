import datetime
import discord
import asyncio
import json
import time
import re


from utils import default
from utils.default import lib
from discord.ext import commands

start_time = time.time()

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("./data/customcommands/commands.json") as f:
            self.cc = json.load(f)
            with open("./utils/essentials/deltimer.json") as f:
                self.deltimer = json.load(f)

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
        embed.add_field(name="Economy", value="**bank**\n\n**register** - Creates a bank account at Devo Bank\n**balance** - Returns your balance\n**transfer** - Send credits to your friends\n**set** - Set the credits of an account\n**economyset** - Change economy values\n**slot** - Play the slot machine", inline=False)
        embed.add_field(name="Useful", value="**say** - Speak as the bot\n**rename** - Change a users nickname\n**invite** - Gives usage details\n**embed** - Creates an embed message\n**role** - Gives role options\n**music** - Gives music help\n**customcommand** - Add customcommands to your server", inline=False)
        embed.add_field(name="Moderation", value="**kick** - Kick a mentioned user\n**ban** - Ban a mentioned user\n**hackban** - Allows you to ban a UserID\n**punish** - Gives mute options\n**cleanup** - Gives message moderation options\n**clean** - Deletes the last 100 command messages and bot messages\n**logs** - Get logs on nearly everything\n**deltimer** - Change the timer at which the bot auto deletes its messages", inline=False)
        embed.add_field(name="Admin", value="**leave** - Makes the bot leave the guild\n**leaveid** - Leaves a server by ID\n**setpresence(sp)** - Change the playing status of the bot.\n**shutdown** - Sends the bot into a deep sleep ...\n**cog** - Displays list of Cog Options\n**todo** - Displays List of shit todo\n**pm** - PMs Target user as bot\n**pmid** - PMs target ID as bot\n**amiadmin** - Tells you if your UserID is inside the cfg file.\n**admin** - Add and remove admins", inline=False)
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
            description = "__**Changelog (04/07/2019) v1.4**__\n+ Added !deltimer\n\n- Fixed time being off in logs\n- Bug Fixes\n- Updated help command\n\n__**Changelog (05/07/2019) v1.5**__\n+ Added !admin\n\n- Bug fixes\n\n__**Changelog (05/07/2019) v1.5**__\n+ Added !admin\n\n- Changed !amiadmin to incorperate the new admin command\n- Updated error handler\n- Bug fixes\n\n__**Changelog (06/07/2019) v1.5.1\n\n- Bug fixes\n\n__**Changelog (03/08/2019) v1.6**__\n+ Added custom prefix support\n+ Added economy update\n+ Added slots\n\n- Optimized code and remove unnecessary checks.\n- Added Economy to help command\n- Bug Fixes\n\n__**Changelog (03/08/2019) v1.6.1**__\n- Made each server have its own bank\n- Many code optimizations\n- Began work on blackjack\n- Bug fixes",
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

    @commands.group(aliases=["cc"], invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def customcommand(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            await ctx.send(embed=lib.Editable("Custom Commands - Usage", f"{ctx.prefix}cc add (name) (text)\n{ctx.prefix}cc edit (name) (text)\n{ctx.prefix}cc delete (name)\n{ctx.prefix}cc list\n\nAllows for the use of custom commands.", "Custom Commands"))
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @customcommand.command(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def add(self, ctx, command : str=None, *, text):
        if ctx.author.guild_permissions.manage_messages:
            server = ctx.guild
            gid = str(server.id)
            cc = self.cc
            if command is None:
                await ctx.send(embed=lib.Editable("Custom Commands - Usage", f"{ctx.prefix}cc add (name) (text)\n\nCreate a custom command on this server.", "Custom Commands"))
            else:
                command = command.lower()
                if command in self.bot.commands:
                    await ctx.send(embed=lib.Editable("Error", "That command already exists!", "Error"))
                    return
                if gid not in cc:
                    cc[gid] = {}
                cmdlist = cc[gid]
                if command not in cmdlist:
                    cmdlist[command] = text
                    cc[gid] = cmdlist
                    with open("./data/customcommands/commands.json", "w") as f:
                        json.dump(cc, f)
                        await ctx.send(embed=lib.Editable("Success", "Custom command successfully added.", "Custom Commands"))
                else:
                    await ctx.send(embed=lib.Editable("Error", f"This customcommand already exists. Use `{ctx.prefix}customcommand edit` to edit it.", "Error"))
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @customcommand.command(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def edit(self, ctx, command : str=None, *, text):
        if ctx.author.guild_permissions.manage_messages:
            server = ctx.guild
            cc = self.cc
            gid = str(server.id)
            if command is None:
                await ctx.send(embed=lib.Editable("Custom Commands - Usage", f"{ctx.prefix}cc edit (name) (text)\n\nEdit a custom command on this server.", "Custom Commands"))
            else:
                command = command.lower()
                if gid in cc:
                    cmdlist = cc[gid]
                    if command in cmdlist:
                        cmdlist[command] = text
                        cc[gid] = cmdlist
                        with open("./data/customcommands/commands.json", "w") as f:
                            json.dump(cc, f)
                            await ctx.send(embed=lib.Editable("Success", "Custom command successfully edited.", "Custom Commands"))
                    else:
                        await ctx.send(embed=lib.Editable("Error", f"That command doesn't exist. Use `{ctx.prefix}!customcom add` to add it.", "Error"))
                else:
                    await ctx.send(embed=lib.Editable("Error", f"There are no custom commands in this server. Use `{ctx.prefix}customcom add` to start adding some.", "Error"))
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @customcommand.command(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def delete(self, ctx, command:str=None):
        if ctx.author.guild_permissions.manage_messages:
            server = ctx.guild
            cc = self.cc
            gid = str(server.id)
            if command is None:
                await ctx.send(embed=lib.Editable("Custom Commands - Usage", f"!{ctx.prefix} delete (name)\n\nDelete a custom command on this server.", "Custom Commands"))
            else:
                command = command.lower()
                if gid in cc:
                    cmdlist = cc[gid]
                    if command in cmdlist:
                        cmdlist.pop(command, None)
                        cc[gid] = cmdlist
                        with open("./data/customcommands/commands.json", "w") as f:
                            json.dump(cc, f)
                            await ctx.send(embed=lib.Editable("Success", "Custom command successfully deleted.", "Custom Commands"))
                    else:
                        await ctx.send(embed=lib.Editable("Error", "That command doesn't exist.", "Error"))
                else:
                    await ctx.send(embed=lib.Editable("Error", f"There are no custom commands in this server. Use `{ctx.prefix}customcom add` to start adding some.", "Error"))
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @customcommand.command(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def list(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            server = ctx.guild
            cc = self.cc
            gid = str(server.id)

            commands = cc.get(gid, {})

            if not commands:
                await ctx.send(embed=lib.Editable("Error", f"There are no custom commands for this server. Use `{ctx.prefix}customcommand add` to start adding some.", "Error"))
                return

            commands = ", ".join([ctx.prefix + c for c in sorted(commands)])
            commands = "Custom commands:\n\n" + commands

            if len(commands) < 1500:
                await ctx.send(commands)
            else:
                for page in pagify(commands, delims=[" ", "\n"]):
                    await ctx.author.send(page)
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




def setup(bot):
    bot.add_cog(Core(bot))
