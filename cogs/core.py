import discord
from discord.ext import commands
import datetime
import time
import asyncio
import json
import aiohttp
from cogs.tools import tools

start_time = time.time()

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        await ctx.send('Pong')

    @commands.command(pass_context=True, no_pm=True)
    async def help(self, ctx):
        await ctx.message.delete()
        author = ctx.message.author
        #await author.send(embed=tools.Editable('Help','**Core**\n`ping` - Returns Pong!\n`help` - Sends a list of commands\n`bug` - Gives usage details.\n\n**Information**\n`sinfo` - Displays guild information.\n`uinfo` - Displays user information\n`uptime` - Displays the bots uptime\n`about` - Displays stuff about the bot\n`changelog` - Displays the entire bots changelog\n\n**Fun**\n`coinflip` - Flip a coin\n`space` - Get live information about the ISS\n`colour` - Get a random colour\n\n**Music**\n`play` - Plays the song\n`pause` - Pauses the song\n`resume` - Resumes the song\n`stop` - Stops the song\n`skip` - Skips the song\n\n\n**Moderation**\n`kick` - Kick a mentioned user\n`ban` - Ban a mentioned user\n`punish` - Gives mute options\n`purge` - Option to purge a channel.\n\n\n**Useful**\n`say` - Speak as the bot\n`rename` - Change a users nickname\n`invite` - Gives usage details\n`embed` - Creates an embed message\n`role` - Gives usage details\n\n\n**Admin**\n`leave` - Makes the bot leave the guild\n\n**Owner**\n`setpresence(sp)` - Change the playing status of the bot.\n`shutdown` - Shutdown the bot\n`cog` - Displays list of Cog Options\n`todo` - Displays List of shit todo\n\n\n **Music is currently not working as it needs recoded. Check the changelog!**', 'Help'))
        embed = discord.Embed(
            title = "Help",
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        embed.set_author(name="Devolution", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        embed.set_footer(text="Devolution | Help", icon_url="https://i.imgur.com/BS6YRcT.jpg")
        embed.add_field(name="Information", value="**Help** - Gives help!\n**Bug** - Use it to report bugs.\n**sinfo** - Displays guild information.\n**uinfo** - Displays user information\n**uptime** - Displays the bots uptime\n**about** - Displays stuff about the bot\n**changelog** - Displays the entire bots changelog", inline=False)
        embed.add_field(name="Fun", value="**coinflip** - Flip a coin\n**space** - Get live information about the ISS\n**colour** - Get a random colour", inline=False)
        embed.add_field(name="Moderation", value="**kick** - Kick a mentioned user\n**ban** - Ban a mentioned user\n**punish** - Gives mute options\n**purge(prune)** - Option to purge a channel.", inline=False)
        embed.add_field(name="Useful", value="**say** - Speak as the bot\n**rename** - Change a users nickname\n**invite** - Gives usage details\n**embed** - Creates an embed message\n**role** - Gives role options", inline=False)
        embed.add_field(name="Admin", value="**leave** - Makes the bot leave the guild", inline=False)
        embed.add_field(name="Owner", value="**setpresence(sp)** - Change the playing status of the bot.\n**shutdown** - Sends the bot into a deep sleep ...\n**cog** - Displays list of Cog Options\n**todo** - Displays List of shit todo\n\n\n **Music is currently not working as it needs recoded. Check the changelog!**", inline=False)
        await author.send(embed=embed)

    @commands.command(pass_context=True, no_pm=True)
    async def debug(self, ctx):
        help1 = await ctx.send(embed=tools.Editable('Help','Page 1 - Core\nPage 2 - Information\nPage 3 - Fun\nPage 4 - Music\nPage 5 - Moderation\n Page 6 - Useful\n Page 7 - Admin\n Page 8 - Owner', 'Help'))
        await help1.add_reaction('1\N{combining enclosing keycap}')
        await help1.add_reaction('2\N{combining enclosing keycap}')
        await help1.add_reaction('3\N{combining enclosing keycap}')
        await help1.add_reaction('4\N{combining enclosing keycap}')
        await help1.add_reaction('5\N{combining enclosing keycap}')
        await help1.add_reaction('6\N{combining enclosing keycap}')
        await help1.add_reaction('7\N{combining enclosing keycap}')
        await help1.add_reaction('8\N{combining enclosing keycap}')

    @commands.command(pass_context=True, no_pm=True)
    async def uptime(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(
            colour = 0x9bf442,
            timestamp=datetime.datetime.utcnow()
            )
        embed.add_field(name="Uptime", value=text)
        embed.set_author(name='Devolution', icon_url='https://i.imgur.com/BS6YRcT.jpg')
        embed.set_footer(icon_url='https://i.imgur.com/BS6YRcT.jpg', text='Devolution | Core')
        await ctx.send(embed=embed)

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
    bot.add_cog(Core(bot))
    print('Core has successfully been loaded')
