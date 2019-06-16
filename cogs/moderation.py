import discord
import datetime
import asyncio
from discord.ext import commands
from cogs.tools import tools

class Mod(commands.Cog):
    def __init__(self, bot):
            self.bot = bot

    @commands.command(pass_context=True, no_pm=True, aliases=['prune'])
    async def purge(self, ctx, amount:int=None):
            if not ctx.message.author.guild_permissions.manage_messages:
                await self.bot.say(embed=tools.NoPerm())
            else:
                if amount is None:
                    msg2 = await ctx.send(embed=tools.Editable('Error!', 'Please enter an amount of messages to delete!', 'Moderation'))
                    await asyncio.sleep(30)
                    await msg2.delete()
                else:
                     deleted = await ctx.channel.purge(limit=amount)
                     msg = await ctx.send(embed=tools.Editable('Success', f'{len(deleted)} Messages were deleted!', 'Moderation'))
                     await asyncio.sleep(30)
                     await msg.delete()

    @commands.command(pass_context=True, no_pm=True)
    async def say(self, ctx, *args):
        if not ctx.message.author.guild_permissions.manage_messages:
            await ctx.message.delete()
            msg2 = await ctx.send(embed=tools.NoPerm())
            await asyncio.sleep(30)
            await msg.delete()
        else:
            await ctx.message.delete()
            output = ''
            for word in args:
                output += word
                output += ' '
            if output is ' ':
                msg = await ctx.send(embed=tools.Editable('Error!', 'Please enter a message to send!', 'Moderation'))
                await asyncio.sleep(30)
                await msg.delete()
            else:
                await ctx.send(output)

    @commands.command(pass_context=True, no_pm=True)
    async def kick(self, ctx, user : discord.User=None, *args):
        if not ctx.message.author.guild_permissions.kick_members:
            msg = await self.bot.say(embed=tools.NoPerm())
            await asyncio.sleep(30)
            await msg.delete()
        else:
            if user is None:
                msg2 = await ctx.send(embed=tools.Editable('Kick - Usage', '!kick @user\n !kick @user (reason)\n\n Kicks a user from the server, with or without a reason.', 'Moderation'))
                await asyncio.sleep(30)
                await msg2.delete()
            else:
                try:
                    server = ctx.message.author.guild.name
                    author = ctx.message.author.mention
                    reason = ''
                    for word in args:
                        reason += word
                        reason += ' '
                    if reason == '':
                        await user.send(embed=tools.Editable('You were kicked', 'You were kicked from {} by {}'.format(server, author), 'Moderation'))
                        await ctx.send(embed=tools.Editable('Success!', 'User has been kicked by {}'.format(author), 'Moderation'))
                        await ctx.guild.kick(user)
                    else:
                        await user.send(embed=tools.Editable('You were kicked', 'You were kicked from {} by {} for {}'.format(server, author, reason), 'Moderation'))
                        await ctx.send(embed=tools.Editable('Success!', 'User has been kicked by {} for {}'.format(author, reason), 'Moderation'))
                except Exception as error:
                        await ctx.send('{} cannot be kicked.'.format(user))

    @commands.command(pass_context=True, no_pm=True)
    async def ban(self, ctx, user : discord.User=None, *args):
        if not ctx.message.author.guild_permissions.ban_members:
            msg = await ctx.send(embed=tools.NoPerm())
            await asyncio.sleep(30)
            await msg.delete()
        else:
            if user is None:
                msg2 = await ctx.send(embed=tools.Editable('Ban - Usage', '!ban @user\n !ban @user (reason)\n\n Bans a user from the server, with or without a reason.', 'Moderation'))
                await asyncio.sleep(30)
                await msg2.delete()
            else:
                try:
                    server = ctx.message.author.guild.name
                    author = ctx.message.author.mention
                    reason = ''
                    for word in args:
                        reason += word
                        reason += ' '
                    if reason == '':
                        await user.send(embed=tools.Editable('You were banned', 'You were banned from {} by {}'.format(server, author), 'Moderation'))
                        await ctx.send(embed=tools.Editable('Success!', 'User has been banned by {}'.format(author), 'Moderation'))
                        await ctx.guild.ban(user)
                    else:
                        await user.send(embed=tools.Editable('You were banned', 'You were banned from {} by {} for {}'.format(server, author, reason), 'Moderation'))
                        await ctx.send(embed=tools.Editable('Success!', 'User has been banned by {} for {}'.format(author, reason), 'Moderation'))
                        await ctx.guild.ban(user)
                except Exception as error:
                        await self.bot.say('{} cannot be banned. [{}]'.format(user, error))

    @commands.command(pass_context=True, no_pm=True)
    async def punish(self, ctx, member: discord.Member=None, *args):
        if not ctx.message.author.guild_permissions.manage_roles:
            msg = await ctx.send(embed=tools.NoPerm())
            await asyncio.sleep(30)
            await msg.delete()
        else:
            if member is None:
                msg2 = await ctx.send(embed=tools.Editable('Punish - Usage', '!punish @user\n!unpunish @user\n!lspunish - Lists all punished users\n!spp - **Warning** Use this command only, if there are channels which do not have the permissions for the punished role.\n\n Mutes or unmutes users from all channels on the server.', 'Moderation'))
                await asyncio.sleep(30)
                await mg2.delete()
            else:
                server = ctx.message.author.guild.name
                author = ctx.message.author.mention
                role = discord.utils.get(member.guild.roles, name='punished')
                if role is None:
                    channel = ctx.message.channel
                    await ctx.send(embed=tools.Editable('Error!', 'Punished role not found! Creating...', 'Error'))
                    await ctx.guild.create_role(name='punished'),
                    await asyncio.sleep(5)
                    await ctx.send(embed=tools.Editable('Working...', 'Settings Permissions...', 'Moderation'))
                    for channel in ctx.message.guild.channels:
                        role = discord.utils.get(channel.guild.roles, name='punished')
                        overwrite = discord.PermissionOverwrite()
                        overwrite.send_messages = False
                        overwrite.send_tts_messages = False
                        overwrite.add_reactions = False
                        await role.channel.set_permissions(overwrite),
                        await asyncio.sleep(5)
                    await ctx.send(embed=tools.Editable('Done!', 'The role has been created and the permissions set! Now Retry the command.', 'Moderation'))
                else:
                    if role in member.roles:
                        msg3 = await ctx.send(embed=tools.Editable('Error!', 'User already punished!', 'Error'))
                        await asyncio.sleep(30)
                        await msg3.delete()
                    else:
                        #try:
                        reason = ''
                        for word in args:
                            reason += word
                            reason += ' '
                        if reason == '':
                            await member.send(embed=tools.Editable('Punished!', 'You were punished from {} by {}'.format(server, author, reason), 'Moderation'))
                            await ctx.send(embed=tools.Editable('Success!', 'User has been punished by {}'.format(author), 'Moderation'))
                            await member.add_roles(role)
                        else:
                            await member.send(embed=tools.Editable('Punished!', 'You were punished from {} by {} for {}'.format(server, author, reason), 'Moderation'))
                            await ctx.send(embed=tools.Editable('Success!', 'User has been punished by {} for {}'.format(author, reason), 'Moderation'))
                            await member.add_roles(role)
                        #except Exception as error:
                                #await ctx.send(embed=tools.Editable('Error!', '{} could not be punished!'.format(member), 'Error'))

    @commands.command(pass_context=True, no_pm=True)
    async def unpunish(self, ctx, member: discord.Member=None):
        if not ctx.message.author.guild_permissions.manage_roles:
            msg = await ctx.send(embed=tools.NoPerm())
            await asyncio.sleep(30)
            await msg.delete()
        else:
            if member is None:
                msg2 = await ctx.send(embed=tools.Editable('Punish - Usage', '!punish @user\n!unpunish @user\n!lspunish - Lists all punished users\n!spp - **Warning** Use this command only, if there are channels which do not have the permissions for the punished role.\n\n Mutes or unmutes users from all channels on the server.', 'Moderation'))
                await asyncio.sleep(30)
                await msg2.delete()
            else:
                server = ctx.message.author.guild.name
                author = ctx.message.author.mention
                role = discord.utils.get(member.guild.roles, name='punished')
                if member is None:
                    msg2 = await ctx.send(embed=tools.Editable('Punish - Usage', '!punish @user\n!unpunish @user\n!lspunish - Lists all punished users\n!spp - **Warning** Use this command only, if there are channels which do not have the permissions for the punished role.\n\n Mutes or unmutes users from all channels on the server.', 'Moderation'))
                    await asyncio.sleep(30)
                    await msg2.delete()
                else:
                    if not role in member.roles:
                        msg3 = await ctx.send(embed=tools.Editable('Error!', 'User is not punished', 'Error'))
                        await asyncio.sleep(30)
                        await msg3.delete(msg3)
                    else:
                        await member.send(embed=tools.Editable('Unpunished!', 'You were unpunished from {} by {}'.format(server, author), 'Moderation'))
                        await ctx.send(embed=tools.Editable('Success!', 'User unpunished by {}'.format(author), 'Moderation'))
                        await member.remove_roles(role)

    @commands.command(pass_context=True, no_pm=True)
    async def lspunish(self, ctx):
        pusers = []
        if not ctx.message.author.guild_permissions.manage_roles:
            msg = await ctx.send(embed=tools.NoPerm())
            await asyncio.sleep(30)
            await msg.delete()
        else:
            role = discord.utils.get(ctx.message.guild.roles, name="punished")
            for member in ctx.message.guild.members:
                if role in member.roles:
                        pusers.append(member.name)
        await asyncio.sleep(2)
        await ctx.send(embed=tools.Editable('Punished List', '{}'.format(', '.join(pusers)), 'Moderation'))

    @commands.command(pass_context=True, no_pm=True)
    async def rename(self, ctx, user:discord.User=None, *args):
        if not ctx.message.author.guild_permissions.manage_nicknames:
            msg = await ctx.send(embed=tools.NoPerm())
            await asyncio.sleep(30)
            await msg.delete()
        else:
            try:
                author = ctx.message.author.mention
                name = ''
                for word in args:
                    name += word
                    name += ' '
                if name is '':
                    msg2 = await ctx.send(embed=tools.Editable('Error!', 'Enter a nickname!', 'Error'))
                    await asyncio.sleep(30)
                    await msg.delete()
                else:
                    await ctx.send(embed=tools.Editable('Success!', 'User has been renamed by {} to "{}"'.format(author, name), 'Moderation'))
                    await user.edit(nick=name)
            except Exception as error:
                    await self.bot.say('{} cannot be renamed.'.format(user))

    @commands.command(pass_context=True, no_pm=True)
    async def spp(self, ctx):
        for channel in ctx.message.guild.channels:
            role = discord.utils.get(channel.guild.roles, name='punished')
            overwrite = discord.PermissionOverwrite()
            overwrite.send_messages = False
            overwrite.send_tts_messages = False
            overwrite.add_reactions = False
            await channel.set_permissions(role, overwrite=overwrite),
        msg = await ctx.send(embed=tools.Editable('Setting Permissions', 'This may take a while, Ill tell you when im done.', 'Moderation'))
        await asyncio.sleep(5)
        await msg.delete()
        msg2 = await ctx.send(embed=tools.Editable('Im Finished!', 'Depending on how many channels you have, all permissions should be set.', 'Moderation'))
        await asyncio.sleep(5)
        await msg2.delete()

def setup(bot):
    bot.add_cog(Mod(bot))
    print('Mod has been loaded')
