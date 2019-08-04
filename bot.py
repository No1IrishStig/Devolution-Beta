import os, sys, traceback
import discord
import json

from utils.default import lib
from discord.ext import commands
from utils import default

config = default.get("utils/cfg.json")

bot = commands.Bot(command_prefix = config.prefix)
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'\nSuccessfully logged in as: {bot.user.name}\nVersion: {discord.__version__}\nBuild: {default.version}')
    await bot.change_presence(activity=discord.Game(name=config.playing, type=1, url='https://github.com/No1IrishStig/Devolution-Beta/'))

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        try:
            bot.load_extension(f"cogs.{name}")
        except Exception as error:
            traceback.print_exc()

bot.load_extension("utils.errorhandler")
print('Boot Successful!')
bot.run(config.token, reconnect=True)
