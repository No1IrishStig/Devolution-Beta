from discord.ext import commands
from utils.default import lib
from utils import default
import datetime
import discord
import asyncio
import random
import json

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("./utils/cfg.json")

    @commands.command()
    async def amiadmin(self, ctx):
        """ Are you admin? """
        if ctx.author.id in self.config.owner:
            return await ctx.send(f"Yes **{ctx.author.name}** you're an admin!")
        else:
            await ctx.send(f"You arent an admin, {ctx.author.name}")

    @commands.command(pass_context=True, no_pm=True)
    async def pm(self, ctx, user : discord.User=None, *args):
        if ctx.author.id in self.config.owner:
            if user is None:
                await ctx.channel.send(embed=lib.Editable('Error!', 'Tag a user to PM!', 'Error'))
            else:
                message = ''
                for word in args:
                    message += word
                    message += ' '
                if message is '':
                    await ctx.channel.send(embed=lib.Editable('Error!', 'Write a message for me to send!', 'Error'))
                else:
                    await user.send(message)
                    await ctx.message.delete()
        else:
            await ctx.channel.send(embed=lib.NoPerm())

    @commands.command(pass_context=True, no_pm=True)
    async def pmid(self, ctx, id=None, *args):
        if ctx.author.id in self.config.owner:
            if id is None:
                await ctx.channel.send(embed=lib.Editable('Error!', 'Tag enter an ID to PM!', 'Error'))
            else:
                member = ctx.author
                userid = ctx.author.id
                avatar = ctx.author.avatar_url
                message = ''
                for word in args:
                    message += word
                    message += ' '
                if message is '':
                    await ctx.channel.send(embed=lib.Editable('Error!', 'Write a message for me to send!', 'Error'))
                else:
                    try:
                        user = await self.bot.fetch_user(id)
                        embed = discord.Embed(
                            title = "You've recieved a message from {}".format(member),
                            colour = 0x9bf442,
                            )
                        embed.set_author(name='Message from {}'.format(member), icon_url='{}'.format(avatar))
                        embed.add_field(name="Message", value=message, inline=True)
                        embed.set_footer(text='UserID: {}'.format(userid))
                        await user.send(embed=embed)
                    except Exception as error:
                            await ctx.send('I couldnt send your message to {} because of the error: [{}]'.format(member, error))
                    await ctx.message.delete()
        else:
            await ctx.channel.send(embed=lib.NoPerm())

def setup(bot):
    bot.add_cog(Admin(bot))
    print('Admin - Initialized')
