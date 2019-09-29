import os, sys, traceback
import datetime
import discord
import json

from utils.default import lib
from discord.ext import commands
from utils import default

config = default.get("utils/cfg.json")
settings = {"token": "Token", "owner": [0], "prefix": "!", "playing": "Stable v1.7.6"}

if config.token == "Token" or config.owner == 0:
    lib.cfg_file()

bot = commands.Bot(command_prefix = config.prefix)
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'\nSuccessfully logged in as: {bot.user.name}\nVersion: {discord.__version__}\nBuild: {default.version}')
    await bot.change_presence(activity=discord.Game(name=config.playing, type=1, url='https://github.com/No1IrishStig/Devolution-Beta/'))
    global bot_name
    global bot_avatar_url
    bot_name = bot.user.name
    bot_avatar_url = bot.user.avatar_url

lib.initilization()

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        try:
            bot.load_extension(f"cogs.{name}")
        except Exception as error:
            traceback.print_exc()

bot.load_extension("utils.errorhandler")
errorfile = open("./utils/error.log","a")
errorfile.write("[{}]: Boot\n".format(datetime.datetime.utcnow().strftime("%d/%m/%Y at %H:%M:%S (GMT)")))
errorfile.close()
print("Boot Successful!")
bot.run(config.token, reconnect=True)
