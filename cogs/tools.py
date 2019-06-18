import discord
import datetime
import time
from discord.ext import commands

class tools(commands.Cog):
    def __init__(self, client):
        self.client = client

    # await bot.say(embed=tools.NoPerm())
    # await self.bot.say(embed=tools.NoPerm())
    def NoPerm():
        embed = discord.Embed(
            title = 'Error!',
            description = 'You dont have permission to do that!',
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        embed.set_footer(text='Devolution | Error', icon_url="https://i.imgur.com/BS6YRcT.jpg")

        return embed
    # await bot.say(embed=tools.Editable('title', 'desc', 'footer'))
    # await self.bot.say(embed=tools.Editable('title', 'desc', 'footer'))
    def Editable(title, desc, footer):
        e = discord.Embed(
            title = title,
            description = desc,
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        e.set_footer(text='Devolution | {}'.format(footer), icon_url='https://i.imgur.com/BS6YRcT.jpg')
        e.set_author(name='Devolution', icon_url='https://i.imgur.com/BS6YRcT.jpg')
        return e

    def AvatarEdit(author, avatar, title, desc, footer):
        e = discord.Embed(
            title = title,
            description = desc,
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        e.set_footer(text='Devolution | {}'.format(footer))
        e.set_author(name=author, icon_url=avatar)
        return e

    def FromStig(title, desc, footer):
        e = discord.Embed(
            title = title,
            description = desc,
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        e.set_footer(text='Devolution | {}'.format(footer))
        e.set_author(name='Stig', icon_url='https://cdn.discordapp.com/avatars/439327545557778433/a_09b7d5d0f8ecbd826fe3f7b15ee2fb93.gif?size=1024')
        return e

def setup(client):
    client.add_cog(tools(client))
