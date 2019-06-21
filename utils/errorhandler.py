import discord

from discord.ext import commands
from utils.default import lib

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        ignored = (commands.CommandNotFound, commands.NoPrivateMessage, commands.DisabledCommand, discord.NotFound)
        error = getattr(error, "original", error)

        # Bot Error's
        if isinstance(error, ignored):
            return
        elif isinstance(error, commands.BadArgument):
            return await ctx.send(embed=lib.Editable("Error!", f"Oops! Please mention a user! {ctx.author.mention}", "Error"))
        elif isinstance(error, commands.MissingPermissions):
            return await ctx.send(embed=lib.Editable("Error!", "Uh oh.. I seem to be missing some permissions!", "Error"))
        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(embed=lib.Editable("Error!", f"Woah woah {ctx.author.mention} calm down, that command is currently cooling down!", "Error"))

        # Discord Error's
        elif isinstance(error, discord.Forbidden):
            return await ctx.send(embed=lib.Editable("Error!", "Uh oh.. I seem to be missing some permissions! Use `!help permissions` to see what I require!", "Error"))
        elif isinstance(error, discord.HTTPException):
            return await ctx.send(embed=lib.Editable("Error!", f"There was an error with your command! Here it is: {error}", "Error"))

        raise error

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
