import nextcord
import asyncio
from nextcord.ext import commands
import wikipedia
from modules import languages
from PyMultiDictionary import MultiDictionary, DICT_WORDNET
import requests
import urllib.parse
import urbandict
from googletrans import Translator, constants
import re
import os
import time
import requests
from bs4 import BeautifulSoup
import shutil
from bs4 import BeautifulSoup
import datetime
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from urllib.parse import quote_plus
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import wait_for_component


# Define a simple View that gives us a google link button.
# We take in `query` as the query that the command author requests for


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="dictionary",
                       description="Finds dictionary meanings, synonyms and antonyms.",
                       options=[create_option(name="what_to_do",
                                              description="Meaning, synonym or antonum",
                                              option_type=3,
                                              choices=[create_choice('meaning', 'meaning'),
                                                       create_choice('synonym', 'synonym'),
                                                       create_choice('antonym', 'antonym')],
                                              required=True),
                                create_option(name="keyword",
                                              description="The word you want to search up",
                                              option_type=3,
                                              required=True)])
    async def _dictionary(self, ctx: SlashContext, what_to_do, *, keyword):
        dictionary = MultiDictionary()
        try:
            if what_to_do == "meaning":
                try:
                    meaning = dictionary.meaning('en', keyword, dictionary=DICT_WORDNET)
                    embed = nextcord.Embed(
                        title=f"The Meaning of {keyword}.", color=nextcord.Color.random())

                    if meaning.get('Noun') is not None:
                        for i in range(0, len(meaning['Noun'])):
                            embed.add_field(name=f"Noun Meaning {i + 1}:", value=f"{(meaning['Noun'])[i]}",
                                            inline=False)
                    if meaning.get('Verb') is not None:
                        for i in range(0, len(meaning['Verb'])):
                            embed.add_field(name=f"Verb Meaning {i + 1}:", value=f"{(meaning['Verb'])[i]}",
                                            inline=False)
                    if meaning.get('Adjective') is not None:
                        for i in range(0, len(meaning['Adjective'])):
                            embed.add_field(name=f"Adjective Meaning {i + 1}:", value=f"{(meaning['Adjective'])[i]}",
                                            inline=False)
                    await ctx.send(embed=embed)
                except:
                    await ctx.send(embed=nextcord.Embed(title='Meaning not found', color=nextcord.Color.random()))
                return

            if what_to_do == "synonym":
                try:
                    synonym_list = dictionary.synonym('en', keyword)
                    string = ""
                    for i in range(0, len(synonym_list)):
                        string += f"{i + 1}. {synonym_list[i]}\n"
                    embed = nextcord.Embed(
                        title=f"The Synonyms of {keyword}.", description=string, color=nextcord.Color.random())
                    await ctx.send(embed=embed)
                except:
                    await ctx.send(embed=nextcord.Embed(title='Synonym not found', color=nextcord.Color.random()))
                return

            if what_to_do == "antonym":
                try:
                    antonym_list = dictionary.antonym('en', keyword)
                    string = ""
                    for i in range(0, len(antonym_list)):
                        string += f"{i + 1}. {antonym_list[i]}\n"
                    embed = nextcord.Embed(
                        title=f"The Antonyms of the {keyword}.", description=string, color=nextcord.Color.random())
                    await ctx.send(embed=embed)
                except:
                    await ctx.send(embed=nextcord.Embed(title='Antonym not found', color=nextcord.Color.random()))
                return

        except:
            embed = nextcord.Embed(title="Error! Could not find", color=nextcord.Color.random())
            await ctx.send(embed=embed)

    @commands.command(aliases=['dict', 'dic'])
    async def dictionary(self, ctx, *, keyword):
        dictionary = MultiDictionary()

        buttons = [
            create_button(style=ButtonStyle.blue, custom_id="Meaning", label='Meaning'),
            create_button(style=ButtonStyle.green, custom_id="Synonym", label='Synonym'),
            create_button(style=ButtonStyle.red, custom_id="Antonym", label='Antonym')
        ]
        action_row = create_actionrow(*buttons)
        await ctx.send(embed=nextcord.Embed(title="What would you like to find?", color=nextcord.Color.random()),
                       components=[action_row])
        response: ComponentContext = await wait_for_component(self.bot, components=action_row, timeout=30)
        while response.author != ctx.author:
            await response.reply("This ain't your button fool", hidden=True)
            response: ComponentContext = await wait_for_component(self.bot, components=action_row, timeout=30)
        await response.defer(ignore=True)
        try:
            if response.component['custom_id'] == "Meaning":
                try:
                    meaning = dictionary.meaning('en', keyword, dictionary=DICT_WORDNET)
                    embed = nextcord.Embed(
                        title=f"The Meaning of {keyword}.", color=nextcord.Color.random())

                    if meaning.get('Noun') is not None:
                        for i in range(0, len(meaning['Noun'])):
                            embed.add_field(name=f"Noun Meaning {i + 1}:", value=f"{(meaning['Noun'])[i]}",
                                            inline=False)
                    if meaning.get('Verb') is not None:
                        for i in range(0, len(meaning['Verb'])):
                            embed.add_field(name=f"Verb Meaning {i + 1}:", value=f"{(meaning['Verb'])[i]}",
                                            inline=False)
                    if meaning.get('Adjective') is not None:
                        for i in range(0, len(meaning['Adjective'])):
                            embed.add_field(name=f"Adjective Meaning {i + 1}:", value=f"{(meaning['Adjective'])[i]}",
                                            inline=False)
                    await ctx.send(embed=embed)
                except:
                    await ctx.send(embed=nextcord.Embed(title='Meaning not found', color=nextcord.Color.random()))
                return

            if response.component['custom_id'] == "Synonym":
                try:
                    synonym_list = dictionary.synonym('en', keyword)
                    string = ""
                    for i in range(0, len(synonym_list)):
                        string += f"{i + 1}. {synonym_list[i]}\n"
                    if string != "":
                        embed = nextcord.Embed(
                            title=f"The Synonyms of {keyword}.", description=string, color=nextcord.Color.random())
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(embed=nextcord.Embed(title='Synonym not found', color=nextcord.Color.random()))
                except:
                    await ctx.send(embed=nextcord.Embed(title='Synonym not found', color=nextcord.Color.random()))
                return

            if response.component['custom_id'] == "Antonym":
                try:
                    antonym_list = dictionary.antonym('en', keyword)
                    string = ""
                    for i in range(0, len(antonym_list)):
                        string += f"{i + 1}. {antonym_list[i]}\n"
                    if string != "":
                        embed = nextcord.Embed(
                            title=f"The Antonyms of the {keyword}.", description=string, color=nextcord.Color.random())
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(embed=nextcord.Embed(title='Antonym not found', color=nextcord.Color.random()))
                except:
                    await ctx.send(embed=nextcord.Embed(title='Antonym not found', color=nextcord.Color.random()))
                return

        except asycio.TimeoutError:
            embed = nextcord.Embed(title="You took too long to click a button", color=nextcord.Color.random())
            await ctx.send(embed=embed)
        except:
            embed = nextcord.Embed(title="Error! Could not find", color=nextcord.Color.random())
            await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="translate",
                       description="Translates a word into any language needed.",
                       options=[create_option(name="translate_to",
                                              description="The language to translate to",
                                              option_type=3,
                                              required=True),
                                create_option(name="keyword",
                                              description="The word you want to translate",
                                              option_type=3,
                                              required=True)
                                ])
    async def _translate(self, ctx: SlashContext, translate_to, *, keyword):
        translator = Translator()

        translate_to = languages.translate(str(translate_to))
        translation = translator.translate(keyword, dest=translate_to)
        if translate_to == "Undetected":
            embed = nextcord.Embed(
                title="Translate", description="This language is not supported by us.")
            embed.add_field(name="Possible Issues",
                            value=f"1. You have typed an invalid language.\n2. We don't support this language (if this is the case, come to our support server)")
        else:
            embed = nextcord.Embed(title="Translate",
                                   description=f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
        embed.color = nextcord.Color.random()

        await ctx.send(embed=embed)

    @commands.command(aliases=['trans', 'tran'])
    async def translate(self, ctx, *, keyword):
        translator = Translator()

        def check(translate_to):
            return ctx.author == translate_to.author and translate_to.channel == ctx.channel

        await ctx.send(embed=nextcord.Embed(title="Choose your language", color=nextcord.Color.random()))
        translate_to = await self.bot.wait_for("message", check=check)
        translate_to = translate_to.content
        translate_to = languages.translate(str(translate_to))
        translation = translator.translate(keyword, dest=translate_to)
        if translate_to == "Undetected":
            embed = nextcord.Embed(
                title="Translate", description="This language is not supported by us.")
            embed.add_field(name="Possible Issues",
                            value=f"1. You have typed an invalid language.\n2. We don't support this language (if this is the case, come to our support server)")
        else:
            embed = nextcord.Embed(title="Translate",
                                   description=f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
        embed.color = nextcord.Color.random()

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="google",
                       description="Allows you to google anything you want.",
                       options=[create_option(name="query",
                                              description="The thing you wanna google",
                                              option_type=3,
                                              required=True)
                                ])
    async def _google(self, ctx, *, query: str):
        buttons = [
            create_button(style=ButtonStyle.URL, label="Get your results here",
                          url="https://google.com/search?q=" + urllib.parse.quote(query))

        ]
        action_row = create_actionrow(*buttons)

        await ctx.send(embed=nextcord.Embed(title=f'Google Result for: `{query}`', color=nextcord.Color.random()),
                       components=[action_row])

    @commands.command(aliases=['search'])
    async def google(self, ctx: commands.Context, *, query: str):
        buttons = [
            create_button(style=ButtonStyle.URL, label="Get your results here",
                          url="https://google.com/search?q=" + urllib.parse.quote(query))

        ]
        action_row = create_actionrow(*buttons)

        await ctx.send(embed=nextcord.Embed(title=f'Google Result for: `{query}`', color=nextcord.Color.random()),
                       components=[action_row])

    @cog_ext.cog_slash(name="lmgtfy",
                       description="Uses the LMGTFY API to find the answer to your queries.",
                       options=[create_option(name="query",
                                              description="The thing you want me to google for you",
                                              option_type=3,
                                              required=True)
                                ])
    async def _lmgtfy(self, ctx: SlashContext, *, query: str):
        buttons = [
            create_button(style=ButtonStyle.URL, label="Get your results here",
                          url=f"https://lmgtfy.app/?q={query.replace(' ', '+')}")

        ]
        action_row = create_actionrow(*buttons)
        await ctx.send(embed=nextcord.Embed(title=f'LMGTFY Result for: `{query}`', color=nextcord.Color.random()),
                       components=[action_row])

    @commands.command(aliases=['letmegooglethatforyou'])
    async def lmgtfy(self, ctx, *, query: str):
        buttons = [
            create_button(style=ButtonStyle.URL, label="Get your results here",
                          url=f"https://lmgtfy.app/?q={query.replace(' ', '+')}")

        ]
        action_row = create_actionrow(*buttons)
        await ctx.send(embed=nextcord.Embed(title=f'LMGTFY Result for: `{query}`', color=nextcord.Color.random()),
                       components=[action_row])

    @cog_ext.cog_slash(name="wiki",
                       description="Searches up the Wikipedia for you.",
                       options=[create_option(name="question",
                                              description="The question for which you don't got no answer",
                                              option_type=3,
                                              required=True)
                                ])
    async def _wiki(self, ctx: SlashContext, *, question):
        try:
            wiki = wikipedia.summary(question, 2)
            embed = nextcord.Embed(
                title="According to Wikipedia: ",
                description=f"{wiki}"
            )
            embed.set_footer(text="Information requested by: {}".format(
                ctx.author.display_name))
            embed.color = nextcord.Color.random()
            await ctx.send(embed=embed)
        except:
            await ctx.send(embed=nextcord.Embed(ttle=f"Could not find wikipedia results for: {question}",
                                                color=nextcord.Color.random()))

    @commands.command()
    async def wiki(self, ctx, *, question):
        try:
            wiki = wikipedia.summary(question, 2)
            embed = nextcord.Embed(
                title="According to Wikipedia: ",
                description=f"{wiki}"
            )
            embed.set_footer(text="Information requested by: {}".format(
                ctx.author.display_name))
            embed.color = nextcord.Color.random()
            await ctx.send(embed=embed)
        except:
            await ctx.send(f"Could not find wikipedia results for: {question}")

    @cog_ext.cog_slash(name="weather",
                       description="Gives you the current weather of a place.",
                       options=[create_option(name="place",
                                              description="The place for which you need the weather",
                                              option_type=3,
                                              required=True)
                                ])
    async def _weather(self, ctx: SlashContext, *, place):
        api_key = "6d7ac869f461ec0dc59fdf3a7da78262"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "appid=" + api_key + "&q=" + place
        response = requests.get(complete_url)
        x = response.json()

        if x["cod"] != "404":
            y = x["main"]
            current_temperature_kelvin = y["temp"]
            current_temperature_fahrenheit = round(
                (current_temperature_kelvin - 273.15) * 9 / 5 + 32)
            current_temperature_celsius = round(
                current_temperature_kelvin - 273.15)
            current_pressure = round(y["pressure"])
            current_humidiy = round(y["humidity"])
            z = x["weather"]
            weather_description = z[0]["description"]
            embed = nextcord.Embed(
                title=f"Weather in {place}",
                description=" Temperature (in fahrenheit) = " +
                            str(current_temperature_fahrenheit) +
                            "\n Temperature (in celsius) = " +
                            str(current_temperature_celsius) +
                            "\n Atmospheric pressure (in hPa unit) = " +
                            str(current_pressure) +
                            "\n Humidity (in percentage) = " +
                            str(current_humidiy) +
                            "\n Description = " +
                            str(weather_description)
            )
            embed.set_footer(text="Information requested by: {}".format(
                ctx.author.display_name))
            embed.color = nextcord.Color.random()
            await ctx.send(embed=embed)

        else:
            embed = nextcord.Embed(
                title=f"Sorry could not find the weather in {place}", color=nextcord.Color.dark_teal())
            await ctx.send(embed=embed)

    @commands.command(aliases=['climate', 'w'])
    async def weather(self, ctx, *, place):
        api_key = "6d7ac869f461ec0dc59fdf3a7da78262"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "appid=" + api_key + "&q=" + place
        response = requests.get(complete_url)
        x = response.json()

        if x["cod"] != "404":
            y = x["main"]
            current_temperature_kelvin = y["temp"]
            current_temperature_fahrenheit = round(
                (current_temperature_kelvin - 273.15) * 9 / 5 + 32)
            current_temperature_celsius = round(
                current_temperature_kelvin - 273.15)
            current_pressure = round(y["pressure"])
            current_humidiy = round(y["humidity"])
            z = x["weather"]
            weather_description = z[0]["description"]
            embed = nextcord.Embed(
                title=f"Weather in {place}",
                description=" Temperature (in fahrenheit) = " +
                            str(current_temperature_fahrenheit) +
                            "\n Temperature (in celsius) = " +
                            str(current_temperature_celsius) +
                            "\n Atmospheric pressure (in hPa unit) = " +
                            str(current_pressure) +
                            "\n Humidity (in percentage) = " +
                            str(current_humidiy) +
                            "\n Description = " +
                            str(weather_description)
            )
            embed.set_footer(text="Information requested by: {}".format(
                ctx.author.display_name))
            embed.color = nextcord.Color.random()
            await ctx.send(embed=embed)

        else:
            embed = nextcord.Embed(
                title=f"Sorry could not find the weather in {place}", color=nextcord.Color.dark_teal())
            await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="urban",
                       description="Allows you to access the Urban Dictionary.",
                       options=[create_option(name="keyword",
                                              description="The word I should search for in the Urban Dictionary",
                                              option_type=3,
                                              required=True)
                                ])
    async def _urban(self, ctx: SlashContext, *, keyword: str):
        try:
            urban_list = (urbandict.define(keyword))
            embed = nextcord.Embed(
                title=f"Meaning of {keyword} in urban dict.", color=nextcord.Color.random())
            for i in range(0, len(urban_list) - 1):
                embed.add_field(name=f"Type {i + 1}:",
                                value=f"Word: {(urban_list[i])['word']}\n Definition: {(urban_list[i])['def']}\n Examples: {(urban_list[i])['example']}",
                                inline=False)
            await ctx.send(embed=embed)
        except:
            await ctx.send(
                embed=nextcord.Embed(title=f"Sorry mate i couldn't find sh*t for", description=f"```{keyword}```",
                                     color=nextcord.Color.random()))

    @commands.command(aliases=['urb'])
    async def urban(self, ctx, *, keyword: str):
        try:
            urban_list = (urbandict.define(keyword))
            embed = nextcord.Embed(
                title=f"Meaning of {keyword} in urban dict.", color=nextcord.Color.random())
            for i in range(0, len(urban_list) - 1):
                embed.add_field(name=f"Type {i + 1}:",
                                value=f"Word: {(urban_list[i])['word']}\n Definition: {(urban_list[i])['def']}\n Examples: {(urban_list[i])['example']}",
                                inline=False)
            await ctx.send(embed=embed)
        except:
            await ctx.send(
                embed=nextcord.Embed(title=f"Sorry mate i couldn't find sh*t for", description=f"```{keyword}```",
                                     color=nextcord.Color.random()))

    @cog_ext.cog_slash(name="youtube",
                       description="Let's you use YouTube through discord itself!",
                       options=[create_option(name="query",
                                              description="The thing you want to search on YouTube",
                                              option_type=3,
                                              required=True)
                                ])
    async def _youtube(self, ctx: SlashContext, *, query: str):
        req = requests.get(
            ('https://www.googleapis.com/youtube/v3/search?part=id&maxResults=1'
             '&order=relevance&q={}&relevanceLanguage=en&safeSearch=moderate&type=video'
             '&videoDimension=2d&fields=items%2Fid%2FvideoId&key=')
            .format(query) + os.getenv("yt_api"))
        try:
            vid_url = "https://www.youtube.com/watch?v={}".format(req.json()['items'][0]['id']['videoId'])
            await ctx.send(f"Here is the video: \n**{vid_url}**")
        except:
            await ctx.send(embed=nextcord.Embed(title="Sorry mate, i couldn't find sh*t for",
                                                description=f"```{query}```",
                                                color=nextcord.Color.random()))

    @commands.command(aliases=['yt'])
    async def youtube(self, ctx, *, query: str):
        req = requests.get(
            ('https://www.googleapis.com/youtube/v3/search?part=id&maxResults=1&order=relevance&q={}&relevanceLanguage=en&safeSearch=moderate&type=video&videoDimension=2d&fields=items%2Fid%2FvideoId&key='.format(query) + os.getenv("yt_api")))
        try:
            vid_url = "https://www.youtube.com/watch?v={}".format(req.json()['items'][0]['id']['videoId'])
            await ctx.send(f"Here is the video: \n**{vid_url}**")
        except:
            await ctx.send(embed=nextcord.Embed(title="Sorry mate, i couldn't find sh*t for",
                                                description=f"```{query}```",
                                                color=nextcord.Color.random()))

    @dictionary.error
    async def dict_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"Alright.",
                                   description=f"The definition of nothing is ___. It probably has synonyms and antonyms, but idrc.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Im not stupid")
            await ctx.send(embed=embed)

        else:
            raise error

    @translate.error
    async def translate_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"Why is this difficult",
                                   description=f"All you gotta do, is use {ctx.prefix}help translate and do what it says.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Why you being like this")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.errors.CommandInvokeError):
            embed = nextcord.Embed(title=f"Well that didn't work.....",
                                   description=f"Probably u put in some invalid shit",
                                   color=nextcord.Color.random())
            embed.set_footer(text="If you think this language should be added, just use the suggest feature in utils")
            await ctx.send(embed=embed)

        else:
            raise error

    @urban.error
    async def urban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"I can't believe it.",
                                   description=f"This was the place where i really didn't expect an error. Use {ctx.prefix}Help urban for god's sake!",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Wish you could use more brain power for this")
            await ctx.send(embed=embed)

        else:
            raise error

    @weather.error
    async def weather_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"Did you just try to find the weather of NOWHERE?!",
                                   description=f"I don't even know what to say",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Actually I do. Try being smart.")
            await ctx.send(embed=embed)

        else:
            raise error

    @wiki.error
    async def wiki_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title=f"It's good you search for knowledge",
                                   description=f"But at least tell me what knowledge you want.\n There are a trillion+ websites of info out there.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="It's a huge world")
            await ctx.send(embed=embed)

        else:
            raise error

    @lmgtfy.error
    async def lmgtfy_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(embed=nextcord.Embed(title="I would love to help you",
                                                description="But you gotta tell me what to google...",
                                                color=nextcord.Color.random()))

        else:
            raise error

    @google.error
    async def google_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(embed=nextcord.Embed(title="I would love to help you",
                                                description="But you gotta tell me what to google...\nThis also seems kinda familiar lol",
                                                color=nextcord.Color.random()))

        else:
            raise error

    @youtube.error
    async def youtube_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(embed=nextcord.Embed(title="Watching YouTube may be fun",
                                                description="But stop ruining it by asking for NOTHING",
                                                color=nextcord.Color.random()))

        else:
            raise error


def setup(bot):
    bot.add_cog(Info(bot))
