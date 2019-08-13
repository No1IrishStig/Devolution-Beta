import os, sys, traceback
import discord
import json

from utils.default import lib
from discord.ext import commands
from utils import default

dbcheck = os.path.exists(f"data/db/data.db.dat")
JSON_VALIDATION = ['settings/deltimer.json', 'settings/logs.json', "settings/leveling.json"]
ERRORS = ["deltimer", "logs", "leveling"]
config = default.get("utils/cfg.json")

bot = commands.Bot(command_prefix = config.prefix)
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'\nSuccessfully logged in as: {bot.user.name}\nVersion: {discord.__version__}\nBuild: {default.version}')
    await bot.change_presence(activity=discord.Game(name=config.playing, type=1, url='https://github.com/No1IrishStig/Devolution-Beta/'))

i = 0
for files in JSON_VALIDATION:
    check = os.path.exists(f"data/{files}")
    if check is False:
        ERRORS[i]
        if ERRORS[i] == "deltimer":
            lib.deltimer()
        elif ERRORS[i] == "logs":
            lib.logs()
        elif ERRORS[i] == "leveling":
            lib.levels()
    i += 1

if check is False:
    print("JSON Files Generated")

if dbcheck is False:
    print("Database Generated")


for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        try:
            bot.load_extension(f"cogs.{name}")
        except Exception as error:
            traceback.print_exc()

bot.load_extension("utils.errorhandler")
print("Boot Successful!")
bot.run(config.token, reconnect=True)
