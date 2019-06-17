import discord
from discord.ext import commands
import datetime
import time
import asyncio
import json
import aiohttp
from cogs.tools import tools

start_time = time.time()

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def changelog(self, ctx):
        user = ctx.message.author
        e = discord.Embed(
            description = '**Changelog (17/06/2019)**\nSquashed a **lot** of nasty bugs\n- Huge amounts of optimization with the cogs\n- Reintroduced the beloved data folder!\n- Added bot launcher\n- Added github issue link to bug command\n- Added roll command\n- Added Insult command\n- Added Boobs & Ass command\n- Added Cleanup\n- Removed Purge \n\n**Changelog (16/06/2019) V2.0**\n- Rewrote the entire bot into the newest version of Python and Discord.py\n- Reworked Bug report command\n- Reworked help command & Began work on a new help command\n- Updated Todo Command and made it public.\n- Added a command to list all roles in a server\n- Removed meme api as it was broken. ',
            colour = 0x9bf442,
            )
        e.set_author(name='Stig#1337 - The developer of Devolution', icon_url='https://cdn.discordapp.com/avatars/439327545557778433/a_09b7d5d0f8ecbd826fe3f7b15ee2fb93.gif')
        await user.send(embed=e)
        e = discord.Embed(
            description = '**Changelog (09/03/2019) V1.51**\n- Fixed Music:\n - Fixed Embed Messages not sending\n - Fixed Music failing to play\n - Fixed anyone being able to skip on the fist vote\n - Added volume min and max 0 - 200\n\n**Changelog (02/03/2019) V1.5**\n- Added new cog for tournaments\n- Added Tournament commands\n- Added changelog command (So you can see all this)\n- Changed bots default playing status\n- Updated Help command\n\n**Changelog (27/01/2019) V1.4**- Added role commands\n- Added Bug command\n- Updated Help command\n\n**Changelog (26/01/2019) V1.35**\n- Added Embed command\n- Changed Punish command to present a menu of options\n- Updated Help command\n- Added lspunish command\n\n**Changelog (26/01/2019) V1.3**\n- Major code overhaul. File sizes cut in half bot should now run faster.\n\n**Changelog (24/01/2019) V1.25**\n- Added Punish command\n- Added Unpunish command\n- Added spp command (Sets the punished permissions for every channel incase the automation failed.)\n- Updated Help command\n\n**Changelog (14/01/2019) V1.21**\n- Fixed Invite command\n- Added Prefix command\n- Added Leave command\n- Updated Help command\n\n**Changelog (04/01/2019) V1.2**\nToday I figured out how to implement WebAPis into the bot sooo\n- Added Colour command (generates random hex value and sets embed colour to it)\n- Added Space command (Sends info about the ISS)\n- Added Meme command\n- Updated Help command\n\n**Changelog (04/01/2019) V1.13**\n- Edited music Play embed again... (Added details)\n\n**Changelog (29/12/2018) V1.12**\n- Added rename command\n- Added coinflip command\n- Updated Help command\n\n**Changelog (23/12/2018) V1.1**\n- Changed kick embed message, bot sends embed to kick user {guild} {kicked_by} {reason (if there was one)}\n- Kick command now accepts reasons. If no reason is given, they just get kicked.\n- Added ban command. With the same parameters and embeds\n- Added Purge command\n- Added Say command\n- Added uinfo command, works with mentioned users\n- Added Avatar command. (Embedded)\n- Added About command\n- Added PM Command\n- Updated Help command\n\n',
            colour = 0x9bf442,
            )
        await user.send(embed=e)
        ee = discord.Embed(
            description = '**Changelog (22/12/2018) V1.05**\n- Added Set Presence command (Alias sp)\n- Added Cog commands Load, Unload and List.\n- Added Cog check, if you arent me, goodluck using that one.\n- Updated Help command\n\n**Changelog (21/12/2018 (3 hours later)) V1.04**\n- Changed all timestamps to make them actually work.\n- Changed set presence command text to be inside an embedded message\n- Added Uptime command\n- Added Kick command (Permission checks included)\n- Updated Help command (Added Music commands. Added Moderation (Purge, Say))\n\n**Changelog (21/12/2018) V1.03**\n- Music Cog Work - Edited many embed messages. Author will now be the command author for nearly all other music commands.\n- Added guild info\n- Updated Help command\n\n**Changelog (18/12/2018) V1.02**\n__Please keep in mind, these commands wont actually work yet, they are just placeholders.__\n- Music cleanup. (Put all messages into embedded messages)\n- Help command updated to add (sinfo, uinfo, uptime)\n\n**Changelog (16/12/2018) V1.01**\n- Added a few embed to music for testing. Author will now be command author for some commands.\n- Added shutdown command\n\n**Changelog (15/12/2018) V1.0**\n- Bot creation\n- Music Cog implementation\n- Added Help command\n- Added Ping command',
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        ee.set_footer(text='Devolution | Changelogs')
        await user.send(embed=ee)

    @commands.command(pass_context=True, no_pm=True)
    async def todo(ctx):
            user = ctx.message.author
            await user.send(embed=tools.Editable('Todo List', 'Remake Music, Finish cleanup command', 'Todo'))

    @commands.command(pass_context=True, no_pm=True)
    async def help(self, ctx):
        await ctx.message.delete()
        author = ctx.message.author
        embed = discord.Embed(
            title = "Help",
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        embed.set_author(name="Devolution", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        embed.set_footer(text="Devolution | Help", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        embed.add_field(name="Information", value="**Help** - Gives help!\n**Bug** - Use it to report bugs.\n**sinfo** - Displays guild information.\n**uinfo** - Displays user information\n**uptime** - Displays the bots uptime\n**about** - Displays stuff about the bot\n**changelog** - Displays the entire bots changelog", inline=False)
        embed.add_field(name="Fun", value="**coinflip** - Flip a coin\n**space** - Get live information about the ISS\n**colour** - Get a random colour\n**roll** - Roles a dice\n**insult** - Insult people you dislike!\n**boobs** - See some melons!\n**ass** - See some peaches!", inline=False)
        embed.add_field(name="Moderation", value="**kick** - Kick a mentioned user\n**ban** - Ban a mentioned user\n**punish** - Gives mute options\n**cleanup** - Gives message moderation options", inline=False)
        embed.add_field(name="Useful", value="**say** - Speak as the bot\n**rename** - Change a users nickname\n**invite** - Gives usage details\n**embed** - Creates an embed message\n**role** - Gives role options", inline=False)
        embed.add_field(name="Admin", value="**leave** - Makes the bot leave the guild", inline=False)
        embed.add_field(name="Owner", value="**setpresence(sp)** - Change the playing status of the bot.\n**shutdown** - Sends the bot into a deep sleep ...\n**cog** - Displays list of Cog Options\n**todo** - Displays List of shit todo\n\n\n **Music is currently not working as it needs recoded. Check the changelog!**", inline=False)
        await author.send(embed=embed)

    @commands.command(pass_context=True)
    async def invite(ctx):
        user = ctx.message.author
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
    async def pm(self, ctx, user : discord.User=None, *args):
        if ctx.message.author.id == int('439327545557778433'):
            if user is None:
                await ctx.channel.send(embed=tools.Editable('Error!', 'Tag a user to PM!', 'Error'))
            else:
                message = ''
                for word in args:
                    message += word
                    message += ' '
                if message is '':
                    await ctx.channel.send(embed=tools.Editable('Error!', 'Write a message for me to send!', 'Error'))
                else:
                    await user.send(message)
                    await ctx.message.delete()
        else:
            await ctx.channel.send(embed=tools.NoPerm())

    @commands.command(pass_context=True, no_pm=True)
    async def bug(self, ctx):
        await ctx.message.delete()
        ques = await ctx.channel.send('What would you like to say?')
        msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout = 120)
        user = ctx.message.author.name
        userid = ctx.message.author.id
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

def setup(bot):
    bot.add_cog(Core(bot))
    print('Core has been loaded')
