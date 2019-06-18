from collections import namedtuple
from discord.ext import commands
import discord
import json

def get(file):
    try:
        with open(file, encoding='utf8') as data:
            return json.load(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    except AttributeError:
        raise AttributeError("Unknown argument")
    except FileNotFoundError:
        raise FileNotFoundError("JSON file wasn't found")

class lib(commands.Cog):
    def __init__(self, client):
        self.client = client

    def NoPerm():
        embed = discord.Embed(
            title = 'Error!',
            description = 'You dont have permission to do that!',
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        embed.set_footer(text='Devolution | Error', icon_url="https://i.imgur.com/BS6YRcT.jpg")

        return embed

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
    client.add_cog(Lib(client))
