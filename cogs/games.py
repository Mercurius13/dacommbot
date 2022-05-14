import nextcord
from datetime import datetime
import asyncio
import random
import math
import akinator
from nextcord.ext import commands
from discord_slash.model import ButtonStyle
from discord_slash.utils import manage_components
from discord_slash.utils.manage_components import create_button, create_actionrow, spread_to_rows, wait_for_component
from akinator.async_aki import Akinator
import json
from random import sample, randint
from time import time
from tinydb import TinyDB, Query
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from typing import List


def get_embed(_title, _description, _color):
    return nextcord.Embed(title=title, description=_description, color=_color)


def w(name, desc, picture):
    embed_win = nextcord.Embed(title=f"It's {name} ({desc})! Was I correct?",
                               color=0x00FF00)
    embed_win.set_image(url=picture)
    return embed_win


aki = Akinator()

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("text_files/emojimovie.json", "r") as f:
            self.data = json.load(f)
            f.close()
        with open("text_files/pokemon.json", "r") as f:
            self.pokemon_data = json.load(f)
            f.close()
        self.total = len(self.pokemon_data)
        with open("text_files/riddles.json", "r", encoding="utf-8") as f:
            self.riddles_json = json.load(f)
            f.close()

    @cog_ext.cog_slash(name="riddle",
                       description="Gives you a riddle.")
    async def _riddle(self, ctx: SlashContext):
        data = self.riddles_json
        i = random.randint(1, 173)
        data = data[i]
        buttons = [
            create_button(style=ButtonStyle.blue, custom_id="answer", label="Reveal Answer",
                          disabled=False)
        ]
        action_row = create_actionrow(*buttons)
        embed = await ctx.send(embed=nextcord.Embed(title=data["question"], color=nextcord.Color.random()),
                               components=[action_row])
        response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                              messages=embed, timeout=120)
        while response.author != ctx.author:
            await response.reply("This ain't your button fool", hidden=True)
            response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                  messages=embed, timeout=120)
        try:
            buttons = [
                create_button(style=ButtonStyle.blue, custom_id="answer", label="Reveal Answer",
                              disabled=True)
            ]
            action_row = create_actionrow(*buttons)
            await response.edit_origin(components=[action_row])
            await response.send(embed=nextcord.Embed(title=data['answer'], color=nextcord.Color.random()))
        except asyncio.TimeoutError:
            buttons = [
                create_button(style=ButtonStyle.blue, custom_id="answer", label="Reveal Answer",
                              disabled=True)
            ]
            action_row = create_actionrow(*buttons)
            await response.edit_origin(components=[action_row])

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=['riddles', 'rid'])
    async def riddle(self, ctx):
        data = self.riddles_json
        i = random.randint(1, 173)
        data = data[i]
        buttons = [
            create_button(style=ButtonStyle.blue, custom_id="answer", label="Reveal Answer",
                          disabled=False)
        ]
        action_row = create_actionrow(*buttons)
        embed = await ctx.send(embed=nextcord.Embed(title=data["question"], color=nextcord.Color.random()),
                               components=[action_row])
        response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                              messages=embed, timeout=120)
        while response.author != ctx.author:
            await response.reply("This ain't your button fool", hidden=True)
            response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                  messages=embed, timeout=120)
        try:
            buttons = [
                create_button(style=ButtonStyle.blue, custom_id="answer", label="Reveal Answer",
                              disabled=True)
            ]
            action_row = create_actionrow(*buttons)
            await response.edit_origin(components=[action_row])
            await response.send(embed=nextcord.Embed(title=data['answer'], color=nextcord.Color.random()))
        except asyncio.TimeoutError:
            buttons = [
                create_button(style=ButtonStyle.blue, custom_id="answer", label="Reveal Answer",
                              disabled=True)
            ]
            action_row = create_actionrow(*buttons)
            await response.edit_origin(components=[action_row])

    @cog_ext.cog_slash(name="coinflip",
                       description="Allows you to try your luck with the coin!",
                       options=[
                           create_option(name="heads_tails",
                                         description="Heads/Tails: what you think will be the outcome (don't use member if you use this)",
                                         option_type=3,
                                         required=False),
                           create_option(name="member",
                                         description="Member who you want to try your luck against (don't use this if you use heads/tails)",
                                         option_type=6,
                                         required=False)
                       ])
    async def _coinflip(self, ctx: SlashContext, *, heads_tails=None, member=None):
        if heads_tails is not None and member is not None:
            await ctx.send(embed=nextcord.Embed(title="I told you not to use both options together smh",
                                                color=nextcord.Color.random()))
            return

        elif heads_tails is None and member is None:
            option = None

        else:
            if heads_tails is not None:
                option = heads_tails
            else:
                option = member
        r = random.choice(['heads', 'tails'])
        try:
            option = await commands.MemberConverter().convert(ctx, option)
        except:
            pass

        if option is None:
            embed = nextcord.Embed(
                title=f"I flipped a coin",
                description=f"and got a {r.replace('s', '')}.",
                color=nextcord.Color.random()
            )
            await ctx.send(embed=embed)

        elif type(option) is nextcord.Member:
            def check(answer):
                return answer.author == ctx.author or answer.author == option and answer.channel == ctx.channel

            await ctx.send(embed=nextcord.Embed(
                title=f"So {ctx.author.name} thinks their luck is better than {option.name}",
                description=f"Let's see if their right!\nType heads or tails in the chat now!",
                color=nextcord.Color.random()
            ))
            answer = await self.bot.wait_for("message", check=check)
            while answer.content != 'heads' and answer.content != 'tails':
                await ctx.send(embed=nextcord.Embed(
                    title=f"That's an invalid option {answer.author.name}",
                    description=f"Either heads or tails pls\nTry again",
                    color=nextcord.Color.random()
                ))
                answer = await self.bot.wait_for("message", check=check)
            if r == answer.content:
                await ctx.send(embed=nextcord.Embed(
                    title=f"Hooray! {answer.author.name} wins!",
                    description=f"They seem to be luckier.",
                    color=nextcord.Color.random()
                ))
            else:
                await ctx.send(embed=nextcord.Embed(
                    title=f"Noooo {answer.author.name} lost!",
                    description=f"Bad luck for you ig.",
                    color=nextcord.Color.random()
                ))
        else:
            choice = option.lower()
            if choice == r:
                result = f'You win! :grin:'
                boolean = False
            elif choice != r and choice == 'heads' or choice == 'tails':
                result = f'You lose. :cry:'
                boolean = False
            else:
                result = 'Invalid option. :rolling_eyes:'
                boolean = True

            if boolean is False:
                embed = nextcord.Embed(
                    title=f"{result}",
                    description=f"It was {r}."
                )
                embed.color = nextcord.Color.random()

            elif boolean is True:
                embed = nextcord.Embed(
                    title=f"{result}",
                    description=f"Please enter either heads or tails next time. \nIt was {r}.",
                    color=nextcord.Color.random()
                )
            await ctx.send(embed=embed)

    @commands.command(aliases=['cf', 'cflip', 'coinf'])
    async def coinflip(self, ctx, *, option=None):
        r = random.choice(['heads', 'tails'])
        try:
            option = await commands.MemberConverter().convert(ctx, option)
        except:
            pass
        if option is None:
            embed = nextcord.Embed(
                title=f"I flipped a coin",
                description=f"and got a {r.replace('s', '')}.",
                color=nextcord.Color.random()
            )
            await ctx.send(embed=embed)

        elif type(option) is nextcord.Member:
            def check(answer):
                return answer.author == ctx.author or answer.author == option and answer.channel == ctx.channel

            buttons = [
                create_button(style=ButtonStyle.green, custom_id="heads", label="Heads"),
                create_button(style=ButtonStyle.green, custom_id="tails", label="Tails")
            ]
            action_row = create_actionrow(*buttons)

            await ctx.send(embed=nextcord.Embed(
                title=f"So {ctx.author.name} thinks their luck is better than {option.name}",
                description=f"Let's see if their right!\nClick heads or tails now!",
                color=nextcord.Color.random()
            ), components=[action_row])
            answer = await self.bot.wait_for("message", check=check)
            response: ComponentContext = await wait_for_component(self.bot, components=action_row, timeout=20)
            await response.defer(ignore=True)
            try:
                if response.component['custom_id'] == r:
                    await ctx.send(embed=nextcord.Embed(
                        title=f"Hooray! {answer.author.name} wins!",
                        description=f"They seem to be luckier.",
                        color=nextcord.Color.random()
                    ))
                else:
                    await ctx.send(embed=nextcord.Embed(
                        title=f"Noooo {answer.author.name} lost!",
                        description=f"Bad luck for you ig.",
                        color=nextcord.Color.random()
                    ))
            except asyncio.TimeoutError:
                await ctx.send(title="You are too late",
                               description="The button timed out",
                               color=nextcord.Color.random())

        else:
            choice = option.lower()
            if choice == r:
                result = f'You win! :grin:'
                boolean = False
            elif choice != r and choice == 'heads' or choice == 'tails':
                result = f'You lose. :cry:'
                boolean = False
            else:
                result = 'Invalid option. :rolling_eyes:'
                boolean = True

            if boolean is False:
                embed = nextcord.Embed(
                    title=f"{result}",
                    description=f"It was {r}."
                )
                embed.color = nextcord.Color.random()

            elif boolean is True:
                embed = nextcord.Embed(
                    title=f"{result}",
                    description=f"Please enter either heads or tails next time. \nIt was {r}.",
                    color=nextcord.Color.random()
                )
            await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="dice",
                       description="Rolls a dice, which is useful for bets.",
                       options=[create_option(name="lower", description="Lower limit of your bet",
                                              option_type=4, required=False),
                                create_option(name="upper", description="Upper limit of your bet",
                                              option_type=4, required=False)
                                ])
    async def _dice(self, ctx: SlashContext, lower=0, upper=0):
        def set_image(digit):
            if digit == 1:
                embed.set_image(url="https://www.calculator.net/img/dice1.png")
            if digit == 2:
                embed.set_image(url="https://www.calculator.net/img/dice2.png")
            if digit == 3:
                embed.set_image(url="https://www.calculator.net/img/dice3.png")
            if digit == 4:
                embed.set_image(url="https://www.calculator.net/img/dice4.png")
            if digit == 5:
                embed.set_image(url="https://www.calculator.net/img/dice5.png")
            if digit == 6:
                embed.set_image(url="https://www.calculator.net/img/dice6.png")
            return

        digit = random.randint(1, 6)
        if lower == 0 and upper == 0:
            embed = nextcord.Embed(title=f"I rolled a dice and got {digit}", color=nextcord.Color.random())
            set_image(digit=digit)
            await ctx.send(embed=embed)

        elif lower not in range(1, 7):
            await ctx.send(embed=nextcord.Embed(title=f"It pains me that I have to say this",
                                                description=f"But a dice has 6 numbers\n{lower} isn't one of them",
                                                color=nextcord.Color.random()))

        elif upper not in range(0, 7):
            await ctx.send(embed=nextcord.Embed(title=f"It pains me that I have to say this",
                                                description=f"But a dice has 6 numbers\n{upper} isn't one of them",
                                                color=nextcord.Color.random()))

        elif lower > upper != 0:
            await ctx.send(embed=nextcord.Embed(title=f"Your lower limit cannot be MORE than ur upper limit",
                                                description=f"Unless you change the way numbers work...",
                                                color=nextcord.Color.random()))

        else:
            if upper == 0:
                to_edit = await ctx.send(embed=nextcord.Embed(
                    title=f"You have placed bets on the dice getting the number {lower}",
                    description=f"Rolling dice....",
                    color=nextcord.Color.random()))
                await asyncio.sleep(3)
                if lower == digit:
                    string = "You win! :star_struck:"
                else:
                    string = "You lose :weary:"
            else:
                to_edit = await ctx.send(embed=nextcord.Embed(
                    title=f"You have placed bets on the dice getting a number between {lower} and {upper}",
                    description=f"Rolling dice....",
                    color=nextcord.Color.random()))
                await asyncio.sleep(3)
                if lower <= digit <= upper:
                    string = "You win! :star_struck:"
                    if lower == 1 and upper == 6:
                        string += "... obviously :face_with_raised_eyebrow:"
                else:
                    string = "You lose :weary:"
            embed = nextcord.Embed(
                title=f"You have placed bets on the dice getting a number between {lower} and {upper}",
                description=f"Its a {digit}\n{string}",
                color=nextcord.Color.random())
            set_image(digit=digit)
            await to_edit.edit(embed=embed)

    @commands.command()
    async def dice(self, ctx, lower=0, upper=0):
        def set_image(digit):
            if digit == 1:
                embed.set_image(url="https://www.calculator.net/img/dice1.png")
            if digit == 2:
                embed.set_image(url="https://www.calculator.net/img/dice2.png")
            if digit == 3:
                embed.set_image(url="https://www.calculator.net/img/dice3.png")
            if digit == 4:
                embed.set_image(url="https://www.calculator.net/img/dice4.png")
            if digit == 5:
                embed.set_image(url="https://www.calculator.net/img/dice5.png")
            if digit == 6:
                embed.set_image(url="https://www.calculator.net/img/dice6.png")
            return

        digit = random.randint(1, 6)
        if lower == 0 and upper == 0:
            embed = nextcord.Embed(title=f"I rolled a dice and got {digit}", color=nextcord.Color.random())
            set_image(digit=digit)
            await ctx.send(embed=embed)

        elif lower not in range(1, 7):
            await ctx.send(embed=nextcord.Embed(title=f"It pains me that I have to say this",
                                                description=f"But a dice has 6 numbers\n{lower} isn't one of them",
                                                color=nextcord.Color.random()))

        elif upper not in range(0, 7):
            await ctx.send(embed=nextcord.Embed(title=f"It pains me that I have to say this",
                                                description=f"But a dice has 6 numbers\n{upper} isn't one of them",
                                                color=nextcord.Color.random()))

        elif lower > upper != 0:
            await ctx.send(embed=nextcord.Embed(title=f"Your lower limit cannot be MORE than ur upper limit",
                                                description=f"Unless you change the way numbers work...",
                                                color=nextcord.Color.random()))

        else:
            if upper == 0:
                to_edit = await ctx.send(embed=nextcord.Embed(
                    title=f"You have placed bets on the dice getting the number {lower}",
                    description=f"Rolling dice....",
                    color=nextcord.Color.random()))
                await asyncio.sleep(3)
                if lower == digit:
                    string = "You win! :star_struck:"
                else:
                    string = "You lose :weary:"
            else:
                to_edit = await ctx.send(embed=nextcord.Embed(
                    title=f"You have placed bets on the dice getting a number between {lower} and {upper}",
                    description=f"Rolling dice....",
                    color=nextcord.Color.random()))
                await asyncio.sleep(3)
                if lower <= digit <= upper:
                    string = "You win! :star_struck:"
                    if lower == 1 and upper == 6:
                        string += "... obviously :face_with_raised_eyebrow:"
                else:
                    string = "You lose :weary:"
            embed = nextcord.Embed(
                title=f"You have placed bets on the dice getting a number between {lower} and {upper}",
                description=f"Its a {digit}\n{string}",
                color=nextcord.Color.random())
            set_image(digit=digit)
            await to_edit.edit(embed=embed)

    @commands.cooldown(1, 20, commands.BucketType.user)
    @cog_ext.cog_slash(name="guess",
                       description="Lets you guess a number within any range.",
                       options=[create_option(name="lower",
                                              description="The lowest possible number that I should give you to guess",
                                              option_type=4,
                                              required=True),
                                create_option(name="upper",
                                              description="The upper possible number that I should give you to guess",
                                              option_type=4,
                                              required=True)
                                ]
                       )
    async def _guess(self, ctx: SlashContext, lower, upper):
        boolean = False
        lower = int(lower)
        upper = int(upper)
        if upper < lower:
            embed = nextcord.Embed(title="Nope :satisfied:",
                                   description="Your upper limit CANNOT BE less then your lower limit smh")
            embed.set_footer(text="Like, wth dude")
            embed.color = nextcord.Color.random()
            await ctx.send(embed=embed)
            return
        if upper == lower:
            embed = nextcord.Embed(title="Nope :satisfied:",
                                   description="Think about it.\nIf your lower limit is the same as the upper limit, you can't really guess anything.")
            embed.set_footer(text=f"Basically, its obviously {upper} rn")
            embed.color = nextcord.Color.random()
            await ctx.send(embed=embed)
            return
        if lower < 0:
            embed = nextcord.Embed(title="Nope :satisfied:",
                                   description="Your limits can only be positive numbers.")
            embed.set_footer(text="Dont' even THINK about it")
            await ctx.send(embed=embed)
            embed.color = nextcord.Color.random()
            return
        if upper > 10000:
            embed = nextcord.Embed(title="Nope :satisfied:",
                                   description="Your upper limit can only be equal to or less than 10000.")
            embed.set_footer(text="Dont' even THINK about it")
            embed.color = nextcord.Color.random()
            await ctx.send(embed=embed)
            return
        x = random.randint(lower, upper)
        embed = nextcord.Embed(
            title=f"You have {round(math.log(upper - lower + 1, 2))} chances to guess the number!",
            description="Good Luck :thumbsup:"
        )
        embed.color = nextcord.Color.random()
        await ctx.send(embed=embed)
        count = 1

        while count <= round(math.log(upper - lower + 1, 2)):
            count += 1

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            msg = await self.bot.wait_for("message", check=check)
            guess = int(str(msg.content))

            if x == guess:
                embed = nextcord.Embed(
                    title=f"You did it! :partying_face:",
                    description=f"You have guessed the number!\n It was {x}"
                )
                embed.color = nextcord.Color.random()
                await ctx.send(embed=embed)
                boolean = True
                break

            elif x > guess:
                if (round(math.log(upper - lower + 1, 2)) - count + 1) == 0:
                    break
                embed = nextcord.Embed(
                    title=f"You guessed too low! :arrow_down:",
                    description=f"You have {round(math.log(upper - lower + 1, 2)) - count + 1} remaining!"
                )
                embed.color = nextcord.Color.random()
                await ctx.send(embed=embed)

            elif x < guess:
                if (round(math.log(upper - lower + 1, 2)) - count + 1) == 0:
                    break
                embed = nextcord.Embed(
                    title=f"You guessed too high! :arrow_up:",
                    description=f"You have {round(math.log(upper - lower + 1, 2)) - count + 1} remaining!"
                )
                embed.color = nextcord.Color.random()
                await ctx.send(embed=embed)

            if round(math.log(upper - lower + 1, 2)) - count + 1 == 0:
                break

        if boolean is False:
            embed = nextcord.Embed(title="Better luck next time!",
                                   description=f"The number was {x}")
            embed.color = nextcord.Color.random()
            await ctx.send(embed=embed)

    @commands.command(aliases=['g'])
    async def guess(self, ctx, lower, upper):
        boolean = False
        lower = int(lower)
        upper = int(upper)
        if upper < lower:
            embed = nextcord.Embed(title="Nope :satisfied:",
                                   description="Your upper limit CANNOT BE less then your lower limit smh")
            embed.set_footer(text="Like, wth dude")
            embed.color = nextcord.Color.random()
            await ctx.send(embed=embed)
            return
        if upper == lower:
            embed = nextcord.Embed(title="Nope :satisfied:",
                                   description="Think about it.\nIf your lower limit is the same as the upper limit, you can't really guess anything.")
            embed.set_footer(text=f"Basically, its obviously {upper} rn")
            embed.color = nextcord.Color.random()
            await ctx.send(embed=embed)
            return
        if lower < 0:
            embed = nextcord.Embed(title="Nope :satisfied:",
                                   description="Your limits can only be positive numbers.")
            embed.set_footer(text="Dont' even THINK about it")
            await ctx.send(embed=embed)
            embed.color = nextcord.Color.random()
            return
        if upper > 10000:
            embed = nextcord.Embed(title="Nope :satisfied:",
                                   description="Your upper limit can only be equal to or less than 10000.")
            embed.set_footer(text="Dont' even THINK about it")
            embed.color = nextcord.Color.random()
            await ctx.send(embed=embed)
            return
        x = random.randint(lower, upper)
        embed = nextcord.Embed(
            title=f"You have {round(math.log(upper - lower + 1, 2))} chances to guess the number!",
            description="Good Luck :thumbsup:"
        )
        embed.color = nextcord.Color.random()
        await ctx.send(embed=embed)
        count = 1

        while count <= round(math.log(upper - lower + 1, 2)):
            count += 1

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            msg = await self.bot.wait_for("message", check=check)
            guess = int(str(msg.content))

            if x == guess:
                embed = nextcord.Embed(
                    title=f"You did it! :partying_face:",
                    description=f"You have guessed the number!\n It was {x}"
                )
                embed.color = nextcord.Color.random()
                await ctx.send(embed=embed)
                boolean = True
                break

            elif x > guess:
                if (round(math.log(upper - lower + 1, 2)) - count + 1) == 0:
                    break
                embed = nextcord.Embed(
                    title=f"You guessed too low! :arrow_down:",
                    description=f"You have {round(math.log(upper - lower + 1, 2)) - count + 1} remaining!"
                )
                embed.color = nextcord.Color.random()
                await ctx.send(embed=embed)

            elif x < guess:
                if (round(math.log(upper - lower + 1, 2)) - count + 1) == 0:
                    break
                embed = nextcord.Embed(
                    title=f"You guessed too high! :arrow_up:",
                    description=f"You have {round(math.log(upper - lower + 1, 2)) - count + 1} remaining!"
                )
                embed.color = nextcord.Color.random()
                await ctx.send(embed=embed)

            if round(math.log(upper - lower + 1, 2)) - count + 1 == 0:
                break

        if boolean is False:
            embed = nextcord.Embed(title="Better luck next time!",
                                   description=f"The number was {x}")
            embed.color = nextcord.Color.random()
            await ctx.send(embed=embed)  # whats popping

    @cog_ext.cog_slash(name="rps",
                       description="Find out if you can get the imposter in time!",
                       options=[create_option(name="rock_paper_scissor",
                                              description="Rock/Paper/Scissors: what you want to use against me",
                                              option_type=3,
                                              required=False),
                                create_option(name="member",
                                              description="Member who you want to play oddeve against",
                                              option_type=6,
                                              required=False)])
    async def _rps(self, ctx: SlashContext, *, rock_paper_scissor=None, member=None):
        if rock_paper_scissor is not None and member is not None:
            await ctx.send(embed=nextcord.Embed(title="I told you not to use both options together smh",
                                                color=nextcord.Color.random()))
            return

        elif rock_paper_scissor is None and member is None:
            msg = None

        else:
            if rock_paper_scissor is not None:
                msg = rock_paper_scissor
            else:
                msg = member

        if msg is None:
            await ctx.send(embed=nextcord.Embed(title="You might wanna", description="CHOOSE SOMETHING!!",
                                                color=nextcord.Color.random()))

            return

        if isinstance(msg, str):
            t = ["rock", "paper", "scissors"]
            computer = t[random.randint(0, 2)]
            player = msg.lower()
            if player == computer:
                embed = nextcord.Embed(
                    title="Tie",
                    description=f"I played {player} too!")
                embed.color = nextcord.Color.random()
                embed.set_footer(text="Its not over yet...")
                await ctx.send(embed=embed)

            elif player == "rock" or player == "r":
                if computer == "paper":
                    embed = nextcord.Embed(
                        title="You lose!",
                        description=f"{t[1]} covers {t[0]}".format(computer, player))
                    embed.color = nextcord.Color.random()
                    embed.set_footer(text="Sad life 4 u...")
                    await ctx.send(embed=embed)
                else:
                    embed = nextcord.Embed(
                        title="You win!",
                        description=f"{t[0]} breaks {t[2]}".format(player, computer))
                    embed.color = nextcord.Color.random()
                    embed.set_footer(text="GG")
                    await ctx.send(embed=embed)

            elif player == "paper" or player == "p":
                if computer == "scissors":
                    embed = nextcord.Embed(
                        title="You lose!",
                        description=f"{t[2]} cut {t[1]}".format(computer, player))
                    embed.color = nextcord.Color.random()
                    embed.set_footer(text="Sad life 4 u...")
                    await ctx.send(embed=embed)
                else:
                    embed = nextcord.Embed(
                        title="You win!",
                        description=f"{t[1]} covers {t[0]}".format(player, computer))
                    embed.color = nextcord.Color.random()
                    embed.set_footer(text="GG")  # dont test yet im almost done too
                    await ctx.send(embed=embed)

            elif player == "scissors" or player == "s" or player == "s":
                if computer == "rock":
                    embed = nextcord.Embed(
                        title="You lose!",
                        description=f"{t[0]} breaks {t[2]}".format(computer, player))
                    embed.color = nextcord.Color.random()
                    embed.set_footer(text="Sad life 4 u...")
                    await ctx.send(embed=embed)
                else:
                    embed = nextcord.Embed(
                        title="You win!",
                        description=f"{t[2]} cut {t[1]}".format(player, computer))
                    embed.color = nextcord.Color.random()
                    embed.set_footer(text="GG")
                    await ctx.send(embed=embed)

            else:
                embed = nextcord.Embed(
                    title="What the hell bruh",
                    description=f"You have managed to put an invalid option in rock paper scissors. :rolling_eyes:")
                embed.color = nextcord.Color.random()
                embed.set_footer(text="Imagine having just 3 brain cells")
                await ctx.send(embed=embed)

        elif isinstance(msg, nextcord.Member):
            embed1 = nextcord.Embed(
                title=f"Hello!! So you have challenged {msg.name} to an epic rock paper scissor battle!",
                description="Enter your choice from Rock, Paper, Scissors here",
                color=nextcord.Color.random())
            embed2 = nextcord.Embed(
                title=f"Hello! So you have been challenged by {ctx.author.name} to an epic rock paper scissor battle!",
                description="Enter your choice from Rock, Paper or Scissors here (if you wanna play)",
                color=nextcord.Color.random())
            embed2.set_footer(text="Otherwise just ignore me like everyone else (SOB SOB)")
            if msg.bot:
                embed = nextcord.Embed(title=f"This is a bot.",
                                       description=f"I seriously don't know how you expect a bot to play rock paper scissors with you WHEN IT CAN'T EVEN DM YOU BACK",
                                       color=nextcord.Color.random())
                embed.set_footer(text="People expect too much from my kind")
                await ctx.send(embed=embed)
                return

            if msg == ctx.author:
                embed = nextcord.Embed(title=f"Oh you lonely kid",
                                       description=f"If you got no friends to play with, try `{ctx.prefix}rock` or something",
                                       color=nextcord.Color.random())
                embed.set_footer(text="People expect too much from my kind")
                await ctx.send(embed=embed)
                return

            await msg.send(embed=embed2)
            await ctx.author.send(embed=embed1)
            await ctx.send("<a:ZO_DMS:871341236236193792>")

            def check1(message):
                return message.author == ctx.author and str(message.channel.type) == "private"

            def check2(message):
                return message.author == msg and str(message.channel.type) == "private"

            try:
                reply1 = await self.bot.wait_for('message', check=check1, timeout=60)
                reply2 = await self.bot.wait_for('message', check=check2, timeout=60)
                player = reply2.content.lower()
                challenger = reply1.content.lower()
                player_name = msg.name
                challenger_name = ctx.author.name
                if player == challenger:
                    embed = nextcord.Embed(
                        title="Tie",
                        description=f"Both played {player}!")
                    embed.color = nextcord.Color.random()
                    embed.set_footer(text="Its not over yet...")
                    await ctx.send(embed=embed)

                elif player == "rock" or player == "r":
                    if challenger == "paper" or challenger == "p":
                        embed = nextcord.Embed(
                            title=f"{challenger_name} wins!",
                            description=f"Paper[{challenger_name}] covers Rock[{player_name}]!!")
                        embed.color = nextcord.Color.random()
                        embed.set_footer(text=f"Sad life {player_name}...")
                        await ctx.send(embed=embed)
                    else:
                        embed = nextcord.Embed(
                            title=f"{player_name} wins!",
                            description=f"Rock[{player_name}] breaks Scissors[{challenger_name}]!!")
                        embed.color = nextcord.Color.random()
                        embed.set_footer(text=f"Sad life {challenger_name}...")
                        await ctx.send(embed=embed)

                elif player == "paper" or player == "p":
                    if challenger == "scissors" or challenger == "s" or challenger == "scissor":
                        embed = nextcord.Embed(
                            title=f"{challenger_name} wins!",
                            description=f"Scissors[{challenger_name}] cut paper[{player_name}]!!")
                        embed.color = nextcord.Color.random()
                        embed.set_footer(text=f"Sad life {player_name}...")
                        await ctx.send(embed=embed)
                    else:
                        embed = nextcord.Embed(
                            title=f"{player_name} wins!",
                            description=f"Paper[{player_name}] covers rock[{challenger_name}]!!")
                        embed.color = nextcord.Color.random()
                        embed.set_footer(text=f"Sad life {challenger_name}...")
                        await ctx.send(embed=embed)

                elif player == "scissors" or player == "s" or player == "scissor":
                    if challenger == "rock" or challenger == "r":
                        embed = nextcord.Embed(
                            title=f"{challenger_name} wins!",
                            description=f"Rock[{challenger_name}] breaks scissors[{player_name}]!!")
                        embed.color = nextcord.Color.random()
                        embed.set_footer(text=f"Sad life {player_name}...")
                        await ctx.send(embed=embed)
                    else:
                        embed = nextcord.Embed(
                            title=f"{player_name} wins!",
                            description=f"Scissors[{player_name}] cut paper[{challenger_name}]!!")
                        embed.color = nextcord.Color.random()
                        embed.set_footer(text=f"Sad life {challenger_name}...")
                        await ctx.send(embed=embed)

                else:
                    embed = nextcord.Embed(
                        title="Well either you dont want to play or you have not spelled correctly",
                        description=f"Why are you like this.... :rolling_eyes:")
                    embed.color = nextcord.Color.random()
                    embed.set_footer(text="Imagine being such a spoil sport")
                    await ctx.send(embed=embed)

            except asyncio.TimeoutError:
                await ctx.send(embed=nextcord.Embed(title="That kid didn't answer in time",
                                                    description="THEY IGNORED MEEEEE <a:ZO_Cry:871340549725102081>",
                                                    color=nextcord.Color.random()))

        else:
            await ctx.send(embed=nextcord.Embed(title="You might wanna", description="CHOOSE SOMETHING USEFUL",
                                                color=nextcord.Color.random()))

    @commands.command()
    async def rps(self, ctx, *, msg=None):
        if msg is None:
            await ctx.send(embed=nextcord.Embed(title="You might wanna", description="CHOOSE SOMETHING!!",
                                                color=nextcord.Color.random()))

            return

        if '@' in msg:
            msg = await commands.MemberConverter().convert(ctx, msg)

        if isinstance(msg, str):
            t = ["rock", "paper", "scissors"]
            computer = t[random.randint(0, 2)]
            player = msg.lower()
            if player == computer:
                embed = nextcord.Embed(
                    title="Tie",
                    description=f"I played {player} too!")
                embed.color = nextcord.Color.random()
                embed.set_footer(text="Its not over yet...")
                await ctx.send(embed=embed)

            elif player == "rock" or player == "r":
                if computer == "paper":
                    embed = nextcord.Embed(
                        title="You lose!",
                        description=f"{t[1]} covers {t[0]}".format(computer, player))
                    embed.color = nextcord.Color.random()
                    embed.set_footer(text="Sad life 4 u...")
                    await ctx.send(embed=embed)
                else:
                    embed = nextcord.Embed(
                        title="You win!",
                        description=f"{t[0]} breaks {t[2]}".format(player, computer))
                    embed.color = nextcord.Color.random()
                    embed.set_footer(text="GG")
                    await ctx.send(embed=embed)

            elif player == "paper" or player == "p":
                if computer == "scissors":
                    embed = nextcord.Embed(
                        title="You lose!",
                        description=f"{t[2]} cut {t[1]}".format(computer, player))
                    embed.color = nextcord.Color.random()
                    embed.set_footer(text="Sad life 4 u...")
                    await ctx.send(embed=embed)
                else:
                    embed = nextcord.Embed(
                        title="You win!",
                        description=f"{t[1]} covers {t[0]}".format(player, computer))
                    embed.color = nextcord.Color.random()
                    embed.set_footer(text="GG")  # dont test yet im almost done too
                    await ctx.send(embed=embed)

            elif player == "scissors" or player == "s" or player == "s":
                if computer == "rock":
                    embed = nextcord.Embed(
                        title="You lose!",
                        description=f"{t[0]} breaks {t[2]}".format(computer, player))
                    embed.color = nextcord.Color.random()
                    embed.set_footer(text="Sad life 4 u...")
                    await ctx.send(embed=embed)
                else:
                    embed = nextcord.Embed(
                        title="You win!",
                        description=f"{t[2]} cut {t[1]}".format(player, computer))
                    embed.color = nextcord.Color.random()
                    embed.set_footer(text="GG")
                    await ctx.send(embed=embed)

            else:
                embed = nextcord.Embed(
                    title="What the hell bruh",
                    description=f"You have managed to put an invalid option in rock paper scissors. :rolling_eyes:")
                embed.color = nextcord.Color.random()
                embed.set_footer(text="Imagine having just 3 brain cells")
                await ctx.send(embed=embed)

        elif isinstance(msg, nextcord.Member):
            embed1 = nextcord.Embed(
                title=f"Hello!! So you have challenged {msg.name} to an epic rock paper scissor battle!",
                description="Enter your choice from Rock,Paper,Scissors here",
                color=nextcord.Color.random())
            embed2 = nextcord.Embed(
                title=f"Hello! So you have been challenged by {ctx.author.name} to an epic rock paper scissor battle!",
                description="Enter your choice from Rock, Paper or Scissors here (if you wanna play)",
                color=nextcord.Color.random())
            embed2.set_footer(text="Otherwise just ignore me like everyone else (SOB SOB)")
            if msg.bot:
                embed = nextcord.Embed(title=f"This is a bot.",
                                       description=f"I seriously don't know how you expect a bot to play rock paper scissors with you WHEN IT CAN'T EVEN DM YOU BACK",
                                       color=nextcord.Color.random())
                embed.set_footer(text="People expect too much from my kind")
                await ctx.send(embed=embed)
                return

            if msg == ctx.author:
                embed = nextcord.Embed(title=f"Oh you lonely kid",
                                       description=f"If you got no friends to play with, try `{ctx.prefix}rock` or something",
                                       color=nextcord.Color.random())
                embed.set_footer(text="People expect too much from my kind")
                await ctx.send(embed=embed)
                return

            await msg.send(embed=embed2)
            await ctx.author.send(embed=embed1)
            await ctx.send("<a:ZO_DMS:871341236236193792>")

            def check1(message):
                return message.author == ctx.author and str(message.channel.type) == "private"

            def check2(message):
                return message.author == msg and str(message.channel.type) == "private"

            try:
                reply1 = await self.bot.wait_for('message', check=check1, timeout=60)
                reply2 = await self.bot.wait_for('message', check=check2, timeout=60)
                player = reply2.content.lower()
                challenger = reply1.content.lower()
                player_name = msg.name
                challenger_name = ctx.author.name
                if player == challenger:
                    embed = nextcord.Embed(
                        title="Tie",
                        description=f"Both played {player}!")
                    embed.color = nextcord.Color.random()
                    embed.set_footer(text="Its not over yet...")
                    await ctx.send(embed=embed)

                elif player == "rock" or player == "r":
                    if challenger == "paper" or challenger == "p":
                        embed = nextcord.Embed(
                            title=f"{challenger_name} wins!",
                            description=f"Paper[{challenger_name}] covers Rock[{player_name}]!!")
                        embed.color = nextcord.Color.random()
                        embed.set_footer(text=f"Sad life {player_name}...")
                        await ctx.send(embed=embed)
                    else:
                        embed = nextcord.Embed(
                            title=f"{player_name} wins!",
                            description=f"Rock[{player_name}] breaks Scissors[{challenger_name}]!!")
                        embed.color = nextcord.Color.random()
                        embed.set_footer(text=f"Sad life {challenger_name}...")
                        await ctx.send(embed=embed)

                elif player == "paper" or player == "p":
                    if challenger == "scissors" or challenger == "s" or challenger == "scissor":
                        embed = nextcord.Embed(
                            title=f"{challenger_name} wins!",
                            description=f"Scissors[{challenger_name}] cut paper[{player_name}]!!")
                        embed.color = nextcord.Color.random()
                        embed.set_footer(text=f"Sad life {player_name}...")
                        await ctx.send(embed=embed)
                    else:
                        embed = nextcord.Embed(
                            title=f"{player_name} wins!",
                            description=f"Paper[{player_name}] covers rock[{challenger_name}]!!")
                        embed.color = nextcord.Color.random()
                        embed.set_footer(text=f"Sad life {challenger_name}...")
                        await ctx.send(embed=embed)

                elif player == "scissors" or player == "s" or player == "scissor":
                    if challenger == "rock" or challenger == "r":
                        embed = nextcord.Embed(
                            title=f"{challenger_name} wins!",
                            description=f"Rock[{challenger_name}] breaks scissors[{player_name}]!!")
                        embed.color = nextcord.Color.random()
                        embed.set_footer(text=f"Sad life {player_name}...")
                        await ctx.send(embed=embed)
                    else:
                        embed = nextcord.Embed(
                            title=f"{player_name} wins!",
                            description=f"Scissors[{player_name}] cut paper[{challenger_name}]!!")
                        embed.color = nextcord.Color.random()
                        embed.set_footer(text=f"Sad life {challenger_name}...")
                        await ctx.send(embed=embed)

                else:
                    embed = nextcord.Embed(
                        title="Well either you dont want to play or you have not spelled correctly",
                        description=f"Why are you like this.... :rolling_eyes:")
                    embed.color = nextcord.Color.random()
                    embed.set_footer(text="Imagine being such a spoil sport")
                    await ctx.send(embed=embed)

            except asyncio.TimeoutError:
                await ctx.send(embed=nextcord.Embed(title="That kid didn't answer in time",
                                                    description="THEY IGNORED MEEEEE <a:ZO_Cry:871340549725102081>",
                                                    color=nextcord.Color.random()))

        else:
            await ctx.send(embed=nextcord.Embed(title="You might wanna", description="CHOOSE SOMETHING USEFUL",
                                                color=nextcord.Color.random()))

    @cog_ext.cog_slash(name="oddeve",
                       description="Find out if you can get the imposter in time!",
                       options=[create_option(name="odd_eve",
                                              description="Odd/Eve: what you want to choose against me",
                                              option_type=3,
                                              required=False),
                                create_option(name="member",
                                              description="Member who you want to play oddeve against",
                                              option_type=6,
                                              required=False)]
                       )
    async def _oddeve(self, ctx: SlashContext, *, odd_eve=None, member=None):
        if odd_eve is not None and member is not None:
            await ctx.send(embed=nextcord.Embed(title="I told you not to use both options together smh",
                                                color=nextcord.Color.random()))
            return

        elif odd_eve is None and member is None:
            msg = None

        else:
            if odd_eve is not None:
                msg = odd_eve
            else:
                msg = member

        if msg is None:
            await ctx.send(
                embed=nextcord.Embed(title="You might wanna", description="CHOOSE SOMETHING!!\n try odd or even",
                                     color=nextcord.Color.random()))
            return

        if isinstance(msg, str):
            if msg.lower() == "odd" or msg.lower() == "o":
                euro = "odd"

            elif msg.lower() == "even" or msg.lower() == "e" or msg.lower() == "eve":
                euro = "even"

            else:
                embed = nextcord.Embed(
                    title="What the hell bruh",
                    description=f"You have managed to put an invalid option in odd n even.\nIts either odd or even :rolling_eyes:",
                    color=nextcord.Color.random()
                )
                embed.color = nextcord.Color.random()
                embed.set_footer(text="Imagine having just 3 brain cells")
                await ctx.send(embed=embed)
                return

            await ctx.send(
                embed=nextcord.Embed(title="Please select a number for 0 to 9", color=nextcord.Color.random()))

            def check1(message):
                return message.author == ctx.author

            try:
                msg1 = await self.bot.wait_for('message', check=check1, timeout=60)
                try:
                    num1 = int(msg1.content)
                except:
                    await ctx.send(embed=nextcord.Embed(title="You didn't give a valid NUMBER",
                                                        description="WOW ppl can do lit anything wrong",
                                                        color=nextcord.Color.random()))
                if num1 >= 10 or num1 < 0:
                    await ctx.send(
                        embed=nextcord.Embed(title="WHAT PART OF 0 TO 9 DO YOU NOT UNDERSTAND",
                                             color=nextcord.Color.random()))
                    return

                n = i = 0
                while i < 1:
                    n = random.randint(0, 9)
                    i += 1

                sum = int(num1) + int(n)
                await ctx.send(embed=nextcord.Embed(title=f"I played {n} and you played {num1} and it adds up to {sum}",
                                                    color=nextcord.Color.random()))

                if sum % 2 == 0:
                    if euro == "even":
                        await ctx.send(embed=nextcord.Embed(title="Result is even", description="You win! \n GGs",
                                                            color=nextcord.Color.random()))

                    else:
                        await ctx.send(embed=nextcord.Embed(title="Result Is even", description="You lose! \n sed leef",
                                                            color=nextcord.Color.random()))

                else:
                    if euro == "even":
                        await ctx.send(embed=nextcord.Embed(title="Result Is Odd", description="You lose! \n sed leef",
                                                            color=nextcord.Color.random()))

                    else:
                        await ctx.send(embed=nextcord.Embed(title="Result Is Odd", description="You win! \n GGs",
                                                            color=nextcord.Color.random()))
            except asyncio.exceptions.TimeoutError:
                await ctx.send("Timed out :(")

        elif isinstance(msg, nextcord.Member):
            def check3(message):
                return message.author == ctx.author

            def check1(message):
                return message.author == ctx.author and str(message.channel.type) == "private"

            def check2(message):
                return message.author == msg and str(message.channel.type) == "private"

            if msg.bot:
                embed = nextcord.Embed(title=f"This is a bot.",
                                       description=f"I seriously don't know how you expect a bot to play oddeve with you WHEN IT CAN'T EVEN DM YOU BACK",
                                       color=nextcord.Color.random())
                embed.set_footer(text="People expect too much from my kind")
                await ctx.send(embed=embed)
                return

            if msg == ctx.author:
                embed = nextcord.Embed(title=f"Oh you lonely kid",
                                       description=f"If you got no friends to play with, try `/oddeve` or something",
                                       color=nextcord.Color.random())
                embed.set_footer(text="People expect too much from my kind")
                await ctx.send(embed=embed)
                return

            embed3 = nextcord.Embed(
                title=f"Hey {ctx.author.display_name}, as you have started the match, you get to choose....",
                description="Choose whether you want \"odd\" or \"even\"", color=nextcord.Color.random())
            await ctx.send(embed=embed3)
            try:
                reply3 = await self.bot.wait_for('message', check=check3, timeout=60)
                author_choice = reply3.content.lower()

                if author_choice == "odd" or author_choice == "o":
                    challenger = "odd"
                    player = "even"
                    await ctx.send(f"Alright you have chosen {challenger} so that makes {msg.display_name} {player}")

                elif author_choice == "even" or author_choice == "e":
                    challenger = "even"
                    player = "odd"
                    await ctx.send(f"Alright you have chosen {challenger} so that makes {msg.display_name} {player}")

                else:
                    embed = nextcord.Embed(
                        title="What the hell bruh",
                        description=f"You have managed to put an invalid option in odds n evens Its either odd or even :rolling_eyes:",
                        color=nextcord.Color.random())
                    embed.set_footer(text="Imagine having just 3 brain cells")
                    await ctx.send(embed=embed)
                    return
            except asyncio.TimeoutError:
                await ctx.send(embed=nextcord.Embed(title="You didn't answer in time",
                                                    description="HOW DARE YOU IGNORED ME <a:ZO_Cry:871340549725102081>"))
                return

            embed1 = nextcord.Embed(
                title=f"Hello!! So you have challenged {msg.name} to an epic odds and evens battle!",
                description=f"Enter your number from 0 to 9 here\n And remember, you are {challenger}",
                color=nextcord.Color.random())

            embed2 = nextcord.Embed(
                title=f"Hello!! So you have been challenged by {ctx.author.name} to an odds and evens battle!!",
                description=f"Enter your number from 0 to 9 here(if you wanna play)\n And remember, you are {player}",
                color=nextcord.Color.random())
            embed2.set_footer(text="Otherwise just ignore me like everyone else (SOB SOB)")
            await ctx.send("<a:ZO_DMS:871341236236193792>")
            await ctx.author.send(embed=embed1)
            await msg.send(embed=embed2)

            try:
                reply1 = await self.bot.wait_for('message', check=check1, timeout=60)
                reply2 = await self.bot.wait_for('message', check=check2, timeout=60)
                playerno = int(reply2.content)
                challengerno = int(reply1.content)
                player_name = msg.name
                challenger_name = ctx.author.name

                if playerno >= 10 or playerno < 0 or challengerno >= 10 or challengerno < 0:
                    await ctx.send(embed=nextcord.Embed(title="WHAT PART OF 0 TO 9 DO YOU NOT UNDERSTAND",
                                                        description="You ruined the game man",
                                                        color=nextcord.Color.random()))
                    return

                sum = int(challengerno) + int(playerno)
                await ctx.send(embed=nextcord.Embed(
                    title=f"{challenger_name} played {challengerno} and {player_name} played {playerno} and it adds up to {sum}",
                    color=nextcord.Color.random()))

                if sum % 2 == 0:
                    if player == "even":
                        await ctx.send(
                            embed=nextcord.Embed(title="Result is even", description=f"{player_name} wins! \n Poggers",
                                                 color=nextcord.Color.random()))

                    else:
                        await ctx.send(
                            embed=nextcord.Embed(title="Result Is even",
                                                 description=f"{challenger_name} wins! \n Poggers",
                                                 color=nextcord.Color.random()))

                else:
                    if player == "odd":
                        await ctx.send(
                            embed=nextcord.Embed(title="Result Is Odd", description=f"{player_name} wins! \n Poggers",
                                                 color=nextcord.Color.random()))

                    else:
                        await ctx.send(
                            embed=nextcord.Embed(title="Result Is Odd",
                                                 description=f"{challenger_name} wins! \n Poggers",
                                                 color=nextcord.Color.random()))
            except asyncio.TimeoutError:
                await ctx.send(embed=nextcord.Embed(title="That kid didn't answer in time",
                                                    description="THEY IGNORED MEEEEE <a:ZO_Cry:871340549725102081>"))

        else:
            await ctx.send(embed=nextcord.Embed(title="You might wanna", description="CHOOSE SOMETHING USEFUL",
                                                color=nextcord.Color.random())) @ commands.command(
                aliases=['oddeven', 'oe'])

    @commands.command(aliases=['oe'])
    async def oddeve(self, ctx, *, msg=None):
        if msg is None:
            await ctx.send(
                embed=nextcord.Embed(title="You might wanna", description="CHOOSE SOMETHING!!\n try odd or even",
                                     color=nextcord.Color.random()))
            return

        if '@' in msg:
            msg = await commands.MemberConverter().convert(ctx, msg)

        if isinstance(msg, str):
            if msg.lower() == "odd" or msg.lower() == "o":
                euro = "odd"

            elif msg.lower() == "even" or msg.lower() == "e" or msg.lower() == "eve":
                euro = "even"

            else:
                embed = nextcord.Embed(
                    title="What the hell bruh",
                    description=f"You have managed to put an invalid option in odd n even.\nIts either odd or even :rolling_eyes:",
                    color=nextcord.Color.random()
                )
                embed.color = nextcord.Color.random()
                embed.set_footer(text="Imagine having just 3 brain cells")
                await ctx.send(embed=embed)
                return

            await ctx.send(
                embed=nextcord.Embed(title="Please select a number for 0 to 9", color=nextcord.Color.random()))

            def check1(message):
                return message.author == ctx.author

            try:
                msg1 = await self.bot.wait_for('message', check=check1, timeout=60)
                num1 = int(msg1.content)
                if num1 >= 10 or num1 < 0:
                    await ctx.send(
                        embed=nextcord.Embed(title="WHAT PART OF 0 TO 9 DO YOU NOT UNDERSTAND",
                                             color=nextcord.Color.random()))
                    return

                n = i = 0
                while i < 1:
                    n = random.randint(0, 9)
                    i += 1

                sum = int(num1) + int(n)
                await ctx.send(embed=nextcord.Embed(title=f"I played {n} and you played {num1} and it adds up to {sum}",
                                                    color=nextcord.Color.random()))

                if sum % 2 == 0:
                    if euro == "even":
                        await ctx.send(embed=nextcord.Embed(title="Result is even", description="You win! \n GGs",
                                                            color=nextcord.Color.random()))

                    else:
                        await ctx.send(embed=nextcord.Embed(title="Result Is even", description="You lose! \n sed leef",
                                                            color=nextcord.Color.random()))

                else:
                    if euro == "even":
                        await ctx.send(embed=nextcord.Embed(title="Result Is Odd", description="You lose! \n sed leef",
                                                            color=nextcord.Color.random()))

                    else:
                        await ctx.send(embed=nextcord.Embed(title="Result Is Odd", description="You win! \n GGs",
                                                            color=nextcord.Color.random()))
            except asyncio.exceptions.TimeoutError:
                await ctx.send("Timed out :(")

        elif isinstance(msg, nextcord.Member):
            def check3(message):
                return message.author == ctx.author

            def check1(message):
                return message.author == ctx.author and str(message.channel.type) == "private"

            def check2(message):
                return message.author == msg and str(message.channel.type) == "private"

            if msg.bot:
                embed = nextcord.Embed(title=f"This is a bot.",
                                       description=f"I seriously don't know how you expect a bot to play oddeve with you WHEN IT CAN'T EVEN DM YOU BACK",
                                       color=nextcord.Color.random())
                embed.set_footer(text="People expect too much from my kind")
                await ctx.send(embed=embed)
                return

            if msg == ctx.author:
                embed = nextcord.Embed(title=f"Oh you lonely kid",
                                       description=f"If you got no friends to play with, try `{ctx.prefix}rock` or something",
                                       color=nextcord.Color.random())
                embed.set_footer(text="People expect too much from my kind")
                await ctx.send(embed=embed)
                return

            embed3 = nextcord.Embed(
                title=f"Hey {ctx.author.display_name}, as you have started the match, you get to choose....",
                description="Choose whether you want \"odd\" or \"even\"", color=nextcord.Color.random())
            await ctx.send(embed=embed3)
            try:
                reply3 = await self.bot.wait_for('message', check=check3, timeout=60)
                author_choice = reply3.content.lower()

                if author_choice == "odd" or author_choice == "o":
                    challenger = "odd"
                    player = "even"
                    await ctx.send(f"Alright you have chosen {challenger} so that makes {msg.display_name} {player}")

                elif author_choice == "even" or author_choice == "e":
                    challenger = "even"
                    player = "odd"
                    await ctx.send(f"Alright you have chosen {challenger} so that makes {msg.display_name} {player}")

                else:
                    embed = nextcord.Embed(
                        title="What the hell bruh",
                        description=f"You have managed to put an invalid option in odds n evens Its either odd or even :rolling_eyes:",
                        color=nextcord.Color.random())
                    embed.set_footer(text="Imagine having just 3 brain cells")
                    await ctx.send(embed=embed)
                    return
            except asyncio.TimeoutError:
                await ctx.send(embed=nextcord.Embed(title="You didn't answer in time",
                                                    description="HOW DARE YOU IGNORED ME <a:ZO_Cry:871340549725102081>"))
                return

            embed1 = nextcord.Embed(
                title=f"Hello!! So you have challenged {msg.name} to an epic odds and evens battle!",
                description=f"Enter your number from 0 to 9 here\n And remember, you are {challenger}",
                color=nextcord.Color.random())

            embed2 = nextcord.Embed(
                title=f"Hello!! So you have been challenged by {ctx.author.name} to an odds and evens battle!!",
                description=f"Enter your number from 0 to 9 here(if you wanna play)\n And remember, you are {player}",
                color=nextcord.Color.random())
            embed2.set_footer(text="Otherwise just ignore me like everyone else (SOB SOB)")
            await ctx.send("<a:ZO_DMS:871341236236193792>")
            await ctx.author.send(embed=embed1)
            await msg.send(embed=embed2)

            try:
                reply1 = await self.bot.wait_for('message', check=check1, timeout=60)
                reply2 = await self.bot.wait_for('message', check=check2, timeout=60)
                playerno = int(reply2.content)
                challengerno = int(reply1.content)
                player_name = msg.name
                challenger_name = ctx.author.name

                if playerno >= 10 or playerno < 0 or challengerno >= 10 or challengerno < 0:
                    await ctx.send(embed=nextcord.Embed(title="WHAT PART OF 0 TO 9 DO YOU NOT UNDERSTAND",
                                                        description="You ruined the game man",
                                                        color=nextcord.Color.random()))
                    return

                sum = int(challengerno) + int(playerno)
                await ctx.send(embed=nextcord.Embed(
                    title=f"{challenger_name} played {challengerno} and {player_name} played {playerno} and it adds up to {sum}",
                    color=nextcord.Color.random()))

                if sum % 2 == 0:
                    if player == "even":
                        await ctx.send(
                            embed=nextcord.Embed(title="Result is even", description=f"{player_name} wins! \n Poggers",
                                                 color=nextcord.Color.random()))

                    else:
                        await ctx.send(
                            embed=nextcord.Embed(title="Result Is even",
                                                 description=f"{challenger_name} wins! \n Poggers",
                                                 color=nextcord.Color.random()))

                else:
                    if player == "odd":
                        await ctx.send(
                            embed=nextcord.Embed(title="Result Is Odd", description=f"{player_name} wins! \n Poggers",
                                                 color=nextcord.Color.random()))

                    else:
                        await ctx.send(
                            embed=nextcord.Embed(title="Result Is Odd",
                                                 description=f"{challenger_name} wins! \n Poggers",
                                                 color=nextcord.Color.random()))
            except asyncio.TimeoutError:
                await ctx.send(embed=nextcord.Embed(title="That kid didn't answer in time",
                                                    description="THEY IGNORED MEEEEE <a:ZO_Cry:871340549725102081>"))

        else:
            await ctx.send(embed=nextcord.Embed(title="You might wanna", description="CHOOSE SOMETHING USEFUL",
                                                color=nextcord.Color.random()))

    @cog_ext.cog_slash(name="amogus",
                       description="Find out if you can get the imposter in time!")
    async def _amogus(self, ctx: SlashContext):
        """Impostors can sabotage the reactor,
        which gives Crewmates 30–45 seconds to resolve the sabotage.
        If it is not resolved in the allotted time, The Impostor(s) will win."""

        # determining
        embed1 = nextcord.Embed(title="Who's the imposter?",
                                description="Find out who the imposter is, before the reactor breaks down!",
                                color=nextcord.Color.random())

        # fields
        embed1.add_field(name='Red', value='<:AmongUsRed:891933102912458842>', inline=False)
        embed1.add_field(name='Blue', value='<:AmongUsBlue:891933540512587806>', inline=False)
        embed1.add_field(name='Cyan', value='<:AmongUsCyan:891934003454705715>', inline=False)
        embed1.add_field(name='White', value='<:AmongUsWhite:891934283613220924>', inline=False)

        # sending the message
        msg = await ctx.send(embed=embed1)

        # emojis
        emojis = {
            'Red': '<:AmongUsRed:891933102912458842>',
            'Blue': '<:AmongUsBlue:891933540512587806>',
            'Cyan': '<:AmongUsCyan:891934003454705715>',
            'White': '<:AmongUsWhite:891934283613220924>'
        }

        # who is the imposter?
        imposter = random.choice(list(emojis.items()))
        imposter = imposter[0]

        # for testing...

        # adding choices
        for emoji in emojis.values():
            await msg.add_reaction(emoji)

        # a simple check, whether reacted emoji is in given choises.

        def check(reaction, user):
            return reaction.message.id == msg.id and user == ctx.author and str(reaction.emoji) in emojis.values()

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            await msg.remove_reaction(reaction, user)
            if str(reaction.emoji) == emojis[imposter]:
                description = "**{0}** was the imposter...".format(imposter)
                embed = get_embed("Victory", description, nextcord.Color.blue())
                await ctx.send(embed=embed)

            # defeat
            else:
                for key, value in emojis.items():
                    if value == str(reaction.emoji):
                        description = "**{0}** was not the imposter...\nIt was **{1}**".format(key, imposter)
                        embed = get_embed("Defeat", description, nextcord.Color.red())
                        await ctx.send(embed=embed)
                        break

        except asyncio.TimeoutError:
            # reactor meltdown - defeat
            pass
            description = "Reactor Meltdown. **{0}** was the imposter...".format(imposter)
            embed = get_embed("Defeat. You took too long", description, nextcord.Color.red())
            await ctx.send(embed=embed)

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command(aliases=['amongus', 'sus'])
    async def amogus(self, ctx):
        """Impostors can sabotage the reactor,
        which gives Crewmates 30–45 seconds to resolve the sabotage.
        If it is not resolved in the allotted time, The Impostor(s) will win."""

        # determining
        embed1 = nextcord.Embed(title="Who's the imposter?",
                                description="Find out who the imposter is, before the reactor breaks down!",
                                color=nextcord.Color.random())

        # fields
        embed1.add_field(name='Red', value='<:AmongUsRed:891933102912458842>', inline=False)
        embed1.add_field(name='Blue', value='<:AmongUsBlue:891933540512587806>', inline=False)
        embed1.add_field(name='Cyan', value='<:AmongUsCyan:891934003454705715>', inline=False)
        embed1.add_field(name='White', value='<:AmongUsWhite:891934283613220924>', inline=False)

        # sending the message
        # emojis
        emojis = {
            'Red': '<:AmongUsRed:891933102912458842>',
            'Blue': '<:AmongUsBlue:891933540512587806>',
            'Cyan': '<:AmongUsCyan:891934003454705715>',
            'White': '<:AmongUsWhite:891934283613220924>'
        }

        red = {
            'id': 891933102912458842,
            'name': 'red'
        }

        blue = {
            'id': 891933540512587806,
            'name': "blue"
        }

        cyan = {
            'id': 891934003454705715,
            'name': 'cyan'
        }

        white = {
            'id': 891934283613220924,
            'name': "white"
        }

        # who is the imposter?
        imposter = random.choice(list(emojis.items()))
        imposter = imposter[0]

        # adding choices

        # a simple check, whether reacted emoji is in given choices.
        buttons = [
            create_button(style=ButtonStyle.green, custom_id="<:AmongUsRed:891933102912458842>", emoji=red,
                          disabled=False),
            create_button(style=ButtonStyle.green, custom_id="<:AmongUsBlue:891933540512587806>", emoji=blue,
                          disabled=False),
            create_button(style=ButtonStyle.green, custom_id="<:AmongUsCyan:891934003454705715>", emoji=cyan,
                          disabled=False),
            create_button(style=ButtonStyle.green, custom_id="<:AmongUsWhite:891934283613220924>", emoji=white,
                          disabled=False),
        ]
        action_row = create_actionrow(*buttons)
        msg = await ctx.send(embed=embed1, components=[action_row])

        try:
            response: ComponentContext = await wait_for_component(self.bot, messages=msg,
                                                                  components=action_row, timeout=15)
            if response.component['custom_id'] == emojis[imposter]:
                description = "**{0}** was the imposter...".format(imposter)
                embed = nextcord.Embed(title="Victory", description=description, color=nextcord.Color.blue())
                await ctx.send(embed=embed)

            else:
                for key, value in emojis.items():
                    if value == response.component['custom_id']:
                        description = "**{0}** was not the imposter...\nIt was **{1}**".format(key, imposter)
                        embed = nextcord.Embed(title="Defeat", description=description, color=nextcord.Color.red())
                        await ctx.send(embed=embed)
                        break

            buttons_all_disabled = [
                create_button(style=ButtonStyle.green, custom_id="<:AmongUsRed:891933102912458842>", emoji=red,
                              disabled=True),
                create_button(style=ButtonStyle.green, custom_id="<:AmongUsBlue:891933540512587806>", emoji=blue,
                              disabled=True),
                create_button(style=ButtonStyle.green, custom_id="<:AmongUsCyan:891934003454705715>", emoji=cyan,
                              disabled=True),
                create_button(style=ButtonStyle.green, custom_id="<:AmongUsWhite:891934283613220924>", emoji=white,
                              disabled=True),
            ]
            action_row = create_actionrow(*buttons_all_disabled)
            await response.edit_origin(components=[action_row])

        except asyncio.TimeoutError:
            # reactor meltdown - defeat
            pass
            description = "Reactor Meltdown. **{0}** was the imposter...".format(imposter)
            embed = nextcord.Embed(title="Defeat. You took too long", description=description, color=nextcord.Color.red())
            await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="guessthemovie",
                       description="Will you be able to guess the movie with the emojis I give you?")
    async def _guessthemovie(self, ctx: SlashContext):
        emoji = sample([k for k in self.data], 1)[0]
        movie = self.data[emoji]
        await ctx.channel.send(embed=nextcord.Embed(title="May the one who is worthy\nGuess the movie:",
                                                    description="%s" % emoji,
                                                    color=nextcord.Color.random()))

        def check(msg):
            return not msg.author.bot and \
                   "".join(k for k in msg.content.lower() if k.isalnum()) == "".join(k for k in movie.lower()
                                                                                     if
                                                                                     k.isalnum()) and msg.channel == ctx.channel

        try:
            resp = await self.bot.wait_for("message", timeout=30, check=check)
            embed = nextcord.Embed(title="That's right, %s!" % resp.author.display_name,
                                   description="You've guessed the movie correctly: **%s**." % movie,
                                   color=nextcord.Color.random())
            embed.set_footer(text=f"You get a virtual cookie!")
            await ctx.channel.send(embed=embed)
            ctx.command.reset_cooldown(ctx)
        except asyncio.TimeoutError:
            embed = nextcord.Embed(title="Looks like nobody knew the answer.",
                                   description=f"The movie was **%s**." % movie,
                                   color=nextcord.Color.random())
            embed.set_footer(text=f"The movie got dissed lol")
            await ctx.channel.send(embed=embed)

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(pass_context=True, name="guessthemovie", aliases=['gtm'])
    async def guessthemovie(self, ctx):
        emoji = sample([k for k in self.data], 1)[0]
        movie = self.data[emoji]
        await ctx.channel.send(embed=nextcord.Embed(title="May the one who is worthy\nGuess the movie:",
                                                    description="%s" % emoji,
                                                    color=nextcord.Color.random()))

        def check(msg):
            return not msg.author.bot and \
                   "".join(k for k in msg.content.lower() if k.isalnum()) == "".join(k for k in movie.lower()
                                                                                     if
                                                                                     k.isalnum()) and msg.channel == ctx.channel

        try:
            resp = await self.bot.wait_for("message", timeout=30, check=check)
            embed = nextcord.Embed(title="That's right, %s!" % resp.author.display_name,
                                   description="You've guessed the movie correctly: **%s**." % movie,
                                   color=nextcord.Color.random())
            embed.set_footer(text=f"You get a virtual cookie!")
            await ctx.channel.send(embed=embed)
            ctx.command.reset_cooldown(ctx)
        except asyncio.TimeoutError:
            embed = nextcord.Embed(title="Looks like nobody knew the answer.",
                                   description=f"The movie was **%s**." % movie,
                                   color=nextcord.Color.random())
            embed.set_footer(text=f"The movie got dissed lol")
            await ctx.channel.send(embed=embed)

    @cog_ext.cog_slash(name="whosthatpokemon",
                       description="Test your knowledge of Pokémon!")
    async def _whosthatpokemon(self, ctx: SlashContext):
        number = randint(1, self.total)
        name = self.pokemon_data[str(number)]
        img_url = "https://assets.pokemon.com/assets/cms2/img/pokedex/full/{}.png".format(
            "0" * (3 - len(str(number))) + str(number))
        hint_1 = "".join([c if not c.isalnum() else "*" for c in name])
        letters = [i for i in range(len(name)) if name[i].isalnum()]
        to_delete = set(sample(range(len(letters)), int(len(letters) / 2)))
        letters = [x for i, x in enumerate(letters) if i not in to_delete]
        hint_2 = "".join("*" if k in letters else name[k] for k in range(len(name)))
        embed = nextcord.Embed(title="Who's That Pokémon!", color=nextcord.Color.dark_blue())
        embed.set_image(url=img_url)
        embed.add_field(name="Hint 1", value="`" + hint_1 + "`")
        embed.add_field(name="Time", value="20 seconds")
        embed.set_footer(text="To answer, simply type the name of the pokemon in chat!", icon_url=ctx.author.avatar.url)
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar.url)
        message = await ctx.channel.send(embed=embed)

        async def second():
            await asyncio.sleep(10)
            if message:
                embed.set_field_at(index=0, name="Hint 2", value='`' + hint_2 + '`')
                embed.set_field_at(index=1, name="Time", value="10 seconds")
                await message.edit(embed=embed)

        asyncio.ensure_future(second())

        def check(msg):
            return not msg.author.bot and msg.content.strip().lower().replace(" ", "") == name.lower().replace(" ",
                                                                                                               "") and msg.channel == ctx.channel

        resp = None
        try:
            resp = await self.bot.wait_for('message', timeout=20, check=check)
        except asyncio.TimeoutError:
            embed = nextcord.Embed(title="Time's up, nubs!",
                                   description="The pokemon was **%s**." % name,
                                   color=nextcord.Color.random())
            embed.set_footer(text=f"Get rekt")
            await ctx.channel.send(embed=embed)

        if resp:
            ctx.command.reset_cooldown(ctx)
            try:
                await resp.add_reaction("✅")
            except Exception:
                pass
            embed = nextcord.Embed(title=f"Congratulations {resp.author.display_name}!",
                                   description=f" You've given the correct answer! The pokemon was **%s**." % name,
                                   color=nextcord.Color.green())
            embed.set_thumbnail(url=img_url)
            embed.set_footer(text=f"Game started by {str(ctx.author)}\nWhat a nerd!", icon_url=ctx.author.avatar.url)
            message = await message.edit(embed=embed)

    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.command(pass_context=True, name="whosthatpokemon", aliases=["pokemon", "wtp"])
    async def whosthatpokemon(self, ctx):
        number = randint(1, self.total)
        name = self.pokemon_data[str(number)]
        img_url = "https://assets.pokemon.com/assets/cms2/img/pokedex/full/{}.png".format(
            "0" * (3 - len(str(number))) + str(number))
        hint_1 = "".join([c if not c.isalnum() else "*" for c in name])
        letters = [i for i in range(len(name)) if name[i].isalnum()]
        to_delete = set(sample(range(len(letters)), int(len(letters) / 2)))
        letters = [x for i, x in enumerate(letters) if i not in to_delete]
        hint_2 = "".join("*" if k in letters else name[k] for k in range(len(name)))
        embed = nextcord.Embed(title="Who's That Pokémon!", color=nextcord.Color.dark_blue())
        embed.set_image(url=img_url)
        embed.add_field(name="Hint 1", value="`" + hint_1 + "`")
        embed.add_field(name="Time", value="20 seconds")
        embed.set_footer(text="To answer, simply type the name of the pokemon in chat!", icon_url=ctx.author.avatar.url)
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar.url)
        message = await ctx.channel.send(embed=embed)

        async def second():
            await asyncio.sleep(10)
            if message:
                embed.set_field_at(index=0, name="Hint 2", value='`' + hint_2 + '`')
                embed.set_field_at(index=1, name="Time", value="10 seconds")
                await message.edit(embed=embed)

        asyncio.ensure_future(second())

        def check(msg):
            return msg.author == ctx.author and msg.content.strip().lower().replace(" ", "") == name.lower().replace(
                " ",
                "") and msg.channel == ctx.channel

        resp = None
        try:
            resp = await self.bot.wait_for('message', timeout=20, check=check)
        except asyncio.TimeoutError:
            embed = nextcord.Embed(title="Time's up, nubs!",
                                   description="The pokemon was **%s**." % name,
                                   color=nextcord.Color.random())
            embed.set_footer(text=f"Get rekt")
            await ctx.channel.send(embed=embed)

        if resp:
            ctx.command.reset_cooldown(ctx)
            try:
                await resp.add_reaction("✅")
            except Exception:
                pass
            embed = nextcord.Embed(title=f"Congratulations {resp.author.display_name}!",
                                   description=f" You've given the correct answer! The pokemon was **%s**." % name,
                                   color=nextcord.Color.green())
            embed.set_thumbnail(url=img_url)
            embed.set_footer(text=f"Game started by {str(ctx.author)}\nWhat a nerd!", icon_url=ctx.author.avatar.url)
            message = await message.edit(embed=embed)

    @cog_ext.cog_slash(name="akihelp", description="Help of Akinator")
    async def _akihelp(self, ctx: SlashContext):
        desc_helpme = f'__**HOW TO PLAY**__\n\nUse the `{ctx.prefix}aki` command followed by the game mode you want to play. Here is ' \
                      f'a list of currently available game modes : **people, animals, objects**.\nFor example : `{ctx.prefix}aki people`\n\n__**GAME MODES**__\n\n' \
                      '**People** : This is the game mode for guessing people (fictional or real)\n**Animals** : ' \
                      'This is the game mode for guessing animals\n**Objects** : This is the game mode for guessing objects' \
                      '\n\n__**MISCELLANEOUS**__\n\n**1.**Wait until all emojis are displayed before adding your reaction, or' \
                      ' else it will not register it and you will have to react again once it is done displaying' \
                      '\n**2.**The game ends in 45 seconds if you do not answer the question by reacting with the right' \
                      ' emoji\n**3.** The bot might sometimes be slow, please be patient and wait for it to ask you the questions. If it is stuck, do not worry the game will automatically end in 30 seconds and you can start playing again\n**4.** Only one person can play at a time\n\n' \
                      '__**EMOJI MEANINGS**__\n\n✅ = This emoji means "yes"\n❌ = This emoji means "no"\n🤷 = This emoji means' \
                      '"I do not know"\n👍 = This emoji means "probably"\n👎 = This emoji means "probably not"\n⏮ = This ' \
                      'emoji repeats the question before\n🛑 = This emoji ends the game being played'\
                      'The slash command for akinator DOES NOT EXIST.'

        embed_var_helpme = nextcord.Embed(description=desc_helpme, color=0x00FF00)
        await ctx.send(embed=embed_var_helpme)

    @commands.command()
    async def akihelp(self, ctx):
        desc_helpme = f'__**HOW TO PLAY**__\n\nUse the `{ctx.prefix}aki` command followed by the game mode you want to play. Here is ' \
                      f'a list of currently available game modes : **people, animals, objects**.\nFor example : `{ctx.prefix}aki people`\n\n__**GAME MODES**__\n\n' \
                      '**People** : This is the game mode for guessing people (fictional or real)\n**Animals** : ' \
                      'This is the game mode for guessing animals\n**Objects** : This is the game mode for guessing objects' \
                      '\n\n__**MISCELLANEOUS**__\n\n**1.**Wait until all emojis are displayed before adding your reaction, or' \
                      ' else it will not register it and you will have to react again once it is done displaying' \
                      '\n**2.**The game ends in 45 seconds if you do not answer the question by reacting with the right' \
                      ' emoji\n**3.** The bot might sometimes be slow, please be patient and wait for it to ask you the questions. If it is stuck, do not worry the game will automatically end in 30 seconds and you can start playing again\n**4.** Only one person can play at a time\n\n' \
                      '__**EMOJI MEANINGS**__\n\n✅ = This emoji means "yes"\n❌ = This emoji means "no"\n🤷 = This emoji means' \
                      '"I do not know"\n👍 = This emoji means "probably"\n👎 = This emoji means "probably not"\n⏮ = This ' \
                      'emoji repeats the question before\n🛑 = This emoji ends the game being played'

        embed_var_helpme = nextcord.Embed(description=desc_helpme, color=0x00FF00)
        await ctx.send(embed=embed_var_helpme)

    @commands.command(aliases=['aki'])
    @commands.max_concurrency(1, per=commands.BucketType.guild, wait=False)
    async def akinator(self, ctx, *, extra=None):
        if ctx.channel.id == ctx.channel.id:
            desc_loss = ''
            d_loss = ''

            def check_w(reaction, user):
                return user == ctx.author and str(reaction.emoji) in emojis_w

            buttons: list[dict] = [
                create_button(style=ButtonStyle.blue, custom_id="Yes", label='✅'),
                create_button(style=ButtonStyle.blue, custom_id="No", label='❌'),
                create_button(style=ButtonStyle.blue, custom_id="Idk", label='🤷'),
                create_button(style=ButtonStyle.blue, custom_id="Prolly_Yes", label='👍'),
                create_button(style=ButtonStyle.blue, custom_id="Prolly_No", label='👎'),
                create_button(style=ButtonStyle.blue, custom_id="Previous", label='⏮'),
                create_button(style=ButtonStyle.blue, custom_id="Stop", label='🛑')
            ]
            action_row = spread_to_rows(*buttons, max_in_row=4)
            async with ctx.typing():
                if extra is None:
                    await ctx.send(embed=nextcord.Embed(title=f"Read {ctx.prefix}akihelp smartass",
                                                        description="Otherwise you will not know how to play",
                                                        color=nextcord.Color.random()))
                    return
                elif extra == 'people':
                    q = await aki.start_game(child_mode=True)
                elif extra == 'objects' or extra == 'animals':
                    q = await aki.start_game(language=f'en_{extra}',
                                             child_mode=True)
                else:
                    title_error_three = 'This game mode does not exist'
                    desc_error_three = f'Use **{ctx.prefix}akihelp** to see a list of all the game modes available'
                    embed_var_three = nextcord.Embed(title=title_error_three,
                                                     description=desc_error_three,
                                                     color=0xFF0000)
                    await ctx.reply(embed=embed_var_three)
                    return

                embed_question = nextcord.Embed(
                    title='Tip : Wait until all emojis finish being added before reacting'
                          ' or you will have to unreact and react again',
                    color=0x00FF00)
                await ctx.reply(embed=embed_question)

            while aki.progression <= 85:
                message = await ctx.reply(embed=nextcord.Embed(title=q, color=0xFF0000), components=action_row)

                try:
                    response: Component = await wait_for_component(self.bot, components=action_row, messages=message,
                                                                   timeout=45.0)
                    while response.author != ctx.author:
                        await response.reply("Stop clicking other people's buttons!",hidden=True)
                        response: Component = await wait_for_component(self.bot, components=action_row,
                                                                       messages=message,
                                                                       timeout=45.0)
                    await response.defer(ignore=True)
                except asyncio.TimeoutError:
                    embed_game_ended = nextcord.Embed(
                        title='You took too long, the game has ended',
                        color=0xFF0000)
                    await ctx.reply(embed=embed_game_ended)
                    return

                if response.component['custom_id'] == "Yes":
                    a = 'y'
                elif response.component['custom_id'] == "No":
                    a = 'n'
                elif response.component['custom_id'] == "Idk":
                    a = 'idk'
                elif response.component['custom_id'] == "Prolly_Yes":
                    a = 'p'
                elif response.component['custom_id'] == "Prolly_No":
                    a = 'pn'
                elif response.component['custom_id'] == "Previous":
                    a = 'b'
                elif response.component['custom_id'] == "Stop":
                    embed_game_end = nextcord.Embed(
                        title='I ended the game because you asked me to do it',
                        color=0x00FF00)
                    await ctx.reply(embed=embed_game_end)
                    return

                if a == "b":
                    try:
                        q = await aki.back()
                    except akinator.CantGoBackAnyFurther:
                        pass
                else:
                    q = await aki.answer(a)

            await aki.win()
            buttons_win = [
                create_button(style=ButtonStyle.blue, custom_id="Yes", label="✅",
                              disabled=False),
                create_button(style=ButtonStyle.blue, custom_id="No", label="❌",
                              disabled=False),
            ]
            action_row2 = create_actionrow(*buttons_win)

            wm = await ctx.reply(
                embed=w(aki.first_guess['name'], aki.first_guess['description'],
                        aki.first_guess['absolute_picture_path']),
                components=[action_row2])

            try:
                response: ComponentContext = await wait_for_component(self.bot, components=action_row2, messages=wm, timeout=20)
                while response.author != ctx.author:
                    await response.reply("Stop trying to press other people's buttons fool",hidden=True)
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row2, messages=wm, timeout=20)
            except asyncio.TimeoutError:
                for times in aki.guesses:
                    d_loss = d_loss + times['name'] + '\n'
                t_loss = f'Here is a list of all the {extra} I had in mind :'
                embed_loss = nextcord.Embed(title=t_loss,
                                            description=d_loss,
                                            color=0xFF0000)
                await ctx.reply(embed=embed_loss)
                return

            if response.component['custom_id'] == "Yes":
                embed_win = nextcord.Embed(
                    title='Great! I guessed correctly yet again!', color=0x00FF00)
                await ctx.reply(embed=embed_win)
            elif response.component['custom_id'] == "No":
                for times in aki.guesses:
                    desc_loss = desc_loss + times['name'] + '\n'
                title_loss = 'No problem, I will win next time! But here is a list of all the people I had in mind :'
                embed_loss = nextcord.Embed(title=title_loss,
                                            description=desc_loss,
                                            color=0xFF0000)
                await ctx.reply(embed=embed_loss)
        else:
            right_channel = self.bot.get_channel(ctx.channel.id)
            channel_mention = right_channel.mention
            wrong_channel = nextcord.Embed(
                title='You can only play in the following channel ' +
                      channel_mention,
                color=0xFF0000)
            await ctx.reply(embed=wrong_channel)

    @akinator.error
    async def aki_error(self, ctx, error: commands.CommandError):
        if isinstance(error, commands.MaxConcurrencyReached):
            title_error_four = 'Someone is already using Akinator on this server'
            desc_error_four = 'Please wait until the person currently playing is done with their turn'
            embed_var_four = nextcord.Embed(title=title_error_four,
                                            description=desc_error_four,
                                            color=0xFF0000)
            await ctx.reply(embed=embed_var_four)

    @guessthemovie.error
    async def gtm_error(self, ctx, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=nextcord.Embed(title=f"Slow down bro. Try after {round(error.retry_after)} seconds",
                                                color=nextcord.Color.random()))

    @whosthatpokemon.error
    async def pokemon_error(self, ctx, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=nextcord.Embed(title=f"Slow down bro. Try after {round(error.retry_after)} seconds",
                                                color=nextcord.Color.random()))

    @amogus.error
    async def amogus_error(self, ctx, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=nextcord.Embed(title=f"Slow down bro. Try after {round(error.retry_after)} seconds",
                                                color=nextcord.Color.random()))

    @dice.error
    async def dice_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = nextcord.Embed(title="Please u can only give numbers between 1 and 6",
                                   description="It is the unfortunate limitation of a dice",
                                   color=nextcord.Color.random())
            embed.set_footer(text="When board games get replaced by online games...")
            await ctx.send(embed=embed)

        else:
            raise error

    @rps.error
    async def rps_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed = nextcord.Embed(title=f"Ok no",
                                   description=f"Reminding you that playing rps with an imaginary user is not allowed.... Just play singleplayer mate",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Kids these days...")
            await ctx.send(embed=embed)

        else:
            raise error

    @oddeve.error
    async def oddeve_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed = nextcord.Embed(title=f"Ok no",
                                   description=f"Reminding you that playing with an imaginary user is not allowed.... Just play singleplayer mate",
                                   color=nextcord.Color.random())

            embed.set_footer(text="Kids these days...")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.errors.CommandInvokeError):
            embed = nextcord.Embed(title=f"No shit",
                                   description=f"I take numbers only for your choice",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Kids these days...")
            await ctx.send(embed=embed)

        else:
            raise error

    @guess.error
    async def guess_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"Do you want to sit here FOREVER",
                                   description=f"Seriously dude, I need both an upper and a lower limit.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Imagine guessing a number in infinity")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.errors.CommandInvokeError):
            embed = nextcord.Embed(title=f"Do you want to sit here FOREVER",
                                   description=f"Seriously dude, I need it to be in numbers please.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Imagine guessing a number in infinity")
            await ctx.send(embed=embed)

        else:
            raise error


def setup(bot):
    bot.add_cog(Games(bot))
