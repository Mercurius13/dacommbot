import os
import nextcord
from nextcord.ext import commands
import math
import asyncio
import wolframalpha
from modules import calculation_filter as cf
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.utils.manage_components import wait_for_component


class Nerd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_subcommand(base="math", name="add", description="Adds numbers for you.",
                            options=[
                                create_option(name="numbers",
                                              description="The numbers you want to add",
                                              option_type=3,
                                              required=True)])
    async def _add(self, ctx: SlashContext, *, numbers=""):
        if numbers == "":
            await ctx.send(embed=nextcord.Embed(title=f"Not this again",
                                                description=f"I need numbers to add and not thin air!",
                                                color=nextcord.Color.random()))
            return
        split = numbers.split(' ')
        if len(split) == 1:
            await ctx.send(embed=nextcord.Embed(title=f"To add numbers,",
                                                description=f"you need number**s**\nEmphasis on the 's'",
                                                color=nextcord.Color.random()))
            return
        if len(split) > 10:
            await ctx.send(embed=nextcord.Embed(title=f"I shall not add these many numbers",
                                                description=f"My limit is no more than 10 numbers at a time.\nCause I have better things to do.",
                                                color=nextcord.Color.random()))
            return
        ans = await cf.asmd(ctx, split, '+')
        if ans is None:
            return
        string = split[0]
        count = True
        for i in split:
            if count is True:
                count = False
                continue
            string = string + " + " + i
        embed = nextcord.Embed(title=str(ans),
                               description=f"This is the answer to {string}.",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def add(self, ctx, *, arguments=""):
        if arguments == "":
            await ctx.send(embed=nextcord.Embed(title=f"Not this again",
                                                description=f"I need numbers to add and not thin air!",
                                                color=nextcord.Color.random()))
            return
        split = arguments.split(' ')
        if len(split) == 1:
            await ctx.send(embed=nextcord.Embed(title=f"To add numbers,",
                                                description=f"you need number**s**\nEmphasis on the 's'",
                                                color=nextcord.Color.random()))
            return
        if len(split) > 10:
            await ctx.send(embed=nextcord.Embed(title=f"I shall not add these many numbers",
                                                description=f"My limit is no more than 10 numbers at a time.\nCause I have better things to do.",
                                                color=nextcord.Color.random()))
            return
        ans = await cf.asmd(ctx, split, '+')
        if ans is None:
            return
        string = split[0]
        count = True
        for i in split:
            if count is True:
                count = False
                continue
            string = string + " + " + i
        embed = nextcord.Embed(title=str(ans),
                               description=f"This is the answer to {string}.",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(base="math", name="substract", description="Substract numbers for you.",
                            options=[
                                create_option(name="numbers",
                                              description="The numbers you want to substract",
                                              option_type=3,
                                              required=True)])
    async def _subtract(self, ctx: SlashContext, *, numbers=""):
        if numbers == "":
            await ctx.send(embed=nextcord.Embed(title=f"Not this again again",
                                                description=f"I need numbers to subtract and not thin air!",
                                                color=nextcord.Color.random()))
            return
        split = numbers.split(' ')
        if len(split) == 1:
            embed = nextcord.Embed(title=f"To subtract numbers,",
                                   description=f"you need number**s**\nEmphasis on the 's'",
                                   color=nextcord.Color.random())
            embed.set_footer(text="And I thought you would have learned by now.")
            await ctx.send(embed=embed)
            return
        elif len(split) > 2:
            await ctx.send(embed=nextcord.Embed(title=f"What you ask is just not possible",
                                                description=f"I just can't subtract {len(split)} numbers from each other!",
                                                color=nextcord.Color.random()))
            return
        ans = await cf.asmd(ctx, split, '-')
        if ans is None:
            return
        embed = nextcord.Embed(title=str(ans),
                               description=f"This is the answer to {split[0]} - {split[1]}.",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['subs', 'substract'])
    async def subtract(self, ctx, *, arguments=""):
        if arguments == "":
            await ctx.send(embed=nextcord.Embed(title=f"Not this again again",
                                                description=f"I need numbers to subtract and not thin air!",
                                                color=nextcord.Color.random()))
            return
        split = arguments.split(' ')
        if len(split) == 1:
            embed = nextcord.Embed(title=f"To subtract numbers,",
                                   description=f"you need number**s**\nEmphasis on the 's'",
                                   color=nextcord.Color.random())
            embed.set_footer(text="And I thought you would have learned by now.")
            await ctx.send(embed=embed)
            return
        elif len(split) > 2:
            await ctx.send(embed=nextcord.Embed(title=f"What you ask is just not possible",
                                                description=f"I just can't subtract {len(split)} numbers from each other!",
                                                color=nextcord.Color.random()))
            return
        ans = await cf.asmd(ctx, split, '-')
        if ans is None:
            return
        embed = nextcord.Embed(title=str(ans),
                               description=f"This is the answer to {split[0]} - {split[1]}.",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(base="math", name="multiply", description="Multiplies numbers for you.",
                            options=[
                                create_option(name="numbers",
                                              description="The numbers you want to multiply",
                                              option_type=3,
                                              required=True)])
    async def _multiply(self, ctx: SlashContext, *, numbers=""):
        if numbers == "":
            await ctx.send(embed=nextcord.Embed(title=f"Not this again again again",
                                                description=f"I need numbers to multiply and not thin air!",
                                                color=nextcord.Color.random()))
            return
        split = numbers.split(' ')
        if len(split) == 1:
            await ctx.send(embed=nextcord.Embed(title=f"To multiply numbers,",
                                                description=f"you need number**s**\nEmphasis on the 's'",
                                                color=nextcord.Color.random()))
            return
        if len(split) > 10:
            await ctx.send(embed=nextcord.Embed(title=f"I shall not multiply these many numbers",
                                                description=f"My limit is no more than 10 numbers at a time.\nCause I have better things to do.",
                                                color=nextcord.Color.random()))
            return
        ans = await cf.asmd(ctx, split, '*')
        if ans is None:
            return
        string = split[0]
        count = True
        for i in split:
            if count is True:
                count = False
                continue
            string = string + " * " + i
        embed = nextcord.Embed(title=str(ans),
                               description=f"This is the answer to {string}.",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['multi'])
    async def multiply(self, ctx, *, arguments=""):
        if arguments == "":
            await ctx.send(embed=nextcord.Embed(title=f"Not this again again again",
                                                description=f"I need numbers to multiply and not thin air!",
                                                color=nextcord.Color.random()))
            return
        split = arguments.split(' ')
        if len(split) == 1:
            await ctx.send(embed=nextcord.Embed(title=f"To multiply numbers,",
                                                description=f"you need number**s**\nEmphasis on the 's'",
                                                color=nextcord.Color.random()))
            return
        if len(split) > 10:
            await ctx.send(embed=nextcord.Embed(title=f"I shall not multiply these many numbers",
                                                description=f"My limit is no more than 10 numbers at a time.\nCause I have better things to do.",
                                                color=nextcord.Color.random()))
            return
        ans = await cf.asmd(ctx, split, '*')
        if ans is None:
            return
        string = split[0]
        count = True
        for i in split:
            if count is True:
                count = False
                continue
            string = string + " * " + i
        embed = nextcord.Embed(title=str(ans),
                               description=f"This is the answer to {string}.",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(base="math", name="divide", description="Divides numbers for you.",
                            options=[
                                create_option(name="numbers",
                                              description="The numbers you want to divide",
                                              option_type=3,
                                              required=True)])
    async def _divide(self, ctx, *, numbers=""):
        if numbers == "":
            await ctx.send(embed=nextcord.Embed(title=f"Not this again again again again",
                                                description=f"I need numbers to divide and not thin air!\nIs this starting to get old?",
                                                color=nextcord.Color.random()))
            return
        split = numbers.split(' ')
        if len(split) == 1:
            embed = nextcord.Embed(title=f"To divide numbers,",
                                   description=f"you need number**s**\nEmphasis on the 's'",
                                   color=nextcord.Color.random())
            embed.set_footer(text="And I thought you would have learned by now.")
            await ctx.send(embed=embed)
            return
        elif len(split) > 2:
            await ctx.send(embed=nextcord.Embed(title=f"What you ask is just not possible",
                                                description=f"I just can't divide {len(split)} numbers from each other!",
                                                color=nextcord.Color.random()))
            return
        ans = await cf.asmd(ctx, split, '/')
        if ans is None:
            return
        embed = nextcord.Embed(title=str(ans),
                               description=f"This is the answer to {split[0]} / {split[1]}.",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['div'])
    async def divide(self, ctx, *, arguments=""):
        if arguments == "":
            await ctx.send(embed=nextcord.Embed(title=f"Not this again again again again",
                                                description=f"I need numbers to divide and not thin air!\nIs this starting to get old?",
                                                color=nextcord.Color.random()))
            return
        split = arguments.split(' ')
        if len(split) == 1:
            embed = nextcord.Embed(title=f"To divide numbers,",
                                   description=f"you need number**s**\nEmphasis on the 's'",
                                   color=nextcord.Color.random())
            embed.set_footer(text="And I thought you would have learned by now.")
            await ctx.send(embed=embed)
            return
        elif len(split) > 2:
            await ctx.send(embed=nextcord.Embed(title=f"What you ask is just not possible",
                                                description=f"I just can't divide {len(split)} numbers from each other!",
                                                color=nextcord.Color.random()))
            return
        ans = await cf.asmd(ctx, split, '/')
        if ans is None:
            return
        embed = nextcord.Embed(title=str(ans),
                               description=f"This is the answer to {split[0]} / {split[1]}.",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="perimeter", description="Gets the perimeter of certain shapes for you.")
    async def _perimeter(self, ctx: SlashContext):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        buttons = [
            create_button(style=ButtonStyle.blue, label="Circle"),
            create_button(style=ButtonStyle.red, label="Triangle"),
            create_button(style=ButtonStyle.green, label="Quadrilateral")
        ]
        action_row = create_actionrow(*buttons)

        await ctx.send(
            embed=nextcord.Embed(title="Please choose one of the following options",
                                 color=nextcord.Color.random()),
            components=[action_row])
        try:
            response: ComponentContext = await wait_for_component(self.bot, components=action_row, timeout=20)
            await response.defer(ignore=True)
        except asyncio.TimeoutError:
            await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                color=nextcord.Color.random()))
            return
        if response.component['label'] == "Circle":
            await ctx.send(embed=nextcord.Embed(title="Please enter the radius", color=nextcord.Color.random()))
            try:
                r = await self.bot.wait_for("message", check=check, timeout=20)
            except asyncio.TimeoutError:
                await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                    color=nextcord.Color.random()))
                return

            if r.mentions:
                await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                    description=f"That a circle have a mention as a radius?",
                                                    color=nextcord.Color.random()))
                return
            r = r.content
            for i in r:
                if not i.isdigit() and i != ".":
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a circle can have a radius {r}?\nThe '{i}' there makes it useless",
                                                        color=nextcord.Color.random()))
                    return
            perimeter = round((2 * 22 * float(r)) / 7, 3)
            if perimeter.is_integer() is True:
                perimeter = int(perimeter)
            embed = nextcord.Embed(title=f"{perimeter}",
                                   description=f"Is the perimeter of a circle with radius {r}\nDid you know that a perimeter of a circle is the same as its circumference?",
                                   color=nextcord.Color.random())
            embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

        elif response.component['label'] == "Triangle":
            buttons = [
                create_button(style=ButtonStyle.blue, label="Equilateral Triangle"),
                create_button(style=ButtonStyle.red, label="Isosceles Triangle"),
                create_button(style=ButtonStyle.green, label="Scalene Triangle")
            ]
            action_row = create_actionrow(*buttons)
            await ctx.send(
                embed=nextcord.Embed(title="Please choose the type of triangle you want to use",
                                     color=nextcord.Color.random()),
                components=[action_row]
            )
            try:
                response: ComponentContext = await wait_for_component(self.bot, components=action_row, timeout=20)
                await response.defer(ignore=True)
            except asyncio.TimeoutError:
                await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                    color=nextcord.Color.random()))
                return
            if response.component['label'] == "Equilateral Triangle":
                await ctx.send(embed=nextcord.Embed(title="Please enter the length of the side of the triangle.",
                                                    color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a triangle have a mention as a side?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a triangle can have a side {s}?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                perimeter = round(3 * float(s), 3)
                if perimeter.is_integer() is True:
                    perimeter = int(perimeter)
                embed = nextcord.Embed(title=f"{perimeter}",
                                       description=f"Is the perimeter of an equilateral triangle with side {s}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            elif response.component['label'] == "Isosceles Triangle":
                await ctx.send(embed=nextcord.Embed(
                    title="Please enter the equal and the non-equal sides in this format\n`<equalside> <non-equalside>`",
                    color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a triangle can have a mention as one of its SIDES?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a triangle can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 2:
                    await ctx.send(embed=nextcord.Embed(
                        title=f"Only two numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=nextcord.Color.random()))
                    return
                e = split[0]
                n = split[1]
                perimeter = (2 * float(e)) + float(n)
                if perimeter.is_integer() is True:
                    perimeter = int(perimeter)
                embed = nextcord.Embed(title=f"{perimeter}",
                                       description=f"Is the perimeter of an isosceles triangle with equal sides of length {e} and a non-equal side of length {n}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            elif response.component['label'] == "Scalene Triangle":
                await ctx.send(
                    embed=nextcord.Embed(title="Please enter the three sides in this format\n`<side1> <side2> <side3>`",
                                         color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a triangle can have a mention as one of its SIDES?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a triangle can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 3:
                    await ctx.send(embed=nextcord.Embed(
                        title=f"Only three numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=nextcord.Color.random()))
                    return
                s1 = split[0]
                s2 = split[1]
                s3 = split[2]
                perimeter = float(s1) + float(s2) + float(s3)
                if perimeter.is_integer() is True:
                    perimeter = int(perimeter)
                embed = nextcord.Embed(title=f"{perimeter}",
                                       description=f"Is the perimeter of a scalene triangle with sides of length {s1}, {s2} and {s3}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

        elif response.component['label'] == "Quadrilateral":
            buttons = [
                create_button(style=ButtonStyle.blue, label="Parallelogram/Rectangle"),
                create_button(style=ButtonStyle.red, label="Rhombus/Square"),
                create_button(style=ButtonStyle.green, label="Irregular Quadrilateral")
            ]
            action_row = create_actionrow(*buttons)
            await ctx.send(
                embed=nextcord.Embed(title="Please choose the type of quadrilateral you want to use",
                                     color=nextcord.Color.random()),
                components=[action_row]
            )
            try:
                response: ComponentContext = await wait_for_component(self.bot, components=action_row, timeout=20)
                await response.defer(ignore=True)
            except asyncio.TimeoutError:
                await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                    color=nextcord.Color.random()))
                return
            if response.component['label'] == "Parallelogram/Rectangle":
                await ctx.send(embed=nextcord.Embed(
                    title="Please enter the two sets of opposite sides in this format\n`<oppositeside1> <oppositeside2>`",
                    color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a parallelogram or a rectangle can have a mention as one of its SIDES?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a parallelogram or a rectangle can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 2:
                    await ctx.send(embed=nextcord.Embed(
                        title=f"Only two numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=nextcord.Color.random()))
                    return
                os1 = split[0]
                os2 = split[1]
                perimeter = 2 * (float(os1) + float(os2))
                if perimeter.is_integer() is True:
                    perimeter = int(perimeter)
                embed = nextcord.Embed(title=f"{perimeter}",
                                       description=f"Is the perimeter of a parallelogram or a rectangle with opposite sides of length {os1} and {os2}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            elif response.component['label'] == "Rhombus/Square":
                await ctx.send(embed=nextcord.Embed(title="Please enter the side of the rhombus or square",
                                                    color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a rhombus or square have a mention as a side?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a That a rhombus or square can have a side {s}?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                perimeter = 4 * float(s)
                if perimeter.is_integer() is True:
                    perimeter = int(perimeter)
                embed = nextcord.Embed(title=f"{perimeter}",
                                       description=f"Is the perimeter of a rhombus or square with side {s}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            elif response.component['label'] == "Irregular Quadrilateral":
                await ctx.send(embed=nextcord.Embed(
                    title="Please enter the sides of the quadrilateral in this format\n`<side1> <side2> <side3> <side4>`",
                    color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a quadrilateral can have a mention as one of its SIDES?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a quadrilateral can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 4:
                    await ctx.send(embed=nextcord.Embed(
                        title=f"Only four numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=nextcord.Color.random()))
                    return
                s1 = split[0]
                s2 = split[1]
                s3 = split[2]
                s4 = split[3]
                perimeter = float(s1) + float(s2) + float(s3) + float(s4)
                if perimeter.is_integer() is True:
                    perimeter = int(perimeter)
                embed = nextcord.Embed(title=f"{perimeter}",
                                       description=f"Is the perimeter of an irregular quadrilateral with sides {s1}, {s2}, {s3} and {s4}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

    @commands.command(aliases=['peri'])
    async def perimeter(self, ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        buttons = [
            create_button(style=ButtonStyle.blue, label="Circle"),
            create_button(style=ButtonStyle.red, label="Triangle"),
            create_button(style=ButtonStyle.green, label="Quadrilateral")
        ]
        action_row = create_actionrow(*buttons)

        await ctx.send(
            embed=nextcord.Embed(title="Please choose one of the following options", color=nextcord.Color.random()),
            components=[action_row])

        try:
            response: ComponentContext = await wait_for_component(self.bot, components=action_row, timeout=20)
            await response.defer(ignore=True)
        except asyncio.TimeoutError:
            await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                color=nextcord.Color.random()))
            return
        if response.component['label'] == "Circle":
            await ctx.send(embed=nextcord.Embed(title="Please enter the radius", color=nextcord.Color.random()))
            try:
                r = await self.bot.wait_for(event="message", check=check, timeout=20)
            except asyncio.TimeoutError:
                await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                    color=nextcord.Color.random()))
                return

            if r.mentions:
                await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                    description=f"That a circle have a mention as a radius?",
                                                    color=nextcord.Color.random()))
                return
            r = r.content
            for i in r:
                if not i.isdigit() and i != ".":
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a circle can have a radius {r}?\nThe '{i}' there makes it useless",
                                                        color=nextcord.Color.random()))
                    return
            perimeter = round((2 * 22 * float(r)) / 7, 3)
            if perimeter.is_integer() is True:
                perimeter = int(perimeter)
            embed = nextcord.Embed(title=f"{perimeter}",
                                   description=f"Is the perimeter of a circle with radius {r}\nDid you know that a perimeter of a circle is the same as its circumference?",
                                   color=nextcord.Color.random())
            embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

        elif response.component['label'] == "Triangle":
            buttons = [
                create_button(style=ButtonStyle.blue, label="Equilateral Triangle"),
                create_button(style=ButtonStyle.red, label="Isosceles Triangle"),
                create_button(style=ButtonStyle.green, label="Scalene Triangle")
            ]
            action_row = create_actionrow(*buttons)
            await ctx.send(
                embed=nextcord.Embed(title="Please choose the type of triangle you want to use",
                                     color=nextcord.Color.random()),
                components=[action_row]
            )
            try:
                response: ComponentContext = await wait_for_component(self.bot, components=action_row, timeout=20)
                await response.defer(ignore=True)
            except asyncio.TimeoutError:
                await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                    color=nextcord.Color.random()))
                return
            if response.component['label'] == "Equilateral Triangle":
                await ctx.send(embed=nextcord.Embed(title="Please enter the length of the side of the triangle.",
                                                    color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a triangle have a mention as a side?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a triangle can have a side {s}?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                perimeter = round(3 * float(s), 3)
                if perimeter.is_integer() is True:
                    perimeter = int(perimeter)
                embed = nextcord.Embed(title=f"{perimeter}",
                                       description=f"Is the perimeter of an equilateral triangle with side {s}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            elif response.component['label'] == "Isosceles Triangle":
                await ctx.send(nextcord.Embed(
                    title="Please enter the equal and the non-equal sides in this format\n`<equalside> <non-equalside>`",
                    color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a triangle can have a mention as one of its SIDES?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a triangle can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 2:
                    await ctx.send(embed=nextcord.Embed(
                        title=f"Only two numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=nextcord.Color.random()))
                    return
                e = split[0]
                n = split[1]
                perimeter = (2 * float(e)) + float(n)
                if perimeter.is_integer() is True:
                    perimeter = int(perimeter)
                embed = nextcord.Embed(title=f"{perimeter}",
                                       description=f"Is the perimeter of an isosceles triangle with equal sides of length {e} and a non-equal side of length {n}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            elif response.component['label'] == "Scalene Triangle":
                await ctx.send(
                    embed=nextcord.Embed(title="Please enter the three sides in this format\n`<side1> <side2> <side3>`",
                                         color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a triangle can have a mention as one of its SIDES?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a triangle can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 3:
                    await ctx.send(embed=nextcord.Embed(
                        title=f"Only three numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=nextcord.Color.random()))
                    return
                s1 = split[0]
                s2 = split[1]
                s3 = split[2]
                perimeter = float(s1) + float(s2) + float(s3)
                if perimeter.is_integer() is True:
                    perimeter = int(perimeter)
                embed = nextcord.Embed(title=f"{perimeter}",
                                       description=f"Is the perimeter of a scalene triangle with sides of length {s1}, {s2} and {s3}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

        elif response.component['label'] == "Quadrilateral":
            buttons = [
                create_button(style=ButtonStyle.blue, label="Parallelogram/Rectangle"),
                create_button(style=ButtonStyle.red, label="Rhombus/Square"),
                create_button(style=ButtonStyle.green, label="Irregular Quadrilateral")
            ]
            action_row = create_actionrow(*buttons)
            await ctx.send(
                embed=nextcord.Embed(title="Please choose the type of quadrilateral you want to use",
                                     color=nextcord.Color.random()),
                components=[action_row]
            )
            try:
                response: ComponentContext = await wait_for_component(self.bot, components=action_row, timeout=20)
                await response.defer(ignore=True)
            except asyncio.TimeoutError:
                await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                    color=nextcord.Color.random()))
                return
            if response.component['label'] == "Parallelogram/Rectangle":
                await ctx.send(nextcord.Embed(
                    title="Please enter the two sets of opposite sides in this format\n`<oppositeside1> <oppositeside2>`",
                    color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a parallelogram or a rectangle can have a mention as one of its SIDES?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a parallelogram or a rectangle can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 2:
                    await ctx.send(embed=nextcord.Embed(
                        title=f"Only two numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=nextcord.Color.random()))
                    return
                os1 = split[0]
                os2 = split[1]
                perimeter = 2 * (float(os1) + float(os2))
                if perimeter.is_integer() is True:
                    perimeter = int(perimeter)
                embed = nextcord.Embed(title=f"{perimeter}",
                                       description=f"Is the perimeter of a parallelogram or a rectangle with opposite sides of length {os1} and {os2}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            elif response.component['label'] == "Rhombus/Square":
                await ctx.send(embed=nextcord.Embed(title="Please enter the side of the rhombus or square",
                                                    color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a rhombus or square have a mention as a side?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a That a rhombus or square can have a side {s}?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                perimeter = 4 * float(s)
                if perimeter.is_integer() is True:
                    perimeter = int(perimeter)
                embed = nextcord.Embed(title=f"{perimeter}",
                                       description=f"Is the perimeter of a rhombus or square with side {s}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            elif response.component['label'] == "Irregular Quadrilateral":
                await ctx.send(nextcord.Embed(
                    title="Please enter the sides of the quadrilateral in this format\n`<side1> <side2> <side3> <side4>`",
                    color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a quadrilateral can have a mention as one of its SIDES?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a quadrilateral can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 4:
                    await ctx.send(embed=nextcord.Embed(
                        title=f"Only four numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=nextcord.Color.random()))
                    return
                s1 = split[0]
                s2 = split[1]
                s3 = split[2]
                s4 = split[3]
                perimeter = float(s1) + float(s2) + float(s3) + float(s4)
                if perimeter.is_integer() is True:
                    perimeter = int(perimeter)
                embed = nextcord.Embed(title=f"{perimeter}",
                                       description=f"Is the perimeter of an irregular quadrilateral with sides {s1}, {s2}, {s3} and {s4}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="area", description="Gets the area of certain shapes for you.")
    async def _area(self, ctx: SlashContext):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx

        await ctx.send(
            "Please choose one of the following options",
            components=[
                Button(style=ButtonStyle.blue, label="Circle"),
                Button(style=ButtonStyle.red, label="Triangle"),
                Button(style=ButtonStyle.green, label="Quadrilateral")
            ]
        )

        try:
            response: ComponentContext = await wait_for_component(self.bot, components=action_row, timeout=20)
            await response.defer(ignore=True)
        except asyncio.TimeoutError:
            await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                color=nextcord.Color.random()))
            return
        if response.component['label'] == "Circle":
            await ctx.send(embed=nextcord.Embed(title="Please enter the radius", color=nextcord.Color.random()))
            try:
                r = await self.bot.wait_for("message", check=check, timeout=20)
            except asyncio.TimeoutError:
                await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                    color=nextcord.Color.random()))
                return
            if r.mentions:
                await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                    description=f"That a circle have a mention as a radius?",
                                                    color=nextcord.Color.random()))
                return
            r = r.content
            for i in r:
                if not i.isdigit() and i != ".":
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a circle can have a radius {r}?\nThe '{i}' there makes it useless",
                                                        color=nextcord.Color.random()))
                    return
            area = round(22 * float(r) * float(r) / 7, 3)
            if area.is_integer() is True:
                area = int(area)
            embed = nextcord.Embed(title=f"{area}",
                                   description=f"Is the area of a circle with radius {r}",
                                   color=nextcord.Color.random())
            embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

        elif response.component['label'] == "Triangle":
            await ctx.send(
                "Please choose the type of triangle you want to use",
                components=[
                    Button(style=ButtonStyle.blue, label="Equilateral Triangle"),
                    Button(style=ButtonStyle.red, label="Isosceles Triangle"),
                    Button(style=ButtonStyle.green, label="Scalene Triangle"),
                    Button(style=ButtonStyle.grey, label="Right-Angled Triangle")
                ]
            )
            try:
                response: ComponentContext = await wait_for_component(self.bot, components=action_row, timeout=20)
                await response.defer(ignore=True)
            except asyncio.TimeoutError:
                await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                    color=nextcord.Color.random()))
                return
            if response.component['label'] == "Equilateral Triangle":
                await ctx.send(embed=nextcord.Embed(title="Please enter the length of the side of the triangle.",
                                                    color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a triangle have a mention as a side?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a triangle can have a side {s}?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                area = round(math.sqrt(3) * float(s) * float(s) / 4, 3)
                if area.is_integer() is True:
                    area = int(area)
                embed = nextcord.Embed(title=f"{area}",
                                       description=f"Is the area of an equilateral triangle with side {s}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            elif response.component['label'] == "Isosceles Triangle":
                await ctx.send(embed=nextcord.Embed(
                    title="Please enter the equal and the non-equal sides in this format\n`<equalside> <non-equalside>`",
                    color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a triangle can have a mention as one of its SIDES?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a triangle can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 2:
                    await ctx.send(embed=nextcord.Embed(
                        title=f"Only two numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=nextcord.Color.random()))
                    return
                e = split[0]
                n = split[1]
                area = round(float(n) * (math.sqrt(math.pow(float(e), 2) - (math.pow(float(e), 2) / 4))) / 2, 3)
                if area.is_integer() is True:
                    area = int(area)
                embed = nextcord.Embed(title=f"{area}",
                                       description=f"Is the area of an isosceles triangle with equal sides of length {e} and a non-equal side of length {n}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            elif response.component['label'] == "Scalene Triangle":
                await ctx.send(
                    embed=nextcord.Embed(title="Please enter the three sides in this format\n`<side1> <side2> <side3>`",
                                         color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a triangle can have a mention as one of its SIDES?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a triangle can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 3:
                    await ctx.send(embed=nextcord.Embed(
                        title=f"Only three numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=nextcord.Color.random()))
                    return
                s1 = split[0]
                s2 = split[1]
                s3 = split[2]
                s_heron = float(s1) + float(s2) + float(s3)
                area = round(math.sqrt(s_heron * (s_heron - float(s1)) * (s_heron - float(s2)) * (s_heron - float(s3))),
                             3)
                if area.is_integer() is True:
                    area = int(area)
                embed = nextcord.Embed(title=f"{area}",
                                       description=f"Is the area of a scalene triangle with sides of length {s1}, {s2} and {s3}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            elif response.component['label'] == "Right-Angled Triangle":
                await ctx.send(embed=nextcord.Embed(
                    title="Please enter the two sides other then the hypotenuse.\n`<side1> <side2>`",
                    color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a triangle can have a mention as one of its SIDES?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a triangle can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 2:
                    await ctx.send(embed=nextcord.Embed(
                        title=f"Only two numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=nextcord.Color.random()))
                    return
                b = split[0]
                h = split[1]
                area = round((float(b) * float(h)) / 2, 3)
                if area.is_integer() is True:
                    area = int(area)
                embed = nextcord.Embed(title=f"{area}",
                                       description=f"Is the area of an isosceles triangle with the sides {b} and {h}, as long as they aren't the hypotenuses of the triangle!",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

        elif response.component['label'] == "Quadrilateral":
            await ctx.send(
                "Please choose the type of quadrilateral you want to use",
                components=[
                    Button(style=ButtonStyle.blue, label="Parallelogram"),
                    Button(style=ButtonStyle.red, label="Rectangle"),
                    Button(style=ButtonStyle.green, label="Rhombus"),
                    Button(style=ButtonStyle.gray, label="Square"),
                    Button(style=ButtonStyle.blue, label="Trapezium")
                ]
            )
            try:
                response: ComponentContext = await wait_for_component(self.bot, components=action_row, timeout=20)
                await response.defer(ignore=True)
            except asyncio.TimeoutError:
                await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                    color=nextcord.Color.random()))
                return
            if response.component['label'] == "Parallelogram":
                await ctx.send(embed=nextcord.Embed(
                    title="Please enter the base and height of the parallelogram.\n`<base> <height>`",
                    color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a parallelogram can have a mention as one of its SIDES?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a parallelogram can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 2:
                    await ctx.send(embed=nextcord.Embed(
                        title=f"Only two numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=nextcord.Color.random()))
                    return
                b = split[0]
                h = split[1]
                area = float(b) * float(h)
                if area.is_integer() is True:
                    area = int(area)
                embed = nextcord.Embed(title=f"{area}",
                                       description=f"Is the area of an parallelogram with opposite sides of length {b} and {h}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            elif response.component['label'] == "Rectangle":
                await ctx.send(embed=nextcord.Embed(
                    title="Please enter the length and breadth of the rectangle.\n`<length> <breadth>`",
                    color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a rectangle can have a mention as one of its SIDES?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a rectangle can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 2:
                    await ctx.send(embed=nextcord.Embed(
                        title=f"Only two numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=nextcord.Color.random()))
                    return
                l = split[0]
                b = split[1]
                area = float(l) * float(b)
                if area.is_integer() is True:
                    area = int(area)
                embed = nextcord.Embed(title=f"{area}",
                                       description=f"Is the area of an rectangle with opposite sides of length {l} and {b}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            elif response.component['label'] == "Rhombus":
                await ctx.send(embed=nextcord.Embed(
                    title="Please enter the diagonals of the rhombus in this format\n`<diagonal1> <diagonal2>`",
                    color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a rhombus have a mention as a side?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a rhombus can have a side {s}?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 2:
                    await ctx.send(embed=nextcord.Embed(
                        title=f"Only two numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=nextcord.Color.random()))
                    return
                d1 = split[0]
                d2 = split[1]
                area = float(d1) * float(d2)
                if area.is_integer() is True:
                    area = int(area)
                embed = nextcord.Embed(title=f"{area}",
                                       description=f"Is the area of a rhombus with  diagonals {d1} and {d2}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            elif response.component['label'] == "Square":
                await ctx.send(
                    embed=nextcord.Embed(title="Please enter the side of the square", color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a square have a mention as a side?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a square can have a side {s}?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                area = math.pow(float(s), 2)
                if area.is_integer() is True:
                    area = int(area)
                embed = nextcord.Embed(title=f"{area}",
                                       description=f"Is the area of a square with side {s}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            elif response.component['label'] == "Trapezium":
                await ctx.send(embed=nextcord.Embed(
                    title="Please enter the unequal sides of the trapezium, along with its height(altitude), in this format\n`<unequalside1> <unequalside2> <height/altitude>`",
                    color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a trapezium can have a mention as one of its dimensions?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a trapezium can have {s} as one of its DIMENSIONS?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 3:
                    await ctx.send(embed=nextcord.Embed(
                        title=f"Only three numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=nextcord.Color.random()))
                    return
                a = split[0]
                b = split[1]
                h = split[2]
                area = round(((float(a) + float(b)) * float(h)) / 2, 3)
                if area.is_integer() is True:
                    area = int(area)
                embed = nextcord.Embed(title=f"{area}",
                                       description=f"Is the area of a trapezium with unequal sides of length {a}, {b} and height of length{h}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

    @commands.command()
    async def area(self, ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        await ctx.send(
            "Please choose one of the following options",
            components=[
                Button(style=ButtonStyle.blue, label="Circle"),
                Button(style=ButtonStyle.red, label="Triangle"),
                Button(style=ButtonStyle.green, label="Quadrilateral")
            ]
        )

        try:
            response: ComponentContext = await wait_for_component(self.bot, components=action_row, timeout=20)
            await response.defer(ignore=True)
        except asyncio.TimeoutError:
            await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                color=nextcord.Color.random()))
            return
        if response.component['label'] == "Circle":
            await ctx.send(embed=nextcord.Embed(title="Please enter the radius", color=nextcord.Color.random()))
            try:
                r = await self.bot.wait_for("message", check=check, timeout=20)
            except asyncio.TimeoutError:
                await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                    color=nextcord.Color.random()))
                return
            if r.mentions:
                await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                    description=f"That a circle have a mention as a radius?",
                                                    color=nextcord.Color.random()))
                return
            r = r.content
            for i in r:
                if not i.isdigit() and i != ".":
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a circle can have a radius {r}?\nThe '{i}' there makes it useless",
                                                        color=nextcord.Color.random()))
                    return
            area = round(22 * float(r) * float(r) / 7, 3)
            if area.is_integer() is True:
                area = int(area)
            embed = nextcord.Embed(title=f"{area}",
                                   description=f"Is the area of a circle with radius {r}",
                                   color=nextcord.Color.random())
            embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

        elif response.component['label'] == "Triangle":
            await ctx.send(
                "Please choose the type of triangle you want to use",
                components=[
                    Button(style=ButtonStyle.blue, label="Equilateral Triangle"),
                    Button(style=ButtonStyle.red, label="Isosceles Triangle"),
                    Button(style=ButtonStyle.green, label="Scalene Triangle"),
                    Button(style=ButtonStyle.grey, label="Right-Angled Triangle")
                ]
            )
            try:
                response: ComponentContext = await wait_for_component(self.bot, components=action_row, timeout=20)
                await response.defer(ignore=True)
            except asyncio.TimeoutError:
                await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                    color=nextcord.Color.random()))
                return
            if response.component['label'] == "Equilateral Triangle":
                await ctx.send(embed=nextcord.Embed(title="Please enter the length of the side of the triangle.",
                                                    color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a triangle have a mention as a side?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a triangle can have a side {s}?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                area = round(math.sqrt(3) * float(s) * float(s) / 4, 3)
                if area.is_integer() is True:
                    area = int(area)
                embed = nextcord.Embed(title=f"{area}",
                                       description=f"Is the area of an equilateral triangle with side {s}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            elif response.component['label'] == "Isosceles Triangle":
                await ctx.send(nextcord.Embed(
                    title="Please enter the equal and the non-equal sides in this format\n`<equalside> <non-equalside>`",
                    color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a triangle can have a mention as one of its SIDES?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a triangle can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 2:
                    await ctx.send(embed=nextcord.Embed(
                        title=f"Only two numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=nextcord.Color.random()))
                    return
                e = split[0]
                n = split[1]
                area = round(float(n) * (math.sqrt(math.pow(float(e), 2) - (math.pow(float(e), 2) / 4))) / 2, 3)
                if area.is_integer() is True:
                    area = int(area)
                embed = nextcord.Embed(title=f"{area}",
                                       description=f"Is the area of an isosceles triangle with equal sides of length {e} and a non-equal side of length {n}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            elif response.component['label'] == "Scalene Triangle":
                await ctx.send(
                    embed=nextcord.Embed(title="Please enter the three sides in this format\n`<side1> <side2> <side3>`",
                                         color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a triangle can have a mention as one of its SIDES?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a triangle can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 3:
                    await ctx.send(embed=nextcord.Embed(
                        title=f"Only three numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=nextcord.Color.random()))
                    return
                s1 = split[0]
                s2 = split[1]
                s3 = split[2]
                s_heron = float(s1) + float(s2) + float(s3)
                area = round(math.sqrt(s_heron * (s_heron - float(s1)) * (s_heron - float(s2)) * (s_heron - float(s3))),
                             3)
                if area.is_integer() is True:
                    area = int(area)
                embed = nextcord.Embed(title=f"{area}",
                                       description=f"Is the area of a scalene triangle with sides of length {s1}, {s2} and {s3}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            elif response.component['label'] == "Right-Angled Triangle":
                await ctx.send(embed=nextcord.Embed(
                    title="Please enter the two sides other then the hypotenuse.\n`<side1> <side2>`",
                    color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a triangle can have a mention as one of its SIDES?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a triangle can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 2:
                    await ctx.send(embed=nextcord.Embed(
                        title=f"Only two numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=nextcord.Color.random()))
                    return
                b = split[0]
                h = split[1]
                area = round((float(b) * float(h)) / 2, 3)
                if area.is_integer() is True:
                    area = int(area)
                embed = nextcord.Embed(title=f"{area}",
                                       description=f"Is the area of an isosceles triangle with the sides {b} and {h}, as long as they aren't the hypotenuses of the triangle!",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

        elif response.component['label'] == "Quadrilateral":
            await ctx.send(
                "Please choose the type of quadrilateral you want to use",
                components=[
                    Button(style=ButtonStyle.blue, label="Parallelogram"),
                    Button(style=ButtonStyle.red, label="Rectangle"),
                    Button(style=ButtonStyle.green, label="Rhombus"),
                    Button(style=ButtonStyle.gray, label="Square"),
                    Button(style=ButtonStyle.blue, label="Trapezium")
                ]
            )
            try:
                response: ComponentContext = await wait_for_component(self.bot, components=action_row, timeout=20)
                await response.defer(ignore=True)
            except asyncio.TimeoutError:
                await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                    color=nextcord.Color.random()))
                return
            if response.component['label'] == "Parallelogram":
                await ctx.send(embed=nextcord.Embed(
                    title="Please enter the base and height of the parallelogram.\n`<base> <height>`",
                    color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a parallelogram can have a mention as one of its SIDES?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a parallelogram can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 2:
                    await ctx.send(embed=nextcord.Embed(
                        title=f"Only two numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=nextcord.Color.random()))
                    return
                b = split[0]
                h = split[1]
                area = float(b) * float(h)
                if area.is_integer() is True:
                    area = int(area)
                embed = nextcord.Embed(title=f"{area}",
                                       description=f"Is the area of an parallelogram with opposite sides of length {b} and {h}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            elif response.component['label'] == "Rectangle":
                await ctx.send(embed=nextcord.Embed(
                    title="Please enter the length and breadth of the rectangle.\n`<length> <breadth>`",
                    color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a rectangle can have a mention as one of its SIDES?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a rectangle can have {s} as one of its SIDES?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 2:
                    await ctx.send(embed=nextcord.Embed(
                        title=f"Only two numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=nextcord.Color.random()))
                    return
                l = split[0]
                b = split[1]
                area = float(l) * float(b)
                if area.is_integer() is True:
                    area = int(area)
                embed = nextcord.Embed(title=f"{area}",
                                       description=f"Is the area of an rectangle with opposite sides of length {l} and {b}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            elif response.component['label'] == "Rhombus":
                await ctx.send(embed=nextcord.Embed(
                    title="Please enter the diagonals of the rhombus in this format\n`<diagonal1> <diagonal2>`",
                    color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a rhombus have a mention as a side?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a rhombus can have a side {s}?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 2:
                    await ctx.send(embed=nextcord.Embed(
                        title=f"Only two numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=nextcord.Color.random()))
                    return
                d1 = split[0]
                d2 = split[1]
                area = float(d1) * float(d2)
                if area.is_integer() is True:
                    area = int(area)
                embed = nextcord.Embed(title=f"{area}",
                                       description=f"Is the area of a rhombus with  diagonals {d1} and {d2}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            elif response.component['label'] == "Square":
                await ctx.send(
                    embed=nextcord.Embed(title="Please enter the side of the square", color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a square have a mention as a side?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a square can have a side {s}?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                area = math.pow(float(s), 2)
                if area.is_integer() is True:
                    area = int(area)
                embed = nextcord.Embed(title=f"{area}",
                                       description=f"Is the area of a square with side {s}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

            elif response.component['label'] == "Trapezium":
                await ctx.send(nextcord.Embed(
                    title="Please enter the unequal sides of the trapezium, along with its height(altitude), in this format\n`<unequalside1> <unequalside2> <height/altitude>`",
                    color=nextcord.Color.random()))
                try:
                    s = await self.bot.wait_for("message", check=check, timeout=20)
                except asyncio.TimeoutError:
                    await ctx.send(embed=nextcord.Embed(title="Your command has timed out.",
                                                        color=nextcord.Color.random()))
                    return
                if s.mentions:
                    await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                        description=f"That a trapezium can have a mention as one of its dimensions?",
                                                        color=nextcord.Color.random()))
                    return
                s = s.content
                for i in s:
                    if not i.isdigit() and i != " " and i != ".":
                        await ctx.send(embed=nextcord.Embed(title=f"Why do you think",
                                                            description=f"That a trapezium can have {s} as one of its DIMENSIONS?\nThe '{i}' there makes it useless",
                                                            color=nextcord.Color.random()))
                        return
                split = s.split(" ")
                if len(split) != 3:
                    await ctx.send(embed=nextcord.Embed(
                        title=f"Only three numbers needed, nothing more or less.\nI seriously don't know why you are failing at this.",
                        color=nextcord.Color.random()))
                    return
                a = split[0]
                b = split[1]
                h = split[2]
                area = round(((float(a) + float(b)) * float(h)) / 2, 3)
                if area.is_integer() is True:
                    area = int(area)
                embed = nextcord.Embed(title=f"{area}",
                                       description=f"Is the area of a trapezium with unequal sides of length {a}, {b} and height of length{h}",
                                       color=nextcord.Color.random())
                embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
                embed.set_thumbnail(url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(base="math", name="square", description="Gets the square of a number for you.",
                            options=[
                                create_option(name="number",
                                              description="The number whose square you want",
                                              option_type=3,
                                              required=True)])
    async def _square(self, ctx: SlashContext, number=""):
        ans = await cf.power_funcs(ctx=ctx, number=number, power="2", power_or_root="power")
        if ans is None:
            return
        embed = nextcord.Embed(title=f"{ans}",
                               description=f"Is the square of {number}.",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['sq'])
    async def square(self, ctx, number=""):
        ans = await cf.power_funcs(ctx=ctx, number=number, power="2", power_or_root="power")
        if ans is None:
            return
        embed = nextcord.Embed(title=f"{ans}",
                               description=f"Is the square of {number}.",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(base="math", name="cube", description="Gets the cube of a number for you.",
                            options=[
                                create_option(name="number",
                                              description="The number whose cube you want",
                                              option_type=3,
                                              required=True)])
    async def _cube(self, ctx: SlashContext, number=""):
        ans = await cf.power_funcs(ctx=ctx, number=number, power="3", power_or_root="power")
        if ans is None:
            return
        embed = nextcord.Embed(title=f"{ans}",
                               description=f"Is the cube of {number}.",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['cb'])
    async def cube(self, ctx, number=""):
        ans = await cf.power_funcs(ctx=ctx, number=number, power="3", power_or_root="power")
        if ans is None:
            return
        embed = nextcord.Embed(title=f"{ans}",
                               description=f"Is the cube of {number}.",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(base="math", name="squareroot", description="Gets the square root of a number for you.",
                            options=[
                                create_option(name="number",
                                              description="The number whose square root you want",
                                              option_type=3,
                                              required=True)])
    async def _squareroot(self, ctx: SlashContext, number=""):
        ans = await cf.power_funcs(ctx=ctx, number=number, power="2", power_or_root="root")
        if ans is None:
            return
        embed = nextcord.Embed(title=f"{ans}",
                               description=f"Is the square root of {number}.",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['sqrt'])
    async def squareroot(self, ctx, number=""):
        ans = await cf.power_funcs(ctx=ctx, number=number, power="2", power_or_root="root")
        if ans is None:
            return
        embed = nextcord.Embed(title=f"{ans}",
                               description=f"Is the square root of {number}.",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(base="math", name="cuberoot", description="Gets the cube root of a number for you.",
                            options=[
                                create_option(name="number",
                                              description="The number whose cube root you want",
                                              option_type=3,
                                              required=True)])
    async def _cuberoot(self, ctx: SlashContext, number=""):
        ans = await cf.power_funcs(ctx=ctx, number=number, power="3", power_or_root="root")
        if ans is None:
            return
        embed = nextcord.Embed(title=f"{ans}",
                               description=f"Is the cube root of {number}",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['cbrt'])
    async def cuberoot(self, ctx, number=""):
        ans = await cf.power_funcs(ctx=ctx, number=number, power="3", power_or_root="root")
        if ans is None:
            return
        embed = nextcord.Embed(title=f"{ans}",
                               description=f"Is the cube root of {number}",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(base="math", name="power", description="Gets any power of any number for you.",
                            options=[
                                create_option(name="number",
                                              description="The number whose power is needed",
                                              option_type=3,
                                              required=True),
                                create_option(name="power",
                                              description="The exponent required.",
                                              option_type=3,
                                              required=True)])
    async def _power(self, ctx: SlashContext, number="", power=""):
        ans = await cf.power_funcs(ctx=ctx, number=number, power=power, power_or_root="power")
        if ans is None:
            return
        embed = nextcord.Embed(title=f"{ans}",
                               description=f"Is the value of {number} to the power {power}",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['pow'])
    async def power(self, ctx, number="", power=""):
        ans = await cf.power_funcs(ctx=ctx, number=number, power=power, power_or_root="power")
        if ans is None:
            return
        embed = nextcord.Embed(title=f"{ans}",
                               description=f"Is the value of {number} to the power {power}",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(base="math", name="root", description="Gets any power of any number for you.",
                            options=[
                                create_option(name="number",
                                              description="The number whose root is needed",
                                              option_type=3,
                                              required=True),
                                create_option(name="root",
                                              description="The root required.",
                                              option_type=3,
                                              required=True)])
    async def _root(self, ctx: SlashContext, number="", root=""):
        ans = await cf.power_funcs(ctx=ctx, number=number, power=root, power_or_root="root")
        if ans is None:
            return
        embed = nextcord.Embed(title=f"{ans}",
                               description=f"Is the value of root {root} of {number}",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def root(self, ctx, number="", power=""):
        ans = await cf.power_funcs(ctx=ctx, number=number, power=power, power_or_root="root")
        if ans is None:
            return
        embed = nextcord.Embed(title=f"{ans}",
                               description=f"Is the value of root {power} of {number}",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(base="math", name="trig",
                            description="Gives you some info about trigonometric functions...")
    async def _trig(self, ctx: SlashContext):
        string = "sin A = Perpendicular/Hypotenuse\ncos A = Base/Hypotenuse\ntan A = Perpendicular/Base\nsec A = Hypotenuse/Base\ncosec A = Hypotenuse/Perpendicular\ncot A = Base/Perpendicular"
        embed = nextcord.Embed(title=f"Trigonometric values are as follows:",
                               description=f"{string}",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def trig(self, ctx):
        string = "sin A = Perpendicular/Hypotenuse\ncos A = Base/Hypotenuse\ntan A = Perpendicular/Base\nsec A = Hypotenuse/Base\ncosec A = Hypotenuse/Perpendicular\ncot A = Base/Perpendicular"
        embed = nextcord.Embed(title=f"Trigonometric values are as follows:",
                               description=f"{string}",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(base="trig", name="sin", description="Gives you info about sin")
    async def _sin(self, ctx: SlashContext):
        embed = nextcord.Embed(title=f"Info on the trigonometric value 'sin'",
                               color=nextcord.Color.random())
        embed.add_field(name="Full Form:", value="sine", inline=False)
        embed.add_field(name="Value in Respect to Triangular Sides:", value="Perpendicular/Hypotenuse", inline=False)
        embed.add_field(name="Value of Reciprocal:", value="sin A = 1/cosec A", inline=False)
        embed.add_field(name="Relation to the number 1:", value="sin² A = 1 - cos² A", inline=False)
        embed.add_field(name="Relation to Other Trigonometric Function:",
                        value="sin A = tan A cos A\nsin A = cos A/cot A\nsin A = tan A/ sec A", inline=False)
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['sine'])
    async def sin(self, ctx: SlashContext):
        embed = nextcord.Embed(title=f"Info on the trigonometric value 'sin'",
                               color=nextcord.Color.random())
        embed.add_field(name="Full Form:", value="sine", inline=False)
        embed.add_field(name="Value in Respect to Triangular Sides:", value="Perpendicular/Hypotenuse", inline=False)
        embed.add_field(name="Value of Reciprocal:", value="sin A = 1/cosec A", inline=False)
        embed.add_field(name="Relation to the number 1:", value="sin² A = 1 - cos² A", inline=False)
        embed.add_field(name="Relation to Other Trigonometric Function:",
                        value="sin A = tan A cos A\nsin A = cos A/cot A\nsin A = tan A/ sec A", inline=False)
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(base="trig", name="cos", description="Gives you info about cos")
    async def _cos(self, ctx: SlashContext):
        embed = nextcord.Embed(title=f"Info on the trigonometric value 'cos'",
                               color=nextcord.Color.random())
        embed.add_field(name="Full Form:", value="cosine", inline=False)
        embed.add_field(name="Value in Respect to Triangular Sides:", value="Base/Hypotenuse", inline=False)
        embed.add_field(name="Value of Reciprocal:", value="cos A = 1/sec A", inline=False)
        embed.add_field(name="Relation to the number 1:", value="cos² A = 1 - sin² A", inline=False)
        embed.add_field(name="Relation to Other Trigonometric Function:",
                        value="cos A=sin A cot A\ncos A = sin A/tan A\ncos A = cot A/ sec A", inline=False)
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['cosine'])
    async def cos(self, ctx):
        embed = nextcord.Embed(title=f"Info on the trigonometric value 'cos'",
                               color=nextcord.Color.random())
        embed.add_field(name="Full Form:", value="cosine", inline=False)
        embed.add_field(name="Value in Respect to Triangular Sides:", value="Base/Hypotenuse", inline=False)
        embed.add_field(name="Value of Reciprocal:", value="cos A = 1/sec A", inline=False)
        embed.add_field(name="Relation to the number 1:", value="cos² A = 1 - sin² A", inline=False)
        embed.add_field(name="Relation to Other Trigonometric Function:",
                        value="cos A=sin A cot A\ncos A = sin A/tan A\ncos A = cot A/ sec A", inline=False)
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(base="trig", name="tan", description="Gives you info about tan")
    async def _tan(self, ctx: SlashContext):
        embed = nextcord.Embed(title=f"Info on the trigonometric value 'tan'",
                               color=nextcord.Color.random())
        embed.add_field(name="Full Form:", value="tangent", inline=False)
        embed.add_field(name="Value in Respect to Triangular Sides:", value="Perpendicular/Base", inline=False)
        embed.add_field(name="Value of Reciprocal:", value="tan A = 1/cot A", inline=False)
        embed.add_field(name="Relation to the number 1:", value="tan² A = sec² A - 1 ", inline=False)
        embed.add_field(name="Relation to Other Trigonometric Function:",
                        value="tan A = sin A sec A\ntan A = sin A/cos A\ntan A = sec A/ cosec A", inline=False)
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['tangent'])
    async def tan(self, ctx):
        embed = nextcord.Embed(title=f"Info on the trigonometric value 'tan'",
                               color=nextcord.Color.random())
        embed.add_field(name="Full Form:", value="tangent", inline=False)
        embed.add_field(name="Value in Respect to Triangular Sides:", value="Perpendicular/Base", inline=False)
        embed.add_field(name="Value of Reciprocal:", value="tan A = 1/cot A", inline=False)
        embed.add_field(name="Relation to the number 1:", value="tan² A = sec² A - 1 ", inline=False)
        embed.add_field(name="Relation to Other Trigonometric Function:",
                        value="tan A = sin A sec A\ntan A = sin A/cos A\ntan A = sec A/ cosec A", inline=False)
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(base="trig", name="sec", description="Gives you info about sec")
    async def _sec(self, ctx: SlashContext):
        embed = nextcord.Embed(title=f"Info on the trigonometric value 'sec'",
                               color=nextcord.Color.random())
        embed.add_field(name="Full Form:", value="secant", inline=False)
        embed.add_field(name="Value in Respect to Triangular Sides:", value="Hypotenuse/Base", inline=False)
        embed.add_field(name="Value of Reciprocal:", value="sec A = 1/cos A", inline=False)
        embed.add_field(name="Relation to the number 1:", value="sec² A = 1 + tan² A", inline=False)
        embed.add_field(name="Relation to Other Trigonometric Function:",
                        value="sec A=sin A cot A\nsec A = cot A/cosec A\nsec A = cos A/ tan A", inline=False)
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['secant'])
    async def sec(self, ctx):
        embed = nextcord.Embed(title=f"Info on the trigonometric value 'sec'",
                               color=nextcord.Color.random())
        embed.add_field(name="Full Form:", value="secant", inline=False)
        embed.add_field(name="Value in Respect to Triangular Sides:", value="Hypotenuse/Base", inline=False)
        embed.add_field(name="Value of Reciprocal:", value="sec A = 1/cos A", inline=False)
        embed.add_field(name="Relation to the number 1:", value="sec² A = 1 + tan² A", inline=False)
        embed.add_field(name="Relation to Other Trigonometric Function:",
                        value="sec A=sin A cot A\nsec A = cot A/cosec A\nsec A = cos A/ tan A", inline=False)
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(base="trig", name="cosec", description="Gives you info about cosec")
    async def _cosec(self, ctx: SlashContext):
        embed = nextcord.Embed(title=f"Info on the trigonometric value 'cosec'",
                               color=nextcord.Color.random())
        embed.add_field(name="Full Form:", value="cosecant", inline=False)
        embed.add_field(name="Value in Respect to Triangular Sides:", value="Hypotenuse/Perpendicular", inline=False)
        embed.add_field(name="Value of Reciprocal:", value="cosec A = 1/sin A", inline=False)
        embed.add_field(name="Relation to the number 1:", value="cosec² A = 1 + cot² A", inline=False)
        embed.add_field(name="Relation to Other Trigonometric Function:",
                        value="cosec A = tan A cos A\ncosec A = tan A/sec A\ncosec A = cos A/ cot A", inline=False)
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['cosecant'])
    async def cosec(self, ctx):
        embed = nextcord.Embed(title=f"Info on the trigonometric value 'cosec'",
                               color=nextcord.Color.random())
        embed.add_field(name="Full Form:", value="cosecant", inline=False)
        embed.add_field(name="Value in Respect to Triangular Sides:", value="Hypotenuse/Perpendicular", inline=False)
        embed.add_field(name="Value of Reciprocal:", value="cosec A = 1/sin A", inline=False)
        embed.add_field(name="Relation to the number 1:", value="cosec² A = 1 + cot² A", inline=False)
        embed.add_field(name="Relation to Other Trigonometric Function:",
                        value="cosec A = tan A cos A\ncosec A = tan A/sec A\ncosec A = cos A/ cot A", inline=False)
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(base="trig", name="cot", description="Gives you info about cot")
    async def _cot(self, ctx: SlashContext):
        embed = nextcord.Embed(title=f"Info on the trigonometric value 'cot'",
                               color=nextcord.Color.random())
        embed.add_field(name="Full Form:", value="cotangent", inline=False)
        embed.add_field(name="Value in Respect to Triangular Sides:", value="Base/Perpendicular", inline=False)
        embed.add_field(name="Value of Reciprocal:", value="cot A = 1/tan A", inline=False)
        embed.add_field(name="Relation to the number 1:", value="cot² A = cosec² A - 1", inline=False)
        embed.add_field(name="Relation to Other Trigonometric Function:",
                        value="cot A = cos A cosec A\ncot A = cos A/sin A\ncot A = cosec A/ sec A", inline=False)
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['cotan', 'cotangent'])
    async def cot(self, ctx):
        embed = nextcord.Embed(title=f"Info on the trigonometric value 'cot'",
                               color=nextcord.Color.random())
        embed.add_field(name="Full Form:", value="cotangent", inline=False)
        embed.add_field(name="Value in Respect to Triangular Sides:", value="Base/Perpendicular", inline=False)
        embed.add_field(name="Value of Reciprocal:", value="cot A = 1/tan A", inline=False)
        embed.add_field(name="Relation to the number 1:", value="cot² A = cosec² A - 1", inline=False)
        embed.add_field(name="Relation to Other Trigonometric Function:",
                        value="cot A = cos A cosec A\ncot A = cos A/sin A\ncot A = cosec A/ sec A", inline=False)
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Nerd(bot))
