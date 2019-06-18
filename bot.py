from discord.ext import commands
from utils.default import lib
from utils import default
import sys, traceback
import datetime
import discord
import asyncio
import json

config = default.get("utils/cfg.json")

bot = commands.Bot(command_prefix = config.prefix)
bot.remove_command('help')

initial_extensions = ['cogs.core', 'cogs.main', 'cogs.music', 'cogs.fun', 'cogs.moderation', 'cogs.admin']

@bot.event
async def on_ready():
    count = str(len(bot.guilds))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=config.playing))
    print('\nIm ready!')
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            traceback.print_exc()

@bot.command(no_pm=True)
async def leave(ctx):
    guild = ctx.message.guild
    if ctx.author == guild.owner:
        await ctx.guild.leave()
    else:
        await ctx.channel.send(embed=lib.NoPerm())

@bot.command(aliases=['sp'])
async def setpresence(ctx, *args):
    if ctx.author.id in config.owner:
        count = str(len(bot.guilds))
        output = ''
        for gamename in args:
            output += gamename
            output += ' '
        if output == '':
            await ctx.channel.send(embed=lib.Editable('Game Presence', 'The bots game has been reset to the default', 'Owner'))
            await bot.change_presence(status=discord.Status.online, activity=discord.Game(name='with ' + count + ' Guilds'))
            await ctx.message.delete()
        else:
            print(output)
            await ctx.channel.send(embed=lib.Editable('Game Presence', 'The bots game has been changed to ' + output, 'Owner'))
            await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=output))
            await ctx.message.delete()
    else:
        await ctx.channel.send(embed=lib.NoPerm())

@bot.command(aliases=['sa'])
async def setactivity(ctx, activity:str=None, *args):
    if ctx.author.id in config.owner:
        output = ''
        for gamename in args:
            output += gamename
            output += ' '
        if output == '':
            await ctx.channel.send(embed=lib.Editable('Error', 'Please enter one of these activities with the name you would like after it!\n\n**playing {name}**, **listening {name}**, **watching {name}**', 'Error'))
        else:
            await ctx.message.delete()
            if activity == 'playing':
                await bot.change_presence(activity=discord.Game(name=output))
                await ctx.channel.send(embed=lib.Editable('Activity Presence', 'The bots game has been changed to playing  ' + output, 'Owner'))
            if activity == 'listening':
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=output))
                await ctx.channel.send(embed=lib.Editable('Activity Presence', 'The bots game has been changed to listening ' + output, 'Owner'))
            if activity == 'watching':
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=output))
                await ctx.channel.send(embed=lib.Editable('Activity Presence', 'The bots game has been changed to watching ' + output, 'Owner'))
            else:
                await ctx.channel.send(embed=lib.Editable('Error', 'Please enter one of these activities!\n**playing {name}**, **listening {name}**, **watching {name}**', 'Error'))
    else:
        await ctx.channel.send(embed=lib.NoPerm())

@bot.command()
async def shutdown(ctx):
        if ctx.author.id in config.owner:
            await ctx.channel.send(embed=lib.Editable('Shutting Down!', 'I am shutting down in 5 seconds. Goodnight :zzz:', 'Sleep'))
            await asyncio.sleep(5)
            await bot.logout()
        else:
            await ctx.channel.send(embed=lib.NoPerm())

@bot.group(invoke_without_command=True)
async def cog(ctx):
    if ctx.author.id in config.owner:
        await ctx.channel.send(embed=lib.Editable('Cog Commands', '**Load** - loads named cog.\n **Unload** - Unloads named cog.\n **List** - Lists all cogs.', 'Cogs'))
    else:
        await ctx.channel.send(embed=lib.NoPerm())

@cog.group(invoke_without_command=True)
async def load(ctx, extension : str=None):
    if ctx.author.id in config.owner:
        if extension is None:
            await ctx.channel.send(embed=lib.Editable('Error!', 'Enter a cog name to load!', 'Error'))
        else:
            try:
                bot.load_extension(extension)
                await ctx.channel.send(embed=lib.Editable('Success!', '{} has been loaded!'.format(extension), 'Cogs'))
            except Exception as error:
                await ctx.channel.send(embed=lib.Editable('Error!', '{} cannot be loaded!'.format(extension), 'Cogs'))
    else:
        await ctx.channel.send(embed=lib.NoPerm())

@cog.group(invoke_without_command=True)
async def unload(ctx, extension : str=None):
    if ctx.author.id in config.owner:
        if extension is None:
            await ctx.channel.send(embed=lib.Editable('Error!', 'Enter a cog name to load!', 'Error'))
        else:
            try:
                bot.unload_extension(extension)
                await ctx.channel.send(embed=lib.Editable('Success!', '{} has been unloaded!'.format(extension), 'Cogs'))
            except Exception as error:
                await ctx.channel.send(embed=lib.Editable('Error!', '{} cannot be unloaded!'.format(extension), 'Cogs'))
    else:
        await ctx.channel.send(embed=lib.NoPerm())

@cog.command()
async def list(ctx):
    if ctx.author.id in config.owner:
        await ctx.channel.send(embed=lib.Editable('Available Cogs', 'cogs.core','cogs.main', 'cogs.fun, cogs.mod', 'Cogs'))
    else:
        await ctx.channel.send(embed=lib.NoPerm())

bot.run(config.token)
