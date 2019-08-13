import datetime
import asyncio
import discord
import shelve
import json

from utils import default
from utils.default import lib
from discord.ext import commands

punished_users = []

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("utils/cfg.json")
        self.db = shelve.open("./data/db/data.db", writeback=True)
        with open("./data/settings/deltimer.json") as f:
            self.deltimer = json.load(f)
            with open("./data/settings/logs.json") as f:
                self.logs = json.load(f)

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
    async def punish(self, ctx, member: discord.Member=None, time:int=None, *args):
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
                            s = await ctx.send(embed=lib.Editable("Uh oh", f"Please use punish like this: `{ctx.prefix}punish @user time (reason)`", "Moderation"))
                            await lib.eraset(self, ctx, s)
                        else:
                            punished_users.append(member.id)
                            if time is not None:
                                await member.send(embed=lib.Editable("Punished!", f"You were punished from **{server}** by **{author}** for **{reason}** with a duration of **{time}**", "Moderation"))
                                s1 = await ctx.send(embed=lib.Editable("Success", f"**{member.name}** has been punished by **{author}** for **{reason}** with a duration of **{time}**", "Moderation"))
                                await member.add_roles(role)
                                await asyncio.sleep(time)
                                await member.remove_roles(role)
                                if member.id in punished_users:
                                    await member.send(embed=lib.Editable("Punished!", f"You were unpunished from **{server}** as your time expried!", "Moderation"))
                                    s2 = await ctx.send(embed=lib.Editable("Unpunished", f"**{member.name}** has been unpunished because their time expired!", "Moderation"))
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
                    punished_users.remove(member.id)
                    await lib.eraset(self, ctx, s)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def lspunish(self, ctx):
        if ctx.author.guild_permissions.manage_roles:
            await ctx.send(embed=lib.Editable("Punished List", "{}".format(", ".join(punished_users)), "Moderation"))
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
                    with open("./data/admin/deltimer.json", "w") as f:
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
                with open("./data/admin/deltimer.json", "w") as f:
                    json.dump(db, f)
                    s = await ctx.send(embed=lib.Editable("Success", f"{ctx.author.mention} enabled the Custom Deletion Timer. It has automatically been set to **20** seconds.", "Deletion Timer"))
                    await lib.eraset(self, ctx, s)
            else:
                del db[gid]
                with open("./data/admin/deltimer.json", "w") as f:
                    json.dump(db, f)
                    s1 = await ctx.send(embed=lib.Editable("Success", f"{ctx.author.mention} disabled the Custom Deletion Timer. Message deletion timers have been reset to **20** seconds.", "Deletion Timer"))
                    await lib.eraset(self, ctx, s1)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @commands.Cog.listener(name="on_member_join")
    async def on_join_(self, member):
        role = discord.utils.get(member.guild.roles, name="punished")
        if member.id in punished_users:
            await member.add_roles(role)

# Logs Start ------------------------------------------------------------------------------------------------

    @commands.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def logs(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            db = self.logs
            guild = ctx.guild
            gid = str(guild.id)
            await ctx.send(embed=lib.Editable("Logs - Usage", f"{ctx.prefix}logs set channel\n{ctx.prefix}logs toggle\n\n Enable logs for this server.", "Logs"))
            if not gid in db:
                db[gid] = inv_settings
                db[gid]["Channel"] = ctx.channel.id
                with open("./data/logs/settings.json", "w") as f:
                    json.dump(db, f)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @logs.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def set(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            await ctx.send(embed=lib.Editable("Logs - Usage", f"{ctx.prefix}logs set channel\n{ctx.prefix}logs toggle\n\n Enable logs for this server.", "Logs"))
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @set.group(name="channel", invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def set_channel(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            db = self.logs
            guild = ctx.guild
            gid = str(guild.id)

            if gid in db:
                db[gid]["Channel"] = ctx.channel.id
                with open("./data/logs/settings.json", "w") as f:
                    json.dump(db, f)
                    await ctx.send("Channel set")
            else:
                await ctx.send(embed=lib.Editable("Uh oh", f"To set the logs channel you first need to enable them!\nTry this command:\n\n{ctx.prefix}logs enable", "Logs"))
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @logs.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def toggle(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            db = self.logs
            guild = ctx.guild
            gid = str(guild.id)
            try:
                e = discord.Embed(title=f"Setting for {guild.name}", colour=0x9bf442)
                e.add_field(name="Delete", value=str(db[gid]['delete']))
                e.add_field(name="Edit", value=str(db[gid]['edit']))
                e.add_field(name="User", value=str(db[gid]['user']))
                e.add_field(name="Join", value=str(db[gid]['join']))
                e.add_field(name="Leave", value=str(db[gid]['leave']))
                e.add_field(name="Server", value=str(db[gid]['server']))
                e.set_thumbnail(url=guild.icon_url)
                await ctx.send(embed=e)
            except KeyError:
                return
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @logs.group(invoke_without_command=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def enable(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            db = self.logs
            guild = ctx.guild
            gid = str(guild.id)
            if not gid in db:
                db[gid] = inv_settings
                db[gid]["Channel"] = ctx.channel.id
                with open("./data/logs/settings.json", "w") as f:
                    json.dump(db, f)
                    await ctx.send("Logs are now enabled for this server.")
            else:
                del db[gid]
                with open("./data/logs/settings.json", "w") as f:
                    json.dump(db, f)
                    await ctx.send("I will no longer send log notifications here.")
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @toggle.group(invoke_without_command=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def delete(self, ctx):
        db = self.logs
        guild = ctx.guild
        gid = str(guild.id)
        if db[gid]["delete"] == False:
            db[gid]["delete"] = True
            with open("./data/logs/settings.json", "w") as f:
                json.dump(db, f)
                await ctx.send("Delete logs enabled")
        elif db[gid]["delete"] == True:
            db[gid]["delete"] = False
            with open("./data/logs/settings.json", "w") as e:
                json.dump(db, e)
                await ctx.send("Delete logs disabled")

    @toggle.group(invoke_without_command=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def edit(self, ctx):
        db = self.logs
        guild = ctx.guild
        gid = str(guild.id)
        if db[gid]["edit"] == False:
            db[gid]["edit"] = True
            with open("./data/logs/settings.json", "w") as f:
                json.dump(db, f)
                await ctx.send("Edit logs enabled")
        elif db[gid]["edit"] == True:
            db[gid]["edit"] = False
            with open("./data/logs/settings.json", "w") as e:
                json.dump(db, e)
                await ctx.send("Edit logs disabled")

    @toggle.group(invoke_without_command=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def user(self, ctx):
        db = self.logs
        guild = ctx.guild
        gid = str(guild.id)
        if db[gid]["user"] == False:
            db[gid]["user"] = True
            with open("./data/logs/settings.json", "w") as f:
                json.dump(db, f)
                await ctx.send("User logs enabled")
        elif db[gid]["user"] == True:
            db[gid]["user"] = False
            with open("./data/logs/settings.json", "w") as e:
                json.dump(db, e)
                await ctx.send("User logs disabled")

    @toggle.group(invoke_without_command=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def join(self, ctx):
        db = self.logs
        guild = ctx.guild
        gid = str(guild.id)
        if db[gid]["join"] == False:
            db[gid]["join"] = True
            with open("./data/logs/settings.json", "w") as f:
                json.dump(db, f)
                await ctx.send("Join logs enabled")
        elif db[gid]["join"] == True:
            db[gid]["join"] = False
            with open("./data/logs/settings.json", "w") as e:
                json.dump(db, e)
                await ctx.send("Join logs disabled")

    @toggle.group(invoke_without_command=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def leave(self, ctx):
        db = self.logs
        guild = ctx.guild
        gid = str(guild.id)
        if db[gid]["leave"] == False:
            db[gid]["leave"] = True
            with open("./data/logs/settings.json", "w") as f:
                json.dump(db, f)
                await ctx.send("Leave logs enabled")
        elif db[gid]["leave"] == True:
            db[gid]["leave"] = False
            with open("./data/logs/settings.json", "w") as e:
                json.dump(db, e)
                await ctx.send("Leave logs disabled")

    @toggle.group(invoke_without_command=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def server(self, ctx):
        db = self.logs
        guild = ctx.guild
        gid = str(guild.id)
        if db[gid]["server"] == False:
            db[gid]["server"] = True
            with open("./data/logs/settings.json", "w") as f:
                json.dump(db, f)
                await ctx.send("Server logs enabled")
        elif db[gid]["server"] == True:
            db[gid]["server"] = False
            with open("./data/logs/settings.json", "w") as e:
                json.dump(db, e)
                await ctx.send("Server logs disabled")

    @toggle.group(invoke_without_command=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def all(self, ctx):
        db = self.logs
        guild = ctx.guild
        gid = str(guild.id)
        db[gid]["delete"] = True
        db[gid]["edit"] = True
        db[gid]["user"] = True
        db[gid]["join"] = True
        db[gid]["leave"] = True
        db[gid]["server"] = True
        with open("./data/logs/settings.json", "w") as f:
            json.dump(db, f)
            await ctx.send("All logs enabled")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        db = self.logs
        guild = message.guild
        gid = str(guild.id)
        if gid in db:
            if db[gid]['delete'] == True:
                if not message.author is message.author.bot:
                    channel = db[gid]["Channel"]
                    time = datetime.datetime.utcnow()
                    cleanmsg = message.content
                    for i in message.mentions:
                        cleanmsg = cleanmsg.replace(i.mention, str(i))
                    fmt = '%H:%M:%S'
                    name = message.author
                    name = " ~ ".join((name.name, name.nick)) if name.nick else name.name
                    delmessage = discord.Embed(
                    colour=0x9bf442,
                    timestamp=datetime.datetime.utcnow()
                    )
                    infomessage = "A message by __{}__, was deleted in {}".format(message.author.nick if message.author.nick else message.author.name, message.channel.mention)
                    delmessage.add_field(name="Info:", value=infomessage, inline=False)
                    delmessage.add_field(name="Message:", value=cleanmsg)
                    delmessage.set_footer(text="User ID: {}".format(message.author.id))
                    delmessage.set_author(name="Deleted Message", url="http://i.imgur.com/fJpAFgN.png")
                    delmessage.set_thumbnail(url="http://i.imgur.com/fJpAFgN.png")
                    try:
                        sendto = guild.get_channel(int(channel))
                        await sendto.send(embed=delmessage)
                    except:
                        pass
                else:
                    pass
            else:
                return
        else:
            return

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        db = self.logs
        guild = before
        gid = str(guild.id)
        if gid in db:
            if db[gid]['edit'] == True:
                cleanbefore = before.content
                for i in before.mentions:
                    cleanbefore = cleanbefore.replace(i.mention, str(i))
                cleanafter = after.content
                for i in after.mentions:
                    cleanafter = cleanafter.replace(i.mention, str(i))
                channel = db[gid]["Channel"]
                time = datetime.datetime.utcnow()
                fmt = '%H:%M:%S'
                name = before.author
                name = " ~ ".join((name.name, name.nick)) if name.nick else name.name
                try:
                    edit = discord.Embed(
                    colour=0x9bf442,
                    timestamp=datetime.datetime.utcnow()
                    )
                    infomessage = "A message by __{}__, was edited in {}".format(before.author.nick if before.author.nick else before.author.name, before.channel.mention)
                    edit.add_field(name="Info:", value=infomessage, inline=False)
                    edit.add_field(name="Before Message:", value=cleanbefore, inline=False)
                    edit.add_field(name="After Message:", value=cleanafter)
                    edit.set_footer(text="User ID: {}".format(before.author.id))
                    edit.set_author(name="Edited Message", url="http://i.imgur.com/Q8SzUdG.png")
                    edit.set_thumbnail(url="http://i.imgur.com/Q8SzUdG.png")
                    send_to = guild.get_channel(channel)
                    await send_to.send(embed=edit)
                except Exception as e:
                    return
            else:
                return
        else:
            return

    @commands.Cog.listener()
    async def on_member_join(self, member):
        db = self.logs
        guild = member.guild
        gid = str(guild.id)
        if gid in db:
            if db[gid]['join'] == True:
                channel = db[gid]["Channel"]
                time = datetime.datetime.utcnow()
                fmt = '%H:%M:%S'
                users = len([e.name for e in guild.members])
                name = member
                name = " ~ ".join((name.name, name.nick)) if name.nick else name.name
                joinmsg = discord.Embed(colour=0x9bf442,
                timestamp=datetime.datetime.utcnow()
                )
                infomessage = "__{}__ has joined the server.".format(member.nick if member.nick else member.name)
                joinmsg.add_field(name="Info:", value=infomessage, inline=False)
                joinmsg.set_footer(text="User ID: {}".format(member.id))
                joinmsg.set_author(name="Someone Joined")
                joinmsg.set_thumbnail(url="http://www.emoji.co.uk/files/twitter-emojis/objects-twitter/11031-inbox-tray.png")
                send_to = guild.get_channel(channel)
                await send_to.send(embed=joinmsg)
            else:
                return
        else:
            return

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        db = self.logs
        guild = member.guild
        gid = str(guild.id)
        if gid in db:
            if db[gid]['leave'] == True:
                channel = db[gid]["Channel"]
                time = datetime.datetime.utcnow()
                fmt = "%H:%M:%S"
                users = len([e.name for e in guild.members])
                name = member
                name = " ~ ".join((name.name, name.nick)) if name.nick else name.name
                leave = discord.Embed(colour=0x9bf442,
                timestamp=datetime.datetime.utcnow()
                )
                infomessage = "__{}__ has left the server.".format(member.nick if member.nick else member.name)
                leave.add_field(name="Info:", value=infomessage, inline=False)
                leave.set_footer(text="User ID: {}".format(member.id))
                leave.set_author(name="Someone Left")
                leave.set_thumbnail(url="http://www.emoji.co.uk/files/mozilla-emojis/objects-mozilla/11928-outbox-tray.png")
                send_to = guild.get_channel(channel)
                await send_to.send(embed=leave)
            else:
                return
        else:
            return

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        db = self.logs
        guild = before
        gid = str(guild.id)
        if gid in db:
            if db[gid]['server'] == True:
                channel = db[gid]["Channel"]
                time = datetime.datetime.utcnow()
                fmt = '%H:%M:%S'
                try:
                    if before.name != after.name:
                        sname = discord.Embed(colour=0x9bf442,
                        timestamp=datetime.datetime.utcnow()
                        )
                        before = f"**{before.name}**"
                        after = f"**{after.name}**"
                        sname.add_field(name="Before:", value=before, inline=False)
                        sname.add_field(name="After:", value=after, inline=False)
                        sname.set_footer(text="Server ID: {}".format(gid))
                        sname.set_author(name="Server Name Changed")
                        send_to = guild.get_channel(channel)
                        await send_to.send(embed=sname)
                    if before.region != after.region:
                        rname = discord.Embed(colour=0x9bf442,
                        timestamp=datetime.datetime.utcnow()
                        )
                        before = f"**{before.region}**"
                        after = f"**{after.region}**"
                        rname.add_field(name="Before:", value=before, inline=False)
                        rname.add_field(name="After:", value=after, inline=False)
                        rname.set_footer(text="Server ID: {}".format(gid))
                        rname.set_author(name="Server Region Changed")
                        send_to = guild.get_channel(channel)
                        await send_to.send(embed=rname)
                except Exception as e:
                    return
            else:
                return
        else:
            return

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        db = self.logs
        guild = before.guild
        gid = str(guild.id)
        if gid in db:
            if db[gid]['user'] == True:
                channel = db[gid]["Channel"]
                time = datetime.datetime.utcnow()
                fmt = '%H:%M:%S'
                if not before.nick == after.nick:
                    name = before
                    name = " ~ ".join((name.name, name.nick)) if name.nick else name.name
                    updmessage = discord.Embed(colour=0x9bf442,
                    timestamp=datetime.datetime.utcnow()
                    )
                    infomessage = "__{}__'s nickname has changed".format(before.name)
                    updmessage.add_field(name="Info:", value=infomessage, inline=False)
                    updmessage.add_field(name="Nickname Before:", value=before.nick)
                    updmessage.add_field(name="Nickname After:", value=after.nick)
                    updmessage.set_footer(text="User ID: {}".format(before.id))
                    updmessage.set_author(name="Nickname Changed")
                    send_to = guild.get_channel(channel)
                    await send_to.send(embed=updmessage)
            else:
                return
        else:
            return

    @commands.group(invoke_without_command=True)
    async def warn(self, ctx, user: discord.User = None, *args):
        if ctx.author.guild_permissions.manage_messages:
            GID = str(ctx.guild.id)
            if "Warnings" in self.db and GID in self.db["Warnings"]:
                if user is not None:
                    UID = str(user.id)
                    if UID in self.db["Warnings"][GID]["Users"]:
                        reason = ""
                        for word in args:
                            reason += word
                            reason += " "
                        if reason is "":
                            await ctx.send(f"{user.mention} has been warned by {ctx.author.name}")
                            self.db["Warnings"][GID]["Users"][UID]["Warnings"] += 1
                            self.db.sync()
                        else:
                            await ctx.send(f"{user.mention} has been warned by {ctx.author.name} for {reason}")
                            self.db["Warnings"][GID]["Users"][UID]["Warnings"] += 1
                            self.db["Warnings"][GID]["Users"][UID]["Reasons"].append(reason)
                            self.db.sync()
                    else:
                        self.db["Warnings"][GID]["Users"][UID] = {"Warnings": 0, "Reasons": []}
                        self.db.sync()
                        await ctx.reinvoke()
                else:
                    await ctx.send(embed=lib.Editable("Uh oh", f"{ctx.author.mention}, Warnings: `{ctx.prefix}warn @user (reason)`, `{ctx.prefix}warn list`, `{ctx.prefix}warn get (userid)`, `{ctx.prefix}warn remove (userid) (warning number)`", "Warnings"))
            else:
                self.db["Warnings"] = {}
                self.db["Warnings"] = {GID: {"Users": {}}}
                self.db.sync()
                print(f"{list(self.db.keys())}")
                await ctx.reinvoke()

        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @warn.group()
    async def list(self, ctx):
        GID = str(ctx.guild.id)
        if "Warnings" in self.db and GID in self.db["Warnings"]:
            warned_users = self.db["Warnings"][GID]["Users"]
            for UID in self.db["Warnings"][GID]:
                await ctx.send(embed=lib.Editable("Warned Users List", "{}".format(", ".join(warned_users)), "Moderation"))
        else:
            await ctx.send(embed=lib.Editable("Uh oh", f"The Warnings System is not set up on this server. Run {ctx.prefix}warn to start!", "Warnings"))

    @warn.group()
    async def get(self, ctx, UID:int=None):
        GID = str(ctx.guild.id)
        UID = str(UID)
        user = await self.bot.fetch_user(UID)
        if "Warnings" in self.db and GID in self.db["Warnings"]:
            if UID is not None:
                await ctx.send(embed=lib.Editable(f"{UID}'s ({user.name}) Warnings", "{}".format(", ".join(self.db["Warnings"][GID]["Users"][UID]["Reasons"])), "Warnings"))
            else:
                await ctx.send(embed=lib.Editable("Uh oh", "Please give me a UserID to get the warnings of!", "Warnings"))
        else:
            await ctx.send(embed=lib.Editable("Uh oh", f"The Warnings System is not set up on this server. Run {ctx.prefix}warn to start!", "Warnings"))

    @warn.group()
    async def remove(self, ctx, UID:str=None, num:int=None):
        GID = str(ctx.guild.id)
        if "Warnings" in self.db and GID in self.db["Warnings"]:
            if UID is not None:
                if num is not None:
                    num -= 1
                    warn = self.db["Warnings"][GID]["Users"][UID]["Reasons"][num]
                    await ctx.send(f"{warn}, Is this the correct warning?\n\nReplies: `Yes` or anything to abort.")
                    choice = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout = 30)
                    if choice.content == "Yes" or choice.content == "yes":
                        del self.db["Warnings"][GID]["Users"][UID]["Reasons"][num]
                        self.db["Warnings"][GID]["Users"][UID]["Warnings"] -= 1
                        if self.db["Warnings"][GID]["Users"][UID]["Warnings"] == 0:
                            del self.db["Warnings"][GID]["Users"][UID]
                            self.db.sync()
                        else:
                            self.db.sync()
                    else:
                        await ctx.send("Ok. Cancelling")
                else:
                    await ctx.send(embed=lib.Editable("Uh oh", "Please give me the number of the warning to remove!", "Warnings"))
            else:
                await ctx.send(embed=lib.Editable("Uh oh", "Please give me a UserID to get the warnings of!", "Warnings"))
        else:
            await ctx.send(embed=lib.Editable("Uh oh", f"The Warnings System is not set up on this server. Run {ctx.prefix}warn to start!", "Warnings"))

# Logs End --------------------------------------------------------------------------------------------------


def setup(bot):
    bot.add_cog(Mod(bot))
