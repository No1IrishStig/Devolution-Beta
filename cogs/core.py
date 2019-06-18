from discord.ext import commands
from utils.default import lib
from utils import default
import datetime
import discord
import asyncio
import time
import json

start_time = time.time()

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, invoke_without_command=True)
    async def help(self, ctx):
        await ctx.message.add_reaction("📄")
        user = ctx.author
        e1 = discord.Embed(
            description = "Use command **!help all** to see all the pages in one message\n\n1.) **info** - Gives help on all 'Information' commands\n2.) **fun** - Gives help on all 'Fun' commands\n3.) **mod** - Gives help on all 'Moderation' commands\n4.) **useful** - Gives help on all 'Useful' commands\n5.) **admin** - Gives help on all 'Admin' commands",
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        e1.set_author(name="Devolution - Help", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        e1.set_footer(text="Devolution | Help", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        await user.send(embed=e1)

    @help.group(pass_context=True, invoke_without_command=True)
    async def info(self, ctx):
        await ctx.message.add_reaction("📄")
        author = ctx.author
        e2 = discord.Embed(
            title = "Help - Information",
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        e2.set_author(name="Devolution", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        e2.set_footer(text="Devolution | Information Help", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        e2.add_field(name="Information", value="**help** - Gives help!\n**bug** - Use it to report bugs.\n**sinfo** - Displays guild information.\n**uinfo** - Displays user information\n**uptime** - Displays the bots uptime\n**about** - Displays stuff about the bot\n**changelog** - Displays the entire bots changelog\n**github** - Provides github link", inline=False)
        await author.send(embed=e2)

    @help.group(pass_context=True, invoke_without_command=True)
    async def fun(self, ctx):
        await ctx.message.add_reaction("📄")
        author = ctx.author
        e3 = discord.Embed(
            title = "Help - Fun",
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        e3.set_author(name="Devolution", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        e3.set_footer(text="Devolution | Fun Help", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        e3.add_field(name="Fun", value="**coinflip** - Flip a coin\n**space** - Get live information about the ISS\n**colour** - Get a random colour\n**roll** - Roles a dice\n**insult** - Insult people you dislike!\n**boobs** - See some melons!\n**ass** - See some peaches!\n**gif** - Search up a gif on giphy by name\n**gifr** - Gives a random gif from giphy", inline=False)
        await author.send(embed=e3)

    @help.group(pass_context=True, invoke_without_command=True)
    async def mod(self, ctx):
        await ctx.message.add_reaction("📄")
        author = ctx.author
        e4 = discord.Embed(
            title = "Help - Moderation",
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        e4.set_author(name="Devolution", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        e4.set_footer(text="Devolution | Moderation Help", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        e4.add_field(name="Moderation", value="**kick** - Kick a mentioned user\n**ban** - Ban a mentioned user\n**hackban** - Allows you to ban a UserID\n**punish** - Gives mute options\n**cleanup** - Gives message moderation options", inline=False)
        await author.send(embed=e4)

    @help.group(pass_context=True, invoke_without_command=True)
    async def useful(self, ctx):
        await ctx.message.add_reaction("📄")
        author = ctx.author
        e5 = discord.Embed(
            title = "Help - Useful",
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        e5.set_author(name="Devolution", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        e5.set_footer(text="Devolution | Useful Help", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        e5.add_field(name="Useful", value="**say** - Speak as the bot\n**rename** - Change a users nickname\n**invite** - Gives usage details\n**embed** - Creates an embed message\n**role** - Gives role options\n**music** - Gives music help", inline=False)
        await author.send(embed=e5)

    @help.group(pass_context=True, invoke_without_command=True)
    async def admin(self, ctx):
        await ctx.message.add_reaction("📄")
        author = ctx.author
        e6 = discord.Embed(
            title = "Help - Admin",
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        e6.set_author(name="Devolution", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        e6.set_footer(text="Devolution | Admin Help", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        e6.add_field(name="Admin", value="**leave** - Makes the bot leave the guild\n**setpresence(sp)** - Change the playing status of the bot.\n**shutdown** - Sends the bot into a deep sleep ...\n**cog** - Displays list of Cog Options\n**todo** - Displays List of shit todo\n**pm** - PMs Target user as bot\n**pmid** - PMs target ID as bot\n**amiadmin** - Tells you if your UserID is inside the cfg file.", inline=False)
        await author.send(embed=e6)

    @help.group(pass_context=True, invoke_without_command=True)
    async def all(self, ctx):
        await ctx.message.add_reaction("📄")
        author = ctx.author
        embed = discord.Embed(
            title = "Help",
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        embed.set_author(name="Devolution", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        embed.set_footer(text="Devolution | Help", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        embed.add_field(name="Information", value="**help** - Gives help!\n**bug** - Use it to report bugs.\n**sinfo** - Displays guild information.\n**uinfo** - Displays user information\n**uptime** - Displays the bots uptime\n**about** - Displays stuff about the bot\n**changelog** - Displays the entire bots changelog\n**github** - Provides github link", inline=False)
        embed.add_field(name="Fun", value="**coinflip** - Flip a coin\n**space** - Get live information about the ISS\n**colour** - Get a random colour\n**roll** - Roles a dice\n**insult** - Insult people you dislike!\n**boobs** - See some melons!\n**ass** - See some peaches!\n**gif** - Search up a gif on giphy by name\n**gifr** - Gives a random gif from giphy", inline=False)
        embed.add_field(name="Moderation", value="**kick** - Kick a mentioned user\n**ban** - Ban a mentioned user\n**hackban** - Allows you to ban a UserID\n**punish** - Gives mute options\n**cleanup** - Gives message moderation options", inline=False)
        embed.add_field(name="Useful", value="**say** - Speak as the bot\n**rename** - Change a users nickname\n**invite** - Gives usage details\n**embed** - Creates an embed message\n**role** - Gives role options\n**music** - Gives music help", inline=False)
        embed.add_field(name="Admin", value="**leave** - Makes the bot leave the guild\n**setpresence(sp)** - Change the playing status of the bot.\n**shutdown** - Sends the bot into a deep sleep ...\n**cog** - Displays list of Cog Options\n**todo** - Displays List of shit todo\n**pm** - PMs Target user as bot\n**pmid** - PMs target ID as bot", inline=False)
        await author.send(embed=embed)

    @commands.command(pass_context=True)
    async def changelog(self, ctx):
        user = ctx.author
        await ctx.message.add_reaction("📄")
        e = discord.Embed(
            description = '__**Changelog (15/12/2018) V0.01 Beta 1**__\n+ Added Help command\n+ Added Ping command\n+ Added Music Cog\n\n__**Changelog (16/12/2018) V0.02 Beta 2**__\n+ Added shutdown command\n\n- Changed some Music messages to embeds, the author will now be embed author for some commands\n\n__**Changelog (18/12/2018) V0.03 Beta 3**__\n- Finished changing all music embeds\n- Updated help command\n\n__**Changelog (21/12/2018) V0.04 Beta 4**__\n+ Added sinfo command\n\n- Edited many embed messages Author will now be the command author for nearly all other music commands\n- Updated Help command\n- Music Cog Work\n\n__**Changelog (21/12/2018  V0.05 Beta 5**__\n+ Added Uptime command\n+ Added Kick command\n\n- Fixed all timestamps to make them actually work\n- Changed set presence command to an embed\n- Updated Help command\n\n__**Changelog (22/12/2018) V0.1**__\n+ Added Cog check, if you arent me, goodluck using that one\n+ Added Cog commands Load, Unload and List\n+ Added Set Presence command (Alias sp)\n\n- Updated Help command\n\n__**Changelog (23/12/2018) V0.12**__\n+ Added Avatar command\n+ Added Avatar command\n+ Added purge command\n+ Added uinfo command\n+ Added ban command\n+ Added say command\n+ Added about command\n+ Added pm Command\n\n- Changed kick embed message, bot sends embed to kicked user {server} {kicked_by} {reason (if there was one)}\n- Kick command now accepts reasons\n- Updated Help command\n\n__**Changelog (29/12/2018) V0.13**__\n+ Added rename command\n+ Added coinflip command\n\n- Updated Help command\n\n__**Changelog (04/01/2019) V0.14**__\n- Changed music play embed again',
            colour = 0x9bf442,
            )
        e.set_author(name='Stig#1337 - The developer of Devolution', icon_url='https://cdn.discordapp.com/avatars/439327545557778433/a_09b7d5d0f8ecbd826fe3f7b15ee2fb93.gif')
        await user.send(embed=e)
        ee = discord.Embed(
            description = '__**Changelog (04/01/2019) V0.2 **__\n+ Added Colour command\n+ Added Meme command\n+ Added Space command\n\n- Updated Help command\n\n__**Changelog (14/01/2019) V0.21**__\n+ Added Prefix command\n+ Added Leave command\n\n- Reworked Invite command\n- Updated Help command\n\n__**Changelog (24/01/2019) V0.25**__\n+ Added spp command (Set punish permissions)\n+ Added punish & unpunish commands\n\n- Updated Help command\n\n__**Changelog (26/01/2019) V0.3 **__\n- Major code overhaul\n- File sizes cut in half, bot should now run smoother\n\n__**Changelog (26/01/2019) V0.35**__\n+ Added lspunish command\n+ Added Embed command\n\n- Updated Punish command to give usage details\n- Updated Help command\n\n__**Changelog (27/01/2019) V0.4 **__\n+ Added role commands\n+ Added Bug command\n\n- Updated Help command\n\n__**Changelog (02/03/2019) V0.5 **__\n+ Added changelog command (So you can see all this)\n+ Added new cog for tournaments\n+ Added Tournament commands\n\n- Updated bots default playing status\n- Updated Help command\n\n__**Changelog (09/03/2019) V0.51**__\n+ Added volume min and max 0 - 200\n\n - Fixed anyone being able to skip on the fist vote\n - Fixed Embed Messages not sending\n- Fixed Music failing to play\n\n__**Changelog (16/06/2019) V1.0 **__\n- Rewrote the entire bot into the newest version of Python and Discordpy\n- Updated Todo Command and made it public\n- Reworked Bug report command\n- Reworked help command\n\n__**Changelog (17/06/2019) V1.01 **__\n+ Added a command to list all roles in a server\n+ Added github issue link to bug command\n+ Reintroduced the beloved data folder!\n+ Added Boobs & Ass command\n+ Added Insult command\n+ Added roll command\n+ Added bot launcher\n+ Added Cleanup\n\n- Huge amounts of optimization with the cogs\n- Removed meme api as it was broken\n- Removed unnecessary json loading\n- Squashed a **lot** of nasty bugs\n- Removed Purge command\n- Removed prefix command\n- Removed tournament cog',
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        await user.send(embed=ee)
        eee = discord.Embed(
            description = '__**Changelog (17/06/2019) V1.02**__\nAdded music command!(Play, Pause, Resume, Volume, Stop)\n+ Added gif and gifr commands\n+ Added Hackban!\n+ Added pmid\n\n- Reworked the changelog command and put it in size order (iiCarelessness)\n- Reworked and updated Help command\n- Planted logos everywhere!\n\n__**Changelog (18/06/2019) V1.03**__\n+ Added a launcher gui with a few features\n+ Added Set Activity command\n+ Created a new admin cog\n+ Added amiadmin command\n+ Added utils folder\n+ Added config file\n\n- Merged tools into a new file named default inside util\n- Music now creates a folder for songs\n- Updated help command\n- Fixed some music bugs',
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        eee.set_footer(text='Devolution | Changelogs', icon_url="https://i.imgur.com/BS6YRcT.jpg")
        await user.send(embed=eee)

    @commands.command(pass_context=True, no_pm=True)
    async def todo(self, ctx, *args):
        user = ctx.author
        await user.send(embed=tools.Editable('Todo List', 'Remake Music, Finish cleanup command', 'Todo'))

    @commands.command(pass_context=True)
    async def invite(self, ctx):
        user = ctx.author
        await user.send('Heres the link to invite me to your guilds!\n\nhttps://discordapp.com/oauth2/authorize?client_id=449328225001406467&scope=bot&permissions=8')
        await ctx.message.delete()

    @commands.command(pass_context=True, no_pm=True)
    async def uptime(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        embed.add_field(name="Uptime", value=text)
        embed.set_author(name='Devolution', icon_url='https://i.imgur.com/BS6YRcT.jpg')
        embed.set_footer(icon_url='https://i.imgur.com/BS6YRcT.jpg', text='Devolution | Core')
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def about(self, ctx):
        embed=discord.Embed(
            title="About Devolution",
            description="A discord bot created for guild Administration, with plenty of commands for Admins, Moderators, games and more. For more information see below:",
            colour = 0x9bf442
            )
        embed.set_author(name="Stig", icon_url='https://cdn.discordapp.com/avatars/439327545557778433/a_09b7d5d0f8ecbd826fe3f7b15ee2fb93.gif?size=1024')
        embed.add_field(name="Discord Support", value="https://discord.gg/frcc5vF", inline=True)
        embed.add_field(name="Bot Creator", value="Stig#1337", inline=True)
        embed.add_field(name="Discord & API Version", value="Discord - 3.7.3 & API version 1.2.2", inline=True)
        embed.set_footer(text="Devolution | About - Providing Discord support since May 2018")
        await ctx.channel.send(embed=embed)

    @commands.command(pass_context=True, no_pm=True)
    async def bug(self, ctx):
        await ctx.message.delete()
        ques = await ctx.channel.send('What would you like to say?')
        msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout = 120)
        user = ctx.author
        userid = ctx.author.id
        guild = ctx.message.guild.name
        guildid = ctx.message.guild.id
        me = await self.bot.fetch_user('439327545557778433')
        embed = discord.Embed(
            title = "You've recieved a bug report from {}".format(user),
            colour = 0x9bf442,
            )
        embed.add_field(name="User ID", value=userid, inline=True)
        embed.add_field(name="Server Name", value=guild, inline=True)
        embed.add_field(name="Server ID", value=guildid, inline=True)
        embed.add_field(name="Message", value=msg.content, inline=True)
        await me.send(embed=embed)
        await ques.delete()
        await msg.delete()
        feedback = await ctx.channel.send('Your message has been sent! Thank you for your feedback.')
        await user.send("https://github.com/No1IrishStig/Devolution-Beta/issues")
        await asyncio.sleep(30)
        await feedback.delete()

    @commands.command(pass_context=True, no_pm=True)
    async def spp(self, ctx):
        for channel in ctx.message.guild.channels:
            role = discord.utils.get(channel.guild.roles, name='punished')
            overwrite = discord.PermissionOverwrite()
            overwrite.send_messages = False
            overwrite.send_tts_messages = False
            overwrite.add_reactions = False
            await channel.set_permissions(role, overwrite=overwrite),
        msg = await ctx.send(embed=tools.Editable('Setting Permissions', 'This may take a while, Ill tell you when im done.', 'Moderation'))
        await asyncio.sleep(5)
        await msg.delete()
        msg2 = await ctx.send(embed=tools.Editable('Im Finished!', 'Depending on how many channels you have, all permissions should be set.', 'Moderation'))
        await asyncio.sleep(5)
        await msg2.delete()

    @commands.command(pass_context=True, no_pm=True)
    async def music(self, ctx):
        user = ctx.author
        ctx.message.delete()
        await user.send(embed=tools.Editable('Music Usage', '**play** - Plays a song by name or url from youtube\n**pause** - Pauses the current song\n**resume** - Resumes the current song\n**volume {number}** - Change the volume of the bot\n**stop** - Disconnects the bot ', 'Todo'))

    @commands.command(pass_context=True, no_pm=True)
    async def github(self, ctx):
        user = ctx.author
        ctx.message.delete()
        await user.send(embed=tools.Editable('Github', 'https://github.com/No1IrishStig/Devolution-Beta/', 'Github'))


def setup(bot):
    bot.add_cog(Core(bot))
    print('Core - Initialized')
