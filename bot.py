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

print(discord.__version__ + '    <---------- If this isnt 1.2.2 your bot wont work!')
print()

bot = commands.Bot(command_prefix = "!")
bot.remove_command('help')

initial_extensions = ['cogs.core', 'cogs.main', 'cogs.music', 'cogs.moderation', 'cogs.fun']

@bot.event
async def on_ready():
    count = str(len(bot.guilds))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name='with ' + count + ' Guilds'))
    print('\nIm ready!')
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

@bot.command(pass_context=True, no_pm=True)
async def leave(ctx):
    guild = ctx.message.guild
    if ctx.message.author == guild.owner:
        await ctx.guild.leave()
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
    if ctx.message.author.id == int('439327545557778433'):
        await ctx.channel.send(embed=tools.Editable('Cog Commands', '**Load** - loads named cog.\n **Unload** - Unloads named cog.\n **List** - Lists all cogs.', 'Cogs'))
    else:
        await ctx.channel.send(embed=tools.NoPerm())

@cog.group(pass_context=True, invoke_without_command=True)
async def load(ctx, extension : str=None):
    if ctx.message.author.id == int('439327545557778433'):
        if extension is None:
            await ctx.channel.send(embed=tools.Editable('Error!', 'Enter a cog name to load!', 'Error'))
        else:
            try:
                bot.load_extension(extension)
                await ctx.channel.send(embed=tools.Editable('Success!', '{} has been loaded!'.format(extension), 'Cogs'))
            except Exception as error:
                await ctx.channel.send(embed=tools.Editable('Error!', '{} cannot be loaded!'.format(extension), 'Cogs'))
    else:
        await ctx.channel.send(embed=tools.NoPerm())

@cog.group(pass_context=True, invoke_without_command=True)
async def unload(ctx, extension : str=None):
    if ctx.message.author.id == int('439327545557778433'):
        if extension is None:
            await ctx.channel.send(embed=tools.Editable('Error!', 'Enter a cog name to load!', 'Error'))
        else:
            try:
                bot.unload_extension(extension)
                await ctx.channel.send(embed=tools.Editable('Success!', '{} has been unloaded!'.format(extension), 'Cogs'))
            except Exception as error:
                await ctx.channel.send(embed=tools.Editable('Error!', '{} cannot be unloaded!'.format(extension), 'Cogs'))
    else:
        await ctx.channel.send(embed=tools.NoPerm())

@cog.command(pass_context=True)
async def list(ctx):
    if ctx.message.author.id == int('439327545557778433'):
        await ctx.channel.send(embed=tools.Editable('Available Cogs', 'cogs.core','cogs.main', 'cogs.fun, cogs.mod', 'Cogs'))
    else:
        await ctx.channel.send(embed=tools.NoPerm())


bot.run(token)
