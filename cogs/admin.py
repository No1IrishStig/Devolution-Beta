import sys, traceback
import discord
import asyncio

from utils.default import lib
from discord.ext import commands
from utils import default

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("./utils/cfg.json")

    @commands.group(invoke_without_command=True, no_pm=True)
    async def cog(self, ctx):
        if ctx.author.id in self.config.owner:
            usage = await ctx.send(embed=lib.Editable("Cog Commands", "**Load** - loads named cog.\n **Unload** - Unloads named cog.\n **List** - Lists all cogs.", "Cogs"))
            await lib.erase(ctx, 20, usage)
        else:
            noperm = await ctx.send(embed=lib.NoPerm())
            await lib.erase(ctx, 20, noperm)

    @cog.group(invoke_without_command=True, no_pm=True)
    async def load(self, ctx, cog : str=None):
        if ctx.author.id in self.config.owner:
            if cog is None:
                e = await ctx.send(embed=lib.Editable("Error!", "Enter a cog name to load!", "Error"))
                await lib.erase(ctx, 20, e)
            else:
                try:
                    self.bot.load_extension(cog)
                    s = await ctx.send(embed=lib.Editable("Success!", f"{cog} has been loaded!", "Cogs"))
                    await lib.erase(ctx, 20, s)
                except Exception as error:
                    ee = await ctx.send(embed=lib.Editable("Error!", f"{cog} cannot be loaded because {error}!", "Cogs"))
                    await lib.erase(ctx, 20, ee)
        else:
            noperm = await ctx.send(embed=lib.NoPerm())
            await lib.erase(ctx, 20, noperm)

    @cog.group(invoke_without_command=True, no_pm=True)
    async def unload(self, ctx, cog : str=None):
        if ctx.author.id in self.config.owner:
            if cog is None:
                e = await ctx.send(embed=lib.Editable("Error!", "Enter a cog name to unload!", "Error"))
                await lib.erase(ctx, 20, e)
            else:
                try:
                    self.bot.unload_extension(cog)
                    s = await ctx.send(embed=lib.Editable("Success!", "{cog} has been unloaded!", "Cogs"))
                    await lib.erase(ctx, 20, s)
                except Exception as error:
                    ee = await ctx.send(embed=lib.Editable("Error!", "{cog} cannot be unloaded because {error}!", "Cogs"))
                    await lib.erase(ctx, 20, ee)
        else:
            noperm = await ctx.send(embed=lib.NoPerm())
            await lib.erase(ctx, 20, noperm)

    @cog.command(no_pm=True)
    async def list(self, ctx):
        if ctx.author.id in self.config.owner:
            u = await ctx.send(embed=lib.Editable("Available Cogs", "cogs.core, cogs.main, cogs.fun, cogs.music, cogs.moderation, cogs.admin", "Cogs"))
            await lib.erase(ctx, 20, u)
        else:
            noperm = await ctx.send(embed=lib.NoPerm())
            await lib.erase(ctx, 20, noperm)

    @commands.command(aliases=["sp"], no_pm=True)
    async def setpresence(self, ctx, activity:str=None, *args):
        if ctx.author.id in self.config.owner:
            listening = discord.ActivityType.listening
            watching = discord.ActivityType.watching
            game = ""
            for gamename in args:
                game += gamename
                game += " "
            if game == "":
                e = await ctx.send(embed=lib.Editable("Error", "Please enter one of these activities with the name you would like after it!\n\n**playing {name}**\n**listening {name}**\n**watching {name}**", "Usage"))
                await lib.erase(ctx, 20, e)
            else:
                if activity == "playing":
                    await lib.sp(self, ctx, game)
                    p = await ctx.send(embed=lib.Editable("Activity Presence", f"The bots status has been set to **Playing** {game} ", "Owner"))
                    await lib.erase(ctx, 20, p)
                if activity == "listening":
                    await lib.sa(self, ctx, listening, game)
                    l = await ctx.send(embed=lib.Editable("Activity Presence", f"The bots status has been set to **Listening to** {game}", "Owner"))
                    await lib.erase(ctx, 20, l)
                if activity == "watching":
                    await lib.sa(self, ctx, watching, game)
                    w = await ctx.send(embed=lib.Editable("Activity Presence", f"The bots status has been set to **Watching** {game}", "Owner"))
                    await lib.erase(ctx, 20, w)
        else:
            noperm = await ctx.send(embed=lib.NoPerm())
            await lib.erase(ctx, 20, noperm)

    @commands.command(no_pm=True)
    async def shutdown(self, ctx):
            if ctx.author.id in self.config.owner:
                o = await ctx.send(embed=lib.Editable("Going Offline", "Self Destruct Sequence Initiation detected.. Shutting down!.", "Owner"))
                await self.bot.logout()
            else:
                noperm = await ctx.send(embed=lib.NoPerm())
                await lib.erase(ctx, 20, noperm)

    @commands.command(no_pm=True)
    async def leave(self, ctx):
        guild = ctx.message.guild
        if ctx.author == guild.owner:
            await ctx.guild.leave()
        else:
            noperm = await ctx.send(embed=lib.NoPerm())
            await lib.erase(ctx, 20, noperm)

    @commands.command(no_pm=True)
    async def amiadmin(self, ctx):
        if ctx.author.id in self.config.owner:
            y = await ctx.send(f"Yes **{ctx.author.name}**, you're an admin!")
            await lib.erase(ctx, 20, y)
        else:
            n = await ctx.send(f"You arent an admin, {ctx.author.name}")
            await lib.erase(ctx, 20, n)

    @commands.command(no_pm=True)
    async def pm(self, ctx, user : discord.User=None, *args):
        if ctx.author.id in self.config.owner:
            member = ctx.author
            userid = ctx.author.id
            avatar = ctx.author.avatar_url
            if user is None:
                await ctx.send(embed=lib.Editable("Oops!", "You forgot something!\n\n!pm {@user} {message}\n\n This will send a dm to the mentioned user.", "PM Usage"))
            else:
                message = ""
                for word in args:
                    message += word
                    message += " "
                if message is "":
                    await ctx.send(embed=lib.Editable("Oops!", "You forgot something!\n\n!pm {@user} {message}\n\n This will send a dm to the mentioned user.", "PM Usage"))
                else:
                    embed = discord.Embed(
                        title = f"You've recieved a message from {member}",
                        colour = 0x9bf442,
                        )
                    embed.set_author(name=f"Message from {member}", icon_url=f"{avatar}")
                    embed.add_field(name="Message:", value=message, inline=True)
                    embed.set_footer(text=f"UserID: {userid}")
                    await user.send(embed=embed)
                    await ctx.message.delete()
        else:
            noperm = await ctx.send(embed=lib.NoPerm())
            await lib.erase(ctx, 20, noperm)

    @commands.command(no_pm=True)
    async def pmid(self, ctx, id=None, *args):
        if ctx.author.id in self.config.owner:
            if id is None:
                e = await ctx.send(embed=lib.Editable("Oops!", "You forgot something!\n\n!pmid {userid} {message}\n\n This will send a dm to the user with that ID", "PMID Usage"))
                await lib.erase(ctx, 20, e)
            else:
                member = ctx.author
                userid = ctx.author.id
                avatar = ctx.author.avatar_url
                message = ""
                for word in args:
                    message += word
                    message += " "
                if message is "":
                    e1 = await ctx.send(embed=lib.Editable("Oops!", "You forgot something!\n\n!pmid {userid} {message}\n\n This will send a dm to the user with that ID.", "PMID Usage"))
                    await lib.erase(ctx, 20, e1)
                else:
                    try:
                        user = await self.bot.fetch_user(id)
                        embed = discord.Embed(
                            title = f"You've recieved a message from {member}",
                            colour = 0x9bf442,
                            )
                        embed.set_author(name=f"Message from {member}", icon_url=f"{avatar}")
                        embed.add_field(name="Message:", value=message, inline=True)
                        embed.set_footer(text=f"UserID: {userid}")
                        await user.send(embed=embed)
                    except Exception as error:
                            er = await ctx.send(f"I couldnt send your message to {member} because of the error: {error}")
                            await lib.erase(ctx, 20, er)
        else:
            noperm = await ctx.send(embed=lib.NoPerm())
            await lib.erase(ctx, 20, noperm)



def setup(bot):
    bot.add_cog(Admin(bot))
