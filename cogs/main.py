import discord
import datetime
import json
import asyncio
import random
import aiohttp
from random import choice as randchoice
from discord.ext import commands
from cogs.tools import tools

class Main(commands.Cog):
    def __init__(self, bot):
            self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
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
            title = 'Server Information for ' + name,
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        embed.add_field(name='Creation Date', value=created.strftime('%d/%m/%Y at %H:%M:%S (GMT)'), inline=False)
        embed.add_field(name='Owner', value=owner, inline=True)
        embed.add_field(name='Region', value=region, inline=True)
        embed.add_field(name='Roles', value=len(roles), inline=True)
        embed.add_field(name='Users', value=members, inline=True)
        embed.add_field(name='Channels', value=len(channels), inline=True)
        embed.add_field(name='AFK Channel', value=afk, inline=True)
        embed.set_author(name='Devolution                                                                              ID: {}'.format(id), icon_url='https://i.imgur.com/BS6YRcT.jpg', )
        embed.set_footer(icon_url='https://i.imgur.com/BS6YRcT.jpg', text='Devolution | Info')
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, no_pm=True)
    async def uinfo(self, ctx, user:discord.User=None):
        if user is None:
            name = ctx.message.author.name
            id = ctx.message.author.id
            avatar = ctx.message.author.avatar_url
            joined = ctx.message.author.joined_at
            created = ctx.message.author.created_at
            status = ctx.message.author.status
            playing = ctx.message.author.activity
            roles = ctx.message.author.roles
            display = ctx.message.author.nick
            embed = discord.Embed(
                title = 'User Information',
                colour = 0x9bf442,
                timestamp=datetime.datetime.utcnow()
                )
            embed.add_field(name='Status', value=status, inline=True)
            embed.add_field(name='Playing', value=playing, inline=True)
            embed.add_field(name='Nickname', value=display, inline=True)
            embed.add_field(name='Role Count', value=len(roles), inline=True)
            embed.add_field(name='Account Creation', value=created.strftime('Since %d/%m/%Y'), inline=True)
            embed.add_field(name='Joined guild', value=joined.strftime('Since %d/%m/%Y'), inline=True)
            embed.set_author(name=name + 's User Information', icon_url=avatar)
            embed.set_footer(icon_url='https://i.imgur.com/BS6YRcT.jpg', text='Devolution | Info')
            await ctx.send(embed=embed)
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
                    title = 'User Information',
                    colour = 0x9bf442,
                    timestamp=datetime.datetime.utcnow()
                    )
                embed.add_field(name='Status', value=status, inline=True)
                embed.add_field(name='Playing', value=playing, inline=True)
                embed.add_field(name='Nickname', value=display, inline=True)
                embed.add_field(name='Role Count', value=len(roles), inline=True)
                embed.add_field(name='Account Creation', value=created.strftime('Since %d/%m/%Y'), inline=True)
                embed.add_field(name='Joined guild', value=joined.strftime('Since %d/%m/%Y'), inline=True)
                embed.set_author(name=name + 's User Information', icon_url=avatar)
                embed.set_footer(icon_url='https://i.imgur.com/BS6YRcT.jpg', text='Devolution | Info')
                await ctx.send(embed=embed)

    @commands.command(pass_context=True, no_pm=True)
    async def avatar(self, ctx, user:discord.User=None):
        if ctx.message.author.id == int('439327545557778433'):
            if user is None:
                sname = ctx.message.author.name
                savatar = str(ctx.message.author.avatar_url)
                embed = discord.Embed(
                    title = 'Avatar Stealer',
                    description = savatar,
                    colour = 0x9bf442,
                    timestamp=datetime.datetime.utcnow()
                    )
                embed.set_image(url=savatar)
                embed.set_thumbnail(url=savatar)
                embed.set_author(name=sname, icon_url=savatar)
                embed.set_footer(icon_url='https://i.imgur.com/BS6YRcT.jpg', text='Devolution | Info')
                await ctx.send(embed=embed)
            else:
                for user in ctx.message.mentions:
                    avatar = str(user.avatar_url)
                    name = user.name
                    embed = discord.Embed(
                        title = 'Avatar Stealer',
                        description = avatar,
                        colour = 0x9bf442,
                        timestamp=datetime.datetime.utcnow()
                        )
                    embed.set_image(url=avatar)
                    embed.set_thumbnail(url=avatar)
                    embed.set_author(name=name, icon_url=avatar)
                    embed.set_footer(icon_url='https://i.imgur.com/BS6YRcT.jpg', text='Devolution | Info')
                    await ctx.send(embed=embed)
        else:
            await ctx.send(embed=tools.NoPerm())

    @commands.command(pass_context=True, no_pm=True)
    async def embed(self, ctx):
        if ctx.message.author.guild_permissions.manage_messages:
            await ctx.message.delete()
            ques = await ctx.send('What title?')
            msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout = 120)
            ques1 = await ctx.send('What would you like to say?')
            title = msg.content
            msg1 = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout = 120)
            ques2 = await ctx.send('Ok.. What footer text?')
            desc = msg1.content
            msgg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout = 120)
            ans = await ctx.send('Generating Embed...')
            footer = msgg.content
            await asyncio.sleep(2)
            await ctx.send(embed=tools.Editable(title, desc, footer))
            await ques.delete()
            await msg.delete()
            await ques1.delete()
            await msg1.delete()
            await ques2.delete()
            await msgg.delete()
            await ans.delete()
        else:
            await ctx.send(embed=tools.NoPerm())

    @commands.group(pass_context=True, invoke_without_command=True)
    async def role(self, ctx):
        if not ctx.message.author.guild_permissions.manage_roles:
            error = await ctx.send(embed=tools.NoPerm())
            await asyncio.sleep(30)
            await ctx.message.delete()
            await error.delete()
        else:
            usage = await ctx.send(embed=tools.Editable('Role Usage', '**Add** - Adds a user to a role.\n **List** - List all roles in the server\n **Remove** - Removes a user from a role\n **Create** - Creates a role\n **Delete** - Deletes a role\n **Edit** - **Warning** This will ask to edit every part of the role, including colour.', 'Roles'))
            await asyncio.sleep(30)
            await ctx.message.delete()
            await usage.delete()

    @role.group(pass_context=True, invoke_without_command=True)
    async def list(self, ctx):
        if not ctx.message.author.guild_permissions.manage_roles:
            await ctx.send(embed=tools.NoPerm())
        else:
            roles = []
            for role in ctx.guild.roles:
                roles.append(role.name)
            roles.remove('@everyone')
            await ctx.send(embed=tools.Editable('Role List', '{}'.format(', '.join(roles)), 'Roles'))

    @role.group(pass_context=True, invoke_without_command=True)
    async def add(self, ctx, rolename=None, member: discord.Member=None):
        if not ctx.message.author.guild_permissions.manage_roles:
            await ctx.send(embed=tools.NoPerm())
        else:
            if rolename is None:
                usage = await ctx.send(embed=tools.Editable('Role Add Usage', 'You forgot something!\n\n!role add {role} {@user}\n\n This will add the role to the user.', 'Roles'))
                await asyncio.sleep(30)
                await ctx.message.delete()
                await usage.delete()
            else:
                if member is None:
                    usage1 = await ctx.send(embed=tools.Editable('Role Add Usage', 'You forgot to mention a user!\n\n!role add {role} {@user}\n\n This will add the role to the user.', 'Roles'))
                    await asyncio.sleep(30)
                    await ctx.message.delete()
                    await usage1.delete()
                else:
                    role = discord.utils.get(ctx.message.guild.roles, name=rolename)
                    if role in member.roles:
                        error = await ctx.send(embed=tools.Editable('Error', '{} already has the role {}'.format(member, role), 'Roles'))
                        await asyncio.sleep(30)
                        await ctx.message.delete()
                        await error.delete()
                    else:
                        await member.add_roles(role)
                        done = await ctx.send(embed=tools.Editable('Role Added', '{} added to {}'.format(role, member), 'Roles'))
                        await asyncio.sleep(30)
                        await ctx.message.delete()
                        await done.delete()

    @role.group(pass_context=True, invoke_without_command=True)
    async def remove(self, ctx, rolename=None, member: discord.Member=None):
        if not ctx.message.author.guild_permissions.manage_roles:
            await ctx.send(embed=tools.NoPerm())
        else:
            if rolename is None:
                usage1 = await ctx.send(embed=tools.Editable('Role Remove Usage', 'You forgot something!\n\n!role remove {role} {@user}\n\n This will remove the role from the user.', 'Roles'))
                await asyncio.sleep(30)
                await ctx.message.delete()
                await usage1.delete()
            else:
                if member is None:
                    usage = await ctx.send(embed=tools.Editable('Role Remove Usage', 'You forgot to mention a user!\n\n!role remove {role} {@user}\n\n This will remove the role from the user.', 'Roles'))
                    await asyncio.sleep(30)
                    await ctx.message.delete()
                    await usage.delete()
                else:
                    role = discord.utils.get(ctx.message.guild.roles, name=rolename)
                    if role in member.roles:
                        await member.remove_roles(role)
                        done = await ctx.send(embed=tools.Editable('Role Removed', '{} removed from {}'.format(role, member), 'Roles'))
                        await asyncio.sleep(30)
                        await ctx.message.delete()
                        await done.delete()
                    else:
                        error = await ctx.send(embed=tools.Editable('Error', '{} doesnt have the role {}'.format(member, role), 'Roles'))
                        await asyncio.sleep(30)
                        await ctx.message.delete()
                        await error.delete()

    @role.group(pass_context=True, invoke_without_command=True)
    async def create(self, ctx, rolename=None):
        if not ctx.message.author.guild_permissions.manage_roles:
            await ctx.send(embed=tools.NoPerm())
        else:
            if rolename is None:
                usage = await ctx.send(embed=tools.Editable('Role Create Usage', 'You forgot something!\n\n!role create {role}\n\n This will create a role with the specified name.', 'Roles'))
                await asyncio.sleep(30)
                await ctx.message.delete()
                await usage.delete()
            else:
                role = discord.utils.get(ctx.message.guild.roles, name=rolename)
                if role in ctx.message.guild.roles:
                    error = await ctx.send(embed=tools.Editable('Error', 'The role {} already exists!'.format(rolename), 'Roles'))
                    await asyncio.sleep(30)
                    await ctx.message.delete()
                    await error.delete()
                else:
                    await ctx.guild.create_role(name=rolename)
                    done = await ctx.send(embed=tools.Editable('Role Created', 'The role {} has been created!'.format(rolename), 'Roles'))
                    await asyncio.sleep(30)
                    await ctx.message.delete()
                    await done.delete()

    @role.group(pass_context=True, invoke_without_command=True)
    async def delete(self, ctx, rolename=None):
        if not ctx.message.author.guild_permissions.manage_roles:
            await ctx.send(embed=tools.NoPerm())
        else:
            if rolename is None:
                usage = await ctx.send(embed=tools.Editable('Role delete Usage', 'You forgot something!\n\n!role delete {role}\n\n This will delete the role with the specified name.', 'Roles'))
                await asyncio.sleep(30)
                await ctx.message.delete()
                await usage.delete()
            else:
                role = discord.utils.get(ctx.message.guild.roles, name=rolename)
                if role in ctx.message.guild.roles:
                    await role.delete()
                    done = await ctx.send(embed=tools.Editable('Role Deleted', 'The role {} has been deleted!'.format(rolename), 'Roles'))
                    await asyncio.sleep(30)
                    await ctx.message.delete()
                    await done.delete()
                else:
                    error = await ctx.send(embed=tools.Editable('Error', 'The role {} doesnt exist!'.format(rolename), 'Roles'))
                    await asyncio.sleep(30)
                    await ctx.message.delete()
                    await error.delete()

def setup(bot):
    bot.add_cog(Main(bot))
    print('Main has been loaded.')
