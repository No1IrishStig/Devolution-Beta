# Embed with Command Author Name + Pic

    name = ctx.message.author.name
    avatar = ctx.message.author.avatar_url
    embed = discord.Embed(
        title = 'Volume',
        description = '',
        colour = 0x9bf442,
        timestamp=datetime.datetime.utcnow()
        )
    embed.set_footer(text='Devolution | ')
    embed.set_author(name=ctx.'{}', icon_url='{}'.format(name, avatar))
    await self.bot.say(embed=embed)

    embed.set_author(name='{}', icon_url='{}'.format(name, avatar))

# Use role colour as embed colour

@bot.command(pass_context=True)
async def test(ctx):
    colour = ctx.message.author.top_role.colour
    embed = discord.Embed(
        title = 'Server Information',
        description = 'Test',
        colour = colour,
        timestamp=datetime.datetime.utcnow()
        )
    await bot.say(embed=embed)

# List all servers bot in

@bot.command()
async def listservers():
    print('Servers connected to:')
    for server in bot.servers:
    name = server.name
    print(name.encode("utf-8"))

# Permissions Test

@bot.command(pass_context=True)
async def test(ctx):
    if ctx.message.author.server_permissions.administrator:
        await bot.say('You have admin')
    else:
        await bot.say('You dont have admin')

# Simple Owner Check

@bot.command(pass_context=True)
async def test(ctx):
    if ctx.message.author.id == '439327545557778433':
        await bot.say('')
    else:
        await bot.say('')

# No Permission

await bot.say(embed=tools.ErrorEmbed())

# New Cog

import discord
from discord.ext import commands

class Fun:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async


def setup(bot):
    bot.add_cog(Fun(bot))
    print('Fun Cog has been loaded.')

# Better Embed with All

@bot.command(pass_context=True)
async def test(ctx):
    embed = discord.Embed(
        title = "Test",
        colour = 0x9ee4e0,
        description="Test",
        )
    embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_author(name="Devolution", icon_url="https://i.imgur.com/BS6YRcT.jpg")
    embed.set_footer(text="Devolution | Beta", icon_url="https://i.imgur.com/BS6YRcT.jpg")
    embed.add_field(name="🤔", value="some of these properties have certain limits...")
    embed.add_field(name="😱", value="try exceeding some of them!")
    embed.add_field(name="🙄", value="an informative error should show up, and this view will remain as-is until all issues are fixed")
    embed.add_field(name="<:thonkang:219069250692841473>", value="these last two", inline=True)
    embed.add_field(name="<:thonkang:219069250692841473>", value="are inline fields", inline=True)
    await bot.say(embed=embed)

# API Call
@commands.command()
async def meme(self):
    async with aiohttp.botSession() as cs:
        async with cs.get('http://api.open-notify.org/iss-now.json') as r:
            res = await r.json()
            res['longitude']

# Working json

@bot.command(pass_context=True)
async def test(ctx):
    toggle = json.load(open('./data/test/test.json'))
    if ctx.message.author.id not in toggle:
        toggle[ctx.message.author.id] = str(ctx.message.author.name)
        toggle[ctx.message.server.id] = False
    else:
        toggle[ctx.message.server.id] = not toggle[ctx.message.server.id]

    with open('./data/test/test.json', 'w') as f:
        json.dump(toggle, f)

    await bot.say(toggle)

@bot.command(pass_context=True)
async def tester(ctx):
    with open('./data/test/test.json', "r") as f1:
        if toggle[ctx.message.author.id] == False:
            await bot.say('Toggle is false, failed')
        else:
            await bot.say('Success toggle is true!')
