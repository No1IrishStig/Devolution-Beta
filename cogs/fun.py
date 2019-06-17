import discord
import datetime
import json
import asyncio
import random
import aiohttp
from random import choice as randchoice
from discord.ext import commands
from cogs.tools import tools

class Fun(commands.Cog):
    def __init__(self, bot):
            self.bot = bot
            with open("./data/insults/insults.json") as f:
                self.insults = json.load(f)
                with open("./data/nsfw/settings.json") as f:
                    self.settings = json.load(f)

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        await ctx.send('Pong')

    @commands.command(pass_context=True, no_pm=True, aliases=['cf'])
    async def coinflip(self, ctx):
        await ctx.send('Flipping...')
        await asyncio.sleep(5)
        choices = ['Heads', 'Tails']
        rancoin = random.choice(choices)
        await ctx.send('You flipped a ' + rancoin)

    @commands.command(pass_context=True, aliases=['color'])
    async def colour(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('http://www.colr.org/json/color/random') as r:
                res = await r.json(content_type=None)
                colour = res['new_color']
                embedcolour = int(colour, 16)
                print(embedcolour)
                embed = discord.Embed(
                    title = '#' + colour,
                    colour = embedcolour
                    )
                await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['iss'])
    async def space(self, ctx):
            async with aiohttp.ClientSession() as cs:
                async with cs.get('http://api.open-notify.org/iss-now.json') as r:
                    res = await r.json()
                    async with cs.get('http://api.open-notify.org/astros.json') as r2:
                        res2 = await r2.json()
                        latitude = res['iss_position']['latitude']
                        longitude = res['iss_position']['longitude']
                        people = res2['number']
                        name = ctx.message.author.name
                        avatar = ctx.message.author.avatar_url
                        embed = discord.Embed(
                            title = 'International Space Station',
                            colour = 0x9bf442,
                            timestamp=datetime.datetime.utcnow()
                            )
                        embed.add_field(name="Longitude", value="{}".format(longitude), inline=True)
                        embed.add_field(name="Latitude", value="{}".format(latitude), inline=True)
                        embed.add_field(name="People in Space", value="{}".format(people), inline=True)
                        embed.set_footer(text="Devolution | Space", icon_url="https://i.imgur.com/BS6YRcT.jpg")
                        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def roll(self, ctx, number : int = 100):
        author = ctx.message.author
        if number > 1:
            n = random.randint(1, number)
            await ctx.send("{} :game_die: {} :game_die:".format(author.mention, n))
        else:
            await ctx.send("{} Enter a number above 1!".format(author.mention))

    @commands.command(pass_context=True)
    async def insult(self, ctx, user : discord.Member=None):
        msg = ' '
        if user != None:
            if user.id == self.bot.user.id:
                user = ctx.message.author
                msg = "How original. No one else had thought of trying to get the bot to insult itself. I applaud your creativity. Yawn. Perhaps this is why you don't have friends. You don't add anything new to any conversation. You are more of a bot than me, predictable answers, and absolutely dull to have an actual conversation with."
                await ctx.send(user.mention + msg)
            else:
                await ctx.send(user.mention + msg + randchoice(self.insults))
        else:
                await ctx.send(ctx.message.author.mention + msg + randchoice(self.insults))

    @commands.command(pass_context=True)
    async def boobs(self, ctx):
        author = ctx.message.author
        rdm = random.randint(0, self.settings["ama_boobs"])
        search = ("http://api.oboobs.ru/boobs/{}".format(rdm))
        async with aiohttp.ClientSession() as cs:
            async with cs.get(search) as r:
                result = await r.json()
                boob = randchoice(result)
                boob = "http://media.oboobs.ru/{}".format(boob["preview"])
            await ctx.send("{}".format(boob))

    @commands.command(pass_context=True)
    async def ass(self, ctx):
        author = ctx.message.author
        rdm = random.randint(0, self.settings["ama_ass"])
        search = ("http://api.obutts.ru/butts/{}".format(rdm))
        async with aiohttp.ClientSession() as cs:
            async with cs.get(search) as r:
                result = await r.json(content_type=None)
                ass = randchoice(result)
                ass = "http://media.obutts.ru/{}".format(ass["preview"])
            await ctx.send("{}".format(ass))



def setup(bot):
    bot.add_cog(Fun(bot))
    print('Fun has been loaded.')
