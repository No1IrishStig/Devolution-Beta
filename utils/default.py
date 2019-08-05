import datetime
import asyncio
import discord
import json

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

version = "Stable v1.63"
invite = "https://discord.gg/V9DhKbW"
config = default.get("./utils/cfg.json")

class lib(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("./utils/essentials/deltimer.json") as f:
            self.deltimer = json.load(f)

    def NoPerm():
        embed = discord.Embed(
            title = "Error!",
            description = "You dont have permission to do that!",
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        embed.set_footer(text="Devolution - Error", icon_url="https://i.imgur.com/BS6YRcT.jpg")

        return embed

    def Editable(title, desc, footer):
        e = discord.Embed(
            title = title,
            description = desc,
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        e.set_footer(text=f"Devolution - {footer}", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        e.set_author(name="Devolution", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        return e

    def EditableC(title, desc, colour, footer):
        e = discord.Embed(
            title = title,
            description = desc,
            colour = colour,
            timestamp=datetime.datetime.utcnow()
            )
        e.set_footer(text=f"Devolution - {footer}", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        e.set_author(name="Devolution", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        return e

    def AvatarEdit(author, avatar, title, desc, footer):
        e = discord.Embed(
            title = title,
            description = desc,
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        e.set_footer(text=f"Devolution - {footer}")
        e.set_author(name=author, icon_url=avatar)
        return e

    def FromStig(title, desc, footer):
        e = discord.Embed(
            title = title,
            description = desc,
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        e.set_footer(text=f"Devolution - {footer}")
        e.set_author(name="Stig", icon_url="https://cdn.discordapp.com/avatars/439327545557778433/a_09b7d5d0f8ecbd826fe3f7b15ee2fb93.gif?size=1024")
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

def setup(client):
    client.add_cog(Lib(client))
