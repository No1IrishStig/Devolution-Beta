import sys, traceback
import discord
import asyncio
import json
import time

from utils import default
from random import randint
from utils.default import lib
from discord.ext import commands

slot_winnings = """Slot machine winnings:
    :six: :six: :six: Bet * 6666
    :four_leaf_clover: :four_leaf_clover: :four_leaf_clover: +1000
    :cherries: :cherries: :cherries: +800
    :six: :nine: Bet * 4
    :cherries: :cherries: Bet * 3
    Three symbols: +500
    Two symbols: Bet * 2"""


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("./utils/cfg.json")
        self.benefits_register = {}
        self.slot_register = {}
        with open("./utils/essentials/economy.json") as f:
            self.bank = json.load(f)
            with open("./data/economy/settings.json") as s:
                self.settings = json.load(s)
                with open("./utils/essentials/deltimer.json") as f:
                    self.deltimer = json.load(f)

    @commands.group(invoke_without_command=True)
    async def bank(self, ctx):
        await ctx.send(embed=lib.Editable("Just do it!", "Use !bank register to create a bank account", "Devo Bank"))

    @bank.group(invoke_without_command=True)
    async def register(self, ctx):
        user = ctx.author
        UID = str(user.id)
        if UID not in self.bank:
            self.bank[UID] = {"name": user.name, "balance" : 100}
            with open("./utils/essentials/economy.json", "w") as f:
                json.dump(self.bank, f)
            await ctx.send(embed=lib.Editable("Ayy", f"Bank Account Created for {ctx.author.mention}. Current balance: {str(self.check_balance(user.id))}", "Devo Bank"))
        else:
            await ctx.send(embed=lib.Editable("Uh oh", "You're too poor to make another bank account ;)", "Devo Bank"))

    @bank.group(invoke_without_command=True)
    async def balance(self, ctx, user: discord.Member=None):
        if not user:
            user = ctx.author
            if self.account_check(user.id):
                await ctx.send(embed=lib.Editable("Monayy", f"{user.mention}, Your bank balance is {str(self.check_balance(user.id))}", "Devo Bank"))
            else:
                await ctx.send(embed=lib.Editable("Uh oh", f"{user.mention}, You dont have a bank account at the Devo Bank. Type !bank register to open one.", "Devo Bank"))
        else:
            if self.account_check(user.id):
                balance = self.check_balance(user.id)
                await ctx.send(embed=lib.Editable(f"{user.name} just flexed", f"{user.mention}'s balance is {str(balance)}", "Devo Bank"))
            else:
                await ctx.send(embed=lib.Editable("Uh oh", f"{user.name} has no bank account.", "Devo Bank"))

    @bank.group(invoke_without_command=True)
    async def transfer(self, ctx, user: discord.Member=None, amount : int=None):
        author = ctx.author
        if user is None:
            return await ctx.send(embed=lib.Editable("Uh oh", "Please mention a user to transfer to.", "Devo Bank"))
        if amount is None:
            return await ctx.send(embed=lib.Editable("Oops", "Please specify an amount of credits to set.", "Devo Bank"))
        if author == user:
            return await ctx.send(f"{ctx.author.mention}, Bitch, do I look like a joke to you?")
        if amount < 1:
            return await ctx.send(embed=lib.Editable("Uh oh", "You need to transfer at least 1 credit.", "Devo Bank"))
        if self.account_check(user.id):
            if self.enough_money(author.id, amount):
                self.withdraw_money(author.id, amount)
                self.add_money(user.id, amount)
                await ctx.send(embed=lib.Editable("Bye Bye Money", f"Transferred {amount} credits to {user.name}'s account.", "Devo Bank"))
            else:
                await ctx.send(embed=lib.Editable("Aw shit, here we go again", f"{author.mention} You're too poor to do that", "Devo Bank"))
        else:
            await ctx.send(embed=lib.Editable("Uh oh", f"{user.name} has no bank account.", "Devo Bank"))

    @bank.group(invoke_without_command=True)
    async def set(self, ctx, user: discord.Member=None, amount : int=None):
        if user is None:
            return await ctx.send(embed=lib.Editable("Uh oh", "Please mention a users bank to set.", "Devo Bank"))
        if amount is None:
            return await ctx.send(embed=lib.Editable("Oops", "Please specify an amount of credits to set.", "Devo Bank"))
        if ctx.author.id in self.config.owner:
            done = self.set_money(user.id, amount)
            if done:
                await ctx.send(embed=lib.Editable("Some kind of wizardry", f"Set {user.mention}'s balance to {amount} credits.", "Devo Bank"))
            else:
                await ctx.send(embed=lib.Editable("Uh oh", f"{user.name} has no bank account.", "Devo Bank"))
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @commands.command()
    async def benefits(self, ctx):
        author = ctx.author
        id = author.id
        if self.account_check(id):
            if id in self.benefits_register:
                seconds = abs(self.benefits_register[id] - int(time.perf_counter()))
                if seconds >= self.settings["BENEFITS_TIME"]:
                    self.add_money(id, self.settings["BENEFITS_CREDITS"])
                    self.benefits_register[id] = int(time.perf_counter())
                    await ctx.send(embed=lib.Editable(f"{author.name} collected their benefits", "{} has been added to your account!".format(self.settings["BENEFITS_CREDITS"]), "Devo Bank"))
                else:
                    await ctx.send(embed=lib.Editable("Uh oh", "You need to wait another {} seconds until you can get more benefits.".format(self.display_time(self.settings["BENEFITS_TIME"] - seconds)), "Devo Bank"))
            else:
                self.benefits_register[id] = int(time.perf_counter())
                self.add_money(id, self.settings["BENEFITS_CREDITS"])
                await ctx.send(embed=lib.Editable(f"{author.name} collected their benefits", "{} has been added to your account!".format(self.settings["BENEFITS_CREDITS"]), "Devo Bank"))
        else:
            await ctx.send(embed=lib.Editable("Uh oh", f"{user.mention}, You dont have a bank account at the Devo Bank. Type !bank register to open one.", "Devo Bank"))

    @commands.command()
    async def top(self, ctx, top : int=10):
        if top < 1:
            top = 10
        bank_sorted = sorted(self.bank.items(), key=lambda x: x[1]["balance"], reverse=True)
        if len(bank_sorted) < top:
            top = len(bank_sorted)
        topten = bank_sorted[:top]
        highscore = ""
        place = 1
        for id in topten:
            highscore += str(place).ljust(len(str(top))+1)
            highscore += (id[1]["name"]+ "'s Balance:" + " ").ljust(23-len(str(id[1]["balance"])))
            highscore += str(id[1]["balance"]) + "\n"
            place += 1
        if highscore:
            if len(highscore) < 1985:
                await ctx.send(embed=lib.Editable(f"Top {top}", f"{highscore}", "Devo Bank"))
            else:
                await ctx.send(embed=lib.Editable("Uh oh", "Thats too much data for me to handle, try a lower amount!", "Devo Bank"))
        else:
            await ctx.send(embed=lib.Editable("Uh oh", "There are no accounts in the bank.", "Devo Bank"))

    @commands.command()
    async def winnings(self, ctx):
        await ctx.send(slot_winnings)

    @commands.command(pass_context=True, no_pm=True)
    async def slot(self, ctx, bid : int=None):
        if bid is None:
            return await ctx.send(embed=lib.Editable("Uhhh", "You need to type a bid amound", "Slot Machine"))
        author = ctx.author
        if self.enough_money(author.id, bid):
            if bid >= self.settings["SLOT_MIN"] and bid <= self.settings["SLOT_MAX"]:
                if author.id in self.slot_register:
                    if abs(self.slot_register[author.id] - int(time.perf_counter()))  >= self.settings["SLOT_TIME"]:
                        self.slot_register[author.id] = int(time.perf_counter())
                        await self.slot_machine(ctx.message, bid)
                    else:
                        await ctx.send(embed=lib.Editable("Uh oh", "The slot machine is still cooling off! Wait {} seconds between each pull".format(self.settings["SLOT_TIME"]), "Slot Machine"))
                else:
                    self.slot_register[author.id] = int(time.perf_counter())
                    await self.slot_machine(ctx.message, bid)
            else:
                await ctx.send(embed=lib.Editable("Uh oh", "{0} Bid must be between {1} and {2}.".format(author.mention, self.settings["SLOT_MIN"], self.settings["SLOT_MAX"]), "Slot Machine"))
        else:
            await ctx.send(embed=lib.Editable("You're Skint!", f"{author.mention} You're too poor to play that bet on the slot machine!"))

    async def slot_machine(self, message, bid):
        reel_pattern = [":cherries:", ":cookie:", ":six:", ":four_leaf_clover:", ":cyclone:", ":sunflower:", ":nine:", ":mushroom:", ":heart:", ":snowflake:"]
        padding_before = [":mushroom:", ":heart:", ":snowflake:"] # padding prevents index errors
        padding_after = [":cherries:", ":cookie:", ":six:"]
        reel = padding_before + reel_pattern + padding_after
        reels = []
        for i in range(0, 3):
            n = randint(3,12)
            reels.append([reel[n - 1], reel[n], reel[n + 1]])
        line = [reels[0][1], reels[1][1], reels[2][1]]

        display_reels = "  " + reels[0][0] + " " + reels[1][0] + " " + reels[2][0] + "\n"
        display_reels += "  " + reels[0][1] + " " + reels[1][1] + " " + reels[2][1] + "< \n"
        display_reels += "  " + reels[0][2] + " " + reels[1][2] + " " + reels[2][2] + "\n"

        if line[0] == ":six:" and line[1] == ":six:" and line[2] == ":six:":
            bid = bid * 6666
            await message.channel.send(embed=lib.Editable(f"{message.author.name} Bid {bid}", f"{display_reels} \n\n666! Your bet is multiplied * 6666!", "Slot Machine"))
        elif line[0] == ":four_leaf_clover:" and line[1] == ":four_leaf_clover:" and line[2] == ":four_leaf_clover:":
            bid += 1000
            await message.channel.send(embed=lib.Editable(f"{message.author.name} Bid {bid}", f"{display_reels} \n\nThree FLC! +1000!", "Slot Machine"))
        elif line[0] == ":cherries:" and line[1] == ":cherries:" and line[2] == ":cherries:":
            bid += 800
            await message.channel.send(embed=lib.Editable(f"{message.author.name} Bid {bid}", f"{display_reels} \n\nThree cherries! +800!", "Slot Machine"))
        elif line[0] == line[1] == line[2]:
            bid += 500
            await message.channel.send(embed=lib.Editable(f"{message.author.name} Bid {bid}", f"{display_reels} \n\nThree symbols! +500!", "Slot Machine"))
        elif line[0] == ":two:" and line[1] == ":six:" or line[1] == ":two:" and line[2] == ":six:":
            bid = bid * 4
            await message.channel.send(embed=lib.Editable(f"{message.author.name} Bid {bid}", f"{display_reels} \n\n69! Your bet is multiplied * 4!", "Slot Machine"))
        elif line[0] == ":cherries:" and line[1] == ":cherries:" or line[1] == ":cherries:" and line[2] == ":cherries:":
            bid = bid * 3
            await message.channel.send(embed=lib.Editable(f"{message.author.name} Bid {bid}", f"{display_reels} \n\nTwo cherries! Your bet is multiplied * 3!", "Slot Machine"))
        elif line[0] == line[1] or line[1] == line[2]:
            bid = bid * 2
            await message.channel.send(embed=lib.Editable(f"{message.author.name} Bid {bid}", f"{display_reels} \n\nTwo symbols! Your bet is multiplied * 2!", "Slot Machine"))
        else:
            await message.channel.send(embed=lib.Editable(f"{message.author.name} Bid {bid}", f"{display_reels} \n\nNothing! Bet lost..", "Slot Machine"))
            self.withdraw_money(message.author.id, bid)
            return True
        self.add_money(message.author.id, bid)

    @commands.group(pass_context=True, no_pm=True)
    async def economyset(self, ctx):
        user = ctx.author
        if user.id in self.config.owner:
            msg = "```"
            for k, v in self.settings.items():
                msg += str(k) + ": " + str(v) + "\n"
            msg += "\nType {}help to see the list of commands.```".format(ctx.prefix)
            await ctx.send(msg)
        else:
            p = await ctx.send(embed=lib.NoPerm())
            await lib.eraset(self, ctx, p)

    @economyset.command(invoke_without_command=True)
    async def slotmin(self, ctx, bid : int):
        self.settings["SLOT_MIN"] = bid
        await ctx.send("Minimum bid is now " + str(bid) + " credits.")
        with open("./data/economy/settings.json", "w") as s:
            json.dump(self.settings, s)

    @economyset.command(invoke_without_command=True)
    async def slotmax(self, ctx, bid : int):
        self.settings["SLOT_MAX"] = bid
        await ctx.send("Maximum bid is now " + str(bid) + " credits.")
        with open("./data/economy/settings.json", "w") as s:
            json.dump(self.settings, s)

    @economyset.command(invoke_without_command=True)
    async def slottime(self, ctx, seconds : int):
        self.settings["SLOT_TIME"] = seconds
        await ctx.send("Cooldown is now " + str(seconds) + " seconds.")
        with open("./data/economy/settings.json", "w") as s:
            json.dump(self.settings, s)

    @economyset.command(invoke_without_command=True)
    async def benefitstime(self, ctx, seconds : int):
        self.settings["BENEFITS_TIME"] = seconds
        await ctx.send("Value modified. At least " + str(seconds) + " seconds must pass between each payday.")
        with open("./data/economy/settings.json", "w") as s:
            json.dump(self.settings, s)

    @economyset.command(invoke_without_command=True)
    async def paydaycredits(self, ctx, credits : int):
        self.settings["BENEFITS_CREDITS"] = credits
        await ctx.send("Every payday will now give " + str(credits) + " credits.")
        with open("./data/economy/settings.json", "w") as s:
            json.dump(self.settings, s)









    def account_check(self, id):
        id = str(id)
        if id in self.bank:
            return True
        else:
            return False

    def check_balance(self, id):
        id = str(id)
        if self.account_check(id):
            return self.bank[id]["balance"]
        else:
            return False

    def add_money(self, id, amount):
        id = str(id)
        if self.account_check(id):
            self.bank[id]["balance"] = self.bank[id]["balance"] + int(amount)
            with open("./utils/essentials/economy.json", "w") as f:
                json.dump(self.bank, f)
        else:
            return False

    def withdraw_money(self, id, amount):
        id = str(id)
        if self.account_check(id):
            if self.bank[id]["balance"] >= int(amount):
                self.bank[id]["balance"] = self.bank[id]["balance"] - int(amount)
                with open("./utils/essentials/economy.json", "w") as f:
                    json.dump(self.bank, f)
            else:
                return False
        else:
            return False

    def enough_money(self, id, amount):
        id = str(id)
        if self.account_check(id):
            if self.bank[id]["balance"] >= int(amount):
                return True
            else:
                return False
        else:
            return False

    def set_money(self, id, amount):
        id = str(id)
        if self.account_check(id):
            self.bank[id]["balance"] = amount
            with open("./utils/essentials/economy.json", "w") as f:
                json.dump(self.bank, f)
            return True
        else:
            return False

    def display_time(self, seconds, granularity=2):
        intervals = (
            ('weeks', 604800),  # 60 * 60 * 24 * 7
            ('days', 86400),    # 60 * 60 * 24
            ('hours', 3600),    # 60 * 60
            ('minutes', 60),
            ('seconds', 1),
            )

        result = []

        for name, count in intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append("{} {}".format(value, name))
        return ', '.join(result[:granularity])


def setup(bot):
    bot.add_cog(Economy(bot))
