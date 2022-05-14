import nextcord
import asyncio
from nextcord.ext import commands
import random
import os
import requests
import giphy_client
from giphy_client.rest import ApiException
import datetime
import pyfiglet

from tinydb import TinyDB, Query
from modules import encrypt as enc, decrypt as dec
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from io import BytesIO
import time
from nextcord.utils import get
import re
import json
import os
from dotenv import load_dotenv
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.utils.manage_components import wait_for_component

load_dotenv()

rightbuttonemoji = {
    'id': 928501426055950337,
    'name': 'forward'
}

leftbuttonemoji = {
    'id': 928501266785632266,
    'name': "back1"
}


async def convert(argument):
    matches = time_regex.findall(argument.lower())
    time = 0
    for v, k in matches:
        try:
            time += time_dict[k] * float(v)
        except KeyError:
            raise commands.BadArgument(
                "{} is an invalid time-key! h/m/s/d are valid!".format(k))
        except ValueError:
            raise commands.BadArgument("{} is not a number!".format(v))
    return time


def adjust_text(text, draw, font):
    bits = []
    bit = ""
    for n, c in enumerate(text):
        bit += c
        if draw.textsize(bit, font=font)[0] > 305:
            bits.append(bit)
            bit = ""
        elif n == len(text) - 1:
            bits.append(bit)
    text = "\n".join(bits)
    if draw.textsize(text, font=font)[1] > 199 - 70:
        while draw.textsize(text, font=font)[1] > 199 - 70:
            text = text[:-1]
    return text


emojiLetters = [
    "\N{REGIONAL INDICATOR SYMBOL LETTER A}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER B}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER C}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER D}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER E}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER F}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER G}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER H}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER I}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER J}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER K}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER L}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER M}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER N}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER O}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER P}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER Q}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER R}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER S}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER T}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER U}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER V}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER W}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER X}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER Y}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER Z}"]

time_regex = re.compile(r"(\d{1,5}(?:[.,]?\d{1,5})?)([smhd])")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        matches = time_regex.findall(argument.lower())
        duration = 0
        for v, k in matches:
            try:
                duration += time_dict[k] * float(v)
            except KeyError:
                raise commands.BadArgument("{} is an invalid duration-key! h/m/s/d are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return duration


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("text_files/jokes.json", "r", encoding="utf-8") as f:
            self.jokes_json = json.load(f)
            f.close()

    @commands.command()
    async def christmas(self, ctx):
        count = 0
        failed = 0
        if ctx.author.id == 723032217504186389:
            for guild in self.bot.guilds:
                try:
                    await guild.text_channels[0].send(embed=nextcord.Embed(
                        title="Merry Christmas! :partying_face: :boom: :snowflake: :christmas_tree:",
                        description="Thank you all for inviting me to your server.\nOn behalf of all bot devs wishing all of you a very Merry Christmas! :santa: :heart:",
                        color=nextcord.Color.gold()))
                    count += 1
                except:
                    failed += 1
                    print(guild)
                    pass

    @cog_ext.cog_slash(name="ask", description="Allows you to ask me any random question.",
                       options=[
                           create_option(name="question", description="The question to be asked", option_type=3,
                                         required=True)
                       ])
    async def _ask(self, ctx: SlashContext, *, question):
        message = question
        question_list = ["will", "how", "why", "is",
                         "when", "where", "who", "whom",
                         "I", "@", "can", "am", "should",
                         "are", "were", "if", "did",
                         "does", "do", "has", "was"]
        boolean = False
        for x in question_list:
            if x in message.split():
                boolean = True
        if boolean is False:
            return await ctx.send(embed=nextcord.Embed(title="Invalid question format.", color=nextcord.Color.random()))

        question = question.replace('@', "")
        embed = nextcord.Embed(title=question, description=random.choice([
            "It is certain :8ball:", "It is decidedly so :8ball:",
            "Without a doubt :8ball:", "Yes, definitely :8ball:",
            "You may rely on it :8ball:", "As I see it, yes :8ball:",
            "Most likely :8ball:", "Outlook good :8ball:", "Yes :8ball:",
            "Signs point to yes :8ball:", "Reply hazy try again :8ball:",
            "Ask again later :8ball:", "Better not tell you now :8ball:",
            "Cannot predict now :8ball:", "Concentrate and ask again :8ball:",
            "Don't count on it :8ball:", "My reply is no :8ball:",
            "My sources say no :8ball:", "Outlook not so good :8ball:",
            "Very doubtful :8ball:"
        ]), color=nextcord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command()
    async def ask(self, ctx, *, question):
        message = ctx.message.content.lower()
        question_list = ["will", "how", "why", "is",
                         "when", "where", "who", "whom",
                         "I", "@", "can", "am", "should",
                         "are", "were", "if", "did",
                         "does", "do", "has", "was"]

        boolean = False
        for x in question_list:
            if x in message.split():
                boolean = True
        if boolean is False:
            return await ctx.send(embed=nextcord.Embed(title="Invalid question format.", color=nextcord.Color.random()))

        question = await commands.clean_content().convert(ctx, question)
        question = question.replace('@', "")
        embed = nextcord.Embed(title=question, description=random.choice([
            "It is certain :8ball:", "It is decidedly so :8ball:",
            "Without a doubt :8ball:", "Yes, definitely :8ball:",
            "You may rely on it :8ball:", "As I see it, yes :8ball:",
            "Most likely :8ball:", "Outlook good :8ball:", "Yes :8ball:",
            "Signs point to yes :8ball:", "Reply hazy try again :8ball:",
            "Ask again later :8ball:", "Better not tell you now :8ball:",
            "Cannot predict now :8ball:", "Concentrate and ask again :8ball:",
            "Don't count on it :8ball:", "My reply is no :8ball:",
            "My sources say no :8ball:", "Outlook not so good :8ball:",
            "Very doubtful :8ball:"
        ]), color=nextcord.Color.blue())
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="gif", description="Allows to search for GIFs or send random.",
                       options=[
                           create_option(name="query", description="The topic on which you want a gif", option_type=3,
                                         required=False)
                       ])
    async def _gif(self, ctx: SlashContext, *, query="random"):
        api_key = os.getenv('giphy_api')
        api_instance = giphy_client.DefaultApi()
        try:

            api_response = api_instance.gifs_search_get(api_key, query, limit=5, rating='g')
            lst = list(api_response.data)
            giff = random.choice(lst)

            emb = nextcord.Embed(title=query)
            emb.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')
            emb.color = nextcord.Color.random()

            await ctx.send(embed=emb)

        except ApiException:
            emb = nextcord.Embed(title=query, description="Sorry could not find anything matching that",
                                 color=nextcord.Color.random())
            await(ctx.send(embed=emb))

    @commands.command()
    async def gif(self, ctx, *, q="random"):
        api_key = os.getenv('giphy_api')
        api_instance = giphy_client.DefaultApi()
        try:
            api_response = api_instance.gifs_search_get(api_key, q, limit=5, rating='g')
            lst = list(api_response.data)
            giff = random.choice(lst)

            emb = nextcord.Embed(title=q)
            emb.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')
            emb.color = nextcord.Color.random()

            await ctx.channel.send(embed=emb)
        except ApiException:
            emb = nextcord.Embed(title=q, description="Sorry could not find anything matching that",
                                 color=nextcord.Color.random())
            await(ctx.send(embed=emb))

    @cog_ext.cog_slash(name="epicgamerrate", description="Tells you how EPIC you are at gaming.",
                       options=[
                           create_option(name="member", description="Member whose egr you want", option_type=6,
                                         required=False)
                       ])
    async def _epicgamerrate(self, ctx: SlashContext, member: nextcord.Member = None):
        num = random.randint(1, 100)
        if member is None:
            member = ctx.author

        membervar = member.display_name

        embed = nextcord.Embed(
            title=f"Epic Gamer Rate :sunglasses:",
            description=f"{membervar} is {num}% epic gamer."
        )
        embed.color = nextcord.Color.random()
        embed.set_footer(text="Gamers = Poggers")
        await ctx.send(embed=embed)

    @commands.command(aliases=['epicgamerate', 'egr', 'epicgr', 'egrate', 'epicgamerr8', 'epicgamer8'])
    async def epicgamerrate(self, ctx, member: nextcord.Member = None):
        num = random.randint(1, 100)
        if member is None:
            member = ctx.author

        membervar = member.display_name

        embed = nextcord.Embed(
            title=f"Epic Gamer Rate :sunglasses:",
            description=f"{membervar} is {num}% epic gamer."
        )
        embed.color = nextcord.Color.random()
        embed.set_footer(text="Gamers = Poggers")
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="simprate", description="Tells you how much you are simping.",
                       options=[
                           create_option(name="member", description="Member whose sr you want", option_type=6,
                                         required=False)
                       ])
    async def _simprate(self, ctx: SlashContext, member: nextcord.Member = None):
        num = random.randint(1, 100)
        if member is None:
            member = ctx.author

        membervar = member.display_name

        embed = nextcord.Embed(
            title=f"Simp Rate :blush:",
            description=f"{membervar} is {num}% simp."
        )
        embed.color = nextcord.Color.random()
        embed.set_footer(text="Their favourite show be the SIMPsons")
        await ctx.send(embed=embed)

    @commands.command(aliases=['sr', 'simpr', 'srate', 'sr8'])
    async def simprate(self, ctx, member: nextcord.Member = None):
        num = random.randint(1, 100)
        if member is None:
            member = ctx.author

        member_var = member.display_name

        embed = nextcord.Embed(
            title=f"Simp Rate :blush:",
            description=f"{member_var} is {num}% simp."
        )
        embed.color = nextcord.Color.random()
        embed.set_footer(text="Their favourite show be the SIMPsons")
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="poll", description="Creates a poll for you.",
                       options=[
                           create_option(name="duration", description="For how long should the poll be open",
                                         option_type=3,
                                         required=True),
                           create_option(name="poll_question", description="The poll options (separated by comma)",
                                         option_type=3,
                                         required=True),
                           create_option(name="poll_options", description="The poll options (separated by comma)",
                                         option_type=3,
                                         required=True)
                       ])
    async def _poll(self, ctx: SlashContext, duration: TimeConverter, *, poll_question: str, poll_options: str):
        if duration != 0:
            voters = []
            vote_counts = {}

            if ':' in argument:
                split_question = argument.split(':', maxsplit=1)
                question = split_question[0]
            else:
                await ctx.send(embed=nextcord.Embed(title="You must put a colon(:) after your poll question.",
                                                    color=nextcord.Color.random()))
                return

            if ',' in split_question[1]:
                options = split_question[1].split(',')

            else:
                await ctx.send(embed=nextcord.Embed(title="You must put a comma(,) after each poll options.",
                                                    color=nextcord.Color.random()))
                return

            description = ""
            for i, option in enumerate(options):
                option = options[i]
                description += emojiLetters[i] + " " + option + "\n"
            pass
            # Initialize vote_counts dictionary
            for option in options:
                vote_counts[option] = 0
            pass
            my_poll = nextcord.Embed(
                title=question,
                description=description, color=nextcord.Color.random()
            )
            start_time = datetime.datetime.now()

            buttons = []
            for i, option in enumerate(options):
                buttons.append(create_button(style=ButtonStyle.blue, custom_id=option, emoji=emojiLetters[i],
                                             disabled=False))
            action_row = create_actionrow(*buttons)

            message = await ctx.send(embed=my_poll, components=[action_row])

            async def this_thing(buttons, action_row, message):
                while True:
                    response: ComponentContext = await wait_for_component(self.bot, messages=message,
                                                                          components=action_row)
                    if response.author.bot:
                        continue

                    elif not response.author.bot:
                        if response.author not in voters:
                            voters.append(response.author)
                            vote_counts[response.component["custom_id"]] += 1
                            pass
                    action_row = create_actionrow(*buttons)
                    await response.edit_origin(components=[action_row])

            try:
                await asyncio.wait_for(fut=this_thing(buttons, action_row, message), timeout=duration)
            except asyncio.TimeoutError:
                if datetime.datetime.now() > start_time + datetime.timedelta(seconds=duration):
                    print("Tommy")

            # Send messages of results
            pass
            results = ""
            for option in vote_counts:
                results += option + ": " + str(vote_counts[option]) + "\n"

            # Check if the user has already voted

            results_message = nextcord.Embed(
                title="Results of " + question,
                description=results, color=nextcord.Color.random()
            )
            pass
            await message.clear_reactions()
            await ctx.send(embed=results_message)

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Please mention a valid duration!", color=nextcord.Color.random()))

    @commands.command(aliases=['pole'])
    async def poll(self, ctx, duration: TimeConverter, *, argument: str):
        if duration != 0:
            voters = []
            vote_counts = {}

            if ':' in argument:
                split_question = argument.split(':', maxsplit=1)
                question = split_question[0]
            else:
                await ctx.send(embed=nextcord.Embed(title="You must put a colon(:) after your poll question.",
                                                    color=nextcord.Color.random()))
                return

            if ',' in split_question[1]:
                options = split_question[1].split(',')

            else:
                await ctx.send(embed=nextcord.Embed(title="You must put a comma(,) after each poll options.",
                                                    color=nextcord.Color.random()))
                return

            description = ""
            for i, option in enumerate(options):
                option = options[i]
                description += emojiLetters[i] + " " + option + "\n"
            pass
            # Initialize vote_counts dictionary
            for option in options:
                vote_counts[option] = 0
            pass
            my_poll = nextcord.Embed(
                title=question,
                description=description, color=nextcord.Color.random()
            )
            start_time = datetime.datetime.now()

            buttons = []
            for i, option in enumerate(options):
                buttons.append(create_button(style=ButtonStyle.blue, custom_id=option, emoji=emojiLetters[i],
                                             disabled=False))
            action_row = create_actionrow(*buttons)

            message = await ctx.send(embed=my_poll, components=[action_row])

            async def this_thing(buttons, action_row, message):
                while True:
                        response: ComponentContext = await wait_for_component(self.bot, messages=message,
                                                                              components=action_row)
                        if response.author.bot:
                            continue

                        elif not response.author.bot:
                            if response.author not in voters:
                                voters.append(response.author)
                                vote_counts[response.component["custom_id"]] += 1
                                pass
                        action_row = create_actionrow(*buttons)
                        await response.edit_origin(components=[action_row])

            try:
                await asyncio.wait_for(fut=this_thing(buttons, action_row, message), timeout=duration)
            except asyncio.TimeoutError:
                if datetime.datetime.now() > start_time + datetime.timedelta(seconds=duration):
                    print("Tommy")

            # Send messages of results
            pass
            results = ""
            for option in vote_counts:
                results += option + ": " + str(vote_counts[option]) + "\n"

            # Check if the user has already voted

            results_message = nextcord.Embed(
                title="Results of " + question,
                description=results, color=nextcord.Color.random()
            )
            pass
            await message.clear_reactions()
            await ctx.send(embed=results_message)

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Please mention a valid duration!", color=nextcord.Color.random()))

    @cog_ext.cog_slash(name="ascii", description="Creates a cool ASCII art for you.",
                       options=[
                           create_option(name="text", description="Text to convert", option_type=3,
                                         required=True)
                       ])
    async def _ascii(self, ctx: SlashContext, *, text: str):
        try:
            split_text = text.split(" ", maxsplit=1)
            if split_text[0] == 'rem':
                result = pyfiglet.figlet_format(split_text[1])
            else:
                result = pyfiglet.figlet_format(text)
        except:
            embed = nextcord.Embed(title=f"Done!",
                                   description=f"Successfully converted *nothing* into a beautiful picture!\nNow try actually giving me something to use",
                                   color=nextcord.Color.random())
            embed.set_footer(text="smh smh SMH")
            await ctx.send(embed=embed)
            return

        await ctx.send("```" + result + "```")

    @commands.command(aliases=['as'])
    async def ascii(self, ctx, *, text: str):
        try:
            split_text = text.split(" ", maxsplit=1)
            if split_text[0] == 'rem':
                result = pyfiglet.figlet_format(split_text[1])
                await ctx.message.delete()
            else:
                result = pyfiglet.figlet_format(text)
        except:
            embed = nextcord.Embed(title=f"Done!",
                                   description=f"Successfully converted *nothing* into a beautiful picture!\nNow try actually giving me something to use",
                                   color=nextcord.Color.random())
            embed.set_footer(text="smh smh SMH")
            await ctx.send(embed=embed)
            return

        await ctx.send("```" + result + "```")

    @cog_ext.cog_slash(name="emojify", description="Turns your text into emojis!",
                       options=[
                           create_option(name="text", description="Text to convert", option_type=3,
                                         required=True)
                       ])
    async def _emojify(self, ctx: SlashContext, *, text: str):
        emojified = ''
        formatted = re.sub(r'[^A-Za-z ]+', "", text).lower()
        for i in formatted:
            if i == ' ':
                emojified += '     '
            else:
                emojified += ':regional_indicator_{}: '.format(i)
        if len(emojified) + 2 >= 2000:
            await ctx.send(embed=nextcord.Embed(title='Your message in emojis exceeds 2000 characters!',
                                                color=nextcord.Color.random()))
            return
        if len(emojified) <= 25:
            await ctx.send(embed=nextcord.Embed(title='Your message could not be converted!',
                                                color=nextcord.Color.random()))
            return
        else:
            await ctx.send(emojified)

    @commands.command(aliases=['emo', 'emogify'])
    async def emojify(self, ctx, *, text: str):
        emojified = ''
        formatted = re.sub(r'[^A-Za-z ]+', "", text).lower()
        for i in formatted:
            if i == ' ':
                emojified += '     '
            else:
                emojified += ':regional_indicator_{}: '.format(i)
        if len(emojified) + 2 >= 2000:
            await ctx.send(embed=nextcord.Embed(title='Your message in emojis exceeds 2000 characters!',
                                                color=nextcord.Color.random()))
            return
        if len(emojified) <= 25:
            await ctx.send(embed=nextcord.Embed(title='Your message could not be converted!'),
                           color=nextcord.Color.random())
            return
        else:
            await ctx.send(emojified)

    @cog_ext.cog_slash(name="spoilify", description="Spoils your message just for you! (Its nicer than it sounds)",
                       options=[
                           create_option(name="text", description="Text to convert", option_type=3,
                                         required=True)
                       ])
    async def _spoilify(self, ctx: SlashContext, *, text: str):
        split = text.split(" ", maxsplit=1)
        spoilified = ''
        if split[0] == 'rem' or split[0] == 'remove':
            await ctx.message.delete()
            text = split[1]
        for i in text:
            spoilified += '||{}||'.format(i)
        if len(spoilified) + 2 >= 2000:
            await ctx.send(embed=nextcord.Embed(title='Your message in spoilers exceeds 2000 characters!',
                                                color=nextcord.Color.random()))
            return
        if len(spoilified) <= 4:
            await ctx.send(embed=nextcord.Embed(title='Your message could not be converted!',
                                                color=nextcord.Color.random()))
            return
        else:
            await ctx.send(spoilified)

    @commands.command(aliases=['spoil'])
    async def spoilify(self, ctx, *, text: str):
        split = text.split(" ", maxsplit=1)
        spoilified = ''
        if split[0] == 'rem' or split[0] == 'remove':
            await ctx.message.delete()
            text = split[1]
        for i in text:
            spoilified += '||{}||'.format(i)
        if len(spoilified) + 2 >= 2000:
            await ctx.send(embed=nextcord.Embed(title='Your message in spoilers exceeds 2000 characters!'),
                           color=nextcord.Color.random())
            return
        if len(spoilified) <= 4:
            await ctx.send(embed=nextcord.Embed(title='Your message could not be converted!'),
                           color=nextcord.Color.random())
            return
        else:
            await ctx.send(spoilified)

    @cog_ext.cog_slash(name="act", description="Makes me act as though I'm another user...",
                       options=[
                           create_option(name="member", description="Member to act like", option_type=6,
                                         required=True),
                           create_option(name="message", description="Message to be typed", option_type=3,
                                         required=True)
                       ])
    async def _act(self, ctx, member: nextcord.Member, *, message):
        if message is None:
            await ctx.send(
                embed=nextcord.Embed(title=f'Please provide a message with that!', color=nextcord.Color.random()))
            return

        if '@' in str(message):
            await ctx.send(
                embed=nextcord.Embed(title=f"Imagine exploiting the act command like dis...\nNo pinging anyone please",
                                     color=nextcord.Color.random()))
            return

        try:
            webhook = await ctx.channel.create_webhook(name=member.display_name)
            try:
                await webhook.send(
                    message, username=member.display_name, avatar_url=member.avatar.url
                )
            except:
                await webhook.send(
                    message, username=member.display_name
                )
            webhooks = await ctx.channel.webhooks()
            for webhook in webhooks:
                try:
                    await webhook.delete()
                except:
                    return

        except nextcord.errors.Forbidden:
            await ctx.send(embed=nextcord.Embed(title="Ouch! I'm sorry but I got no perms.",
                                                description="I can't do the act command!",
                                                color=nextcord.Color.random()))

    @commands.command()
    async def act(self, ctx, member: nextcord.Member, *, message=None):
        if message is None:
            await ctx.send(
                embed=nextcord.Embed(title=f'Please provide a message with that!', color=nextcord.Color.random()))
            return

        if '@' in str(message):
            await ctx.send(
                embed=nextcord.Embed(title=f"Imagine exploiting the act command like dis...\nNo pinging anyone please",
                                     color=nextcord.Color.random()))
            return

        try:
            await ctx.message.delete()
            webhook = await ctx.channel.create_webhook(name=member.display_name)
            try:
                await webhook.send(
                    message, username=member.display_name, avatar_url=member.avatar.url
                )
            except:
                await webhook.send(
                    message, username=member.display_name
                )
            webhooks = await ctx.channel.webhooks()
            for webhook in webhooks:
                try:
                    await webhook.delete()
                except:
                    return

        except nextcord.errors.Forbidden:
            await ctx.send(embed=nextcord.Embed(title="Ouch! I'm sorry but I got no perms.",
                                                description="I can't do the act command!",
                                                color=nextcord.Color.random()))

    @cog_ext.cog_slash(name="encrypt", description="Encrypts your message in the ZOScript",
                       options=[
                           create_option(name="text_to_encrypt", description="Text to encrypt obviously", option_type=3,
                                         required=True)
                       ])
    async def _encrypt(self, ctx: SlashContext, *, text_to_encrypt: str):
        embed = nextcord.Embed(title="Encoding your message <a:zo_typing:873129455483256832>",
                               description="This stays in between us. :wink:\n Keep this a secret. :zipper_mouth:")
        embed.color = nextcord.Color.dark_blue()
        embed.set_footer(text="You all saw NOTHING")
        embed.add_field(name="Encrypted Text", value='```' + enc.encrypt_text(text_to_encrypt) + '```')
        message = await ctx.send(embed=embed)
        await message.add_reaction('<:trash:867001275634417714>')

        def check(reaction, user):
            return reaction.message.id == message.id and str(
                reaction.emoji) == '<:trash:867001275634417714>' and user == ctx.author

        await self.bot.wait_for('reaction_add', check=check)

        await message.delete()

    @commands.command(aliases=['enc', 'script'])
    async def encrypt(self, ctx, *, text_to_encrypt: str):
        embed = nextcord.Embed(title="Encoding your message <a:zo_typing:873129455483256832>",
                               description="This stays in between us. :wink:\n Keep this a secret. :zipper_mouth:")
        embed.color = nextcord.Color.dark_blue()
        embed.set_footer(text="You all saw NOTHING")
        embed.add_field(name="Encrypted Text", value='```' + enc.encrypt_text(text_to_encrypt) + '```')
        message = await ctx.send(embed=embed)
        await message.add_reaction('<:trash:867001275634417714>')

        def check(reaction, user):
            return reaction.message.id == message.id and str(
                reaction.emoji) == '<:trash:867001275634417714>' and user == ctx.author

        await self.bot.wait_for('reaction_add', check=check)

        await message.delete()

    @cog_ext.cog_slash(name="decrypt", description="Decrypts your ZOScript message to actual English",
                       options=[
                           create_option(name="text_to_decrypt", description="Text to decrypt obviously", option_type=3,
                                         required=True)
                       ])
    async def _decrypt(self, ctx: SlashContext, *, text_to_decrypt: str):
        embed = nextcord.Embed(title="Decoding your message <a:zo_typing:873129455483256832>",
                               description="This is your message. :face_with_monocle:\n Hope you have what you need. :slight_smile:")
        embed.color = nextcord.Color.dark_blue()

        embed.add_field(name="Encrypted Text", value='```' + dec.decrypt_text(text_to_decrypt) + '```')
        message = await ctx.send(embed=embed)
        await message.add_reaction('<:trash:867001275634417714>')

        def check(reaction, user):
            return reaction.message.id == message.id and str(
                reaction.emoji) == '<:trash:867001275634417714>' and user == ctx.author

        await self.bot.wait_for('reaction_add', check=check)
        await message.delete()

    @commands.command(aliases=['dec'])
    async def decrypt(self, ctx, *, text_to_decrypt: str):
        embed = nextcord.Embed(title="Decoding your message <a:zo_typing:873129455483256832>",
                               description="This is your message. :face_with_monocle:\n Hope you have what you need. :slight_smile:")
        embed.color = nextcord.Color.dark_blue()

        embed.add_field(name="Encrypted Text", value='```' + dec.decrypt_text(text_to_decrypt) + '```')
        message = await ctx.send(embed=embed)
        await message.add_reaction('<:trash:867001275634417714>')

        def check(reaction, user):
            return reaction.message.id == message.id and str(
                reaction.emoji) == '<:trash:867001275634417714>' and user == ctx.author

        await self.bot.wait_for('reaction_add', check=check)
        await message.delete()

    @cog_ext.cog_slash(name="binary", description="Converts message to binary as zeros and ones are cool",
                       options=[
                           create_option(name="text", description="Text to convert into binary", option_type=3,
                                         required=True)
                       ])
    async def _binary(self, ctx: SlashContext, *, text: str):
        def to_binary(a):
            l, m = [], []
            for i in a:
                l.append(ord(i))
            for i in l:
                m.append(int(bin(i)[2:]))
            return m

        a = to_binary(text)
        b = ' '.join(str(e) for e in a)
        embed = nextcord.Embed(title=f"Your text converted to binary.",
                               description="My devs are Zero And One.\nObviously I have a binary feature.",
                               color=nextcord.Color.random())
        embed.add_field(name=text, value=f"{b}", inline=False)
        embed.set_footer(text="I respect my devs")
        await ctx.send(embed=embed)

    @commands.command(aliases=['bin'])
    async def binary(self, ctx, *, string: str):
        def to_binary(a):
            l, m = [], []
            for i in a:
                l.append(ord(i))
            for i in l:
                m.append(int(bin(i)[2:]))
            return m

        a = to_binary(string)
        b = ' '.join(str(e) for e in a)
        embed = nextcord.Embed(title=f"Your text converted to binary.",
                               description="My devs are Zero And One.\nObviously I have a binary feature.",
                               color=nextcord.Color.random())
        embed.add_field(name=string, value=f"{b}", inline=False)
        embed.set_footer(text="I respect my devs")
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="choose", description="Lets you choose between the given options.",
                       options=[
                           create_option(name="choices",
                                         description="Choices for me to choose from (separate with comma)",
                                         option_type=3,
                                         required=True)
                       ])
    async def _choose(self, ctx: SlashContext, *, choices: str):
        if ',' in choices:
            choices = choices.split(",")
        else:
            choices = choices.split(" ")
        embed = nextcord.Embed(title=f"I choose...", description=f"{random.choice(choices)}",
                               color=nextcord.Color.random()
                               )
        embed.set_footer(text=f"It is better and I am awesome")
        await ctx.send(embed=embed)

    @commands.command(aliases=['ch'])
    async def choose(self, ctx, *, choices: str):
        if ',' in choices:
            choices = choices.split(",")
        else:
            choices = choices.split(" ")
        embed = nextcord.Embed(title=f"I choose...", description=f"{random.choice(choices)}",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"It is better and I am awesome")
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="hack", description="Hacks the required user.",
                       options=[
                           create_option(name="member",
                                         description="Member who I should hack Mwa ha ha ha",
                                         option_type=6,
                                         required=True)
                       ])
    async def _hack(self, ctx: SlashContext, member: nextcord.User):
        extensions_list = ["au", "in", "us", "uk", "fr"]
        emails_list = [f"{str(member.name)}@gmail.com",
                       f"{str(member.name)}@yahoo.co.{extensions_list[random.randint(0, 4)]}",
                       f"{str(member.name)}_is_cool@smallppmail.com",
                       f"{member.name}{str(random.randint(1, 100))}{str(random.randint(1, 100))}{str(random.randint(1, 100))}@gmail.com",
                       f"{str(member.name)}@oogamail.{random.choice(extensions_list)}"]
        passwords_list = [
            f"Deadpool{str(random.randint(1, 20))}{str(random.randint(1, 20))}{str(random.randint(1, 20))}",
            "Ineedfriends123", "ChamakChalo!@", "OogaBooga69", "@d****isaqt", "IluvCoffinDance2020"]
        dms_list = ["Yo i got ignored by her again", "Yup it's 3 inches", "Man i wanna punch you",
                    "I really need friends",
                    "Sure k", "THATS WHAT SHE SAID", "OOH GET REK'D", "lmao", "ooga", "That's cool",
                    "NOOO DONT FRIENDZONE ME PLSSSSSSS"]
        common_words = ["mom", "cringe", "LOL", "bOb", "pp", "yes", "ooga"]
        ips = ["46.193.82.45",
               "19.139.7.84",
               "237.16.92.184",
               "230.23.100.200",
               "100.234.227.192",
               "146.202.187.26",
               "237.6.170.85",
               "122.236.83.78",
               "207.95.203.62",
               "133.217.120.204",
               "237.36.146.217",
               "176.49.159.213",
               "64.171.92.234",
               "36.19.97.53",
               "199.12.190.203",
               "82.91.235.250",
               "39.21.236.178",
               "228.181.137.57",
               "7.51.143.121",
               "100.96.194.206"]
        hack_embed_1 = nextcord.Embed(title=f"Hacking {member.display_name}.....",
                                      description=f"Brute-forcing passwords and emails....")
        hack_embed_2 = nextcord.Embed(title=f"Login Credentials of {member.display_name}")
        hack_embed_2.add_field(name="Email", value=f"`{random.choice(emails_list)}`", inline=False)
        hack_embed_2.add_field(name="Password", value=f"`{random.choice(passwords_list)}`", inline=False)
        hack_embed_3 = nextcord.Embed(title="Fetching last DMs....")
        hack_embed_3.add_field(name="Last DMs", value=f"{random.choice(dms_list)}")
        hack_embed_4 = nextcord.Embed(title="Finding most commonly used word......")
        hack_embed_4.add_field(name=f"`Const_Commonly_used word=discord.Query(WordList[{member.display_name}])`",
                               value=random.choice(common_words))
        hack_embed_5 = nextcord.Embed(
            title=f"Inserting Virus into Discriminator: {member.discriminator} <a:ZO_IconLoadingGreen:866710482328485908>")
        hack_embed_6 = nextcord.Embed(title=f"Grabbing IP address of {member.display_name}......")
        hack_embed_6.add_field(name="IP Address", value=random.choice(ips))
        hack_embed_7 = nextcord.Embed(title=f"Done hacking {member}",
                                      description="It was totally real and flipping accurate")
        hack_embed_5.set_thumbnail(url=member.avatar.url)
        hack_embed_7.set_thumbnail(url=member.avatar.url)
        hack_embed_6.set_thumbnail(url=member.avatar.url)
        hack_embed_4.set_thumbnail(url=member.avatar.url)
        hack_embed_3.set_thumbnail(url=member.avatar.url)
        hack_embed_2.set_thumbnail(url=member.avatar.url)
        hack_embed_1.set_thumbnail(url=member.avatar.url)
        hack_embed_1.color = nextcord.Color.random()
        hack_embed_2.color = nextcord.Color.random()
        hack_embed_3.color = nextcord.Color.random()
        hack_embed_4.color = nextcord.Color.random()
        hack_embed_5.color = nextcord.Color.random()
        hack_embed_6.color = nextcord.Color.random()
        hack_embed_7.color = nextcord.Color.random()
        message = await ctx.send(embed=hack_embed_1)
        await asyncio.sleep(5)
        await message.edit(embed=hack_embed_2)
        await asyncio.sleep(5)
        await message.edit(embed=hack_embed_3)
        await asyncio.sleep(5)
        await message.edit(embed=hack_embed_4)
        await asyncio.sleep(5)
        await message.edit(embed=hack_embed_5)
        await asyncio.sleep(5)
        await message.edit(embed=hack_embed_6)
        await asyncio.sleep(5)
        await message.edit(embed=hack_embed_7)

    @commands.command(aliases=['infect', 'destroy'])
    async def hack(self, ctx, member: nextcord.User):
        extensions_list = ["au", "in", "us", "uk", "fr"]
        emails_list = [f"{str(member.name)}@gmail.com",
                       f"{str(member.name)}@yahoo.co.{extensions_list[random.randint(0, 4)]}",
                       f"{str(member.name)}_is_cool@smallppmail.com",
                       f"{member.name}{str(random.randint(1, 100))}{str(random.randint(1, 100))}{str(random.randint(1, 100))}@gmail.com",
                       f"{str(member.name)}@oogamail.{random.choice(extensions_list)}"]
        passwords_list = [
            f"Deadpool{str(random.randint(1, 20))}{str(random.randint(1, 20))}{str(random.randint(1, 20))}",
            "Ineedfriends123", "ChamakChalo!@", "OogaBooga69", "@d****isaqt", "IluvCoffinDance2020"]
        dms_list = ["Yo i got ignored by her again", "Yup it's 3 inches", "Man i wanna punch you",
                    "I really need friends",
                    "Sure k", "THATS WHAT SHE SAID", "OOH GET REK'D", "lmao", "ooga", "That's cool",
                    "NOOO DONT FRIENDZONE ME PLSSSSSSS"]
        common_words = ["mom", "cringe", "LOL", "bOb", "pp", "yes", "ooga"]
        ips = ["46.193.82.45",
               "19.139.7.84",
               "237.16.92.184",
               "230.23.100.200",
               "100.234.227.192",
               "146.202.187.26",
               "237.6.170.85",
               "122.236.83.78",
               "207.95.203.62",
               "133.217.120.204",
               "237.36.146.217",
               "176.49.159.213",
               "64.171.92.234",
               "36.19.97.53",
               "199.12.190.203",
               "82.91.235.250",
               "39.21.236.178",
               "228.181.137.57",
               "7.51.143.121",
               "100.96.194.206"]
        hack_embed_1 = nextcord.Embed(title=f"Hacking {member.display_name}.....",
                                      description=f"Brute-forcing passwords and emails....")
        hack_embed_2 = nextcord.Embed(title=f"Login Credentials of {member.display_name}")
        hack_embed_2.add_field(name="Email", value=f"`{random.choice(emails_list)}`", inline=False)
        hack_embed_2.add_field(name="Password", value=f"`{random.choice(passwords_list)}`", inline=False)
        hack_embed_3 = nextcord.Embed(title="Fetching last DMs....")
        hack_embed_3.add_field(name="Last DMs", value=f"{random.choice(dms_list)}")
        hack_embed_4 = nextcord.Embed(title="Finding most commonly used word......")
        hack_embed_4.add_field(name=f"`Const_Commonly_used word=discord.Query(WordList[{member.display_name}])`",
                               value=random.choice(common_words))
        hack_embed_5 = nextcord.Embed(
            title=f"Inserting Virus into Discriminator: {member.discriminator} <a:ZO_IconLoadingGreen:866710482328485908>")
        hack_embed_6 = nextcord.Embed(title=f"Grabbing IP address of {member.display_name}......")
        hack_embed_6.add_field(name="IP Address", value=random.choice(ips))
        hack_embed_7 = nextcord.Embed(title=f"Done hacking {member}",
                                      description="It was totally real and flipping accurate")
        hack_embed_5.set_thumbnail(url=member.avatar.url)
        hack_embed_7.set_thumbnail(url=member.avatar.url)
        hack_embed_6.set_thumbnail(url=member.avatar.url)
        hack_embed_4.set_thumbnail(url=member.avatar.url)
        hack_embed_3.set_thumbnail(url=member.avatar.url)
        hack_embed_2.set_thumbnail(url=member.avatar.url)
        hack_embed_1.set_thumbnail(url=member.avatar.url)
        hack_embed_1.color = nextcord.Color.random()
        hack_embed_2.color = nextcord.Color.random()
        hack_embed_3.color = nextcord.Color.random()
        hack_embed_4.color = nextcord.Color.random()
        hack_embed_5.color = nextcord.Color.random()
        hack_embed_6.color = nextcord.Color.random()
        hack_embed_7.color = nextcord.Color.random()
        message = await ctx.send(embed=hack_embed_1)
        await asyncio.sleep(5)
        await message.edit(embed=hack_embed_2)
        await asyncio.sleep(5)
        await message.edit(embed=hack_embed_3)
        await asyncio.sleep(5)
        await message.edit(embed=hack_embed_4)
        await asyncio.sleep(5)
        await message.edit(embed=hack_embed_5)
        await asyncio.sleep(5)
        await message.edit(embed=hack_embed_6)
        await asyncio.sleep(5)
        await message.edit(embed=hack_embed_7)

    @commands.command(aliases=['imgmemes', 'imagememe', 'imgmeme', 'img', 'image'])
    async def imagememes(self, ctx):
        embed = nextcord.Embed(title="Image Memes List",
                               description="Here is the list of POG image memes you can use.",
                               color=nextcord.Color.random())
        embed.add_field(name="List",
                        value=f"1.  {ctx.prefix}worthless\n2. {ctx.prefix}wanted\n3. {ctx.prefix}rip\n4. {ctx.prefix}chad.\n5. {ctx.prefix}yeet\n6. {ctx.prefix}shut")
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="imagememes", description="Gives you a list of image memes. Enjoy!")
    async def _imagememes(self, ctx: SlashContext):
        embed = nextcord.Embed(title="Image Memes List",
                               description="Here is the list of POG image memes you can use.",
                               inline=False,
                               color=nextcord.Color.random())
        embed.add_field(name="List",
                        value=f"1. /worthless\n2. /wanted\n3. /rip\n4. /chad\n5. /yeet\n6. /shut")
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(
        base="imagememe",
        name="worthless",
        description="Allows you to make stuff worthless",
        options=[
            create_option(name="worthless_text",
                          description="the text you want to show up on the paper",
                          option_type=3,
                          required=True
                          )])
    async def _worthless(self, ctx, worthless_text):
        img = Image.open('templates/worthless_template.jpg')
        draw = ImageDraw.Draw(img)
        txt = await commands.clean_content().convert(ctx, worthless_text)
        font = ImageFont.truetype("fonts/Roboto-Regular.ttf", size=21)
        text = adjust_text(txt, draw, font)
        draw.text((70, 70), text, (0, 0, 0), font=font)
        guild_id = str(ctx.guild.id)
        author_id = str(ctx.author.id)
        time1 = str(time.time())
        img.save(f'images/{guild_id + author_id + time1}.png')
        await ctx.send(file=nextcord.File(f'images/{guild_id + author_id + time1}.png'))

    @commands.command(aliases=['wls'])
    async def worthless(self, ctx, *, worthless_text):
        img = Image.open('templates/worthless_template.jpg')
        draw = ImageDraw.Draw(img)
        txt = await commands.clean_content().convert(ctx, worthless_text)
        font = ImageFont.truetype("fonts/Roboto-Regular.ttf", size=21)
        text = adjust_text(txt, draw, font)
        draw.text((70, 70), text, (0, 0, 0), font=font)
        guild_id = str(ctx.guild.id)
        author_id = str(ctx.author.id)
        time1 = str(time.time())
        img.save(f'images/{guild_id + author_id + time1}.png')
        await ctx.send(file=nextcord.File(f'images/{guild_id + author_id + time1}.png'))

    @cog_ext.cog_subcommand(
        base="imagememe",
        name="wanted",
        description="Place a bounty on that dude", options=[
            create_option(name="wanted_member",
                          description="The person who you wanna make wanted",
                          option_type=6,
                          required=False
                          )])
    async def _wanted(self, ctx, wanted_member: nextcord.Member = None):
        if not wanted_member:
            wanted_member = ctx.author

        wanted = Image.open('templates/wanted_template.jpg')
        asset = wanted_member.avatar.with_size(128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((224, 224))

        wanted.paste(pfp, (116, 216))
        guild_id = str(ctx.guild.id)
        author_id = str(ctx.author.id)
        time1 = str(time.time())
        wanted.save(f'images/{guild_id + author_id + time1}.png')
        await ctx.send(file=nextcord.File(f'images/{guild_id + author_id + time1}.png'))

    @commands.command()
    async def wanted(self, ctx, wanted_member: nextcord.Member = None):
        if not wanted_member:
            wanted_member = ctx.author

        wanted = Image.open('templates/wanted_template.jpg')
        asset = wanted_member.avatar.with_size(128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((224, 224))

        wanted.paste(pfp, (116, 216))
        guild_id = str(ctx.guild.id)
        author_id = str(ctx.author.id)
        time1 = str(time.time())
        wanted.save(f'images/{guild_id + author_id + time1}.png')
        await ctx.send(file=nextcord.File(f'images/{guild_id + author_id + time1}.png'))

    @cog_ext.cog_subcommand(
        base="imagememe",
        name="rip",
        description="Allows you give peace to the people you kill",
        options=[
            create_option(name="rip_member",
                          description="Member who should R.I.P",
                          option_type=6,
                          required=False
                          )])
    async def _rip(self, ctx: SlashContext, rip_member: nextcord.Member = None):
        if not rip_member:
            rip_member = ctx.author

        rip = Image.open('templates/rip_template.jpg').convert("RGBA")
        asset = rip_member.avatar.with_size(128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((240, 211))
        pfp = pfp.convert('RGB')

        mask = Image.new("L", pfp.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, mask.size[0], mask.size[1]), fill=255)
        rip.paste(pfp, (82, 235), mask=mask)
        guild_id = str(ctx.guild.id)
        author_id = str(ctx.author.id)
        time1 = str(time.time())
        rip.save(f'images/{guild_id + author_id + time1}.png')
        await ctx.send(file=nextcord.File(f'images/{guild_id + author_id + time1}.png'))

    @commands.command()
    async def rip(self, ctx, user: nextcord.Member = None):
        if not user:
            user = ctx.author

        rip = Image.open('templates/rip_template.jpg').convert("RGBA")
        asset = user.avatar.with_size(128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((240, 211))
        pfp = pfp.convert('RGB')

        mask = Image.new("L", pfp.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, mask.size[0], mask.size[1]), fill=255)
        rip.paste(pfp, (82, 235), mask=mask)
        guild_id = str(ctx.guild.id)
        author_id = str(ctx.author.id)
        time1 = str(time.time())
        rip.save(f'images/{guild_id + author_id + time1}.png')
        await ctx.send(file=nextcord.File(f'images/{guild_id + author_id + time1}.png'))

    @cog_ext.cog_subcommand(
        base="imagememe",
        name="chad",
        description="Makes things chadder, and I do mean chadder",
        options=[
            create_option(name="chad_member",
                          description="Member who needs to chad-up more",
                          option_type=6,
                          required=False
                          )])
    async def _chad(self, ctx: SlashContext, chad_member: nextcord.Member = None):
        if not chad_member:
            chad_member = ctx.author

        chad = Image.open('templates/chad_template.jpg').convert("RGBA")
        asset = chad_member.avatar.with_size(128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((298, 335))
        pfp = pfp.convert('RGB')
        mask = Image.new("L", pfp.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, mask.size[0], mask.size[1]), fill=255)
        chad.paste(pfp, (105, 2), mask=mask)
        guild_id = str(ctx.guild.id)
        author_id = str(ctx.author.id)
        time1 = str(time.time())
        chad.save(f'images/{guild_id + author_id + time1}.png')
        await ctx.send(file=nextcord.File(f'images/{guild_id + author_id + time1}.png'))

    @commands.command()
    async def chad(self, ctx, user: nextcord.Member = None):
        if not user:
            user = ctx.author

        chad = Image.open('templates/chad_template.jpg').convert("RGBA")
        asset = user.avatar.with_size(128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((298, 335))
        pfp = pfp.convert('RGB')
        mask = Image.new("L", pfp.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, mask.size[0], mask.size[1]), fill=255)
        chad.paste(pfp, (105, 2), mask=mask)
        guild_id = str(ctx.guild.id)
        author_id = str(ctx.author.id)
        time1 = str(time.time())
        chad.save(f'images/{guild_id + author_id + time1}.png')
        await ctx.send(file=nextcord.File(f'images/{guild_id + author_id + time1}.png'))

    @cog_ext.cog_subcommand(
        base="imagememe",
        name="yeet",
        description="Gives you a real-life picture of you throwing anyone of your choice.",
        options=[
            create_option(name="throw_member",
                          description="Throw DAT MAN LMAO",
                          option_type=6,
                          required=False
                          )])
    async def _yeet(self, ctx: SlashContext, throw_member: nextcord.User = None):
        if throw_member is None:
            throw_member = ctx.author

        yeet = Image.open('templates/yeet_template.jpg')
        asset = throw_member.avatar.with_size(128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((70, 70))
        pfp = pfp.convert('RGB')
        mask = Image.new("L", pfp.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, mask.size[0], mask.size[1]), fill=255)
        yeet.paste(pfp, (447, 417), mask=mask)
        guild_id = str(ctx.guild.id)
        author_id = str(ctx.author.id)
        time1 = str(time.time())
        yeet.save(f'images/{guild_id + author_id + time1}.png')
        await ctx.send(file=nextcord.File(f'images/{guild_id + author_id + time1}.png'))

    @commands.command(aliases=['throw'])
    async def yeet(self, ctx, user: nextcord.User = None):
        if user is None:
            user = ctx.author

        yeet = Image.open('templates/yeet_template.jpg')
        asset = user.avatar.with_size(128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((70, 70))
        pfp = pfp.convert('RGB')
        mask = Image.new("L", pfp.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, mask.size[0], mask.size[1]), fill=255)
        yeet.paste(pfp, (447, 417), mask=mask)
        guild_id = str(ctx.guild.id)
        author_id = str(ctx.author.id)
        time1 = str(time.time())
        yeet.save(f'images/{guild_id + author_id + time1}.png')
        await ctx.send(file=nextcord.File(f'images/{guild_id + author_id + time1}.png'))

    @cog_ext.cog_subcommand(
        base="imagememe",
        name="shut",
        description="Provides you a satisfying image when someone just won't keep quite...",
        options=[
            create_option(name="member",
                          description="Member who needs to be shutted.",
                          option_type=6,
                          required=False
                          )])
    async def _shut(self, ctx: SlashContext, user: nextcord.Member = None):
        if user is None:
            user = ctx.author

        shut = Image.open('templates/shut.jpg')
        asset = user.avatar.with_size(128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.convert('RGB')
        mask = Image.new("L", pfp.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, mask.size[0], mask.size[1]), fill=255)
        shut.paste(pfp, (180, 200), mask=mask)
        guild_id = str(ctx.guild.id)
        author_id = str(ctx.author.id)
        time1 = str(time.time())
        shut.save(f'images/{guild_id + author_id + time1}.png')
        await ctx.send(file=nextcord.File(f'images/{guild_id + author_id + time1}.png'))

    @commands.command(aliases=['shush', 'shutup', 'stfu'])
    async def shut(self, ctx, user: nextcord.Member = None):
        if user is None:
            user = ctx.author

        shut = Image.open('templates/shut.jpg')
        asset = user.avatar.with_size(128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.convert('RGB')
        mask = Image.new("L", pfp.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, mask.size[0], mask.size[1]), fill=255)
        shut.paste(pfp, (180, 200), mask=mask)
        guild_id = str(ctx.guild.id)
        author_id = str(ctx.author.id)
        time1 = str(time.time())
        shut.save(f'images/{guild_id + author_id + time1}.png')
        await ctx.send(file=nextcord.File(f'images/{guild_id + author_id + time1}.png'))

    @cog_ext.cog_slash(name="kill", description="Kill your friends... But minecraft style",
                       options=[
                           create_option(name="person",
                                         description="Person who I should kill IRL (totally)",
                                         option_type=3,
                                         required=False)
                       ])
    async def _kill(self, ctx: SlashContext, *, person='You'):
        victim = person
        killer = ctx.author.name
        # victim is person to kill
        # killer is person who does command
        phrases = [f"{victim} fell out of the world",
                   f"{victim} was shot by {killer}",
                   f"{victim} was pummeled by {killer}",
                   f"{victim} was pricked to death",
                   f"{victim} walked into a cactus whilst trying to escape {killer}",
                   f"{victim} drowned",
                   f"{victim} drowned whilst trying to escape {killer}",
                   f"{victim} experienced kinetic energy",
                   f"{victim} blew up",
                   f"{victim} was blown up by Creeper",
                   f"{victim} was killed by [Intentional Game Design]",
                   f"{victim} hit the ground too hard",
                   f"{victim} hit the ground too hard whilst trying to escape {killer}",
                   f"{victim} fell from a high place",
                   f"death.fell.accident.water"
                   f"{victim} was impaled on a stalagmite",
                   f"{victim} was squashed by a falling anvil",
                   f"{victim} went up in flames",
                   f"{victim} walked into fire whilst fighting {killer}",
                   f"{victim} burned to death",
                   f"{victim} tried to swim in lava"
                   f"{victim} was slain by {killer}",
                   f"{victim} was slain by {killer}",
                   f"{victim} suffocated in a wall",
                   f"{victim} was impaled by {killer}",
                   f"{victim} fell out of the world",
                   f"{victim} didn't want to live in the same world as {killer}",
                   f"{victim} withered away",
                   f"{victim} died",
                   f"{victim} was killed by magic"]
        await ctx.send(embed=nextcord.Embed(description=random.choice(phrases), color=nextcord.Color.random()))

    @commands.command()
    async def kill(self, ctx, *, user='You'):
        victim = user
        killer = ctx.message.author.name
        # victim is person to kill
        # killer is person who does command
        phrases = [f"{victim} fell out of the world",
                   f"{victim} was shot by {killer}",
                   f"{victim} was pummeled by {killer}",
                   f"{victim} was pricked to death",
                   f"{victim} walked into a cactus whilst trying to escape {killer}",
                   f"{victim} drowned",
                   f"{victim} drowned whilst trying to escape {killer}",
                   f"{victim} experienced kinetic energy",
                   f"{victim} blew up",
                   f"{victim} was blown up by Creeper",
                   f"{victim} was killed by [Intentional Game Design]",
                   f"{victim} hit the ground too hard",
                   f"{victim} hit the ground too hard whilst trying to escape {killer}",
                   f"{victim} fell from a high place",
                   f"death.fell.accident.water"
                   f"{victim} was impaled on a stalagmite",
                   f"{victim} was squashed by a falling anvil",
                   f"{victim} went up in flames",
                   f"{victim} walked into fire whilst fighting {killer}",
                   f"{victim} burned to death",
                   f"{victim} tried to swim in lava"
                   f"{victim} was slain by {killer}",
                   f"{victim} was slain by {killer}",
                   f"{victim} suffocated in a wall",
                   f"{victim} was impaled by {killer}",
                   f"{victim} fell out of the world",
                   f"{victim} didn't want to live in the same world as {killer}",
                   f"{victim} withered away",
                   f"{victim} died",
                   f"{victim} was killed by magic"]
        await ctx.send(embed=nextcord.Embed(description=random.choice(phrases), color=nextcord.Color.random()))

    @cog_ext.cog_slash(name="roast", description="Respect? Nah mate...")
    async def _roast(self, ctx: SlashContext):
        random_lines = random.choice(open("text_files/roasts.txt", encoding="utf-8").readlines())
        await ctx.send(embed=nextcord.Embed(description=random_lines, color=nextcord.Color.random()))

    @commands.command()
    async def roast(self, ctx):
        random_lines = random.choice(open("text_files/roasts.txt", encoding="utf-8").readlines())
        await ctx.send(embed=nextcord.Embed(description=random_lines, color=nextcord.Color.random()))

    @cog_ext.cog_slash(name="vcmeme", description="Lets you have some fun with the people in your VC.",
                       options=[
                           create_option(name="meme_number",
                                         description="Meme Number of the VC Meme you want (Check /vcmemes for list)",
                                         option_type=4,
                                         required=False)
                       ])
    async def _vcmeme(self, ctx: SlashContext, *, meme_number=None):
        if meme_number is None:
            page = 1
            pages = 5
            vc_embed_1 = nextcord.Embed(title="Here is the list of all VC MEMES", color=nextcord.Color.gold())
            vc_embed_1.add_field(name="1", value=f"20th Century", inline=False)
            vc_embed_1.add_field(name="2", value=f"AirHorn", inline=False)
            vc_embed_1.add_field(name="3", value=f"Big pew pew", inline=False)
            vc_embed_1.add_field(name="4", value=f"Bye", inline=False)
            vc_embed_1.add_field(name="5", value=f"CENSOR BEEP", inline=False)
            vc_embed_1.add_field(name="6", value=f"DENIED", inline=False)
            vc_embed_1.set_footer(text="Page 1 of 5")

            vc_embed_2 = nextcord.Embed(title="Here is the list of all VC MEMES", color=nextcord.Color.gold())
            vc_embed_2.add_field(name="7", value=f"DRUM ROLL", inline=False)
            vc_embed_2.add_field(name="8", value=f"DUN DUN DUN", inline=False)
            vc_embed_2.add_field(name="9", value=f"Elevator Music", inline=False)
            vc_embed_2.add_field(name="10", value=f"EXPLOSION", inline=False)
            vc_embed_2.add_field(name="11", value=f"Headshot", inline=False)
            vc_embed_2.add_field(name="12", value=f"HIDDEN AGENDA", inline=False)
            vc_embed_2.set_footer(text=f"Page 2 of 5")

            vc_embed_3 = nextcord.Embed(title="Here is the list of all VC MEMES", color=nextcord.Color.gold())
            vc_embed_3.add_field(name="13", value=f"Huh", inline=False)
            vc_embed_3.add_field(name="14", value=f"Illuminati Confirmed", inline=False)
            vc_embed_3.add_field(name="15", value=f"INVESTIGATIONS", inline=False)
            vc_embed_3.add_field(name="16", value=f"OH HELLO THERE", inline=False)
            vc_embed_3.add_field(name="17", value=f"Oof", inline=False)
            vc_embed_3.add_field(name="18", value=f"pew", inline=False)
            vc_embed_3.set_footer(text=f"Page 3 of 5")

            vc_embed_4 = nextcord.Embed(title="Here is the list of all VC MEMES", color=nextcord.Color.gold())
            vc_embed_4.add_field(name="19", value=f"pew pew", inline=False)
            vc_embed_4.add_field(name="20", value=f"REEEEE", inline=False)
            vc_embed_4.add_field(name="21", value=f"Rick Roll", inline=False)
            vc_embed_4.add_field(name="22", value=f"SAD MUSIC", inline=False)
            vc_embed_4.add_field(name="23", value=f"SAY WHAT", inline=False)
            vc_embed_4.add_field(name="24", value=f"SNEAKY SNITCH", inline=False)
            vc_embed_4.add_field(name="25", value=f"STOP RIGHT THERE", inline=False)
            vc_embed_4.set_footer(text=f"Page 4 of 5")

            vc_embed_5 = nextcord.Embed(title="Here is the list of all VC MEMES", color=nextcord.Color.gold())
            vc_embed_5.add_field(name="26", value=f"Surprise Mf", inline=False)
            vc_embed_5.add_field(name="27", value=f"Why are you running", inline=False)
            vc_embed_5.add_field(name="28", value=f"Why you bully me", inline=False)
            vc_embed_5.add_field(name="29", value=f"WOW", inline=False)
            vc_embed_5.add_field(name="30", value=f"YAY", inline=False)
            vc_embed_5.add_field(name="31", value=f"YEET", inline=False)
            vc_embed_5.add_field(name="32", value=f"You got it dude", inline=False)
            vc_embed_5.set_footer(text="Page 5 of 5")

            buttons = [
                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="back", emoji=leftbuttonemoji,
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="forward", emoji=rightbuttonemoji,
                              disabled=False),
                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                              disabled=False),
            ]
            action_row = create_actionrow(*buttons)

            vc_message = await ctx.send(embed=vc_embed_1, components=[action_row])

            while True:
                try:
                    response: ComponentContext = await wait_for_component(self.bot, messages=vc_message,
                                                                          components=action_row, timeout=300)
                    while response.author != ctx.author:
                        await response.reply("This ain't your button fool", hidden=True)
                        response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                              timeout=300)
                    if response.component['custom_id'] == "forward":
                        page += 1

                    elif response.component['custom_id'] == "back":
                        page -= 1

                    elif response.component['custom_id'] == "big_forward":
                        page = pages

                    elif response.component['custom_id'] == "big_back":
                        page = 1

                    if page == 1:
                        try:
                            buttons_left_disabled = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji=leftbuttonemoji,
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji=rightbuttonemoji,
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row = create_actionrow(*buttons_left_disabled)
                            await response.edit_origin(embed=vc_embed_1, components=[action_row])

                        except:
                            pass

                    elif page == 2:
                        try:
                            buttons_normal = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji=leftbuttonemoji,
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji=rightbuttonemoji,
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row2 = create_actionrow(*buttons_normal)
                            await response.edit_origin(embed=vc_embed_2, components=[action_row2])

                        except:
                            pass
                    elif page == 3:
                        try:
                            buttons_normal = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji=leftbuttonemoji,
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji=rightbuttonemoji,
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row3 = create_actionrow(*buttons_normal)
                            await response.edit_origin(embed=vc_embed_3, components=[action_row3])

                        except:
                            pass
                    elif page == 4:
                        try:
                            buttons_right_disabled = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji=leftbuttonemoji,
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji=rightbuttonemoji,
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row4 = create_actionrow(*buttons_right_disabled)
                            await response.edit_origin(embed=vc_embed_4, components=[action_row4])

                        except:
                            pass

                    elif page == 5:
                        try:
                            buttons_right_disabled = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji=leftbuttonemoji,
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji=rightbuttonemoji,
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=True),
                            ]
                            action_row5 = create_actionrow(*buttons_right_disabled)
                            await response.edit_origin(embed=vc_embed_5, components=[action_row5])

                        except:
                            pass
                except asyncio.TimeoutError:
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=vc_message)
                    buttons_all_disabled = [
                        create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="back", emoji=leftbuttonemoji,
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="forward", emoji=rightbuttonemoji,
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                      disabled=True),
                    ]
                    action_row = create_actionrow(*buttons_all_disabled)
                    await response.edit_origin(components=[action_row])
        else:
            meme_number = str(meme_number)
            voice: nextcord.VoiceClient = nextcord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            try:
                if voice and voice.is_connected():
                    await voice.move_to(ctx.author.voice.channel)
                else:
                    voice = await ctx.author.voice.channel.connect()
            except:
                await ctx.send(embed=nextcord.Embed(title="JOIN A VOICE CHANNEL FIRST", color=nextcord.Color.random()))
            if "20th century" in meme_number.lower() or "1" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/20th Century.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "airhorn" in meme_number.lower() or "2" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/AirHorn.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "big pew pew" in meme_number.lower() or "3" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/Big pew pew.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "bye" in meme_number.lower() or "4" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/Big pew pew.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "censor" in meme_number.lower() or "5" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/CENSOR BEEP.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "denied" in meme_number.lower() or "6" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/DENIED.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "drum roll" in meme_number.lower() or "7" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/DRUM ROLL.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "dun dun dun" in meme_number.lower() or "8" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/DUN DUN DUN.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "elevator music" in meme_number.lower() or "9" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/Elevator Music.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "headshot" in meme_number.lower() or "11" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/Headshot.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "explosion" in meme_number.lower() or "10" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/EXPLOSION.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "hidden agenda" in meme_number.lower() or "12" in meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/HIDDEN AGENDA.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "huh" in meme_number.lower() or "13" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/Huh.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "illuminati confirmed" in meme_number.lower() or "14" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/Illuminati Confirmed.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "investigations" in meme_number.lower() or "15" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/INVESTIGATIONS.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "oh hello there" in meme_number.lower() or "16" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/OH HELLO THERE.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "oof" in meme_number.lower() or "17" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/Oof.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "pew" in meme_number.lower() or "18" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/pew.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "pew pew" in meme_number.lower() or "19" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/pew pew.wav'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "reee" in meme_number.lower() or "20" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/REEEEE.m4a'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "rickroll" in meme_number.lower() or "21" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/rickroll.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "sad music" in meme_number.lower() or "22" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/SAD MUSIC.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "say what" in meme_number.lower() or "23" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/SAY WHAT.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "sneaky snitch" in meme_number.lower() or "24" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/SNEAKY SNITCH.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "stop right there" in meme_number.lower() or "25" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/STOP RIGHT THERE.m4a'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "surprise mf" in meme_number.lower() or "26" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/Surprise Mf.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "why are you running" in meme_number.lower() or "27" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/Why are you running.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "why you bully me" in meme_number.lower() or "28" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/Why you bully me.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "wow" in meme_number.lower() or "29" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/WOW.m4a'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "yay" in meme_number.lower() or "30" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/YAY.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "yeet" in meme_number.lower() or "31" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/YEET.m4a'))
                await ctx.send('\N{OK HAND SIGN}')
            elif "you got it dude" in meme_number.lower() or "32" == meme_number:
                voice.play(nextcord.FFmpegPCMAudio(
                    source='sounds/You got it dude.mp3'))
                await ctx.send('\N{OK HAND SIGN}')
            else:
                embed2 = nextcord.Embed(title=f"The meme {meme_number} was not found!",
                                        description="Thanks for wasting my time!",
                                        color=nextcord.Color.red())
                embed2.add_field(name=f"Wrong Meme!",
                                 value="If you would like the owners to add a voice meme, [click here](https://zeroandone.ml/contact/)")
                await ctx.send(embed=embed2)
                await voice.disconnect()

    @commands.command(aliases=['vcm', 'vcmemes'])
    async def vcmeme(self, ctx, *, meme: str):
        voice: nextcord.VoiceClient = nextcord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(ctx.author.voice.channel)
        else:
            voice = await ctx.message.author.voice.channel.connect()
        if "20th century" in meme.lower() or "1" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/20th Century.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "airhorn" in meme.lower() or "2" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/AirHorn.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "big pew pew" in meme.lower() or "3" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/Big pew pew.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "bye" in meme.lower() or "4" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/Big pew pew.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "censor" in meme.lower() or "5" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/CENSOR BEEP.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "denied" in meme.lower() or "6" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/DENIED.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "drum roll" in meme.lower() or "7" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/DRUM ROLL.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "dun dun dun" in meme.lower() or "8" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/DUN DUN DUN.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "elevator music" in meme.lower() or "9" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/Elevator Music.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "headshot" in meme.lower() or "11" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/Headshot.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "explosion" in meme.lower() or "10" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/EXPLOSION.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "hidden agenda" in meme.lower() or "12" in meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/HIDDEN AGENDA.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "huh" in meme.lower() or "13" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/Huh.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "illuminati confirmed" in meme.lower() or "14" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/Illuminati Confirmed.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "investigations" in meme.lower() or "15" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/INVESTIGATIONS.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "oh hello there" in meme.lower() or "16" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/OH HELLO THERE.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "oof" in meme.lower() or "17" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/Oof.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "pew" in meme.lower() or "18" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/pew.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "pew pew" in meme.lower() or "19" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/pew pew.wav'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "reee" in meme.lower() or "20" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/REEEEE.m4a'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "rickroll" in meme.lower() or "21" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/rickroll.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "sad music" in meme.lower() or "22" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/SAD MUSIC.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "say what" in meme.lower() or "23" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/SAY WHAT.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "sneaky snitch" in meme.lower() or "24" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/SNEAKY SNITCH.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "stop right there" in meme.lower() or "25" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/STOP RIGHT THERE.m4a'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "surprise mf" in meme.lower() or "26" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/Surprise Mf.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "why are you running" in meme.lower() or "27" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/Why are you running.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "why you bully me" in meme.lower() or "28" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/Why you bully me.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "wow" in meme.lower() or "29" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/WOW.m4a'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "yeet" in meme.lower() or "30" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/YEET.m4a'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "yay" in meme.lower() or "31" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/YAY.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        elif "you got it dude" in meme.lower() or "32" == meme:
            voice.play(nextcord.FFmpegPCMAudio(
                source='sounds/You got it dude.mp3'))
            await ctx.send('\N{OK HAND SIGN}')
        else:
            embed2 = nextcord.Embed(title=f"The meme {meme} was not found!",
                                    description="Thanks for wasting my time!",
                                    color=nextcord.Color.red())
            embed2.add_field(name=f"Wrong Meme!",
                             value="If you would like the owners to add a voice meme, [click here](https://zeroandone.ml/contact/)")
            await ctx.send(embed=embed2)
            await voice.disconnect()

    @vcmeme.error
    async def vcmeme_error(self, ctx, error):
        page = 1
        pages = 5
        if isinstance(error, commands.MissingRequiredArgument):
            vc_embed_1 = nextcord.Embed(title="Here is the list of all VC MEMES", color=nextcord.Color.gold())
            vc_embed_1.add_field(name="1", value=f"20th Century", inline=False)
            vc_embed_1.add_field(name="2", value=f"AirHorn", inline=False)
            vc_embed_1.add_field(name="3", value=f"Big pew pew", inline=False)
            vc_embed_1.add_field(name="4", value=f"Bye", inline=False)
            vc_embed_1.add_field(name="5", value=f"CENSOR BEEP", inline=False)
            vc_embed_1.add_field(name="6", value=f"DENIED", inline=False)
            vc_embed_1.set_footer(text="Page 1 of 5")

            vc_embed_2 = nextcord.Embed(title="Here is the list of all VC MEMES", color=nextcord.Color.gold())
            vc_embed_2.add_field(name="7", value=f"DRUM ROLL", inline=False)
            vc_embed_2.add_field(name="8", value=f"DUN DUN DUN", inline=False)
            vc_embed_2.add_field(name="9", value=f"Elevator Music", inline=False)
            vc_embed_2.add_field(name="10", value=f"EXPLOSION", inline=False)
            vc_embed_2.add_field(name="11", value=f"Headshot", inline=False)
            vc_embed_2.add_field(name="12", value=f"HIDDEN AGENDA", inline=False)
            vc_embed_2.set_footer(text=f"Page 2 of 5")

            vc_embed_3 = nextcord.Embed(title="Here is the list of all VC MEMES", color=nextcord.Color.gold())
            vc_embed_3.add_field(name="13", value=f"Huh", inline=False)
            vc_embed_3.add_field(name="14", value=f"Illuminati Confirmed", inline=False)
            vc_embed_3.add_field(name="15", value=f"INVESTIGATIONS", inline=False)
            vc_embed_3.add_field(name="16", value=f"OH HELLO THERE", inline=False)
            vc_embed_3.add_field(name="17", value=f"Oof", inline=False)
            vc_embed_3.add_field(name="18", value=f"pew", inline=False)
            vc_embed_3.set_footer(text=f"Page 3 of 5")

            vc_embed_4 = nextcord.Embed(title="Here is the list of all VC MEMES", color=nextcord.Color.gold())
            vc_embed_4.add_field(name="19", value=f"pew pew", inline=False)
            vc_embed_4.add_field(name="20", value=f"REEEEE", inline=False)
            vc_embed_4.add_field(name="21", value=f"Rick Roll", inline=False)
            vc_embed_4.add_field(name="22", value=f"SAD MUSIC", inline=False)
            vc_embed_4.add_field(name="23", value=f"SAY WHAT", inline=False)
            vc_embed_4.add_field(name="24", value=f"SNEAKY SNITCH", inline=False)
            vc_embed_4.add_field(name="25", value=f"STOP RIGHT THERE", inline=False)
            vc_embed_4.set_footer(text=f"Page 4 of 5")

            vc_embed_5 = nextcord.Embed(title="Here is the list of all VC MEMES", color=nextcord.Color.gold())
            vc_embed_5.add_field(name="26", value=f"Surprise Mf", inline=False)
            vc_embed_5.add_field(name="27", value=f"Why are you running", inline=False)
            vc_embed_5.add_field(name="28", value=f"Why you bully me", inline=False)
            vc_embed_5.add_field(name="29", value=f"WOW", inline=False)
            vc_embed_5.add_field(name="30", value=f"YAY", inline=False)
            vc_embed_5.add_field(name="31", value=f"YEET", inline=False)
            vc_embed_5.add_field(name="32", value=f"You got it dude", inline=False)
            vc_embed_5.set_footer(text="Page 5 of 5")

            buttons = [
                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="back", emoji=leftbuttonemoji,
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="forward", emoji=rightbuttonemoji,
                              disabled=False),
                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                              disabled=False),
            ]
            action_row = create_actionrow(*buttons)

            vc_message = await ctx.send(embed=vc_embed_1, components=[action_row])

            while True:
                try:
                    response: ComponentContext = await wait_for_component(self.bot, messages=vc_message,
                                                                          components=action_row, timeout=300)
                    while response.author != ctx.author:
                        await response.reply("This ain't your button fool", hidden=True)
                        response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                              timeout=300)
                    if response.component['custom_id'] == "forward":
                        page += 1

                    elif response.component['custom_id'] == "back":
                        page -= 1

                    elif response.component['custom_id'] == "big_forward":
                        page = pages

                    elif response.component['custom_id'] == "big_back":
                        page = 1

                    if page == 1:
                        try:
                            buttons_left_disabled = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji=leftbuttonemoji,
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji=rightbuttonemoji,
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row = create_actionrow(*buttons_left_disabled)
                            await response.edit_origin(embed=vc_embed_1, components=[action_row])

                        except:
                            pass

                    elif page == 2:
                        try:
                            buttons_normal = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji=leftbuttonemoji,
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji=rightbuttonemoji,
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row2 = create_actionrow(*buttons_normal)
                            await response.edit_origin(embed=vc_embed_2, components=[action_row2])

                        except:
                            pass
                    elif page == 3:
                        try:
                            buttons_normal = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji=leftbuttonemoji,
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji=rightbuttonemoji,
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row3 = create_actionrow(*buttons_normal)
                            await response.edit_origin(embed=vc_embed_3, components=[action_row3])

                        except:
                            pass
                    elif page == 4:
                        try:
                            buttons_right_disabled = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji=leftbuttonemoji,
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji=rightbuttonemoji,
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row4 = create_actionrow(*buttons_right_disabled)
                            await response.edit_origin(embed=vc_embed_4, components=[action_row4])

                        except:
                            pass

                    elif page == 5:
                        try:
                            buttons_right_disabled = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji=leftbuttonemoji,
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji=rightbuttonemoji,
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=True),
                            ]
                            action_row5 = create_actionrow(*buttons_right_disabled)
                            await response.edit_origin(embed=vc_embed_5, components=[action_row5])

                        except:
                            pass
                except asyncio.TimeoutError:
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=vc_message)
                    buttons_all_disabled = [
                        create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="back", emoji=leftbuttonemoji,
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="forward", emoji=rightbuttonemoji,
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                      disabled=True),
                    ]
                    action_row = create_actionrow(*buttons_all_disabled)
                    await response.edit_origin(components=[action_row])

        elif isinstance(error, nextcord.ext.commands.errors.CommandInvokeError):
            await ctx.send(embed=nextcord.Embed(title=f"Sorry Im already playing audio. Do /stop to stop it",
                                                color=nextcord.Color.random()))

        else:
            raise error

    @cog_ext.cog_slash(name="shoo", description="Kicks me out of a VC cause bandwith don't come for free.")
    async def _shoo(self, ctx: SlashContext):
        try:
            channel = ctx.author.voice.channel
            await ctx.voice_client.disconnect()
            await ctx.send(embed=nextcord.Embed(description=f"Left {channel}",
                                                color=nextcord.Color.random()))

        except:
            await ctx.send(
                embed=nextcord.Embed(title="You are not connected to a voice channel", color=nextcord.Color.random()))

    @commands.command(aliases=['leave', 'disconnect'])
    async def shoo(self, ctx):
        try:
            channel = ctx.message.author.voice.channel
            await ctx.voice_client.disconnect()
            await ctx.send(embed=nextcord.Embed(description=f"Left {channel}",
                                                color=nextcord.Color.random()))

        except:
            await ctx.send(
                embed=nextcord.Embed(title="You are not connected to a voice channel", color=nextcord.Color.random()
                                     ))

    @cog_ext.cog_slash(name="pause", description="Pauses my VC activity.")
    async def _pause(self, ctx: SlashContext):
        try:
            channel = ctx.author.voice.channel
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            voice.pause()
            await ctx.send(embed=nextcord.Embed(description=f"Paused playing Audio in {channel}",
                                                color=nextcord.Color.random()))

        except:
            await ctx.send(
                embed=nextcord.Embed(title="You are not connected to a voice channel", color=nextcord.Color.random()))

    @commands.command()
    async def pause(self, ctx):
        try:
            channel = ctx.message.author.voice.channel
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            voice.pause()
            await ctx.send(embed=nextcord.Embed(description=f"Paused playing Audio in {channel}",
                                                color=nextcord.Color.random()))

        except:
            await ctx.send(
                embed=nextcord.Embed(title="You are not connected to a voice channel", color=nextcord.Color.random()))

    @cog_ext.cog_slash(name="resume", description="Pauses my VC activity.")
    async def _resume(self, ctx: SlashContext):
        try:
            channel = ctx.author.voice.channel
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            voice.resume()
            await ctx.send(embed=nextcord.Embed(description=f"Resumed playing Audio in {channel}",
                                                color=nextcord.Color.random()))

        except:
            await ctx.send(
                embed=nextcord.Embed(title="You are not connected to a voice channel", color=nextcord.Color.random()
                                     ))

    @commands.command()
    async def resume(self, ctx):
        try:
            channel = ctx.message.author.voice.channel
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            voice.resume()
            await ctx.send(embed=nextcord.Embed(description=f"Resumed playing Audio in {channel}",
                                                color=nextcord.Color.random()))

        except:
            await ctx.send(
                embed=nextcord.Embed(title="You are not connected to a voice channel", color=nextcord.Color.random()
                                     ))

    @cog_ext.cog_slash(name="stop", description="Stops me from doing what I'm doing in a VC.")
    async def _stop(self, ctx: SlashContext):
        try:
            channel = ctx.message.author.voice.channel
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            voice.stop()
            await ctx.send(embed=nextcord.Embed(description=f"Stopped playing Audio in {channel}",
                                                color=nextcord.Color.random()))

        except:
            await ctx.send(
                embed=nextcord.Embed(title="You are not connected to a voice channel", color=nextcord.Color.random()
                                     ))

    @commands.command()
    async def stop(self, ctx):
        try:
            channel = ctx.message.author.voice.channel
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            voice.stop()
            await ctx.send(embed=nextcord.Embed(description=f"Stopped playing Audio in {channel}",
                                                color=nextcord.Color.random()))

        except:
            await ctx.send(
                embed=nextcord.Embed(title="You are not connected to a voice channel", color=nextcord.Color.random()
                                     ))

    @cog_ext.cog_slash(name="quote",
                       description="Allows you to quote the sayings of your fellow human beings. (Unless you use a bot name)",
                       options=[
                           create_option(name="quoter",
                                         description="Person who I should quote",
                                         option_type=3,
                                         required=True),
                           create_option(name="quote",
                                         description="The quote of fame",
                                         option_type=3,
                                         required=True)])
    async def _quote(self, ctx: SlashContext, quoter, *, quote):
        quote = await commands.clean_content().convert(quote)
        quoter = await commands.clean_content().convert(quoter)
        embed = nextcord.Embed(
            description=f"\"*{quote}*\""
        )
        embed.color = nextcord.Color.random()
        embed.set_footer(text=f"- {quoter.replace('@', '')}")
        await ctx.send(embed=embed)

    @commands.command(aliases=['qu', 'q'])
    async def quote(self, ctx, *, quote_info):
        if ',' not in quote_info:
            await ctx.send(embed=nextcord.Embed(title="You must put the quoter, then a COMMA, then the quote",
                                                color=nextcord.Color.random()))
            return
        split_quote = quote_info.split(",", maxsplit=1)
        quoter = await commands.clean_content().convert(ctx, split_quote[0])
        quote = await commands.clean_content().convert(ctx, split_quote[1].strip())
        embed = nextcord.Embed(
            description=f"\"*{quote}*\""
        )
        embed.color = nextcord.Color.random()
        embed.set_footer(text=f"- {quoter.replace('@', '')}")
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @cog_ext.cog_slash(name="joke",
                       description="Allows you to quote the sayings of your fellow human beings. (Unless you use a bot name)")
    async def _joke(self, ctx: SlashContext):
        data = self.jokes_json
        i = random.randint(1, 386)
        data = data[i]
        setup_embed = nextcord.Embed(title=data["setup"], color=nextcord.Color.random())
        punchline_embed = nextcord.Embed(title=data["setup"], description=data["punchline"],
                                         color=nextcord.Color.random())
        to_edit = await ctx.send(embed=setup_embed)
        await asyncio.sleep(2)
        await to_edit.edit(embed=punchline_embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=['jokes'])
    async def joke(self, ctx):
        data = self.jokes_json
        i = random.randint(1, 386)
        data = data[i]
        setup_embed = nextcord.Embed(title=data["setup"], color=nextcord.Color.random())
        punchline_embed = nextcord.Embed(title=data["setup"], description=data["punchline"],
                                         color=nextcord.Color.random())
        to_edit = await ctx.send(embed=setup_embed)
        await asyncio.sleep(2)
        await to_edit.edit(embed=punchline_embed)

    @joke.error
    async def joke_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=nextcord.Embed(title=f"This command is on cooldown",
                                                description=f"try again after {round(error.retry_after)} seconds.",
                                                color=nextcord.Color.random()))

    @commands.cooldown(1, 4, commands.BucketType.user)
    @cog_ext.cog_slash(name="meme",
                       description="Gives you memes")
    async def _meme(self, ctx: SlashContext):
        r = requests.get(url="https://meme-api.herokuapp.com/gimme")
        data = r.json()
        if data["nsfw"] is False:
            embed = nextcord.Embed(title=data["title"], color=nextcord.Color.random())
            embed.set_image(url=data["url"])
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=nextcord.Embed(title="NO NSFW MEMES HERE", color=nextcord.Color.random()))
            pass

    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.command(aliases=['MEME', 'Meme'])
    async def meme(self, ctx):
        r = requests.get(url="https://meme-api.herokuapp.com/gimme")
        data = r.json()
        if data["nsfw"] is False:
            embed = nextcord.Embed(title=data["title"], color=nextcord.Color.random())
            embed.set_image(url=data["url"])
            await ctx.send(embed=embed)
        else:
            pass

    @meme.error
    async def joke_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=nextcord.Embed(title=f"This command is on cooldown",
                                                description=f"try again after {round(error.retry_after)} seconds.",
                                                color=nextcord.Color.random()))

    @cog_ext.cog_slash(name="dog", description="Its a dog!")
    async def _dog(self, ctx: SlashContext):
        r = requests.get(url="https://dog.ceo/api/breeds/image/random")
        data = r.json()
        embed = nextcord.Embed(title="Woof!", color=nextcord.Color.random())
        embed.set_image(url=data["message"])
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['doggo', 'Doggy'])
    async def dog(self, ctx):
        r = requests.get(url="https://dog.ceo/api/breeds/image/random")
        data = r.json()
        embed = nextcord.Embed(title="Woof!", color=nextcord.Color.random())
        embed.set_image(url=data["message"])
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="cat",
                       description="Its a cat!")
    async def _cat(self, ctx: SlashContext):
        embed = nextcord.Embed(title="Meow!", color=nextcord.Color.random())
        embed.set_image(url="https://cataas.com/cat")
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['kitty', 'meow'])
    async def cat(self, ctx):
        embed = nextcord.Embed(title="Meow!", color=nextcord.Color.random())
        await ctx.send(embed=embed)

    @dog.error
    async def dog_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=nextcord.Embed(title=f"This command is on cooldown",
                                                description=f"try again after {round(error.retry_after)} seconds.",
                                                color=nextcord.Color.random()))

    @cat.error
    async def cat_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=nextcord.Embed(title=f"This command is on cooldown",
                                                description=f"try again after {round(error.retry_after)} seconds.",
                                                color=nextcord.Color.random()))

    @hack.error
    async def hack_error(self, ctx, error):
        member = ctx.author

        member_var = member.display_name

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=nextcord.Embed(title="Your kidding right?",
                                                description=f"{member_var} please mention a user to hack\n That way, I won't need to hack thin air!!",
                                                color=nextcord.Color.random()))

        elif isinstance(error, commands.UserNotFound):
            await ctx.send(embed=nextcord.Embed(title="This is ridiculous",
                                                description=f"<:ZO_Bruh:866252668225585152> {member_var} have the brain cells to mention the target smh.\n How are you unable to MENTION SOMEONE"))

        else:
            raise error

    @ask.error
    async def ask_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"What were you asking again?",
                                   description=f"All I heard was ___",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Either I'm deaf, or you didn't even ask.")
            await ctx.send(embed=embed)

        else:
            raise error

    @gif.error
    async def gif_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"What were you searching gifs for again?",
                                   description=f"All I heard was ___",
                                   color=nextcord.Color.random())
            embed.set_footer(
                text="Either I'm deaf, or you didn't even type anything to search.")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.CommandInvokeError):
            embed = nextcord.Embed(title=f"Lmao sad life!",
                                   description=f"Didn't find anything",

                                   color=nextcord.Color.random())
            embed.set_footer(text=f"sad puppy")
            await ctx.send(embed=embed)

        else:
            raise error

    @epicgamerrate.error
    async def gamerrate_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed = nextcord.Embed(title=f"I wish I knew how EPIC this user is.",
                                   description=f"But sadly he doesn't exist.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Ima go cry now")
            await ctx.send(embed=embed)

        else:
            raise error

    @simprate.error
    async def simprate_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed = nextcord.Embed(title=f"Trying to see how much they simp eh?",
                                   description=f"Oh wait. They don't exist!.\n So ima guess its 0",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Im smart BOI")
            await ctx.send(embed=embed)

        else:
            raise error

    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"Ah I feel you",
                                   description=f"This command is way too complex. Use {ctx.prefix}help poll",
                                   color=nextcord.Color.random())
            embed.set_footer(
                text="The one command where mistakes be understandable")
            await ctx.send(embed=embed)

        else:
            raise error

    @ascii.error
    async def ascii_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"Done!",
                                   description=f"Successfully converted *nothing* into a beautiful picture!\nNow try actually giving me something to use",
                                   color=nextcord.Color.random())
            embed.set_footer(text="smh smh SMH")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.errors.CommandInvokeError):
            embed = nextcord.Embed(title=f"BRUHH!",
                                   description=f"That is too big to send!!",
                                   color=nextcord.Color.random())
            embed.set_footer(text="That's what she said")
            await ctx.send(embed=embed)

        else:
            raise error

    @emojify.error
    async def emojify_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(
                ':regional_indicator_n::regional_indicator_o::regional_indicator_t::regional_indicator_h::regional_indicator_i::regional_indicator_n::regional_indicator_g: \t:regional_indicator_l::regional_indicator_m::regional_indicator_a::regional_indicator_o:')

        else:
            raise error

    @spoilify.error
    async def spoilify_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(embed=nextcord.Embed(title=f"For god's sake",
                                                description="What do you want me to spoil?",
                                                color=nextcord.Color.random()))

        elif isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(embed=nextcord.Embed(title=f"For god's sake",
                                                description="What do you want me to spoil and why are you trying to hide it?",
                                                color=nextcord.Color.random()))

        else:
            raise error

    @act.error
    async def act_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"Bruh please give me all arguments for the command!",
                                   description=f"It is... `{ctx.prefix}act @person_you_wanna_enact stuff_u_want_it_to_say`",
                                   color=nextcord.Color.random())
            embed.set_footer(text="smh smh SMH")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MemberNotFound):
            embed = nextcord.Embed(title=f"BRUHH!",
                                   description=f"Mention a human to act",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Who am i supposed to mimic... Joe Ma--")
            await ctx.send(embed=embed)

        else:
            raise error

    @binary.error
    async def binary_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"Well you didn't input anything",
                                   description=f"I'm assuming you want the binary code of a space key.\nIt's `00100000",
                                   color=nextcord.Color.random())
            embed.set_footer(
                text="Tho you didn't want the binary of space did you?")
            await ctx.send(embed=embed)

        if isinstance(error, nextcord.ext.commands.errors.CommandInvokeError):
            embed = nextcord.Embed(title="Chill out dude",
                                   description="I can't send you something that long.\nTry putting a shorter message.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="That was going to be SO difficult to send")
            await ctx.send(embed=embed)
        else:
            raise error

    @encrypt.error
    async def encrypt_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"Encrypted!",
                                   description=f"`*Nothing*`",
                                   color=nextcord.Color.random())
            embed.set_footer(text="lollers")
            await ctx.send(embed=embed)

        else:
            raise error

    @decrypt.error
    async def decrypt_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"Decrypted!",
                                   description=f"`*Nothing*`",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Even more lollers")
            await ctx.send(embed=embed)

        else:
            raise error

    @choose.error
    async def choose_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed = nextcord.Embed(title=f"Alright, if that's what you wish",
                                   description=f"I choose this particular non-existent thing over the other.",
                                   color=nextcord.Color.random())
            embed.set_footer(
                text="Don't really know what you will achieve with that knowledge")
            await ctx.send(embed=embed)

        else:
            raise error

    @worthless.error
    async def worthless_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"Worthlessness has a limit",
                                   description=f"`*Nothing*` can't be worthless",
                                   color=nextcord.Color.random())
            embed.set_footer(text="This is philosophy")
            await ctx.send(embed=embed)

        else:
            raise error

    @wanted.error
    async def wanted_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            if isinstance(error, commands.MissingRequiredArgument):
                embed = nextcord.Embed(title=f"Do you hate your legal system?",
                                       description=f"Your trying to make the authorities do their best to try and catch *no one*",
                                       color=nextcord.Color.random())
                embed.set_footer(text="I wonder why...")
                await ctx.send(embed=embed)

        else:
            raise error

    @rip.error
    async def rip_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed = nextcord.Embed(title=f"Imagine going to a grave yard...",
                                   description=f"And finding gravestones where people have no names.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Low budget cemetery")
            await ctx.send(embed=embed)

        else:
            raise error

    @chad.error
    async def chad_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed = nextcord.Embed(title=f"Chad is great!",
                                   description=f"I mean, I am Chad.\nBut Chad without a head... naaa",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Headless Chad WOULD be funny tho")
            await ctx.send(embed=embed)

        else:
            raise error

    @yeet.error
    async def yeet_error(self, ctx, error):
        if isinstance(error, commands.UserNotFound):
            embed = nextcord.Embed(title=f"Yeet is great!",
                                   description=f"So you yeeted the air.\nBut next time lets just stick to people",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Yeet Go Woosh")
            await ctx.send(embed=embed)

        else:
            raise error

    @shut.error
    async def shut_error(self, ctx, error):
        if isinstance(error, commands.UserNotFound):
            embed = nextcord.Embed(title=f"Shutting people is rude",
                                   description=f"Shutting non existant people is... How do i put this nicely...\nA WASTE OF EVERYONE'S TIME",
                                   color=nextcord.Color.random())
            embed.set_footer(text="No u shut")
            await ctx.send(embed=embed)

        else:
            raise error

    @quote.error
    async def quote_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            abelin = "\n\"The best way to predict your future is to create it.\" -Abraham Lincoln\n"
            suntzu = "\"The supreme art of war is to subdue the enemy without fighting.\" -Sun Tzu, The Art of War"
            embed = nextcord.Embed(title=f"Ahh, the quotes",
                                   description=f"Some famous quotes are: {abelin} {suntzu}\nHowever, Nothing -No One, is not a good quote",
                                   color=nextcord.Color.random())
            embed.set_footer(text="I mean, duh")
            await ctx.send(embed=embed)

        else:
            raise error


def setup(bot):
    bot.add_cog(Fun(bot))
