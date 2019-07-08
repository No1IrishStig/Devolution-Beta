import datetime
import discord
import asyncio
import json

from utils import default
from utils.default import lib
from discord.ext import commands

inv_settings = {"embed": False, "Channel": None, "edit": False, "delete": False, "user": False, "join": False, "leave": False, "server": False}

class Logs(commands.Cog):
    def __init__(self, bot):
            self.bot = bot
            with open("./data/logs/settings.json") as f:
                self.logs = json.load(f)
                with open("./utils/essentials/deltimer.json") as f:
                    self.deltimer = json.load(f)

    @commands.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def logs(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            db = self.logs
            guild = ctx.guild
            gid = str(guild.id)
            await ctx.send(embed=lib.Editable("Logs - Usage", "!logs set {channel}\n!logs toggle\n\n Enable logs for this server.", "Logs"))
            if not gid in db:
                print(type(self.logs))
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
            await ctx.send(embed=lib.Editable("Logs - Usage", "!logs set channel\n!logs toggle\n\n Enable logs for this server.", "Logs"))
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
                await ctx.send(embed=lib.Editable("Uh oh", "To set the logs channel you first need to enable them!\nTry this command:\n\n!logs enable", "Logs"))
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

    #toggles

    @toggle.group(invoke_without_command=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def delete(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
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
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @toggle.group(invoke_without_command=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def edit(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
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
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @toggle.group(invoke_without_command=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def user(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
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
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @toggle.group(invoke_without_command=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def join(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
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
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @toggle.group(invoke_without_command=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def leave(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
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
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @toggle.group(invoke_without_command=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def server(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
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
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    #events

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


def setup(bot):
    bot.add_cog(Logs(bot))
