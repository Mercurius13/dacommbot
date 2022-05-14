import random
from asyncio import TimeoutError
from pathlib import Path
from random import choice
from nextcord import Embed, Message
from nextcord.ext import commands
from random import randint, sample, shuffle
from collections import defaultdict
import nextcord
import asyncio
from discord_slash.model import ButtonStyle
from discord_slash.utils import manage_components
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from discord_slash.utils.manage_commands import create_option, create_choice
from time import time
ALL_WORDS = Path("text_files/hangmanwords.txt").read_text().splitlines()

# Defining a dictionary of images that will be used for the game to represent the hangman person
IMAGES = {
    6: "https://cdn.discordapp.com/attachments/859123972884922418/888133201497837598/hangman0.png",
    5: "https://cdn.discordapp.com/attachments/859123972884922418/888133595259084800/hangman1.png",
    4: "https://cdn.discordapp.com/attachments/859123972884922418/888134194474139688/hangman2.png",
    3: "https://cdn.discordapp.com/attachments/859123972884922418/888133758069395466/hangman3.png",
    2: "https://cdn.discordapp.com/attachments/859123972884922418/888133786724859924/hangman4.png",
    1: "https://cdn.discordapp.com/attachments/859123972884922418/888133828831477791/hangman5.png",
    0: "https://cdn.discordapp.com/attachments/859123972884922418/888133845449338910/hangman6.png",
}


class WordGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        lines = [line.rstrip('\n') for line in open('text_files/searchwords.txt')]
        self.searchwords = defaultdict(list)
        for k in lines:
            self.searchwords[len(k)].append(k)
        self.allwords = [line.rstrip('\n') for line in open('text_files/allwords.txt')]

    def wordfill(self, grid, word, direction):
        possible = []
        if direction == 1:
            for i in range(9):
                for j in range(9 - len(word) + 1):
                    next_route = []
                    flag = True
                    for k in range(len(word)):
                        if grid[i][j + k] in [word[k], "*"]:
                            next_route.append((i, j + k))
                        else:
                            flag = False
                            break
                    if flag:
                        possible.append(next_route)

        if direction == 2:
            for i in range(9 - len(word) + 1):
                for j in range(9):
                    next_route = []
                    flag = True
                    for k in range(len(word)):
                        if grid[i + k][j] in [word[k], "*"]:
                            next_route.append((i + k, j))
                        else:
                            flag = False
                            break
                    if flag:
                        possible.append(next_route)

        if direction == 3:
            for i in range(9 - len(word) + 1):
                for j in range(9 - len(word) + 1):
                    next_route = []
                    flag = True
                    for k in range(len(word)):
                        if grid[i + k][j + k] in [word[k], "*"]:
                            next_route.append((i + k, j + k))
                        else:
                            flag = False
                            break
                    if flag:
                        possible.append(next_route)

        return possible

    def generate_grid(self, wordlist):
        wordgrid = []
        skipped = []
        for row in range(9):
            wordgrid.append([])
            for col in range(9):
                wordgrid[row].append("*")
        for word in wordlist:
            word = word.upper()
            routes = self.wordfill(wordgrid, word, randint(1, 3))
            if not routes:
                skipped.append(word)
                continue
            else:
                route = sample(routes, 1)[0]
                for k in range(len(word)):
                    wordgrid[route[k][0]][route[k][1]] = word[k]

        for i in range(9):
            for j in range(9):
                if wordgrid[i][j] == "*":
                    wordgrid[i][j] = chr(randint(65, 90))

        return wordgrid, skipped

    def check_word(self, word, line_grid):
        for i in range(81):
            if line_grid[i] == word[0]:
                that_row = line_grid[9 * int(i / 9):9 * (int(i / 9) + 1)]
                that_col = "".join(line_grid[i % 9 + 9 * k] for k in range(9))
                that_diagonal = "".join(line_grid[i + 10 * k] for k in range(9) if i + 10 * k < 81)
                that_diagonal = that_diagonal[:(9 - i % 9)]
                another_diagonal = "".join(line_grid[i + 8 * k] for k in range(9) if i + 8 * k < 81)
                another_diagonal = another_diagonal[:(1 + i % 9)]
                if word in that_row or word in that_col or word in that_diagonal or word in another_diagonal:
                    return True
        return False

    @staticmethod
    def create_embed(tries: int, user_guess: str) -> Embed:
        """
        Helper method that creates the embed where the game information is shown.
        This includes how many letters the user has guessed so far, and the hangman photo itself.
        """
        hangman_embed = Embed(
            title="Hangman",
            color=nextcord.Color.blue(),
        )
        hangman_embed.set_image(url=IMAGES[tries])
        hangman_embed.add_field(
            name=f"You've guessed `{user_guess}` so far.",
            value="Guess the word by sending a message with a letter!"
        )
        hangman_embed.set_footer(text=f"Tries remaining: {tries}")
        return hangman_embed

    @commands.cooldown(1, 75, commands.BucketType.channel)
    @commands.command(pass_context=True, name="wordhunt", aliases=['wh', 'wordsearch'])
    async def wordhunt(self, ctx):
        long_words = sample(self.searchwords[6], randint(1, 2)) + sample(self.searchwords[randint(6, 8)], randint(1, 2))
        other_words = sample(self.searchwords[5], randint(2, 3)) + sample(self.searchwords[4], randint(2, 3))
        wordlist = long_words + other_words
        grid, skipped = self.generate_grid(wordlist)
        line_grid = "".join(r for r in ["".join(p for p in k) for k in grid])
        wordlist = [word for word in wordlist if word not in skipped]
        puzzle_text = ""
        howtoplay = "Find as many words as you can from the grid. Words can be found horizontally, vertically or " \
                    "diagonally, and might also be hidden backwards. You have 75 seconds."
        for rows in grid:
            puzzle_text += "".join(":regional_indicator_" + p.lower() + ":" for p in rows) + "\n"
        embed = nextcord.Embed(title="Word Hunt Game", description=puzzle_text, color=nextcord.Color.dark_purple())
        embed.add_field(name="How To Play?", value=howtoplay)
        embed.set_footer(text="Requested by " + str(ctx.author), icon_url=ctx.author.avatar.url)
        await ctx.channel.send(embed=embed)

        usedwords, points = [], {}

        async def react(msg):
            try:
                await msg.add_reaction("✅")
            except Exception:
                pass

        def check(msg):
            nonlocal points, usedwords
            if not msg.author.bot and msg.channel == ctx.channel:
                tocheck = msg.content.strip().upper()
                if len(tocheck) <= 9 and tocheck not in usedwords and tocheck.lower() in self.allwords:
                    if self.check_word(tocheck, line_grid) or self.check_word(tocheck[::-1], line_grid):
                        usedwords.append(tocheck)
                        if msg.author.id not in points:
                            points[msg.author.id] = 1
                        else:
                            points[msg.author.id] += 1
                        self.bot.loop.create_task(react(msg))
            return False

        try:
            
            await self.bot.wait_for('message', timeout=75, check=check)
        except asyncio.TimeoutError:
            not_found = [word for word in wordlist if word.upper() not in usedwords]
            if not points:
                await ctx.channel.send("Looks like nobody could find a word. That's disappointing! :(\n\n"
                                       "Here are some of the hidden words: " + ", ".join(p for p in not_found))
            else:
                top = [sorted(points.values(), reverse=True), sorted(points, key=points.get, reverse=True)]
                top_text = ""
                for i in range(len(top[0])):
                    top_text += "**#" + str(i + 1) + " - <@" + str(top[1][i]) + '> (' + str(
                        int(top[0][i])) + ' words)**' + '\n'
                embed = nextcord.Embed(title="Time's Up!!! Here are the results.",
                                       description=top_text + "**:trophy: <@%s> wins the game!**" % str(top[1][0]),
                                       color=nextcord.Color.random())
                if not_found:
                    embed.add_field(name="Some hidden words which nobody found", value=", ".join(p for p in not_found),
                                    inline=False)
                embed.set_footer(text="Game started by " + str(ctx.author), icon_url=ctx.author.avatar.url)
                await ctx.channel.send(embed=embed)

    @commands.cooldown(1, 60, commands.BucketType.channel)
    @commands.command(pass_context=True, name="extremehunt", aliases=['eh'])
    async def extremehunt(self, ctx):
        long_words = sample(self.searchwords[6], randint(1, 2)) + sample(self.searchwords[randint(6, 8)], randint(1, 2))
        other_words = sample(self.searchwords[5], randint(2, 3)) + sample(self.searchwords[4], randint(2, 3))
        wordlist = long_words + other_words
        grid, skipped = self.generate_grid(wordlist)
        line_grid = "".join(r for r in ["".join(p for p in k) for k in grid])
        puzzle_text = ""
        howtoplay = "Find the longest word that you can from the grid. Words can be found horizontally, vertically or " \
                    "diagonally, and might also be hidden backwards. You have 60 seconds."
        for rows in grid:
            puzzle_text += "".join(":regional_indicator_" + p.lower() + ":" for p in rows) + "\n"
        embed = nextcord.Embed(title="Extreme Hunt Game", description=puzzle_text, color=nextcord.Color.dark_purple())
        embed.add_field(name="How To Play?", value=howtoplay)
        embed.set_footer(text="Requested by " + str(ctx.author), icon_url=ctx.author.avatar.url)
        await ctx.channel.send(embed=embed)

        async def react(msg):
            try:
                await msg.add_reaction("✅")
            except Exception:
                pass

        curword = ""
        winner = 0

        def check(msg):
            nonlocal curword, winner
            if not msg.author.bot and msg.channel == ctx.channel:
                tocheck = msg.content.strip().upper()
                if len(curword) < len(tocheck) <= 9 and tocheck.lower() in self.allwords:
                    if self.check_word(tocheck, line_grid) or self.check_word(tocheck[::-1], line_grid):
                        curword = tocheck
                        winner = msg.author.id
                        self.bot.loop.create_task(react(msg))
            return False

        try:
            await self.bot.wait_for('message', timeout=60, check=check)
        except asyncio.TimeoutError:
            if curword == "":
                await ctx.channel.send(embed=nextcord.Embed(title="Looks like nobody could find a word.",
                                                            description="That's disappointing! :(",
                                                            color=nextcord.Color.random()))
            else:
                await ctx.channel.send(embed=nextcord.Embed(title="Time's up!",
                                                            description="<@%s> wins the game with the longest word '%s'." % (
                                                            str(winner), curword),
                                                            color=nextcord.Color.random()))

    @commands.cooldown(1, 30, commands.BucketType.channel)
    @commands.command(pass_context=True, name="scramble", aliases=["wordscramble"])
    async def scramble(self, ctx):
        words_to_choose_from = self.searchwords[6] + self.searchwords[7] + self.searchwords[8] + self.searchwords[9]
        word = sample(words_to_choose_from, 1)[0]
        letters = [letter for letter in word]
        shuffle(letters)
        scrambled_word = "".join(letter for letter in letters)
        desc_text = "".join(":regional_indicator_" + k + ":" for k in scrambled_word)
        embed = nextcord.Embed(title="Word Scramble", description=desc_text, color=nextcord.Color.blurple())
        embed.add_field(name="How To Play?", value="The letters of a word have been scrambled. Unscramble it and type"
                                                   " the original word. You have 30 seconds.")
        embed.set_footer(text="Game started by " + str(ctx.author), icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

        def check(msg):
            return not msg.author.bot and msg.content.lower().strip() == word and msg.channel == ctx.channel

        resp = None
        try:
            resp = await self.bot.wait_for('message', timeout=30, check=check)
        except asyncio.TimeoutError:
            await ctx.send(embed=nextcord.Embed(title="Looks like nobody knew the answer.",
                                                description="The original word was **%s**." % word.upper(),
                                                color=nextcord.Color.random()))
        if resp:
            await ctx.send(embed=nextcord.Embed(title="**Congratulations** %s" % resp.author.name,
                                                description="You guessed the word correctly: **%s**" % word.upper(),
                                                color=nextcord.Color.random()))
            ctx.command.reset_cooldown(ctx)

    @commands.max_concurrency(1, per=commands.BucketType.channel, wait=False)
    @commands.command(pass_context=True, name="passthebomb", aliases=['ptb'])
    async def passthebomb(self, ctx):
        players = []
        buttons = [create_button(style=ButtonStyle.green, label="✅", custom_id="imin")]
        action_row = create_actionrow(*buttons)
        msg = await ctx.send(embed=nextcord.Embed(title=":bomb: **Pass The Bomb** has been started!",
                                                  description="Click on the 🟩 to join."
                                                              " The bomb will be passed to all the players and they will have 10 seconds to come"
                                                              " up with a word, or they will be eliminated. Words cannot be repeated.",
                                                  color=nextcord.Color.random()),
                             components=[action_row])

        try:
            while True:
                response: ComponentContext = await wait_for_component(self.bot, components=action_row, messages=msg, timeout=10)
                if response.author not in players:
                    string = ""
                    for user in players:
                        string = string + user.display_name + "\n"
                    await response.reply(f"You have joined the game", hidden=True)
                    players.append(response.author)

                    new_embed = nextcord.Embed(title=":bomb: **Pass The Bomb** has been started!",
                                               description="Click on the 🟩 to join."
                                                           " The bomb will be passed to all the players and they will have 10 seconds to come"
                                                           "up with a word, or they will be eliminated. Words cannot be repeated.",

                                               color=nextcord.Color.random())
                    msg.edit(embed=new_embed)

                else:
                    await response.reply("You are already in the game smart-ass", hidden=True)

        except asyncio.TimeoutError:
            if len(players) < 2:
                ctx.command.reset_cooldown(ctx)
                await ctx.send(
                    embed=nextcord.Embed(title="**The game requires at least 2 players to start. Try again!**",
                                         color=nextcord.Color.random()))
                return

        string = ""
        for user in players:
            string = string + user.display_name + "\n"
        await ctx.send(embed=nextcord.Embed(title="We have been joined by:",
                                            description=string,
                                            color=nextcord.Color.random()))
        players = players[:6]
        two_letter = ['ab', 'ad', 'ag', 'am', 'an', 'ar', 'at', 'ay', 'by', 'do', 'en', 'es', 'et', 'fe', 'it', 'mo',
                      'ma', 'pe', 'py', 're', 'ti', 'us']
        three_letter = ['abs', 'abo', 'aby', 'ace', 'ads', 'ail', 'ant', 'are', 'art', 'ass', 'ave', 'avo', 'bal',
                        'ban', 'bas', 'bar', 'bay', 'beg', 'bis', 'boo', 'bot', 'bra', 'bud', 'bug', 'bus', 'cab',
                        'cap', 'cad', 'cat', 'cel', 'chi', 'cob', 'cog', 'cor', 'cow', 'cry', 'cue', 'cut', 'dab',
                        'dis', 'dit', 'doe', 'dog', 'don', 'dot', 'dry', 'eel', 'eek', 'ego', 'elf', 'eme', 'ems',
                        'end', 'eng', 'ere', 'erg', 'ess', 'eye', 'fee', 'fay', 'fes', 'fig', 'fin', 'fit', 'fro',
                        'fur', 'gad', 'gal',
                        'git', 'hin', 'hit', 'icy', 'iff', 'ill', 'ins', 'its', 'lis', 'lit', 'lot', 'lye', 'oar',
                        'obe', 'oes', 'ole', 'oot', 'ore', 'out', 'pes', 'pie', 'red', 'rot', 'sal', 'sat', 'see',
                        'sip', 'sod', 'sot', 'syn', 'vet', 'yet']
        sub, turn, mode = "", 0, 0
        used = []

        async def play():
            nonlocal sub, turn, mode, used
            sub = sample(two_letter + three_letter, 1)[0]

            mode = random.randint(0, 2)
            text = "Type a word that ends with: **%s**/Type a word that starts with: **%s**/Type a word that " \
                   "contains: **%s**".split("/")[mode]
            await ctx.send(
                embed=nextcord.Embed(title=f"{(players[turn].display_name)} You have the :bomb: **Bomb** now. ",
                                     description=text % sub,
                                     color=nextcord.Color.random()))

            async def reactto(msg):
                try:
                    await msg.add_reaction("✅")
                except Exception:
                    pass

            def checkword(msg):
                if msg.author == players[turn]:
                    if msg.content.lower().strip() not in used and msg.content.lower().strip() in self.allwords:
                        content = msg.content.lower().strip()
                        if content == sub:
                            return False
                        if content.endswith(sub) and mode == 0:
                            used.append(content)
                            self.bot.loop.create_task(reactto(msg))
                            return True
                        if content.startswith(sub) and mode == 1:
                            used.append(content)
                            self.bot.loop.create_task(reactto(msg))
                            return True
                        if sub in content and mode == 2:
                            used.append(content)
                            self.bot.loop.create_task(reactto(msg))
                            return True
                return False

            try:
                await self.bot.wait_for('message', timeout=10, check=checkword)
            except asyncio.TimeoutError:
                await ctx.channel.send(embed=nextcord.Embed(title="The :bomb: **Bomb** exploded!",
                                                            description="%s has been eliminated." % (
                                                            players[turn]).display_name,
                                                            color=nextcord.Color.random()))
                players.pop(turn)
            if len(players) == 1:
                ctx.command.reset_cooldown(ctx)
                await ctx.channel.send(
                    embed=nextcord.Embed(
                        title="**:trophy: %s has survived the bomb and won the game!**" % (players[0]).display_name,
                        color=nextcord.Color.random()))
                return
            turn = (turn + 1) % len(players)
            self.bot.loop.create_task(play())

        self.bot.loop.create_task(play())

    @commands.command(aliases=['hm', 'hang'])
    async def hangman(self, ctx):
        # Filtering the list of all words depending on the configuration
        min_length: int = 0
        max_length: int = 25
        min_unique_letters: int = 0
        max_unique_letters: int = 25
        # Filtering the list of all words depending on the configuration
        filtered_words = [
            word for word in ALL_WORDS
            if min_length < len(word) < max_length and min_unique_letters < len(set(word)) < max_unique_letters
        ]

        if not filtered_words:
            filter_not_found_embed = Embed(
                title="Nope",
                description="No words could be found that fit all filters specified.",
                color=nextcord.Color.red()
            )
            await ctx.send(embed=filter_not_found_embed)
            return

        word = choice(filtered_words)

        # `pretty_word` is used for ARE u lonely cursor? comparing the indices where the guess of the user is similar to the word
        # The `user_guess` variable is prettified by adding spaces between every dash, and so is the `pretty_word`
        pretty_word = ''.join([f"{letter} " for letter in word])[:-1]
        user_guess = ("_ " * len(word))[:-1]
        tries = 6
        guessed_letters = set()

        def check(msg: Message) -> bool:
            return msg.author == ctx.author and msg.channel == ctx.channel

        original_message = await ctx.send(embed=Embed(
            title="Hangman",
            description="Loading game...",
            color=nextcord.Color.green()
        ))

        # Game loop
        while user_guess.replace(' ', '') != word:
            # Edit the message to the current state of the game
            await original_message.edit(embed=self.create_embed(tries, user_guess))

            try:
                message = await self.bot.wait_for(
                    event="message",
                    timeout=60.0,
                    check=check
                )
            except TimeoutError:
                timeout_embed = Embed(
                    title="Uh Oh",
                    description="Looks like the bot timed out! You must send a letter within 60 seconds.",
                    color=nextcord.Color.red()
                )
                await original_message.edit(embed=timeout_embed)
                return

            # If the user enters a capital letter as their guess, it is automatically converted to a lowercase letter
            normalized_content = message.content.lower()
            # The user should only guess one letter per message
            if len(normalized_content) > 1:
                letter_embed = Embed(
                    title="Bruh",
                    description="You can only send one letter at a time, try again!",
                    color=nextcord.Color.dark_green(),
                )
                await ctx.send(embed=letter_embed, delete_after=4)
                continue

            # Checks for repeated guesses
            elif normalized_content in guessed_letters:
                already_guessed_embed = Embed(
                    title="Nah",
                    description=f"You have already guessed `{normalized_content}`, try again!",
                    color=nextcord.Color.dark_green(),
                )
                await ctx.send(embed=already_guessed_embed, delete_after=4)
                continue

            # tells them that nothing but letters allowed, tho it also reduces one chance anyway
            elif not normalized_content.isalpha:
                already_guessed_embed = Embed(
                    title="You cannot use anything other than letters",
                    description=f"So keep that in mind",
                    color=nextcord.Color.dark_green(),
                )
                await ctx.send(embed=already_guessed_embed, delete_after=4)

            # Checks for correct guesses from the user
            elif normalized_content in word:
                positions = {idx for idx, letter in enumerate(pretty_word) if letter == normalized_content}
                user_guess = "".join(
                    [normalized_content if index in positions else dash for index, dash in enumerate(user_guess)]
                )

            else:
                tries -= 1

                if tries <= 0:
                    losing_embed = Embed(
                        title="You lost.",
                        description=f"The word was `{word}`.",
                        color=nextcord.Color.red(),
                    )
                    await original_message.edit(embed=self.create_embed(tries, user_guess))
                    await ctx.send(embed=losing_embed)
                    return

            guessed_letters.add(normalized_content)

        # The loop exited meaning that the user has guessed the word
        await original_message.edit(embed=self.create_embed(tries, user_guess))
        win_embed = Embed(
            title="You won!",
            description=f"The word was `{word}`.",
            color=nextcord.Color.green()
        )
        await ctx.send(embed=win_embed)

    @commands.max_concurrency(1, per=commands.BucketType.channel, wait=False)
    @commands.command(aliases=['tr', 'typeracer'])
    async def typerace(self, ctx):
        players = []
        text = random.choice(open("text_files/random_sentences.txt", encoding="utf-8").readlines()).replace('\n', '')
        font_text = text.replace('\u0020',  '\u2007')
        words_in_sentence = len(text.split(" "))
        buttons = [create_button(style=ButtonStyle.green, label="✅", custom_id="imin")]
        action_row = create_actionrow(*buttons)

        msg = await ctx.send(embed=nextcord.Embed(title="Lets begin the typerace!",
                                                  description="React with :white_check_mark: to join.\nThen type the sentence the fastest to win.",
                                                  color=nextcord.Color.random()),
                             components=[action_row],
                             delete_after=20)
        try:
            while True:
                response: ComponentContext = await wait_for_component(self.bot, components=action_row, messages=msg,
                                                                      timeout=10)
                if response.author.name not in players:
                    await response.reply(f"You have joined the game", hidden=True)
                    players.append(response.author.name)
                else:
                    await response.reply("You are already in the game smart-ass", hidden=True)

        except asyncio.TimeoutError:
            if len(players) == 0:
                ctx.command.reset_cooldown(ctx)
                await ctx.send(
                    embed=nextcord.Embed(title=f"{ctx.author.display_name} Why wouldn't you join your own game!",
                                         description=f"Not this again...",
                                         color=nextcord.Color.random()),
                    delete_after=5)
                return

            elif len(players) < 2:
                ctx.command.reset_cooldown(ctx)
                await ctx.send(
                    embed=nextcord.Embed(
                        title="You were the only one to show up, but atleast you can get some practice!",
                        color=nextcord.Color.random()),
                    delete_after=5)
            else:
                string = ""
                for i in players:
                    string += i + "\n"
                embed = nextcord.Embed(title="The people racing against each other are:",
                                       description=string,
                                       color=nextcord.Color.random())
                embed.set_footer(text="May the fastest typer win!")
                await ctx.send(embed=embed, delete_after=5)

        await asyncio.sleep(5)
        embed = nextcord.Embed(title="Sentence to type:",
                               description=font_text,
                               color=nextcord.Color.random())
        await ctx.send(embed=embed)

        def check(message):
            return message.author.name in players and message.channel == ctx.channel

        string = ""
        noplay_string = ""
        i = 1

        start_time = time()
        while len(players) > 0:
            try:
                message = await self.bot.wait_for("message", timeout=words_in_sentence * 6, check=check)
                end_time = time()
                if '\u2007' in message.content:
                    embed = nextcord.Embed(title=f"Nice Try {message.author.name}",
                                           description=f"But don't you dare think you can cheat here.\nCopy pasting isn't TYPING.\nEveryone bully this man, who thinks cheating should be done in CHAD games.",
                                           color=nextcord.Color.random())
                    players.remove(message.author.name)
                    await ctx.send(embed=embed)

                elif message.content == text:
                    string += f"**\#{i}**       {message.author.name} in {round(end_time - start_time, 3)} at a speed of {round(words_in_sentence / round(end_time - start_time, 3) * 60, 3)} words per minute.\n"  # TODO print also in how much time
                    i += 1
                    embed = nextcord.Embed(title=f"Well done {message.author.name}",
                                           description=f"You typed the sentence correctly...",
                                           color=nextcord.Color.random())
                    players.remove(message.author.name)
                    await ctx.send(embed=embed, delete_after=5)

                else:
                    embed = nextcord.Embed(title=f"Sorry {message.author.name}",
                                           description=f"You typed the sentence wrong...",
                                           color=nextcord.Color.random())
                    embed.set_footer(text="Better luck next time")
                    players.remove(message.author.name)
                    await ctx.send(embed=embed, delete_after=5)

            except asyncio.TimeoutError:
                if str(players) != "[]":
                    noplay_string += "The ones who didn't type the sentence in time:\n"
                    for player in players:
                        noplay_string += player + "\n"
                break

        if string == "":
            string = "No one could type properly lmao"
        embed = nextcord.Embed(title="Results",
                               description=string,
                               color=nextcord.Color.random())
        embed.set_footer(text=noplay_string)
        await ctx.send(embed=embed)

    @passthebomb.error
    async def bomb_error(self, ctx, error):
        if isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send(embed=nextcord.Embed(title=f"Ayyo Chill!", description="I am being used in this channel",
                                                color=nextcord.Color.random()))

    @wordhunt.error
    async def word_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=nextcord.Embed(title=f"Slow down bro. Try after {round(error.retry_after)} seconds",
                                                color=nextcord.Color.random()))

    @extremehunt.error
    async def extreme_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=nextcord.Embed(title=f"Slow down bro. Try after {round(error.retry_after)} seconds",
                                                color=nextcord.Color.random()))

    @scramble.error
    async def scrabble_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=nextcord.Embed(title=f"Slow down bro. Try after {round(error.retry_after)} seconds",
                                                color=nextcord.Color.random()))


def setup(bot):
    bot.add_cog(WordGames(bot))
