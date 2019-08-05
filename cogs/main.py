import datetime
import discord
import asyncio
import json

from utils.default import lib
from discord.ext import commands

class Main(commands.Cog):
    def __init__(self, bot):
            self.bot = bot
            with open("./data/admin/deltimer.json") as f:
                self.deltimer = json.load(f)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sinfo(self, ctx):
        name = ctx.message.guild.name
        id = ctx.message.guild.id
        region = ctx.message.guild.region
        members = ctx.message.guild.member_count
        created = ctx.message.guild.created_at
        owner = ctx.message.guild.owner
        roles = ctx.message.guild.roles
        channels = ctx.message.guild.channels
        afk = ctx.message.guild.afk_channel
        embed = discord.Embed(
            title = "Server Information for " + name,
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        embed.add_field(name="Creation Date", value=created.strftime("%d/%m/%Y at %H:%M:%S (GMT)"), inline=False)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Roles", value=len(roles), inline=True)
        embed.add_field(name="Users", value=members, inline=True)
        embed.add_field(name="Channels", value=len(channels), inline=True)
        embed.add_field(name="AFK Channel", value=afk, inline=True)
        embed.set_author(name=f"Devolution                                                                              ID: {id}", icon_url="https://i.imgur.com/BS6YRcT.jpg", )
        embed.set_footer(icon_url="https://i.imgur.com/BS6YRcT.jpg", text="Devolution | Info")
        e = await ctx.send(embed=embed)
        await lib.eraset(self, ctx, e)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def uinfo(self, ctx, user:discord.User=None):
        if user is None:
            name = ctx.author.name
            id = ctx.author.id
            avatar = ctx.author.avatar_url
            joined = ctx.author.joined_at
            created = ctx.author.created_at
            status = ctx.author.status
            playing = ctx.author.activity
            roles = ctx.author.roles
            display = ctx.author.nick
            embed = discord.Embed(
                title = "User Information",
                colour = 0x9bf442,
                timestamp=datetime.datetime.utcnow()
                )
            embed.add_field(name="Status", value=status, inline=True)
            embed.add_field(name="Playing", value=playing, inline=True)
            embed.add_field(name="Nickname", value=display, inline=True)
            embed.add_field(name="Role Count", value=len(roles), inline=True)
            embed.add_field(name="Account Creation", value=created.strftime("Since %d/%m/%Y"), inline=True)
            embed.add_field(name="Joined guild", value=joined.strftime("Since %d/%m/%Y"), inline=True)
            embed.set_author(name=name + "s User Information", icon_url=avatar)
            embed.set_footer(icon_url="https://i.imgur.com/BS6YRcT.jpg", text="Devolution | Info")
            e = await ctx.send(embed=embed)
            await lib.eraset(self, ctx, e)
        else:
            for user in ctx.message.mentions:
                name = user.name
                id = user.id
                avatar = user.avatar_url
                joined = user.joined_at
                created = user.created_at
                status = user.status
                playing = user.activity
                roles = user.roles
                display = user.nick
                embed = discord.Embed(
                    title = "User Information",
                    colour = 0x9bf442,
                    timestamp=datetime.datetime.utcnow()
                    )
                embed.add_field(name="Status", value=status, inline=True)
                embed.add_field(name="Playing", value=playing, inline=True)
                embed.add_field(name="Nickname", value=display, inline=True)
                embed.add_field(name="Role Count", value=len(roles), inline=True)
                embed.add_field(name="Account Creation", value=created.strftime("Since %d/%m/%Y"), inline=True)
                embed.add_field(name="Joined guild", value=joined.strftime("Since %d/%m/%Y"), inline=True)
                embed.set_author(name=name + "s User Information", icon_url=avatar)
                embed.set_footer(icon_url="https://i.imgur.com/BS6YRcT.jpg", text="Devolution | Info")
                ee = await ctx.send(embed=embed)
                await lib.eraset(self, ctx, ee)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, user:discord.User=None):
        if user is None:
            sname = ctx.author.name
            savatar = str(ctx.author.avatar_url)
            embed = discord.Embed(
                title = "Avatar Stealer",
                description = savatar,
                colour = 0x9bf442,
                timestamp=datetime.datetime.utcnow()
                )
            embed.set_image(url=savatar)
            embed.set_thumbnail(url=savatar)
            embed.set_author(name=sname, icon_url=savatar)
            embed.set_footer(icon_url="https://i.imgur.com/BS6YRcT.jpg", text="Devolution | Info")
            e = await ctx.send(embed=embed)
            await lib.eraset(self, ctx, e)
        else:
            for user in ctx.message.mentions:
                avatar = str(user.avatar_url)
                name = user.name
                embed = discord.Embed(
                    title = "Avatar Stealer",
                    description = avatar,
                    colour = 0x9bf442,
                    timestamp=datetime.datetime.utcnow()
                    )
                embed.set_image(url=avatar)
                embed.set_thumbnail(url=avatar)
                embed.set_author(name=name, icon_url=avatar)
                embed.set_footer(icon_url="https://i.imgur.com/BS6YRcT.jpg", text="Devolution | Info")
                e = await ctx.send(embed=embed)
                await lib.eraset(self, ctx, e)

    @commands.command(no_pm=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def embed(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            ques = await ctx.send("What title?")
            msg = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout = 120)
            ques1 = await ctx.send("What would you like to say?")
            title = msg.content
            msg1 = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout = 120)
            ques2 = await ctx.send("Ok.. What footer text?")
            desc = msg1.content
            msgg = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout = 120)
            ans = await ctx.send("Generating Embed...")
            footer = msgg.content
            await asyncio.sleep(2)
            r = await ctx.send(embed=lib.Editable(title, desc, footer))
            await ques.delete()
            await msg.delete()
            await ques1.delete()
            await msg1.delete()
            await ques2.delete()
            await msgg.delete()
            await ans.delete()
            await lib.eraset(self, ctx, r)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @commands.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def role(self, ctx):
        if ctx.author.guild_permissions.manage_roles:
            u = await ctx.send(embed=lib.Editable("Role Usage!", f"**{ctx.prefix}add** - Adds a user to a role.\n**{ctx.prefix}list** - List all roles in the server\n**{ctx.prefix}remove** - Removes a user from a role\n**{ctx.prefix}create** - Creates a role\n**{ctx.prefix}delete** - Deletes a role", "Role Usage"))
            await lib.eraset(self, ctx, u)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @role.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def list(self, ctx):
        if ctx.author.guild_permissions.manage_roles:
            roles = []
            for role in ctx.guild.roles:
                roles.append(role.name)
            roles.remove("@everyone")
            l = await ctx.send(embed=lib.Editable("Role List", "{}".format(", ".join(roles)), "Roles"))
            await lib.eraset(self, ctx, l)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @role.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def add(self, ctx, rolename=None, member: discord.Member=None):
        if ctx.author.guild_permissions.manage_roles:
            if rolename and member:
                role = discord.utils.get(ctx.message.guild.roles, name=rolename)
                if role in ctx.guild.roles:
                    if role in member.roles:
                        e = await ctx.send(embed=lib.Editable("Error", f"**{member.name}** already has the role **{role}**", "Roles"))
                        await lib.eraset(self, ctx, e)
                    else:
                        await member.add_roles(role)
                        d = await ctx.send(embed=lib.Editable("Role Added", f"The role **{role}** was added to **{member.name}**", "Roles"))
                        await lib.eraset(self, ctx, d)
                else:
                    e = await ctx.send(embed=lib.Editable("Error", f"The role **{rolename}** doesnt exist!", "Roles"))
                    await lib.eraset(self, ctx, e)
            else:
                u = await ctx.send(embed=lib.Editable("Oops!", f"You forgot something!\n\n{ctx.prefix}role add (role) (@user)\n\n This will add the role to the user.", "Role Usage"))
                await lib.eraset(self, ctx, u)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @role.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def remove(self, ctx, rolename=None, member: discord.Member=None):
        if ctx.author.guild_permissions.manage_roles:
            if rolename and member:
                role = discord.utils.get(ctx.message.guild.roles, name=rolename)
                if role in ctx.guild.roles:
                    if role in member.roles:
                        await member.remove_roles(role)
                        d = await ctx.send(embed=lib.Editable("Role Removed", f"The role **{role}** was removed from **{member.name}**", "Roles"))
                        await lib.eraset(self, ctx, d)
                    else:
                        e = await ctx.send(embed=lib.Editable("Error", f"**{member.name}** does not have the role **{role}**", "Roles"))
                        await lib.eraset(self, ctx, e)
                else:
                    e = await ctx.send(embed=lib.Editable("Error", f"The role **{rolename}** doesnt exist!", "Roles"))
                    await lib.eraset(self, ctx, e)
            else:
                u = await ctx.send(embed=lib.Editable("Oops!", f"You forgot something!\n\n{ctx.prefix}role remove (role) (@user)\n\n This will remove the role from the user.", "Roles"))
                await lib.eraset(self, ctx, u)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @role.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def create(self, ctx, rolename=None):
        if ctx.author.guild_permissions.manage_roles:
            if rolename:
                role = discord.utils.get(ctx.message.guild.roles, name=rolename)
                if role in ctx.message.guild.roles:
                    e = await ctx.send(embed=lib.Editable("Error", f"The role **{rolename}** already exists!", "Roles"))
                    await lib.eraset(self, ctx, e)
                else:
                    await ctx.guild.create_role(name=rolename)
                    d = await ctx.send(embed=lib.Editable("Role Created", f"The role **{rolename}** has been created!", "Roles"))
                    await lib.eraset(self, ctx, d)
            else:
                u = await ctx.send(embed=lib.Editable("Oops!", f"You forgot something!\n\n{ctx.prefix}role create (role)\n\n This will create a role with the specified name.", "Role Usage"))
                await lib.eraset(self, ctx, u)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @role.group(invoke_without_command=True, no_pm=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def delete(self, ctx, rolename=None):
        if ctx.author.guild_permissions.manage_roles:
            if rolename:
                role = discord.utils.get(ctx.message.guild.roles, name=rolename)
                if role in ctx.message.guild.roles:
                    await role.delete()
                    d = await ctx.send(embed=lib.Editable("Role Deleted", f"The role **{rolename}** has been deleted!", "Roles"))
                    await lib.eraset(self, ctx, d)
                else:
                    e = await ctx.send(embed=lib.Editable("Error", f"The role **{rolename}** doesnt exist!", "Roles"))
                    await lib.eraset(self, ctx, e)
            else:
                u = await ctx.send(embed=lib.Editable("Oops!", f"You forgot something!\n\n{ctx.prefix}role delete (role)\n\n This will delete the role with the specified name.", "Role Usage"))
                await lib.eraset(self, ctx, u)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

def setup(bot):
    bot.add_cog(Main(bot))
