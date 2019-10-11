import datetime
import asyncio
import discord
import shelve
import json
import os

from utils import default
from discord.ext import commands
from collections import namedtuple

def get(file):
    try:
        with open(file, encoding="utf8") as data:
            return json.load(data, object_hook=lambda d: namedtuple("X", d.keys())(*d.values()))
    except AttributeError:
        raise AttributeError("Unknown argument")
    except FileNotFoundError:
        raise FileNotFoundError("JSON file wasn't found")

version = "Stable v1.9.2"
invite = "https://discord.gg/V9DhKbW"
config = default.get("./utils/cfg.json")
economydb = shelve.open("./data/db/economy/data.db", writeback=True)
levelsdb = shelve.open("./data/db/levels/data.db", writeback=True)
warningsdb = shelve.open("./data/db/warnings/data.db", writeback=True)
JSON_VALIDATION = ['settings/deltimer.json', 'settings/logs.json', "settings/leveling.json"]
ERRORS = ["deltimer", "logs", "leveling"]
dbcheck = os.path.exists(f"data/db/db.log")

class lib(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("./data/settings/deltimer.json") as f:
            self.deltimer = json.load(f)

    def NoPerm(self):
        embed = discord.Embed(
            title = "Error!",
            description = "You dont have permission to do that!",
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        embed.set_footer(text=f"{self.bot.user.name} - Error", icon_url=self.bot.user.avatar_url)

        return embed

    def Editable(self, title, desc, footer):
        e = discord.Embed(
            title = title,
            description = desc,
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        e.set_footer(text=f"{self.bot.user.name} - {footer}", icon_url=self.bot.user.avatar_url)
        e.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        return e

    def EditableC(self, title, desc, colour, footer):
        e = discord.Embed(
            title = title,
            description = desc,
            colour = colour,
            timestamp=datetime.datetime.utcnow()
            )
        e.set_footer(text=f"{self.bot.user.name} - {footer}", icon_url=self.bot.user.avatar_url)
        e.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        return e

    def AvatarEdit(self, author, avatar, title, desc, footer):
        e = discord.Embed(
            title = title,
            description = desc,
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        e.set_footer(text=f"{self.bot.user.name} - {footer}")
        e.set_author(name=author, icon_url=avatar)
        return e

    async def erase(ctx, duration, name):
        erase = (
            await asyncio.sleep(duration),
            await ctx.message.delete(),
            await name.delete()
            )
        return erase

    async def eraset(self, ctx, name):
        db = self.deltimer
        guild = ctx.guild
        gid = str(guild.id)
        if not gid in db:
            timer = 20
            eraset = (
                await asyncio.sleep(timer),
                await ctx.message.delete(),
                await name.delete()
                )
            return eraset
        else:
            timer = db[gid]["timer"]
            eraset = (
                await asyncio.sleep(timer),
                await ctx.message.delete(),
                await name.delete()
                )
            return eraset

    async def sp(self, ctx, game):
        sp = (
        await self.bot.change_presence(activity=discord.Game(name=game)),
        )
        return sp

    async def sa(self, ctx, type, game):
        sa = (
        await self.bot.change_presence(activity=discord.Activity(type=type, name=game)),
        )
        return sa


    def deltimer():
        deltimer = open("data/settings/deltimer.json","w+")
        deltimer.write("{}")
        deltimer.close

    def logs():
        logset = open("data/settings/logs.json","w+")
        logset.write("{}")
        logset.close

    def levels():
        levels = open("data/settings/leveling.json","w+")
        levels.write("{}")
        levels.close

    def db_create():
        economydb["Economy"] = {}
        economydb.sync()
        levelsdb["Levels"] = {}
        levelsdb.sync()
        warningsdb["Warnings"] = {}
        warningsdb.sync()
        f = open("./data/db/db.log","w+")
        f.write("Creating Economy Database...\nEconomy_DB Created Successfully\nCreating Levels Database...\nLevels_DB Created Successfully\nCreating Warnings Database...\nWarnings_DB Created Successfully")
        f.close()

    def cfg_file():
        with open("./utils/cfg.json") as f:
            settings = json.load(f)
            print("Uh oh, it looks like you are missing the bot's token or OwnerID from your CFG File.\n")
            input("Press enter to continue.")
            os.system("cls")
            token = input("Enter your bot token.\n\n")
            os.system("cls")
            UID = input("Enter your UserID.\n\n")
            os.system("cls")
            settings["token"] = token
            settings["owner"] = UID
            with open("./utils/cfg.json", "w") as f:
                json.dump(settings, f)
            os.system("cls")
            os.system("py -3 ./self.bot.py")

    def initilization():
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
            print("Database's Generated")
            lib.db_create()

def setup(client):
    client.add_cog(Lib(client))
