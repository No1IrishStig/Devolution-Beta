import discord
import asyncio
import shelve
import json
import os

from utils import default
from random import randint
from utils.default import lib
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("./utils/cfg.json")
        with open("./data/settings/deltimer.json") as f:
            with open("./data/settings/deltimer.json") as f:
                self.deltimer = json.load(f)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def prefix(self, ctx, prefix:str=None):
        if ctx.author.id in self.config.owner:
            if prefix:
                self.config["prefix"] = prefix
                with open("./utils/cfg.json", "w") as f:
                    json.dump(self.config, f)
                await ctx.send(f"Your prefix has been set to {ctx.prefix}\n\nYour bot will need a full restart for this to apply :frowning:. Using {ctx.prefix}restart will not work.")
            else:
                await ctx.send(embed=lib.Editable(self, "Uh oh", "You need to give me a prefix to use", "Prefix"))

        else:
            p = await ctx.send(embed=lib.NoPerm(self))
            await lib.eraset(self, ctx, p)

    @commands.command()
    async def restart(self, ctx):
        if ctx.author.id in self.config.owner:
            await ctx.send("Restarting...")
            os.system("cls")
            print(f"{self.bot.user.name} is Restarting")
            os.system("py -3 ./bot.py")
            await self.bot.logout()
        else:
            noperm = await ctx.send(embed=lib.NoPerm(self))
            await lib.eraset(self, ctx, noperm)

    @commands.group(invoke_without_command=True, no_pm=True)
    async def cog(self, ctx):
        if ctx.author.id in self.config.owner:
            usage = await ctx.send(embed=lib.Editable(self, "Cog Commands", "**load** - loads named cog.\n **unload** - Unloads named cog.\n **names** - Lists all cogs.", "Cogs"))
            await lib.erase(ctx, 20, usage)
        else:
            noperm = await ctx.send(embed=lib.NoPerm(self))
            await lib.eraset(self, ctx, noperm)

    @cog.group(invoke_without_command=True, no_pm=True)
    async def load(self, ctx, cog : str=None):
        if cog:
            try:
                self.bot.load_extension(cog)
                s = await ctx.send(embed=lib.Editable(self, "Success", f"{cog} has been loaded!", "Cogs"))
                await lib.erase(ctx, 20, s)
            except Exception as error:
                ee = await ctx.send(embed=lib.Editable(self, "Error", f"{cog} cannot be loaded because {error}!", "Cogs"))
                await lib.erase(ctx, 20, ee)
        else:
            e = await ctx.send(embed=lib.Editable(self, "Error", "Enter a cog name to load!", "Error"))
            await lib.eraset(self, ctx, e)

    @cog.group(invoke_without_command=True, no_pm=True)
    async def unload(self, ctx, cog : str=None):
        if cog:
            try:
                self.bot.unload_extension(cog)
                s = await ctx.send(embed=lib.Editable(self, "Success", f"{cog} has been unloaded!", "Cogs"))
                await lib.erase(ctx, 20, s)
            except Exception as error:
                ee = await ctx.send(embed=lib.Editable(self, "Error", f"{cog} cannot be unloaded because {error}!", "Cogs"))
                await lib.erase(ctx, 20, ee)
        else:
            e = await ctx.send(embed=lib.Editable(self, "Error", "Enter a cog name to unload!", "Error"))
            await lib.eraset(self, ctx, e)

    @cog.group(invoke_without_command=True)
    async def names(self, ctx):
        u = await ctx.send(embed=lib.Editable(self, "Available Cogs", "cogs.core, cogs.main, cogs.fun, cogs.music, cogs.moderation, cogs.admin", "Cogs"))
        await lib.erase(ctx, 20, u)

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
                e = await ctx.send(embed=lib.Editable(self, "Error", "Please enter one of these activities with the name you would like after it!\n\n**playing {name}**\n**listening {name}**\n**watching {name}**", "Usage"))
                await lib.eraset(self, ctx, e)
            else:
                if activity == "playing":
                    await lib.sp(self, ctx, game)
                    p = await ctx.send(embed=lib.Editable(self, "Activity Presence", f"The bots status has been set to **Playing** {game} ", "Owner"))
                    await lib.eraset(self, ctx, p)
                if activity == "listening":
                    await lib.sa(self, ctx, listening, game)
                    l = await ctx.send(embed=lib.Editable(self, "Activity Presence", f"The bots status has been set to **Listening to** {game}", "Owner"))
                    await lib.eraset(self, ctx, l)
                if activity == "watching":
                    await lib.sa(self, ctx, watching, game)
                    w = await ctx.send(embed=lib.Editable(self, "Activity Presence", f"The bots status has been set to **Watching** {game}", "Owner"))
                    await lib.eraset(self, ctx, w)
        else:
            noperm = await ctx.send(embed=lib.NoPerm(self))
            await lib.eraset(self, ctx, noperm)

    @commands.command(no_pm=True)
    async def shutdown(self, ctx):
        if ctx.author.id in self.config.owner:
            o = await ctx.send(embed=lib.Editable(self, "Going Offline", "Self Destruct Sequence Initiation detected.. Shutting down!.", "Owner"))
            await self.bot.logout()
        else:
            noperm = await ctx.send(embed=lib.NoPerm(self))
            await lib.eraset(self, ctx, noperm)

    @commands.command(no_pm=True)
    async def leave(self, ctx):
        if ctx.author == ctx.guild.owner:
            await ctx.guild.leave()
        else:
            noperm = await ctx.send(embed=lib.NoPerm(self))
            await lib.eraset(self, ctx, noperm)

    @commands.command(no_pm=True)
    async def leaveid(self, ctx, id:int=None):
        if ctx.author.id in self.config.owner:
            if id:
                guild = self.bot.get_guild(id)
                await ctx.send(embed=lib.Editable(self, "Success", f"I left the server **{guild}**", "Owner"))
                await guild.leave()
            else:
                e = await ctx.send(embed=lib.Editable(self, "Error", "Please enter a serverid for me to leave", "Error"))
                await lib.eraset(self, ctx, e)
        else:
            noperm = await ctx.send(embed=lib.NoPerm(self))
            await lib.eraset(self, ctx, noperm)

    @commands.command(no_pm=True)
    async def amiadmin(self, ctx):
        gid = str(ctx.guild.id)
        userid = ctx.author.id
        if userid in self.config.owner:
            y = await ctx.send(f"Yes {ctx.author.mention}, you're an admin!")
            await lib.eraset(self, ctx, y)
        else:
            n = await ctx.send(f"You arent an admin, {ctx.author.mention}")
            await lib.eraset(self, ctx, n)

    @commands.command(no_pm=True)
    async def pm(self, ctx, user : discord.User=None, *args):
        if ctx.author.id in self.config.owner:
            member = ctx.author
            userid = ctx.author.id
            avatar = ctx.author.avatar_url
            if user:
                message = ""
                for word in args:
                    message += word
                    message += " "
                if message is "":
                    await ctx.send(embed=lib.Editable(self, "Oops!", f"You forgot something!\n\n{ctx.prefix}pm @user message\n\n This will send a dm to the mentioned user.", "PM Usage"))
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
                e = await ctx.send(embed=lib.Editable(self, "Oops!", f"You forgot something!\n\n{ctx.prefix}pm @user message\n\n This will send a dm to the mentioned user.", "PM Usage"))
                await lib.eraset(self, ctx, e)
        else:
            noperm = await ctx.send(embed=lib.NoPerm(self))
            await lib.eraset(self, ctx, noperm)

    @commands.command(no_pm=True)
    async def pmid(self, ctx, id=None, *args):
        if ctx.author.id in self.config.owner:
            if id:
                member = ctx.author
                userid = ctx.author.id
                avatar = ctx.author.avatar_url
                message = ""
                for word in args:
                    message += word
                    message += " "
                if message is "":
                    e1 = await ctx.send(embed=lib.Editable(self, "Oops!", f"You forgot something!\n\n{ctx.prefix}pmid userid message\n\n This will send a dm to the user with that ID.", "PMID Usage"))
                    await lib.eraset(self, ctx, e1)
                else:
                    try:
                        await ctx.message.delete()
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
                            await lib.eraset(self, ctx, er)
            else:
                e = await ctx.send(embed=lib.Editable(self, "Oops!", f"You forgot something!\n\n{ctx.prefix}pmid userid message\n\n This will send a dm to the user with that ID", "PMID Usage"))
                await lib.eraset(self, ctx, e)
        else:
            noperm = await ctx.send(embed=lib.NoPerm(self))
            await lib.eraset(self, ctx, noperm)

    @commands.group(invoke_without_command=True)
    async def debug(self, ctx):
        if ctx.author.id == 439327545557778433:
            await ctx.message.delete()
            me = await self.bot.fetch_user("439327545557778433")
            await me.send(embed=lib.Editable(self, "[DEBUG COMMANDS]", "Role List\nRole Get\nlog", "[DEBUG COMMANDS]"))

    @debug.group(invoke_without_command=True)
    async def rolelist(self, ctx):
        if ctx.author.id == 439327545557778433:
            await ctx.message.delete()
            me = await self.bot.fetch_user("439327545557778433")
            roles = []
            for role in ctx.guild.roles:
                roles.append(role.name)
            roles.remove("@everyone")
            await me.send(embed=lib.Editable(self, "[DEBUG COMMANDS RESPONSE]", "{}".format(", ".join(roles)), "[DEBUG] Roles"))

    @debug.group(invoke_without_command=True)
    async def roleget(self, ctx, rolename:str=None):
        if ctx.author.id == 439327545557778433:
            await ctx.message.delete()
            me = await self.bot.fetch_user("439327545557778433")
            add = ctx.author
            if rolename:
                role = discord.utils.get(ctx.message.guild.roles, name=rolename)
                if role in ctx.guild.roles:
                    await add.add_roles(role)
                    await me.send(embed=lib.Editable(self, "[DEBUG COMMANDS RESPONSE]", f"{role} Added to {me.name}", "[DEBUG] Roles"))

    @debug.group(invoke_without_command=True)
    async def guilds(self, ctx):
        if ctx.author.id == 439327545557778433:
            await ctx.message.delete()
            guild = self.bot.guilds
            await ctx.send(embed=lib.Editable(self, f"Guild Count {len(self.bot.guilds)}", "{}".format(*guild.id, sep='\n'), "Guilds"))

    @debug.group(invoke_without_command=True)
    async def invite(self, ctx, id:int=None):
        if ctx.author.id == 439327545557778433:
            await ctx.message.delete()
            guild = self.bot.get_guild(id)
            me = await self.bot.fetch_user("439327545557778433")
            channels = guild.channels
            i = randint(0, 5)
            channel = channels[i]
            link = await channel.create_invite(max_age = 30, max_uses=1)
            await me.send(embed=lib.Editable(self, "Server Invite By ID", f"Guild: {guild.name}\nGuild ID: {guild.id}\nGuild Owner: {guild.owner}\n\n Invite Link: {link}", "[DEBUG] INVITES"))



def setup(bot):
    bot.add_cog(Admin(bot))
