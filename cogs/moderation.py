import datetime
import asyncio
import discord

from utils import default
from utils.default import lib
from discord.ext import commands

class Mod(commands.Cog):
    def __init__(self, bot):
            self.bot = bot
            self.config = default.get("utils/cfg.json")

    @commands.command(no_pm=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def say(self, ctx, *args):
        if ctx.author.guild_permissions.manage_messages:
            output = ""
            for word in args:
                output += word
                output += " "
            if output is " ":
                e = await ctx.send(embed=lib.Editable("Error!", "Please enter a message to send!", "Moderation"))
                await lib.erase(ctx, 20, e)
            else:
                await ctx.message.delete()
                await ctx.send(output)

        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.erase(ctx, 20, p)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kick(self, ctx, user : discord.User=None, *args):
        if ctx.author.guild_permissions.kick_members:
            if user is None:
                e = await ctx.send(embed=lib.Editable("Oops!", "You forgot something!\n\n!kick {@user} {reason}\n\nKicks mentioned user from the server, with or without a reason.", "Kick Usage"))
                await lib.erase(ctx, 20, e)
            else:
                try:
                    server = ctx.guild.name
                    author = ctx.author
                    reason = ""
                    for word in args:
                        reason += word
                        reason += " "
                    if reason == "":
                        await user.send(embed=lib.Editable("You were kicked", f"You were kicked from **{server}** by **{author}**", "Moderation"))
                        s = await ctx.send(embed=lib.Editable("Success!", f"User has been kicked by **{author.name}**", "Moderation"))
                        await ctx.guild.kick(user)
                        await lib.erase(ctx, 20, s)
                    else:
                        await user.send(embed=lib.Editable("You were kicked", f"You were kicked from **{server}** by **{author}** for **{reason}**", "Moderation"))
                        s1 = await ctx.send(embed=lib.Editable("Success!", f"User has been kicked by **{author.name}** for **{reason}**", "Moderation"))
                        await ctx.guild.kick(user)
                        await lib.erase(ctx, 20, s1)
                except Exception as error:
                        ex = await ctx.send(f"I cant kick **{user}** because: {error}")
                        await lib.erase(ctx, 45, ex)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.erase(ctx, 20, p)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ban(self, ctx, user : discord.User=None, *args):
        if ctx.author.guild_permissions.ban_members:
            if user is None:
                e = await ctx.send(embed=lib.Editable("Oops!", "You forgot something!\n\n!ban @user\n!ban @user (reason)\n\nBans mentioned user from the server, with or without a reason.", "Ban Usage"))
                await lib.erase(ctx, 20, e)
            else:
                try:
                    server = ctx.guild.name
                    author = ctx.author
                    reason = ""
                    for word in args:
                        reason += word
                        reason += " "
                    if reason == "":
                        await user.send(embed=lib.Editable("You were banned", f"You were banned from **{server}** by **{author}**", "Moderation"))
                        s = await ctx.send(embed=lib.Editable("Success!", f"User has been banned by **{author.name}**", "Moderation"))
                        await ctx.guild.ban(user)
                        await lib.erase(ctx, 20, s)
                    else:
                        await user.send(embed=lib.Editable("You were banned", f"You were banned from **{server}** by **{author}** for **{reason}**", "Moderation"))
                        s1 = await ctx.send(embed=lib.Editable("Success!", f"User has been banned by **{author.name}** for **{reason}**", "Moderation"))
                        await ctx.guild.ban(user)
                        await lib.erase(ctx, 20, s1)
                except Exception as error:
                        ex = await self.bot.say(f"**{user}** cannot be banned. {error}")
                        await lib.erase(ctx, 20, ex)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.erase(ctx, 20, p)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hackban(self, ctx, user_id: int=None, *, reason: str = None):
        if ctx.author.guild_permissions.ban_members:
            author = ctx.author
            server = author.guild
            avatar = ctx.author.avatar_url
            if user_id is None:
                e = await ctx.send(embed=lib.Editable("Oops!", "You forgot something!\n\n!hackban {userid} {reason}\n\nBans the UserID, with or without a reason.", "Hackban Usage"))
                await lib.erase(ctx, 20, e)
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
                    e1 = await ctx.send(embed=lib.Editable("Error!", "Cant find anyone with that ID try again!", "Moderation"))
                    await lib.erase(ctx, 20, e1)
                else:
                    if reason is None:
                        user = await self.bot.fetch_user(user_id)
                        y = await ctx.send(embed=lib.AvatarEdit("{}".format(author) + " Just yeeted someone!", f"{avatar}", "Yeet!", f"UserID **{user_id}** just got hackbanned!", "Moderation"))
                        await user.send(embed=lib.Editable("You were hackbanned!", f"You got hack banned from **{server}**", "Moderation"))
                        await lib.erase(ctx, 20, y)
                    else:
                        user = await self.bot.fetch_user(user_id)
                        y1 = await ctx.send(embed=lib.AvatarEdit(f"{author} Just yeeted someone!", "{avatar}".format(avatar), "Yeet!", f"UserID **{user_id}** just got hackbanned for **{reason}**!", "Moderation"))
                        await user.send(embed=lib.Editable("You were hackbanned!", f"You got hack banned from **{server}** for **{reason}**", "Moderation"))
                        await lib.erase(ctx, 20, y1)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.erase(ctx, 20, p)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def punish(self, ctx, member: discord.Member=None, *args):
        if ctx.author.guild_permissions.manage_roles:
            if member is None:
                u = await ctx.send(embed=lib.Editable("Punish Usage", "!punish {@user}\n!unpunish {@user}\n!lspunish - Lists all punished users\n!spp - **Warning** Use this command only, if there are channels which do not have the permissions for the punished role.\n\n Mutes or unmutes mentioned user from all channels on the server.", "Moderation"))
                await lib.erase(ctx, 20, u)
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
                    await lib.erase(ctx, 20, d)
                else:
                    if role in member.roles:
                        e1 = await ctx.send(embed=lib.Editable("Error!", f"**{member.name}** is already punished!", "Error"))
                        await lib.erase(ctx, 20, e1)
                    else:
                        reason = ""
                        for word in args:
                            reason += word
                            reason += " "
                        if reason == "":
                            await member.send(embed=lib.Editable("Punished!", f"You were punished from **{server}** by **{author}**", "Moderation"))
                            s = await ctx.send(embed=lib.Editable("Success!", f"**{member.name}** has been punished by **{author}**", "Moderation"))
                            await member.add_roles(role)
                            await lib.erase(ctx, 20, s)
                        else:
                            await member.send(embed=lib.Editable("Punished!", f"You were punished from **{server}** by **{author}** for **{reason}**", "Moderation"))
                            s1 = await ctx.send(embed=lib.Editable("Success!", f"**{member.name}** has been punished by **{author}** for **{reason}**", "Moderation"))
                            await member.add_roles(role)
                            await lib.erase(ctx, 20, s1)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.erase(ctx, 20, p)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unpunish(self, ctx, member: discord.Member=None):
        if ctx.author.guild_permissions.manage_roles:
            if member is None:
                u = await ctx.send(embed=lib.Editable("Oops!", "You forgot something!\n\n!unpunish {@user}\n\nUnmutes mentioned user.", "Punish Usage"))
                await lib.erase(ctx, 20, u)
            else:
                server = ctx.guild.name
                author = ctx.author.name
                role = discord.utils.get(member.guild.roles, name="punished")
                if not role in member.roles:
                    e = await ctx.send(embed=lib.Editable("Error!", f"**{member.name}** is not punished", "Error"))
                    await lib.erase(ctx, 20, e)
                else:
                    await member.send(embed=lib.Editable("Unpunished!", f"You were unpunished from {server} by {author}", "Moderation"))
                    s = await ctx.send(embed=lib.Editable("Success!", f"**{member.name}** unpunished by {author}", "Moderation"))
                    await member.remove_roles(role)
                    await lib.erase(ctx, 20, s)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.erase(ctx, 20, p)

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
            await lib.erase(ctx, 20, p)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rename(self, ctx, member:discord.Member=None, *args):
        if ctx.author.guild_permissions.manage_nicknames:
            try:
                if member is None:
                    e = await ctx.send(embed=lib.Editable("Oops!", "You forgot something!\n\n!rename user {name}\n\nRenames the mentioned user to a specified nickname.", "Rename Usage"))
                    await lib.erase(ctx, 20, e)
                else:
                    author = ctx.author.name
                    name = ""
                    for word in args:
                        name += word
                        name += " "
                    if name is "":
                        e1 = await ctx.send(embed=lib.Editable("Oops!", "You forgot something!\n\n!rename user {name}\n\nRenames the mentioned user to a specified nickname", "Rename Usage"))
                        await lib.erase(ctx, 20, e1)
                    else:
                        await ctx.send(embed=lib.Editable("Success!", f"**{member.name}** has been renamed by **{author}** to **{name}**", "Moderation"))
                        await member.edit(nick=name)
            except Exception as error:
                ex = await ctx.send(f"Uh oh.. I could not rename **{user}**")
                await lib.erase(ctx, 20, ex)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.erase(ctx, 20, p)

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
            await lib.erase(ctx, 20, p)

    @commands.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cleanup(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            u = await ctx.send(embed=lib.Editable("Cleanup Usage", "**after {id}** - Deletes messages after a specified message.\n**messages {amount}** - Deletes X amount of messages\n**user {name} {amount}** - Delete X amount of messages from a specific user\n**bot {amount}** - Delete X amount of command messages and bot messages", "Roles"))
            await lib.erase(ctx, 20, u)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.erase(ctx, 20, p)

    @cleanup.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def after(self, ctx, id=None):
        if ctx.author.guild_permissions.manage_messages:
            channel = ctx.channel
            author = ctx.author
            server = channel.guild
            if id is None:
                e = await ctx.send(embed=lib.Editable("Oops!", "You forgot something!\n\n!cleanup after {message_id}\n\nDeletes all messages after a specified message ID.", "Cleanup After Usage"))
                await lib.erase(ctx, 20, e)
            else:
                to_delete = [ctx.message]
                after = await channel.fetch_message(id)
                async for message in channel.history(limit=100, after=after):
                    to_delete.append(message)
                await channel.delete_messages(to_delete)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.erase(ctx, 20, p)

    @cleanup.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def messages(self, ctx, num:int=None):
        if ctx.author.guild_permissions.manage_messages:
            if num is None:
                e = await ctx.send(embed=lib.Editable("Oops!", "You forgot something!\n\n!cleanup messages {amount}\n\nDeletes the specified number of messages.", "Cleanup Messages Usage"))
                await lib.erase(ctx, 20, e)
            else:
                 await ctx.channel.purge(limit=num + 1)
                 s = await ctx.send(embed=lib.Editable("Success", f"{num} messages were deleted!", "Moderation"))
                 await lib.erase(ctx, 20, s)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.erase(ctx, 20, p)

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
                e1 = await ctx.send(embed=lib.Editable("Oops!", "You forgot something!\n\n!cleanup user {@user} {amount}\n\nDeletes the a specified number of messages for a specified user.", "Cleanup User Usage"))
                await lib.erase(ctx, 20, e1)
            else:
                if number is None:
                    e1 = await ctx.send(embed=lib.Editable("Oops!", "You forgot something!\n\n!cleanup user {@user} {amount}\n\nDeletes the a specified number of messages for a specified user.", "Cleanup User Usage"))
                    await lib.erase(ctx, 20, e2)
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


def setup(bot):
    bot.add_cog(Mod(bot))
