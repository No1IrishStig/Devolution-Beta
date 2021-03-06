import sys, traceback
import shelve
import datetime
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

SETS = ["♥", "♣", "♠", "♦"]

CARDS = ['Ace', 'Two', 'Three', 'Four',
         'Five', 'Six', 'Seven', 'Eight',
         'Nine', 'Ten', 'Jack', 'Queen', 'King']

global is_active, creator, opponent, start_message, join_message
global player_extra, bot_extra, bet_amount, CARDS_TOTAL_WORTH, OPPONENT_TOTAL_WORTH
global STOOD_WHEN_LESS_HOUSE_WINS, STAND, HOUSE_STAND, gameover

is_active = False
STAND = False
STOOD_WHEN_LESS_HOUSE_WINS = False
HOUSE_STAND = False

players_cards = []
bot_cards = []

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("./utils/cfg.json")
        self.benefits_register = {}
        self.slot_register = {}
        self.db = shelve.open("./data/db/economy/data.db", writeback=True)
        with open("./data/settings/economy.json") as s:
            self.settings = json.load(s)
            with open("./data/settings/deltimer.json") as f:
                self.deltimer = json.load(f)

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bank(self, ctx):
        user = ctx.author
        UID = str(user.id)
        GID = str(ctx.guild.id)
        if GID in self.db["Economy"]:
            if UID in self.db["Economy"][GID]:
                await ctx.send(embed=lib.Editable(self, "Bank Commands", f"`{ctx.prefix}bank register` - Creates you a bank account (You already have one)\n`{ctx.prefix}bank balance` - Shows your balance\n`{ctx.prefix}bank transfer @user (amount)` - Transfer credits to another user\n`{ctx.prefix}bank set @user (amount)` - Change the bank balance of another user (Admin Only)\n\nGame Commands\n`{ctx.prefix}blackjack play (bet)` - Play blackjack against the house\n`{ctx.prefix}slots (bet)` - Play the slot machine", "Devo Bank"))
            else:
                await ctx.send(embed=lib.Editable(self, "Just do it!", "Use !bank register to create a bank account", "Devo Bank"))
        else:
            await ctx.send(embed=lib.Editable(self, "Just do it!", "Use !bank register to create a bank account", "Devo Bank"))

    @bank.group(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def register(self, ctx):
        user = ctx.author
        UID = str(user.id)
        GID = str(ctx.guild.id)
        if GID in self.db["Economy"]:
            if UID not in self.db["Economy"][GID]:
                self.db["Economy"][GID][UID] = {"name": user.name, "balance": 100}
                await ctx.send(embed=lib.Editable(self, "Ayy", f"Bank Account Created for {ctx.author.mention}. Current balance: {str(self.check_balance(GID, user.id))}", "Devo Bank"))
                self.db.sync()
            else:
                await ctx.send(embed=lib.Editable(self, "Uh oh", "You're too poor to make another bank account ;)", "Devo Bank"))
        else:
            self.db["Economy"][GID] = {}
            self.db["Economy"][GID][UID] = {"name": user.name, "balance": 100}
            self.db.sync()
            await ctx.send(embed=lib.Editable(self, "Ayy", f"Bank Account Created for {ctx.author.mention}. Current balance: {str(self.check_balance(GID, user.id))}", "Devo Bank"))

    @bank.group(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def balance(self, ctx, user: discord.Member=None):
        GID = str(ctx.guild.id)
        if GID in self.db["Economy"]:
            if user is None:
                user = ctx.author
                if self.account_check(GID, user.id):
                    await ctx.send(embed=lib.Editable(self, "Monayy", f"{user.mention}, Your bank balance is {str(self.check_balance(GID, user.id))}", "Devo Bank"))
                else:
                    await ctx.send(embed=lib.Editable(self, "Uh oh", f"{user.mention}, You dont have a bank account at the Devo Bank. Type !bank register to open one.", "Devo Bank"))
            else:
                if self.account_check(GID, user.id):
                    balance = self.check_balance(GID, user.id)
                    await ctx.send(embed=lib.Editable(self, f"{user.name} just flexed", f"{user.mention}'s balance is {str(balance)}", "Devo Bank"))
                else:
                    await ctx.send(embed=lib.Editable(self, "Uh oh", f"{user.name} has no bank account.", "Devo Bank"))
        else:
            await ctx.send(embed=lib.Editable(self, "Uh oh", f"The bank is not setup on this server! Type {ctx.prefix}bank register to start.", "Devo Bank"))

    @bank.group(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def transfer(self, ctx, user: discord.Member=None, amount : int=None):
        author = ctx.author
        GID = str(ctx.guild.id)
        if GID in self.db["Economy"]:
            if user and amount:
                if not author == user:
                    if amount > 1:
                        if self.account_check(GID, user.id):
                            if self.enough_money(GID, author.id, amount):
                                self.withdraw_money(GID, author.id, amount)
                                self.add_money(GID, user.id, amount)
                                self.db.sync()
                                await ctx.send(embed=lib.Editable(self, "Bye Bye Money", f"Transferred {amount} credits to {user.name}'s account.", "Devo Bank"))
                            else:
                                await ctx.send(embed=lib.Editable(self, "Aw shit, here we go again", f"{author.mention} You're too poor to do that", "Devo Bank"))
                        else:
                            await ctx.send(embed=lib.Editable(self, "Uh oh", f"{user.name} has no bank account.", "Devo Bank"))
                    else:
                        await ctx.send(embed=lib.Editable(self, "Uh oh", "You need to transfer at least 1 credit.", "Devo Bank"))
                else:
                    await ctx.send(f"{ctx.author.mention}, Bitch, do I look like a joke to you?")
            else:
                return await ctx.send(embed=lib.Editable(self, "Oops", "Please specify an amount of credits to set and for who.", "Devo Bank"))
        else:
            await ctx.send(embed=lib.Editable(self, "Uh oh", f"The bank is not setup on this server! Type {ctx.prefix}bank register to start.", "Devo Bank"))

    @bank.group(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def set(self, ctx, user: discord.Member=None, amount : int=None):
        GID = str(ctx.guild.id)
        if ctx.author is ctx.guild.owner or ctx.author.id in self.config.owner:
            if GID in self.db["Economy"]:
                if user and amount:
                    done = self.set_money(GID, user.id, amount)
                    if done:
                        await ctx.send(embed=lib.Editable(self, "Some kind of wizardry", f"Set {user.mention}'s balance to {amount} credits.", "Devo Bank"))
                        self.db.sync()
                    else:
                        await ctx.send(embed=lib.Editable(self, "Uh oh", f"{user.name} has no bank account.", "Devo Bank"))
                else:
                    await ctx.send(embed=lib.Editable(self, "Oops", "Please specify a user and an amount.", "Devo Bank"))
            else:
                await ctx.send(embed=lib.Editable(self, "Uh oh", f"The bank is not setup on this server! Type {ctx.prefix}bank register to start.", "Devo Bank"))
        else:
            p = await ctx.send(embed=lib.NoPerm(self))
            await lib.eraset(self, ctx, p)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def benefits(self, ctx):
        author = ctx.author
        GID = str(ctx.guild.id)
        id = author.id
        if GID in self.db["Economy"]:
            if self.account_check(GID, id):
                if id in self.benefits_register:
                    seconds = abs(self.benefits_register[id] - int(time.perf_counter()))
                    if seconds >= self.settings["BENEFITS_TIME"]:
                        self.add_money(GID, id, self.settings["BENEFITS_CREDITS"])
                        self.benefits_register[id] = int(time.perf_counter())
                        await ctx.send(embed=lib.Editable(self, f"{author.name} collected their benefits", "{} has been added to your account!".format(self.settings["BENEFITS_CREDITS"]), "Devo Bank"))
                        self.db.sync()
                    else:
                        await ctx.send(embed=lib.Editable(self, "Uh oh", "You need to wait another {} seconds until you can get more benefits.".format(self.display_time(self.settings["BENEFITS_TIME"] - seconds)), "Devo Bank"))
                else:
                    self.benefits_register[id] = int(time.perf_counter())
                    self.add_money(GID, id, self.settings["BENEFITS_CREDITS"])
                    await ctx.send(embed=lib.Editable(self, f"{author.name} collected their benefits", "{} has been added to your account!".format(self.settings["BENEFITS_CREDITS"]), "Devo Bank"))
                    self.db.sync()
            else:
                await ctx.send(embed=lib.Editable(self, "Uh oh", f"{author.mention}, You dont have a bank account at the Devo Bank. Type !bank register to open one.", "Devo Bank"))
        else:
            await ctx.send(embed=lib.Editable(self, "Uh oh", f"The bank is not setup on this server! Type {ctx.prefix}bank register to start.", "Devo Bank"))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def top(self, ctx, top : int=10):
        GID = str(ctx.guild.id)
        if GID in self.db["Economy"]:
            if top < 1:
                top = 10
            bank_sorted = sorted(self.db["Economy"][GID].items(), key=lambda x: x[1]["balance"], reverse=True)
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
                    await ctx.send(embed=lib.Editable(self, f"Top {top}", f"{highscore}", "Devo Bank"))
                else:
                    await ctx.send(embed=lib.Editable(self, "Uh oh", "Thats too much data for me to handle, try a lower amount!", "Devo Bank"))
        else:
            await ctx.send(embed=lib.Editable(self, "Uh oh", f"The bank is not setup on this server! Type {ctx.prefix}bank register to start.", "Devo Bank"))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def winnings(self, ctx):
        await ctx.send(slot_winnings)

    @commands.command(pass_context=True, no_pm=True)
    async def slots(self, ctx, bid : int=None):
        GID = str(ctx.guild.id)
        start_bid = bid
        if GID in self.db["Economy"]:
            if bid:
                author = ctx.author
                if self.enough_money(GID, author.id, bid):
                    if bid >= self.settings["SLOT_MIN"] and bid <= self.settings["SLOT_MAX"]:
                        if author.id in self.slot_register:
                            if abs(self.slot_register[author.id] - int(time.perf_counter()))  >= self.settings["SLOT_TIME"]:
                                self.slot_register[author.id] = int(time.perf_counter())
                                await self.slot_machine(ctx.message, bid)
                            else:
                                await ctx.send(embed=lib.Editable(self, "Uh oh", "The slot machine is still cooling off! Wait {} seconds between each pull".format(self.settings["SLOT_TIME"]), "Slot Machine"))
                        else:
                            self.slot_register[author.id] = int(time.perf_counter())
                            await self.slot_machine(ctx.message, bid)
                    else:
                        await ctx.send(embed=lib.Editable(self, "Uh oh", "{0} Bid must be between {1} and {2}.".format(author.mention, self.settings["SLOT_MIN"], self.settings["SLOT_MAX"]), "Slot Machine"))
                else:
                    await ctx.send(embed=lib.Editable(self, "You're Skint!", f"{author.mention} You're too poor to play that bet on the slot machine!", "Slot Machine"))
            else:
                await ctx.send(embed=lib.Editable(self, "Uhhh", "You need to type a bid amound", "Slot Machine"))
        else:
            await ctx.send(embed=lib.Editable(self, "Uh oh", f"The bank is not setup on this server! Type {ctx.prefix}bank register to start.", "Devo Bank"))

    async def slot_machine(self, message, bid):
        start_bid = bid
        GID = str(message.guild.id)
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
            await message.channel.send(embed=lib.Editable(self, f"{message.author.name} Bid {start_bid}", f"{display_reels} \n\n666! Your bet is multiplied * 6666!", "Slot Machine"))
        elif line[0] == ":four_leaf_clover:" and line[1] == ":four_leaf_clover:" and line[2] == ":four_leaf_clover:":
            bid += 1000
            await message.channel.send(embed=lib.Editable(self, f"{message.author.name} Bid {start_bid}", f"{display_reels} \n\nThree FLC! +1000!", "Slot Machine"))
        elif line[0] == ":cherries:" and line[1] == ":cherries:" and line[2] == ":cherries:":
            bid += 800
            await message.channel.send(embed=lib.Editable(self, f"{message.author.name} Bid {start_bid}", f"{display_reels} \n\nThree cherries! +800!", "Slot Machine"))
        elif line[0] == line[1] == line[2]:
            bid += 500
            await message.channel.send(embed=lib.Editable(self, f"{message.author.name} Bid {start_bid}", f"{display_reels} \n\nThree symbols! +500!", "Slot Machine"))
        elif line[0] == ":nine:" and line[1] == ":six:" or line[1] == ":six:" and line[2] == ":nine:":
            bid = bid * 4
            await message.channel.send(embed=lib.Editable(self, f"{message.author.name} Bid {start_bid}", f"{display_reels} \n\n69! Your bet is multiplied * 4!", "Slot Machine"))
        elif line[0] == ":cherries:" and line[1] == ":cherries:" or line[1] == ":cherries:" and line[2] == ":cherries:":
            bid = bid * 3
            await message.channel.send(embed=lib.Editable(self, f"{message.author.name} Bid {start_bid}", f"{display_reels} \n\nTwo cherries! Your bet is multiplied * 3!", "Slot Machine"))
        elif line[0] == line[1] or line[1] == line[2]:
            bid = bid * 2
            await message.channel.send(embed=lib.Editable(self, f"{message.author.name} Bid {start_bid}", f"{display_reels} \n\nTwo symbols! Your bet is multiplied * 2!", "Slot Machine"))
        else:
            await message.channel.send(embed=lib.Editable(self, f"{message.author.name} Bid {start_bid}", f"{display_reels} \n\nNothing! Bet lost..", "Slot Machine"))
            self.withdraw_money(GID, message.author.id, bid)
            self.db.sync()
            return True
        self.add_money(GID, message.author.id, bid)
        self.db.sync()

    @commands.group(pass_context=True, no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def economyset(self, ctx):
        user = ctx.author
        if user.id in self.config.owner:
            msg = "```"
            for k, v in self.settings.items():
                msg += str(k) + ": " + str(v) + "\n"
            msg += "\nType {}help to see the list of commands.```".format(ctx.prefix)
            await ctx.send(msg)
        else:
            p = await ctx.send(embed=lib.NoPerm(self))
            await lib.eraset(self, ctx, p)

    @economyset.command(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slotmin(self, ctx, bid : int=None):
        if bid:
            self.settings["SLOT_MIN"] = bid
            await ctx.send("Minimum bid is now " + str(bid) + " credits.")
            with open("./data/economy/settings.json", "w") as s:
                json.dump(self.settings, s)
        else:
            await ctx.send(embed=lib.Editable(self, "You Missed Something", "You need to enter a minimum amount", "Economy"))

    @economyset.command(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slotmax(self, ctx, bid : int=None):
        if bid:
            self.settings["SLOT_MAX"] = bid
            await ctx.send("Maximum bid is now " + str(bid) + " credits.")
            with open("./data/economy/settings.json", "w") as s:
                json.dump(self.settings, s)
        else:
            await ctx.send(embed=lib.Editable(self, "You Missed Something", "You need to enter a maximum amount", "Economy"))

    @economyset.command(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slottime(self, ctx, seconds : int=None):
        if seconds:
            self.settings["SLOT_TIME"] = seconds
            await ctx.send("Cooldown is now " + str(seconds) + " seconds.")
            with open("./data/economy/settings.json", "w") as s:
                json.dump(self.settings, s)
        else:
            await ctx.send(embed=lib.Editable(self, "You Missed Something", "You need to enter a slot time.", "Economy"))

    @economyset.command(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def benefitstime(self, ctx, seconds : int=None):
        if seconds:
            self.settings["BENEFITS_TIME"] = seconds
            await ctx.send("Value modified. At least " + str(seconds) + " seconds must pass between each benefits claim.")
            with open("./data/economy/settings.json", "w") as s:
                json.dump(self.settings, s)
        else:
            await ctx.send(embed=lib.Editable(self, "You Missed Something", "You need to enter a benefits delay", "Economy"))

    @economyset.command(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def benefitscredits(self, ctx, credits : int=None):
        if credits:
            self.settings["BENEFITS_CREDITS"] = credits
            await ctx.send("Every benefits claim will now give " + str(credits) + " credits.")
            with open("./data/economy/settings.json", "w") as s:
                json.dump(self.settings, s)
        else:
            await ctx.send(embed=lib.Editable(self, "You Missed Something", "You need to enter an amount", "Economy"))

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def blackjack(self, ctx):
        await ctx.send(f"Type `{ctx.prefix}blackjack play (bet)` to begin")

    @blackjack.group(invoke_without_command=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def play(self, ctx, bet:int=None):
        global is_active, creator, gameover, is_active, STOOD_WHEN_LESS_HOUSE_WINS, bet_amount, STAND, HOUSE_STAND, startmsg, bet_amount, UID
        GID = str(ctx.guild.id)
        UID = str(ctx.author.id)
        creator = ctx.author
        gameover = False
        if bet:
            if self.bank_exists(GID):
                if self.enough_money(GID, UID, bet):
                    bet_amount = bet
                    await ctx.message.delete()
                    channel = ctx.message.channel
                    blackjack_start = await ctx.send(embed=self.BJ_START())
                    is_active = True
                    await asyncio.sleep(5)
                    await self.cards(channel)
                    await asyncio.sleep(2)
                    await self.bot_cards(channel)
                    await blackjack_start.delete()
                    startmsg = await ctx.send(embed=self.BJ_E(0xd42c2c, "{}\n**Score:** {}".format(", ".join(players_cards), CARDS_TOTAL_WORTH), f"{bot_cards[0]}", "**Options**: hit, stand, double?"))
                    while is_active is True:
                        await self.win(ctx)
                        if gameover is False:
                            await self.player(ctx)
                            if is_active is True:
                                await self.win(ctx)
                                if gameover is False:
                                    await self.blackjack_math(ctx)
                                    if is_active is False:
                                        break
                                else:
                                    break
                        else:
                            break

                else:
                    await ctx.send(embed=lib.Editable(self, "You're Skint!", f"{ctx.author.mention} You're too poor to play that bet!", "Blackjack"))
            else:
                await ctx.send(embed=lib.Editable(self, "Uh oh", f"This guild doesnt have the bank setup! Type `{ctx.prefix}bank register` to start!", "Devo Bank"))
        else:
            await ctx.send(embed=lib.Editable(self, "Oops", "Please enter an amount to bet.", "Blackjack"))

    async def player(self, ctx):
        global choice, STOOD_WHEN_LESS_HOUSE_WINS, STAND, bet_amount, startmsg
        if STAND is False:
            choice = await self.bot.wait_for("message", check=lambda message: message.author == creator, timeout = 30)
            if choice.content == "Hit" or choice.content == "hit":
                await choice.delete()
                await self.hit(ctx)
            elif choice.content == "Stand" or choice.content == "stand":
                await choice.delete()
                await startmsg.edit(embed=self.BJ_E(0xd42c2c, "{}\n**Score:** {}".format(", ".join(players_cards), CARDS_TOTAL_WORTH), f"{bot_cards[0]}", f"Result: {creator.name} Stood."))
                STAND = True
                if CARDS_TOTAL_WORTH > OPPONENT_TOTAL_WORTH:
                    await asyncio.sleep(2)
                else:
                    STOOD_WHEN_LESS_HOUSE_WINS = True
            elif choice.content == "Double" or choice.content == "double":
                bet_amount = bet_amount * 2
                await self.hit(ctx)
            else:
                await ctx.send("Invalid Response. Skipping.")
        else:
            return

    async def cards(self, channel):
        global creator, CARDS_TOTAL_WORTH, player_extra
        CARDS_TOTAL_WORTH = 0
        player_extra = 2
        for i in range(2):
            s = randint(0, 3)
            c = randint(0, 12)
            crds = c
            if c > 9:
                c = 10
                player_extra = player_extra - 1
            players_cards.append(SETS[s] + " " + CARDS[crds])
            CARDS_TOTAL_WORTH += c
        CARDS_TOTAL_WORTH += player_extra
        # await channel.send(embed=lib.EditableC(self, f"{creator.name}'s Cards", "You got a {} and a {} which equals {}".format(players_cards[0], players_cards[1], CARDS_TOTAL_WORTH), 0x58CCED, "Blackjack"))

    async def bot_cards(self, ctx):
        global OPPONENT_TOTAL_WORTH, bot_extra, bot_onecard
        OPPONENT_TOTAL_WORTH = 0
        bot_extra = 2
        for i in range(2):
            s = randint(0, 3)
            c = randint(0, 12)
            crds = c
            if c > 9:
                c = 10
                bot_extra = bot_extra - 1
            bot_cards.append(SETS[s] + " " + CARDS[crds])
            OPPONENT_TOTAL_WORTH += c
        OPPONENT_TOTAL_WORTH += bot_extra
        bot_onecard = c
        # [DEBUG] await ctx.send(embed=lib.EditableC(self, "Opponents Cards (Debug Only)", "The House got a {} and a {} which equals {}".format(bot_cards[0], bot_cards[1], OPPONENT_TOTAL_WORTH), 0xff0000, "Blackjack"))

    async def hit(self, ctx):
        global player_extra, CARDS_TOTAL_WORTH, startmsg
        player_extra = 1
        s = randint(0, 3)
        c = randint(0, 12)
        crds = c
        if c > 9:
            c = 10
            player_extra = player_extra - 1
        CARDS_TOTAL_WORTH += c
        CARDS_TOTAL_WORTH += player_extra
        players_cards.append(SETS[s] + " " + CARDS[crds])
        await startmsg.edit(embed=self.BJ_E(0xd42c2c, "{}\n**Score:** {}".format(", ".join(players_cards), CARDS_TOTAL_WORTH), f"{bot_cards[0]}", "**Options**: hit, stand, double?"))
        #return await ctx.send(embed=lib.Editable(self, f"{ctx.author.name}'s Turn", "{} got a {} which gives a total of {}".format(creator.name, players_cards[0], CARDS_TOTAL_WORTH), "Blackjack"))

    async def win(self, ctx):
        global STOOD_WHEN_LESS_HOUSE_WINS, gameover, bet_amount, GID
        GID = str(ctx.guild.id)
        if OPPONENT_TOTAL_WORTH > 21:
            await startmsg.edit(embed=self.BJ_E(0x28acd1, "{}\n**Score:** {}".format(", ".join(players_cards), CARDS_TOTAL_WORTH), "{}\n**Score:** {}".format(", ".join(bot_cards), OPPONENT_TOTAL_WORTH), f"{self.bot.user.name} Bust with {OPPONENT_TOTAL_WORTH}!\n\n{creator.name} Wins {bet_amount * 2} credits!"))
            self.win_end()
        elif CARDS_TOTAL_WORTH > 21:
            await startmsg.edit(embed=self.BJ_E(0xd42c2c, "{}\n**Score:** {}".format(", ".join(players_cards), CARDS_TOTAL_WORTH), "{}\n**Score:** {}".format(", ".join(bot_cards), OPPONENT_TOTAL_WORTH), f"{creator.name} Bust with {CARDS_TOTAL_WORTH}!\n\n{self.bot.user.name} Wins {bet_amount * 2} credits!"))
            self.lose_end()
        elif OPPONENT_TOTAL_WORTH == 21:
            await startmsg.edit(embed=self.BJ_E(0xd42c2c, "{}\n**Score:** {}".format(", ".join(players_cards), CARDS_TOTAL_WORTH), "{}\n**Score:** {}".format(", ".join(bot_cards), OPPONENT_TOTAL_WORTH), f"{self.bot.user.name} Got blackjack!\n\n{self.bot.user.name} Wins {bet_amount * 2} credits!"))
            self.lose_end()
        elif CARDS_TOTAL_WORTH == 21:
            await startmsg.edit(embed=self.BJ_E(0x28acd1, "{}\n**Score:** {}".format(", ".join(players_cards), CARDS_TOTAL_WORTH), "{}\n**Score:** {}".format(", ".join(bot_cards), OPPONENT_TOTAL_WORTH), f"{creator.name} Got blackjack!\n\n{creator.name} Wins {bet_amount * 2} credits!"))
            self.win_end()
        elif CARDS_TOTAL_WORTH == OPPONENT_TOTAL_WORTH:
            await startmsg.edit(embed=self.BJ_E(0x28acd1, "{}\n**Score:** {}".format(", ".join(players_cards), CARDS_TOTAL_WORTH), "{}\n**Score:** {}".format(", ".join(bot_cards), OPPONENT_TOTAL_WORTH), f"Its a tie! Your credits have been returned."))
            self.lose_end()
            self.add_money(GID, UID, bet_amount)
        elif STOOD_WHEN_LESS_HOUSE_WINS is True:
            await startmsg.edit(embed=self.BJ_E(0xd42c2c, "{}\n**Score:** {}".format(", ".join(players_cards), CARDS_TOTAL_WORTH), "{}\n**Score:** {}".format(", ".join(bot_cards), OPPONENT_TOTAL_WORTH), f"{creator.name} Stood with {CARDS_TOTAL_WORTH}!\n\n{self.bot.user.name} Wins {bet_amount * 2} credits!"))
            self.lose_end()
        elif STAND is True and HOUSE_STAND is True:
            if OPPONENT_TOTAL_WORTH > CARDS_TOTAL_WORTH:
                await startmsg.edit(embed=self.BJ_E(0xd42c2c, "{}\n**Score:** {}".format(", ".join(players_cards), CARDS_TOTAL_WORTH), "{}\n**Score:** {}".format(", ".join(bot_cards), OPPONENT_TOTAL_WORTH), f"{self.bot.user.name} Stood with {OPPONENT_TOTAL_WORTH}!\n\n{self.bot.user.name} Wins {bet_amount * 2} credits!"))
                self.lose_end()
            else:
                await startmsg.edit(embed=self.BJ_E(0x28acd1, "{}\n**Score:** {}".format(", ".join(players_cards), CARDS_TOTAL_WORTH), "{}\n**Score:** {}".format(", ".join(bot_cards), OPPONENT_TOTAL_WORTH), f"{creator.name} Stood with {CARDS_TOTAL_WORTH}!\n\n{creator.name} Wins {bet_amount * 2} credits!"))
                self.win_end()

    def lose_end(self):
        gameover = True
        self.withdraw_money(GID, UID, bet_amount)
        self.reset_match()
        self.db.sync()

    def win_end(self):
        gameover = True
        self.add_money(GID, UID, bet_amount * 2)
        self.reset_match()
        self.db.sync()

    async def bothit(self, ctx):
        global OPPONENT_TOTAL_WORTH, startmsg
        channel = ctx.message.channel
        extra = 1
        s = randint(0, 3)
        c = randint(0, 12)
        crds = c
        if c > 9:
            c = 10
            extra = extra - 1
        OPPONENT_TOTAL_WORTH += c
        OPPONENT_TOTAL_WORTH += bot_extra
        bot_cards.append(SETS[s] + " " + CARDS[crds])
        # [DEBUG] await channel.send(embed=lib.Editable(self, "Your Cards", "The House hit and got {} which equals {}".format(bot_cards[0], OPPONENT_TOTAL_WORTH), "Blackjack"))

    async def blackjack_math(self, ctx):
        global HOUSE_STAND, startmsg
        if HOUSE_STAND is False:
            if OPPONENT_TOTAL_WORTH < 18:
                await self.bothit(ctx)
            else:
                await startmsg.edit(embed=self.BJ_E(0xd42c2c, "{}\n**Score:** {}".format(", ".join(players_cards), CARDS_TOTAL_WORTH), f"{bot_cards[0]}", f"Result: {self.bot.user.name} Stood."))
                await asyncio.sleep(2)
                HOUSE_STAND = True
                await self.win(ctx)
        else:
            return

    def account_check(self, GID, id):
        id = str(id)
        if self.bank_exists(GID):
            if id in self.db["Economy"][GID]:
                return True
            else:
                return False
        else:
            return False

    def bank_exists(self, GID):
        if GID not in self.db["Economy"]:
            return False
        else:
            return True

    def check_balance(self, GID, id):
        id = str(id)
        GID = str(GID)
        if self.account_check(GID, id):
            return self.db["Economy"][GID][id]["balance"]
        else:
            return False

    def add_money(self, GID, id, amount):
        id = str(id)
        if self.account_check(GID, id):
            self.db["Economy"][GID][id]["balance"] += int(amount)
        else:
            return False

    def withdraw_money(self, GID, id, amount):
        id = str(id)
        if self.account_check(GID, id):
            if self.db["Economy"][GID][id]["balance"] >= int(amount):
                self.db["Economy"][GID][id]["balance"] = self.db["Economy"][GID][id]["balance"] - int(amount)
            else:
                return False
        else:
            return False

    def enough_money(self, GID, id, amount):
        id = str(id)
        if self.account_check(GID, id):
            if self.db["Economy"][GID][id]["balance"] >= int(amount):
                return True
            else:
                return False
        else:
            return False

    def set_money(self, GID, id, amount):
        id = str(id)
        if self.account_check(GID, id):
            self.db["Economy"][GID][id]["balance"] = amount
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

    def reset_match(self):
        global is_active, creator, opponent
        global bet_amount, CARDS_TOTAL_WORTH, OPPONENT_TOTAL_WORTH
        global STOOD_WHEN_LESS_HOUSE_WINS, STAND, HOUSE_STAND, gameover
        players_cards.clear()
        bot_cards.clear()
        is_active = False
        gameover = True
        creator = "Noone"
        opponent = "Noone"
        bet_amount = 0
        CARDS_TOTAL_WORTH = 0
        OPPONENT_TOTAL_WORTH = 0
        STOOD_WHEN_LESS_HOUSE_WINS = False
        STAND = False
        HOUSE_STAND = False

    def BJ_START(self):
        embed = discord.Embed(
            colour=0xd42c2c,
            )
        embed.set_author(name=f"{creator.name} started a match!")
        embed.set_footer(text=f"{self.bot.user.name} - Blackjack", icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Creator", value=f"{creator.name}", inline=True)
        embed.add_field(name="Opponent", value=f"{self.bot.user.name}", inline=True)
        embed.add_field(name="Bet", value=f"{bet_amount}", inline=True)
        embed.add_field(name="Get Ready!", value=f"The match will start in 5 seconds.", inline=False)
        return embed

    def BJ_E(self, color, value1, value2, value3):
        e = discord.Embed(
            colour = color,
            )
        e.add_field(name=f"{creator.name}'s Hand", value=value1, inline=True)
        e.add_field(name="\u200B", value="\u200B", inline=True)
        e.add_field(name=f"Their Hand", value=value2, inline=True)
        e.add_field(name="\u200B", value=value3, inline=False)
        return e

def setup(bot):
    bot.add_cog(Economy(bot))
