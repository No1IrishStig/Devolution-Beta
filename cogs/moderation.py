import datetime
import asyncio
import discord
import json

from utils import default
from utils.default import lib
from discord.ext import commands

db_timer = {"timer": 20}

class Mod(commands.Cog):
    def __init__(self, bot):
            self.bot = bot
            self.config = default.get("utils/cfg.json")
            with open("./utils/essentials/deltimer.json") as f:
                self.deltimer = json.load(f)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def say(self, ctx, *args):
        if ctx.author.guild_permissions.manage_messages:
            output = ""
            for word in args:
                output += word
                output += " "
            if output is " ":
                e = await ctx.send(embed=lib.Editable("Error", "Please enter a message to send!", "Moderation"))
                await lib.eraset(self, ctx, e)
            else:
                await ctx.message.delete()
                await ctx.send(output)

        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kick(self, ctx, user : discord.User=None, *args):
        if ctx.author.guild_permissions.kick_members:
            if user:
                try:
                    server = ctx.guild.name
                    author = ctx.author
                    reason = ""
                    for word in args:
                        reason += word
                        reason += " "
                    if reason == "":
                        await user.send(embed=lib.Editable("You were kicked", f"You were kicked from **{server}** by **{author}**", "Moderation"))
                        s = await ctx.send(embed=lib.Editable("Success", f"User has been kicked by **{author.name}**", "Moderation"))
                        await ctx.guild.kick(user)
                        await lib.eraset(self, ctx, s)
                    else:
                        await user.send(embed=lib.Editable("You were kicked", f"You were kicked from **{server}** by **{author}** for **{reason}**", "Moderation"))
                        s1 = await ctx.send(embed=lib.Editable("Success", f"User has been kicked by **{author.name}** for **{reason}**", "Moderation"))
                        await ctx.guild.kick(user)
                        await lib.eraset(self, ctx, s1)
                except Exception as error:
                        ex = await ctx.send(f"I cant kick **{user}** because: {error}")
                        await lib.eraset(self, ctx, ex)
            else:
                e = await ctx.send(embed=lib.Editable("Oops!", f"You forgot something!\n\n{ctx.prefix}kick (@user) (reason)\n\nKicks mentioned user from the server, with or without a reason.", "Kick Usage"))
                await lib.eraset(self, ctx, e)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ban(self, ctx, user : discord.User=None, *args):
        if ctx.author.guild_permissions.ban_members:
            if user:
                try:
                    server = ctx.guild.name
                    author = ctx.author
                    reason = ""
                    for word in args:
                        reason += word
                        reason += " "
                    if reason == "":
                        await user.send(embed=lib.Editable("You were banned", f"You were banned from **{server}** by **{author}**", "Moderation"))
                        s = await ctx.send(embed=lib.Editable("Success", f"User has been banned by **{author.name}**", "Moderation"))
                        await ctx.guild.ban(user)
                        await lib.eraset(self, ctx, s)
                    else:
                        await user.send(embed=lib.Editable("You were banned", f"You were banned from **{server}** by **{author}** for **{reason}**", "Moderation"))
                        s1 = await ctx.send(embed=lib.Editable("Success", f"User has been banned by **{author.name}** for **{reason}**", "Moderation"))
                        await ctx.guild.ban(user)
                        await lib.eraset(self, ctx, s1)
                except Exception as error:
                        ex = await self.bot.say(f"**{user}** cannot be banned. {error}")
                        await lib.eraset(self, ctx, ex)
            else:
                e = await ctx.send(embed=lib.Editable("Oops!", f"You forgot something!\n\n{ctx.prefix}ban (@user)\n{ctx.prefix}ban (@user) (reason)\n\nBans mentioned user from the server, with or without a reason.", "Ban Usage"))
                await lib.eraset(self, ctx, e)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hackban(self, ctx, user_id: int=None, *, reason: str = None):
        if ctx.author.guild_permissions.ban_members:
            author = ctx.author
            server = author.guild
            avatar = ctx.author.avatar_url
            if user_id is None:
                e = await ctx.send(embed=lib.Editable("Oops!", f"You forgot something!\n\n{ctx.prefix}hackban (userid) (reason)\n\nBans the UserID, with or without a reason.", "Hackban Usage"))
                await lib.eraset(self, ctx, e)
            else:
                user_id = str(user_id)
                ban_list = await ctx.guild.bans()
                user = ctx.guild.get_member(user_id)
                if user is not None:
                    await ctx.invoke(self.ban, user=user, reason=reason)
                    return
                try:
                    await self.bot.http.ban(user_id, server.id, 0)
                except discord.NotFound:
                    e1 = await ctx.send(embed=lib.Editable("Error", "Cant find anyone with that ID try again!", "Moderation"))
                    await lib.eraset(self, ctx, e1)
                else:
                    if reason is None:
                        user = await self.bot.fetch_user(user_id)
                        y = await ctx.send(embed=lib.AvatarEdit("{}".format(author) + " Just yeeted someone!", f"{avatar}", "Yeet!", f"UserID **{user_id}** just got hackbanned!", "Moderation"))
                        await user.send(embed=lib.Editable("You were hackbanned!", f"You got hack banned from **{server}**", "Moderation"))
                        await lib.eraset(self, ctx, y)
                    else:
                        user = await self.bot.fetch_user(user_id)
                        y1 = await ctx.send(embed=lib.AvatarEdit(f"{author} Just yeeted someone!", "{avatar}".format(avatar), "Yeet!", f"UserID **{user_id}** just got hackbanned for **{reason}**!", "Moderation"))
                        await user.send(embed=lib.Editable("You were hackbanned!", f"You got hack banned from **{server}** for **{reason}**", "Moderation"))
                        await lib.eraset(self, ctx, y1)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def punish(self, ctx, member: discord.Member=None, *args):
        if ctx.author.guild_permissions.manage_roles:
            if member is None:
                u = await ctx.send(embed=lib.Editable("Punish Usage", f"{ctx.prefix}punish (@user)\n{ctx.prefix}unpunish (@user)\n{ctx.prefix}lspunish - Lists all punished users\n{ctx.prefix}spp - **Warning** Use this command only, if there are channels which do not have the permissions for the punished role.\n\n Mutes or unmutes mentioned user from all channels on the server.", "Moderation"))
                await lib.eraset(self, ctx, u)
            else:
                server = ctx.guild.name
                author = ctx.author.name
                role = discord.utils.get(member.guild.roles, name="punished")
                if role is None:
                    channel = ctx.channel
                    e = await ctx.send(embed=lib.Editable("Oops!", "Punished role not found! Creating...", "Error"))
                    await ctx.guild.create_role(name="punished"),
                    await asyncio.sleep(5)
                    w = await ctx.send(embed=lib.Editable("Working...", "Settings Permissions...", "Moderation"))
                    await e.delete()
                    for channel in ctx.guild.channels:
                        role = discord.utils.get(channel.guild.roles, name="punished")
                        overwrite = discord.PermissionOverwrite()
                        overwrite.send_messages = False
                        overwrite.send_tts_messages = False
                        overwrite.add_reactions = False
                        await channel.set_permissions(role, overwrite=overwrite),
                    await asyncio.sleep(5)
                    await w.delete()
                    d = await ctx.send(embed=lib.Editable("Done!", "The role has been created and the permissions set! Retrying your command!", "Moderation"))
                    await ctx.reinvoke()
                    await lib.eraset(self, ctx, d)
                else:
                    if role in member.roles:
                        e1 = await ctx.send(embed=lib.Editable("Error", f"**{member.name}** is already punished!", "Error"))
                        await lib.eraset(self, ctx, e1)
                    else:
                        reason = ""
                        for word in args:
                            reason += word
                            reason += " "
                        if reason == "":
                            await member.send(embed=lib.Editable("Punished!", f"You were punished from **{server}** by **{author}**", "Moderation"))
                            s = await ctx.send(embed=lib.Editable("Success", f"**{member.name}** has been punished by **{author}**", "Moderation"))
                            await member.add_roles(role)
                            await lib.eraset(self, ctx, s)
                        else:
                            await member.send(embed=lib.Editable("Punished!", f"You were punished from **{server}** by **{author}** for **{reason}**", "Moderation"))
                            s1 = await ctx.send(embed=lib.Editable("Success", f"**{member.name}** has been punished by **{author}** for **{reason}**", "Moderation"))
                            await member.add_roles(role)
                            await lib.eraset(self, ctx, s1)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unpunish(self, ctx, member: discord.Member=None):
        if ctx.author.guild_permissions.manage_roles:
            if member is None:
                u = await ctx.send(embed=lib.Editable("Oops!", f"You forgot something!\n\n{ctx.prefix}unpunish (@user)\n\nUnmutes mentioned user.", "Punish Usage"))
                await lib.eraset(self, ctx, u)
            else:
                server = ctx.guild.name
                author = ctx.author.name
                role = discord.utils.get(member.guild.roles, name="punished")
                if not role in member.roles:
                    e = await ctx.send(embed=lib.Editable("Error", f"**{member.name}** is not punished", "Error"))
                    await lib.eraset(self, ctx, e)
                else:
                    await member.send(embed=lib.Editable("Unpunished!", f"You were unpunished from {server} by {author}", "Moderation"))
                    s = await ctx.send(embed=lib.Editable("Success", f"**{member.name}** unpunished by {author}", "Moderation"))
                    await member.remove_roles(role)
                    await lib.eraset(self, ctx, s)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def lspunish(self, ctx):
        pusers = []
        if ctx.author.guild_permissions.manage_roles:
            role = discord.utils.get(ctx.guild.roles, name="punished")
            for member in ctx.guild.members:
                if role in member.roles:
                        pusers.append(member.name)
            await ctx.send(embed=lib.Editable("Punished List", "{}".format(", ".join(pusers)), "Moderation"))
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rename(self, ctx, member:discord.Member=None, *args):
        if ctx.author.guild_permissions.manage_nicknames:
            try:
                if member is None:
                    author = ctx.author.name
                    name = ""
                    for word in args:
                        name += word
                        name += " "
                    if name is "":
                        e1 = await ctx.send(embed=lib.Editable("Oops!", f"You forgot something!\n\n{ctx.prefix}rename user (name)\n\nRenames the mentioned user to a specified nickname", "Rename Usage"))
                        await lib.eraset(self, ctx, e1)
                    else:
                        await ctx.send(embed=lib.Editable("Success", f"**{member.name}** has been renamed by **{author}** to **{name}**", "Moderation"))
                        await member.edit(nick=name)
                else:
                    e = await ctx.send(embed=lib.Editable("Oops!", f"You forgot something!\n\n{ctx.prefix}rename user (name)\n\nRenames the mentioned user to a specified nickname.", "Rename Usage"))
                    await lib.eraset(self, ctx, e)
            except Exception as error:
                ex = await ctx.send(f"Uh oh.. I could not rename **{user}**")
                await lib.eraset(self, ctx, ex)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def clean(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            number = 99
            channel = ctx.channel
            author = ctx.author
            server = channel.guild
            is_bot = self.bot.user.bot
            prefixes = self.config.prefix
            if isinstance(prefixes, str):
                prefixes = [prefixes]
            elif callable(prefixes):
                if asyncio.iscoroutine(prefixes):
                    await ctx.send("Coroutine prefixes not yet implemented.")
                    return
                prefixes = prefixes(self.bot, ctx.message)

            if "" in prefixes:
                prefixes.pop("")

            def check(m):
                if m.author.id == self.bot.user.id:
                    return True
                elif m == ctx.message:
                    return True
                p = discord.utils.find(m.content.startswith, prefixes)
                if p and len(p) > 0:
                    return m.content[len(p):]
                return False

            to_delete = [ctx.message]

            tries_left = 5
            tmp = ctx.message

            while tries_left and len(to_delete) - 1 < number:
                async for message in channel.history(limit=number, before=tmp):
                    if len(to_delete) - 1 < number and check(message):
                        to_delete.append(message)
                    tmp = message
                tries_left -= 1

                await channel.delete_messages(to_delete)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @commands.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cleanup(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            u = await ctx.send(embed=lib.Editable("Cleanup Usage", "**after {id}** - Deletes messages after a specified message.\n**messages {amount}** - Deletes X amount of messages\n**user {name} {amount}** - Delete X amount of messages from a specific user\n**bot {amount}** - Delete X amount of command messages and bot messages", "Roles"))
            await lib.eraset(self, ctx, u)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @cleanup.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def after(self, ctx, id=None):
        if ctx.author.guild_permissions.manage_messages:
            channel = ctx.channel
            author = ctx.author
            server = channel.guild
            if id is None:
                e = await ctx.send(embed=lib.Editable("Oops!", f"You forgot something!\n\n{ctx.prefix}cleanup after (message_id)\n\nDeletes all messages after a specified message ID.", "Cleanup After Usage"))
                await lib.eraset(self, ctx, e)
            else:
                to_delete = []
                after = await channel.fetch_message(id)
                async for message in channel.history(limit=100, after=after):
                    to_delete.append(message)
                await channel.delete_messages(to_delete)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @cleanup.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def messages(self, ctx, num:int=None):
        if ctx.author.guild_permissions.manage_messages:
            if num is None:
                e = await ctx.send(embed=lib.Editable("Oops!", f"You forgot something!\n\n{ctx.prefix}cleanup messages (amount)\n\nDeletes the specified number of messages.", "Cleanup Messages Usage"))
                await lib.eraset(self, ctx, e)
            else:
                db = self.deltimer
                guild = ctx.guild
                gid = str(guild.id)
                timer = db[gid]["timer"]
                await ctx.channel.purge(limit=num + 1)
                s = await ctx.send(embed=lib.Editable("Success", f"{num} messages were deleted!", "Moderation"))
                await asyncio.sleep(timer)
                await s.delete()
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @cleanup.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def user(self, ctx, user: discord.Member=None, number: int=None):
        if ctx.author.guild_permissions.manage_messages:
            channel = ctx.channel
            author = ctx.author
            server = author.guild
            is_bot = self.bot.user.bot
            self_delete = user == self.bot.user

            if user is None:
                e1 = await ctx.send(embed=lib.Editable("Oops!", f"You forgot something!\n\n{ctx.prefix}cleanup user (@user) (amount)\n\nDeletes the a specified number of messages for a specified user.", "Cleanup User Usage"))
                await lib.eraset(self, ctx, e1)
            else:
                if number is None:
                    e1 = await ctx.send(embed=lib.Editable("Oops!", f"You forgot something!\n\n{ctx.prefix}cleanup user (@user) (amount)\n\nDeletes the a specified number of messages for a specified user.", "Cleanup User Usage"))
                    await lib.eraset(self, ctx, e2)
                else:
                    def check(m):
                        if m.author == user:
                            return True
                        elif m == ctx.message:
                            return True
                        else:
                            return False

                    to_delete = [ctx.message]
                    tries_left = 5
                    tmp = ctx.message

                    while tries_left and len(to_delete) - 1 < number:
                        async for message in channel.history(limit=number, before=tmp):
                            if len(to_delete) - 1 < number and check(message):
                                to_delete.append(message)
                            tmp = message
                        tries_left -= 1
                        await channel.delete_messages(to_delete)
        else:
            await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @cleanup.group(pass_context=True, no_pm=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def bot(self, ctx, number: int=None):
        if ctx.author.guild_permissions.manage_messages:
            channel = ctx.channel
            author = ctx.author
            server = channel.guild
            is_bot = self.bot.user.bot
            has_permissions = channel.permissions_for(server.me).manage_messages

            prefixes = self.config.prefix
            if isinstance(prefixes, str):
                prefixes = [prefixes]
            elif callable(prefixes):
                if asyncio.iscoroutine(prefixes):
                    await ctx.send("Coroutine prefixes not yet implemented.")
                    return
                prefixes = prefixes(self.bot, ctx.message)

            if "" in prefixes:
                prefixes.pop("")

            def check(m):
                if m.author.id == self.bot.user.id:
                    return True
                elif m == ctx.message:
                    return True
                p = discord.utils.find(m.content.startswith, prefixes)
                if p and len(p) > 0:
                    return m.content[len(p):]
                return False

            to_delete = [ctx.message]

            tries_left = 5
            tmp = ctx.message

            while tries_left and len(to_delete) - 1 < number:
                async for message in channel.history(limit=number, before=tmp):
                    if len(to_delete) - 1 < number and check(message):
                        to_delete.append(message)
                    tmp = message
                tries_left -= 1

                await channel.delete_messages(to_delete)
        else:
            await ctx.send(embed=lib.NoPerm())

    @commands.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def deltimer(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            db = self.deltimer
            guild = ctx.guild
            gid = str(guild.id)
            if not gid in db:
                await ctx.send(embed=lib.Editable("Uh oh", f"The Custom Deletion timer is not enabled for this server!\n\nTry this command:\n**{ctx.prefix}deltimer enable**", "Deletion Timer"))
            else:
                timert = db[gid]["timer"]
                await ctx.send(embed=lib.Editable("Uh oh", f"Deltimer is enabled and is currently set at **{timert}** seconds.\n\nHeres a list of commands you can try!\n**{ctx.prefix}deltimer enable**\n**{ctx.prefix}deltimer set number**", "Deletion Timer"))
        else:
            noperm = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, noperm)

    @deltimer.group(invoke_without_command=True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def set(self, ctx, timer:int = None):
        if ctx.author.guild_permissions.manage_messages:
            db = self.deltimer
            guild = ctx.guild
            gid = str(guild.id)
            if timer is None:
                e = await ctx.send(embed=lib.Editable("Error", f"{ctx.author.mention} Please enter an amount of seconds!", "Error"))
                await lib.eraset(self, ctx, e)
            elif timer < 1:
                e1 = await ctx.send(embed=lib.Editable("Error", f"{ctx.author.mention} Please enter an amount of seconds between 1 and 60!", "Error"))
                await lib.eraset(self, ctx, e1)
            elif timer > 60:
                e1 = await ctx.send(embed=lib.Editable("Error", f"{ctx.author.mention} Please enter an amount of seconds between 1 and 60!", "Error"))
                await lib.eraset(self, ctx, e2)
            else:
                if not gid in db:
                    e3 = await ctx.send(embed=lib.Editable("Error", f"The Custom Deletion timer is not enabled for this server!\n\nRun command `{ctx.prefix}deltimer enable` to begin!", "Error"))
                    await lib.eraset(self, ctx, e3)
                else:
                    db[gid]["timer"] = timer
                    with open("./utils/essentials/deltimer.json", "w") as f:
                        json.dump(db, f)
                        s = await ctx.send(embed=lib.Editable("Success", f"{ctx.author.mention} Changed the deletion timer to {timer}", "Deletion Timer"))
                        await lib.eraset(self, ctx, s)
        else:
            noperm = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, noperm)

    @deltimer.group(invoke_without_command=True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def enable(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            db = self.deltimer
            guild = ctx.guild
            gid = str(guild.id)
            if not gid in db:
                db[gid] = db_timer
                with open("./utils/essentials/deltimer.json", "w") as f:
                    json.dump(db, f)
                    s = await ctx.send(embed=lib.Editable("Success", f"{ctx.author.mention} enabled the Custom Deletion Timer. It has automatically been set to **20** seconds.", "Deletion Timer"))
                    await lib.eraset(self, ctx, s)
            else:
                del db[gid]
                with open("./utils/essentials/deltimer.json", "w") as f:
                    json.dump(db, f)
                    s1 = await ctx.send(embed=lib.Editable("Success", f"{ctx.author.mention} disabled the Custom Deletion Timer. Message deletion timers have been reset to **20** seconds.", "Deletion Timer"))
                    await lib.eraset(self, ctx, s1)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)


def setup(bot):
    bot.add_cog(Mod(bot))
