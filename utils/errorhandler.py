import datetime
import discord
import asyncio

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
            return await ctx.send(embed=lib.Editable(self, "Error!", f"Oops! Invalid arguments provided! {ctx.author.mention}", "Error"))
        elif isinstance(error, commands.MissingPermissions):
            try:
                return ctx.send(embed=lib.Editable(self, "Error!", "Uh oh.. I seem to be missing some permissions!", "Error"))
            except discord.Forbidden:
                return

        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(embed=lib.Editable(self, "Error!", f"Woah woah {ctx.author.mention} calm down, that command is currently cooling down!", "Error"))

        # Discord Error's
        elif isinstance(error, discord.Forbidden):
            try:
                return await ctx.send(embed=lib.Editable(self, "Error!", "Uh oh.. I seem to be missing some permissions! Use `!help permissions` to see what I require!", "Error"))
            except discord.Forbidden:
                return
        elif isinstance(error, discord.HTTPException):
            return await ctx.send(embed=lib.Editable(self, "Error!", f"There was an error with your command! Here it is: {error}", "Error"))

        # Asyncio Error's
        elif isinstance(error, asyncio.TimeoutError):
            return await ctx.send(embed=lib.Editable(self, "Woops!", "You didnt reply, so the action timed out!", "Timed Out"))

        errorfile = open("./utils/error.log","a")
        errorfile.write("[{}]: {} \n".format(datetime.datetime.utcnow().strftime("%d/%m/%Y at %H:%M:%S (GMT)"), error))
        errorfile.close()
        print("An error has been logged.")
        #raise error

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
