import datetime
import discord
import asyncio
import aiohttp
import random
import json

from utils import default
from utils.default import lib
from discord.ext import commands
from random import choice as randchoice

class Fun(commands.Cog):
    def __init__(self, bot):
            self.bot = bot
            with open("./data/insults/insults.json") as f:
                self.insults = json.load(f)
                with open("./data/nsfw/settings.json") as f:
                    self.settings = json.load(f)
                    with open("./data/owo/owo.json") as f:
                        self.owo = json.load(f)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def ping(self, ctx):
        p = await ctx.send("Pong")
        await lib.erase(ctx, 20, p)

    @commands.command(no_pm=True, aliases=["cf"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def coinflip(self, ctx):
        await ctx.send("Flipping...")
        await asyncio.sleep(2)
        choices = ["Heads", "Tails"]
        rancoin = random.choice(choices)
        f = await ctx.send("You flipped a " + rancoin)
        await lib.erase(ctx, 20, f)

    @commands.command(aliases=["color"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def colour(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("http://www.colr.org/json/color/random") as r:
                res = await r.json(content_type=None)
                colour = res["new_color"]
                embedcolour = int(colour, 16)
                embed = discord.Embed(
                    title = "#" + colour,
                    colour = embedcolour
                    )
                c = await ctx.send(embed=embed)
                await lib.erase(ctx, 45, c)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def space(self, ctx):
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://api.open-notify.org/iss-now.json") as r:
                    res = await r.json()
                    async with cs.get("http://api.open-notify.org/astros.json") as r2:
                        res2 = await r2.json()
                        latitude = res["iss_position"]["latitude"]
                        longitude = res["iss_position"]["longitude"]
                        people = res2["number"]
                        name = ctx.author.name
                        avatar = ctx.author.avatar_url
                        embed = discord.Embed(
                            title = "International Space Station",
                            colour = 0x9bf442,
                            timestamp=datetime.datetime.utcnow()
                            )
                        embed.add_field(name="Longitude", value=f"{longitude}", inline=True)
                        embed.add_field(name="Latitude", value=f"{latitude}", inline=True)
                        embed.add_field(name="People in Space", value=f"{people}", inline=True)
                        embed.set_footer(text="Devolution | Space", icon_url="https://i.imgur.com/BS6YRcT.jpg")
                        e = await ctx.send(embed=embed)
                        await lib.erase(ctx, 45, e)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def roll(self, ctx, number : int = 100):
        author = ctx.author
        if number > 1:
            n = random.randint(1, number)
            r = await ctx.send(f"{author.mention} :game_die: {n} :game_die:")
            await lib.erase(ctx, 45, r)
        else:
            number = 69
            n = random.randint(1, number)
            rr = await ctx.send(f"{author.mention} :game_die: {n} :game_die:")
            await lib.erase(ctx, 45, rr)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def insult(self, ctx, user : discord.Member=None):
        author = ctx.author
        msg = " "
        if user != None:
            if user.id == self.bot.user.id:
                msg = " How original. No one else had thought of trying to get the bot to insult itself. I applaud your creativity. Yawn. Perhaps this is why you don't have friends. You don't add anything new to any conversation. You are more of a bot than me, predictable answers, and absolutely dull to have an actual conversation with."
                u = await ctx.send(author.mention + msg)
                await lib.erase(ctx, 45, u)
            else:
                i = await ctx.send(user.mention + msg + randchoice(self.insults))
                await lib.erase(ctx, 45, i)
        else:
                ii = await ctx.send(author.mention + msg + randchoice(self.insults))
                await lib.erase(ctx, 45, ii)

    @commands.command(no_pm=True, aliases=["tits"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def boobs(self, ctx):
        author = ctx.author
        rdm = random.randint(0, self.settings["ama_boobs"])
        search = (f"http://api.oboobs.ru/boobs/{rdm}")
        async with aiohttp.ClientSession() as cs:
            async with cs.get(search) as r:
                result = await r.json()
                boob = randchoice(result)
                boob = "http://media.oboobs.ru/{}".format(boob["preview"])
            await ctx.send(boob)

    @commands.command(no_pm=True, aliases=["booty"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def ass(self, ctx):
        author = ctx.author
        rdm = random.randint(0, self.settings["ama_ass"])
        search = (f"http://api.obutts.ru/butts/{rdm}")
        async with aiohttp.ClientSession() as cs:
            async with cs.get(search) as r:
                result = await r.json(content_type=None)
                ass = randchoice(result)
                ass = "http://media.obutts.ru/{}".format(ass["preview"])
            await ctx.send(ass)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def gif(self, ctx, *keywords):
        url = (f"http://api.giphy.com/v1/gifs/search?&api_key=dc6zaTOxFJmzC&q={keywords}")
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                result = await r.json()
                if r.status == 200:
                    if result["data"]:
                        g = await ctx.send(result["data"][0]["url"])
                        await lib.erase(ctx, 30, g)
                    else:
                        e = await ctx.send(embed=lib.Editable("Error!", "No search results found", "Giphy"))
                        await lib.erase(ctx, 20, e)
                else:
                    ee = await ctx.send(embed=lib.Editable("Error!", "There was an error contacting the API! Report this with !bug", "Giphy"))
                    await lib.erase(ctx, 20, ee)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def gifr(self, ctx, *keywords):
        url = (f"http://api.giphy.com/v1/gifs/random?&api_key=dc6zaTOxFJmzC&tag={keywords}")
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                result = await r.json()
                if r.status == 200:
                    if result["data"]:
                        g = await ctx.send(result["data"]["url"])
                        await lib.erase(ctx, 20, g)
                    else:
                        e = await ctx.send(embed=lib.Editable("Error!", "No search results found", "Giphy"))
                        await lib.erase(ctx, 20, e)
                else:
                    ee = await ctx.send(embed=lib.Editable("Error!", "There was an error contacting the API! Report this with !bug", "Giphy"))
                    await lib.erase(ctx, 20, ee)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def owo(self, ctx, user : discord.Member=None):
        o = await ctx.send(ctx.author.mention + " " + randchoice(self.owo))
        await lib.erase(ctx, 45, o)

def setup(bot):
    bot.add_cog(Fun(bot))
