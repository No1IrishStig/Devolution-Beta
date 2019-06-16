import discord
import datetime
import json
import time
import aiohttp
import asyncio
import random
from discord.ext import commands
from cogs.tools import tools

class Fun(commands.Cog):
    def __init__(self, bot):
            self.bot = bot

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

def setup(bot):
    bot.add_cog(Fun(bot))
    print('Fun Cog has been loaded.')
