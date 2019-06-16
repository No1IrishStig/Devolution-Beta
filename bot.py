import discord
from discord.ext import commands
from itertools import cycle
import datetime
import asyncio
import json
import aiohttp
from cogs.tools import tools
import random

token = 'TOKEN HERE'

print(discord.__version__ + '<---------- If this isnt 1.2.2 your bot wont work!')
bot = commands.Bot(command_prefix = "!")
bot.remove_command('help')

initial_extensions = ['cogs.core', 'cogs.moderation', 'cogs.fun']

@bot.event
async def on_ready():
    count = str(len(bot.guilds))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name='with ' + count + ' Guilds'))
    print('Bot is ready.')
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))

@bot.event
async def on_guild_join():
    count = str(len(bot.guilds))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name='with ' + count + ' Guilds'))

@bot.command(pass_context=True)
async def invite(ctx):
    user = ctx.message.author
    await user.send('Heres the link to invite me to your guilds!\n\nhttps://discordapp.com/oauth2/authorize?client_id=449328225001406467&scope=bot&permissions=8')
    await ctx.message.delete()

@bot.command(pass_context=True, no_pm=True)
async def leave(ctx):
    guild = ctx.message.guild
    if ctx.message.author == guild.owner:
        await bot.leave_guild(guild)
    else:
        await ctx.channel.send(embed=tools.NoPerm())

@bot.command(pass_context=True, aliases=['sp'])
async def setpresence(ctx, *args):
    if ctx.author.id == int('439327545557778433'):
        count = str(len(bot.guilds))
        output = ''
        for gamename in args:
            output += gamename
            output += ' '
        if output == '':
            await ctx.channel.send(embed=tools.Editable('Game Presence', 'The bots game has been reset to the default', 'Owner'))
            await bot.change_presence(status=discord.Status.online, activity=discord.Game(name='with ' + count + ' Guilds'))
            await ctx.message.delete()
        else:
            await ctx.channel.send(embed=tools.Editable('Game Presence', 'The bots game has been changed to ' + output, 'Owner'))
            await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=output))
            await ctx.message.delete()
    else:
        await ctx.channel.send(embed=tools.NoPerm())

@bot.command(pass_context=True)
async def shutdown(ctx):
        if ctx.message.author.id == int('439327545557778433'):
            await ctx.channel.send(embed=tools.Editable('Shutting Down!', 'I am shutting down in 5 seconds. Goodnight :zzz:', 'Sleep'))
            await asyncio.sleep(5)
            await bot.logout()
        else:
            await ctx.channel.send(embed=tools.NoPerm())

@bot.group(pass_context=True, invoke_without_command=True)
async def cog(ctx):
    if not ctx.message.author.id == int('439327545557778433'):
        await ctx.channel.send(embed=tools.NoPerm())
    else:
        await ctx.channel.send(embed=tools.Editable('Cog Commands', '**Load** - loads named cog.\n **Unload** - Unloads named cog.\n **List** - Lists all cogs.', 'Cogs'))

@cog.group(pass_context=True, invoke_without_command=True)
async def load(ctx, extension : str=None):
    if not ctx.message.author.id == int('439327545557778433'):
        await ctx.channel.send(embed=tools.NoPerm())
    else:
        if extension is None:
            await ctx.channel.send(embed=tools.Editable('Error!', 'Enter a cog name to load!', 'Error'))
        else:
            try:
                bot.load_extension(extension)
                await ctx.channel.send(embed=tools.Editable('Success!', '{} has been loaded!'.format(extension), 'Cogs'))
            except Exception as error:
                await ctx.channel.send(embed=tools.Editable('Error!', '{} cannot be loaded!'.format(extension), 'Cogs'))

@cog.group(pass_context=True, invoke_without_command=True)
async def unload(ctx, extension : str=None):
    if not ctx.message.author.id == int('439327545557778433'):
        await ctx.channel.send(embed=tools.NoPerm())
    else:
        if extension is None:
            await ctx.channel.send(embed=tools.Editable('Error!', 'Enter a cog name to load!', 'Error'))
        else:
            try:
                bot.unload_extension(extension)
                await ctx.channel.send(embed=tools.Editable('Success!', '{} has been unloaded!'.format(extension), 'Cogs'))
            except Exception as error:
                await ctx.channel.send(embed=tools.Editable('Error!', '{} cannot be unloaded!'.format(extension), 'Cogs'))

@cog.command(pass_context=True)
async def list(ctx):
    if not ctx.message.author.id == int('439327545557778433'):
        await ctx.channel.send(embed=tools.NoPerm())
    else:
        await ctx.channel.send(embed=tools.Editable('Available Cogs', 'cogs.core','cogs.fun, cogs.mod', 'Cogs'))

@bot.command(pass_context=True)
async def about(ctx):
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

@bot.command(pass_context=True, no_pm=True)
async def pm(ctx, user : discord.User=None, *args):
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

@bot.command(pass_context=True)
async def changelog(ctx):
    user = ctx.message.author
    e = discord.Embed(
        description = '**Changelog (16/06/2019) V2.0**\n- Rewrote the entire bot into the newest version of Python and Discord.py\n- Reworked Bug report command\n- Reworked help command & Began work on a new help command\n- Updated Todo Command and made it public.\n- Added a command to list all roles in a server\n-Removed meme api as it was broken. ',
        colour = 0x9bf442,
        )
    e.set_author(name='Stig#1337 - The developer of Devolution', icon_url='https://cdn.discordapp.com/avatars/439327545557778433/a_09b7d5d0f8ecbd826fe3f7b15ee2fb93.gif')
    await user.send(embed=e)
    e = discord.Embed(
        description = '**Changelog (09/03/2019) V1.51**\n- Fixed Music:\n - Fixed Embed Messages not sending\n - Fixed Music failing to play\n - Fixed anyone being able to skip on the fist vote\n - Added volume min and max 0 - 200\n\n**Changelog (02/03/2019) V1.5**\n- Added new cog for tournaments\n- Added Tournament commands\n- Added changelog command (So you can see all this)\n- Changed bots default playing status\n- Updated Help command\n\n**Changelog (27/01/2019) V1.4**- Added role commands\n- Added Bug command\n- Updated Help command\n\n**Changelog (26/01/2019) V1.35**\n- Added Embed command\n- Changed Punish command to present a menu of options\n- Updated Help command\n- Added lspunish command\n\n**Changelog (26/01/2019) V1.3**\n- Major code overhaul. File sizes cut in half bot should now run faster.\n\n**Changelog (24/01/2019) V1.25**\n- Added Punish command\n- Added Unpunish command\n- Added spp command (Sets the punished permissions for every channel incase the automation failed.)\n- Updated Help command\n\n**Changelog (14/01/2019) V1.21**\n- Fixed Invite command\n- Added Prefix command\n- Added Leave command\n- Updated Help command\n\n**Changelog (04/01/2019) V1.2**\nToday I figured out how to implement WebAPis into the bot sooo\n- Added Colour command (generates random hex value and sets embed colour to it)\n- Added Space command (Sends info about the ISS)\n- Added Meme command\n- Updated Help command\n\n**Changelog (04/01/2019) V1.13**\n- Edited music Play embed again... (Added details)\n\n**Changelog (29/12/2018) V1.12**\n- Added rename command\n- Added coinflip command\n- Updated Help command\n\n**Changelog (23/12/2018) V1.1**\n- Changed kick embed message, bot sends embed to kick user {guild} {kicked_by} {reason (if there was one)}\n- Kick command now accepts reasons. If no reason is given, they just get kicked.\n- Added ban command. With the same parameters and embeds\n- Added Purge command\n- Added Say command\n- Added uinfo command, works with mentioned users\n- Added Avatar command. (Embedded)\n- Added About command\n- Added PM Command\n- Updated Help command\n\n',
        colour = 0x9bf442,
        )
    e.set_author(name='Stig#1337 - The developer of Devolution', icon_url='https://cdn.discordapp.com/avatars/439327545557778433/a_09b7d5d0f8ecbd826fe3f7b15ee2fb93.gif')
    await user.send(embed=e)
    ee = discord.Embed(
        description = '**Changelog (22/12/2018) V1.05**\n- Added Set Presence command (Alias sp)\n- Added Cog commands Load, Unload and List.\n- Added Cog check, if you arent me, goodluck using that one.\n- Updated Help command\n\n**Changelog (21/12/2018 (3 hours later)) V1.04**\n- Changed all timestamps to make them actually work.\n- Changed set presence command text to be inside an embedded message\n- Added Uptime command\n- Added Kick command (Permission checks included)\n- Updated Help command (Added Music commands. Added Moderation (Purge, Say))\n\n**Changelog (21/12/2018) V1.03**\n- Music Cog Work - Edited many embed messages. Author will now be the command author for nearly all other music commands.\n- Added guild info\n- Updated Help command\n\n**Changelog (18/12/2018) V1.02**\n__Please keep in mind, these commands wont actually work yet, they are just placeholders.__\n- Music cleanup. (Put all messages into embedded messages)\n- Help command updated to add (sinfo, uinfo, uptime)\n\n**Changelog (16/12/2018) V1.01**\n- Added a few embed to music for testing. Author will now be command author for some commands.\n- Added shutdown command\n\n**Changelog (15/12/2018) V1.0**\n- Bot creation\n- Music Cog implementation\n- Added Help command\n- Added Ping command',
        colour = 0x9bf442,
        timestamp=datetime.datetime.utcnow()
        )
    ee.set_footer(text='Devolution | Changelogs')
    await user.send(embed=ee)

@bot.command(pass_context=True, no_pm=True)
async def todo(ctx):
        user = ctx.message.author
        await user.send(embed=tools.Editable('Todo List', 'Remake Music, Finish new Help command', 'Todo'))

@bot.command(pass_context=True, no_pm=True)
async def bug(ctx):
    await ctx.message.delete()
    ques = await ctx.channel.send('What would you like to say?')
    msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout = 120)
    user = ctx.message.author.name
    userid = ctx.message.author.id
    guild = ctx.message.guild.name
    guildid = ctx.message.guild.id
    me = await bot.fetch_user('439327545557778433')
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
    await asyncio.sleep(30)
    await feedback.delete()
bot.run(token)
