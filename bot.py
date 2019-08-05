import os, sys, traceback
import discord
import json

from utils.default import lib
from discord.ext import commands
from utils import default

JSON_VALIDATION = ['admin/admins.json', 'admin/deltimer.json', 'customcommands/commands.json', 'economy/economy.json', 'economy/settings.json', 'logs/settings.json']
ERRORS = ["admins", "deltimer", "cc", "economy", "economysettings", "logsettings"]
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
        if ERRORS[i] == "admins":
            lib.admins()
        elif ERRORS[i] == "deltimer":
            lib.deltimer()
        elif ERRORS[i] == "cc":
            lib.cc()
        elif ERRORS[i] == "economy":
            lib.eco()
        elif ERRORS[i] == "economysettings":
            lib.ecoset()
        elif ERRORS[i] == "logsettings":
            lib.logset()
    i += 1
print("JSON Validation Complete")

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
