import discord
import nextcord
import asyncio
from nextcord.ext import commands
import calendar
import time
from tzlocal import get_localzone
from datetime import datetime, timedelta
import aiohttp
from tinydb import TinyDB, Query
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.sniped_messages = {}

    @commands.cooldown(1, 5, commands.BucketType.user)
    @cog_ext.cog_slash(name="ping",
                       description="This allows you to check my ping.")
    async def _ping(self, ctx: SlashContext):
        start_time = time.time()
        message = await ctx.send(embed=nextcord.Embed(title="Testing Ping...", color=nextcord.Color.random()))
        end_time = time.time()

        await message.edit(embed=nextcord.Embed(
            title=f"Latency: {round(self.bot.latency * 1000)}ms\nAPI: {round((end_time - start_time) * 1000)}ms",
            color=nextcord.Color.random()))

    @commands.command(aliases=['p'])
    async def ping(self, ctx):
        """Get the bot's current websocket and API latency."""
        start_time = time.time()
        message = await ctx.send(embed=nextcord.Embed(title="Testing Ping...", color=nextcord.Color.random()))
        end_time = time.time()

        await message.edit(embed=nextcord.Embed(
            title=f"Latency: {round(self.bot.latency * 1000)}ms\nAPI: {round((end_time - start_time) * 1000)}ms",
            color=nextcord.Color.random()))

    @cog_ext.cog_slash(name="makerole",
                       description="Makes a new role in the server for you!",
                       options=[create_option(name="rolename", description="Name of the role you want to make.",
                                              option_type=3,
                                              required=True
                                              )
                                ])
    async def _makerole(self, ctx, rolename: str):
        try:
            rolename = await commands.MemberConverter().convert(ctx, rolename)
        except:
            pass
        color = nextcord.Color.random()
        if ctx.author.guild_permissions.manage_roles:
            guild = ctx.guild
            perms = nextcord.Permissions(send_messages=True, read_messages=True)
            role = await guild.create_role(name=rolename, color=color, permissions=perms)
            embed1 = nextcord.Embed(title="Role Created!",
                                    description=f"Added role {role.mention} to the server!",
                                    color=color)
            embed1.set_footer(text=f"Tip: Do /addrole to add your newly created role to users!")
            await ctx.send(embed=embed1)

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!",
                                     descripction="You require the Manage Roles permission.",
                                     color=color))

    @commands.command(aliases=['mr', 'createrole'])
    async def makerole(self, ctx, *, rolename: str):
        try:
            rolename = await commands.MemberConverter().convert(ctx, rolename)
        except:
            pass
        color = nextcord.Color.random()
        if ctx.author.guild_permissions.manage_roles:
            guild = ctx.guild
            perms = nextcord.Permissions(send_messages=True, read_messages=True)
            role = await guild.create_role(name=str(rolename), color=color, permissions=perms)
            embed1 = nextcord.Embed(title="Role Created!",
                                    description=f"Added role {role.mention} to the server!",
                                    color=color)
            embed1.set_footer(text=f"Tip: Do {ctx.prefix}addrole to add your newly created role to users!")
            await ctx.send(embed=embed1)

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!",
                                     description="You require the Manage Roles permission.",
                                     color=color))

    @cog_ext.cog_slash(name="addrole", description="Gives the user a role!",
                       options=[create_option(name="member",
                                              description="Person to whom you want to add a role",
                                              option_type=6,
                                              required=True
                                              ),
                                create_option(name="role",
                                              description="The role you want to add to that person",
                                              option_type=8,
                                              required=True
                                              )]
                       )
    async def _addrole(self, ctx: SlashContext, member: nextcord.Member, *, role: nextcord.Role = None):
        if ctx.author.guild_permissions.manage_roles:
            embed = nextcord.Embed(
                title=f"Role Added",
                description=f"{role.mention} has been added to {member.mention}."
            )
            embed.color = nextcord.Color.random()
            embed.set_footer(text="Gamers = Poggers but why is this here???")
            await member.add_roles(role)
            await ctx.send(embed=embed)

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!", description="You require the Manage Roles permission.",
                                     color=nextcord.Color.green()))

    @commands.command(aliases=['addr', 'arole', 'ar'])
    async def addrole(self, ctx, member: nextcord.Member, *, role: nextcord.Role = None):
        if ctx.author.guild_permissions.manage_roles:
            embed = nextcord.Embed(
                title=f"Role Added",
                description=f"{role.mention} has been added to {member.mention}."
            )
            embed.color = nextcord.Color.random()
            embed.set_footer(text="Gamers = Poggers but why is this here???")
            await member.add_roles(role)
            await ctx.send(embed=embed)

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!", description="You require the Manage Roles permission.",
                                     color=nextcord.Color.green()))

    @cog_ext.cog_slash(name="editrole", description="Edits an existing role in the server.",
                       options=[create_option(name="from_role",
                                              description="The existing role that you want to change",
                                              option_type=8,
                                              required=True
                                              ),
                                create_option(name="information",
                                              description="The new name of the role or the new color, or both! check help editrole",
                                              option_type=3,
                                              required=True
                                              )]
                       )
    async def _editrole(self, ctx: SlashContext, from_role: nextcord.Role, *, information=None):
        if ctx.author.guild_permissions.manage_roles:
            guild = ctx.guild
            from_role = str(from_role)
            role = nextcord.utils.get(guild.roles, name=from_role)

            if '#' in information:
                if information.startswith("#"):
                    information = information.replace('#', '')
                    await role.edit(colour=nextcord.Colour(int(information, 16)))
                    embed = nextcord.Embed(
                        title="Role has been edited.",
                        description=f"Role color changed to {nextcord.Colour(int(information, 16))}",
                        color=nextcord.Color.random()
                    )
                    embed.set_footer(
                        text=f"Tip: Use /editrole <new_name> <new_color> to change the name and color of a role at the same time")
                    await ctx.send(embed=embed)
                    return
                split = information.split('#')
                if len(split[1]) != 6:
                    await ctx.send(
                        embed=nextcord.Embed(title=f"A colour hex-decimal can only have a length of 6 digits",
                                             color=nextcord.Color.random()))
                    return
                to_role = str(split[0])
                colour = split[1]
                await role.edit(name=to_role, colour=nextcord.Colour(int(colour, 16)))
                embed = nextcord.Embed(
                    title="Role has been edited.",
                    description=f"Role name changed from {from_role} to {to_role}, and color changed to #{colour}",
                    color=nextcord.Color.random()
                )
                embed.set_footer(
                    text=f"Tip: You can use the /color feature to find out what colour a hexdecimal will look like")
                await ctx.send(embed=embed)

            else:
                await role.edit(name=information)
                embed = nextcord.Embed(
                    title="Role has been edited.",
                    description=f"Role name changed from {from_role} to {information}.",
                    color=nextcord.Color.random()
                )
                await ctx.send(embed=embed)

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!",
                                     description="You require the Manage Roles permission.",
                                     color=nextcord.Color.green()))

    @commands.command(aliases=['editr', 'erole', 'er'])
    async def editrole(self, ctx, from_role: nextcord.Role, *, information=None):
        if ctx.author.guild_permissions.manage_roles:
            guild = ctx.guild
            from_role = str(from_role)
            role = nextcord.utils.get(guild.roles, name=from_role)

            if information is None:
                await ctx.send(embed=nextcord.Embed(title="U sir/maam are very annoying",
                                                    description="I need the new name or color of the role as well dude",
                                                    color=nextcord.Color.random()))
                await ctx.send(embed=embed)
            if '#' in information:
                if information.startswith("#"):
                    information = information.replace('#', '')
                    await role.edit(colour=nextcord.Colour(int(information, 16)))
                    embed = nextcord.Embed(
                        title="Role has been edited.",
                        description=f"Role color changed to {nextcord.Colour(int(information, 16))}",
                        color=nextcord.Color.random()
                    )
                    embed.set_footer(
                        text=f"Tip: Use {ctx.prefix}editrole <new_name> <new_color> to change the name and color of a role at the same time")
                    await ctx.send(embed=embed)
                    return
                split = information.split('#')
                if len(split[1]) != 6:
                    await ctx.send(
                        embed=nextcord.Embed(title=f"A colour hex-decimal can only have a length of 6 digits",
                                             color=nextcord.Color.random()))
                    return
                to_role = str(split[0])
                colour = split[1]
                await role.edit(name=to_role, colour=nextcord.Colour(int(colour, 16)))
                embed = nextcord.Embed(
                    title="Role has been edited.",
                    description=f"Role name changed from {from_role} to {to_role}, color changed to #{colour}",
                    color=nextcord.Color.random()
                )
                embed.set_footer(
                    text=f"Tip: You can use the {ctx.prefix}color feature to find out what colour a hexdecimal will look like")
                await ctx.send(embed=embed)

            else:
                await role.edit(name=information)
                embed = nextcord.Embed(
                    title="Role has been edited.",
                    description=f"Role name changed from {from_role} to {information}.",
                    color=nextcord.Color.random()
                )
                await ctx.send(embed=embed)

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!",
                                     description="You require the Manage Roles permission.",
                                     color=nextcord.Color.green()))

    @commands.command(aliases=['remover', 'rrole', 'rr'])
    async def removerole(self, ctx, member: nextcord.Member, *, role: nextcord.Role = None):
        if role is None:
            await ctx.send(embed=nextcord.Embed(title="If I don't get a role",
                                                description="I can't remove a role.\nNo matter how many members u give me!",
                                                color=nextcord.Color.random()))
            return

        elif role not in member.roles:
            embed = nextcord.Embed(title="The user doesn't even have this role",
                                   description="Soooo Ima just act like that was all cause of my hardwork!\nYeah I totally removed this user's role",
                                   color=nextcord.Color.random())
            embed.set_footer(text="#subtlety")
            await ctx.send(embed=embed)
            return

        if ctx.author.guild_permissions.manage_roles:
            embed = nextcord.Embed(
                title=f"Role Removed",
                description=f"{role} has been removed from {member.name}."
            )
            embed.color = nextcord.Color.random()
            embed.set_footer(text=f"")
            try:
                await member.remove_roles(role)
            except:
                raise error
            await ctx.send(embed=embed)

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!", description="You require the Manage Roles permission.",
                                     color=nextcord.Color.green()))

    @cog_ext.cog_slash(name="removerole", description="Takes away a user's role",
                       options=[create_option(name="member",
                                              description="Person whose role you want to snatch!",
                                              option_type=6,
                                              required=True
                                              ),
                                create_option(name="role",
                                              description="The role to be removed",
                                              option_type=8,
                                              required=True
                                              )
                                ]
                       )
    async def _removerole(self, ctx: SlashContext, member: nextcord.Member, *, role: nextcord.Role = None):
        if role is None:
            await ctx.send(embed=nextcord.Embed(title="If I don't get a role",
                                                description="I can't remove a role.\nNo matter how many members u give me!",
                                                color=nextcord.Color.random()))
            return

        elif role not in member.roles:
            embed = nextcord.Embed(title="The user doesn't even have this role",
                                   description="Soooo Ima just act like that was all cause of my hardwork!\nYeah I totally removed this user's role",
                                   color=nextcord.Color.random())
            embed.set_footer(text="#subtlety")
            await ctx.send(embed=embed)
            return
        if ctx.author.guild_permissions.manage_roles:
            embed = nextcord.Embed(
                title=f"Role Removed",
                description=f"{role} has been removed from {member.name}."
            )
            embed.color = nextcord.Color.random()
            embed.set_footer(text=f"")
            await member.remove_roles(role)
            await ctx.send(embed=embed)

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!", description="You require the Manage Roles permission.",
                                     color=nextcord.Color.green()))

    @commands.command(aliases=['deleter', 'drole', 'dr'])
    async def deleterole(self, ctx, rolename: nextcord.Role):
        if ctx.author.guild_permissions.manage_roles:
            await rolename.delete()
            embed = nextcord.Embed(
                title=f"Role {rolename} has been deleted",
                description=f"GET EM OUTTA HERE", color=nextcord.Color.random()
            )
            await ctx.send(embed=embed)

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!",
                                     description="You require the Manage Roles permission.",
                                     color=nextcord.Color.green()))

    @cog_ext.cog_slash(name="deleterole",
                       description="Deletes a role",
                       options=[create_option(name="role",
                                              description="The role you want to delete",
                                              option_type=8,
                                              required=True
                                              )
                                ])
    async def _deleterole(self, ctx: SlashContext, role: nextcord.Role):
        if ctx.author.guild_permissions.manage_roles:
            await role.delete()
            embed = nextcord.Embed(
                title=f"Role {role} has been deleted",
                description=f"GET EM OUTTA HERE", color=nextcord.Color.random()
            )
            await ctx.send(embed=embed)

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!",
                                     description="You require the Manage Roles permission.",
                                     color=nextcord.Color.green()))

    @commands.command(aliases=['user', 'uinfo', 'ui', 'profile', 'prof'])
    async def userinfo(self, ctx, target: nextcord.Member = None):
        if target is None:
            target = ctx.author

        if target in ctx.guild.members:
            roles = [role for role in target.roles if role != ctx.guild.default_role]
            if not roles:
                roles = None
            embed = nextcord.Embed(title="User Information", color=target.top_role.color,
                                   timestamp=datetime.utcnow())

            try:
                embed.set_author(name=target.name, icon_url=target.avatar.url)

                embed.set_thumbnail(url=target.avatar.url)

                embed.set_footer(text=f"Requested by {ctx.author.display_name}",
                                 icon_url=ctx.author.avatar.url)

            except:
                embed.set_author(name=target.name)

                embed.set_footer(text=f"Requested by {ctx.author.display_name}")

            if roles is None:
                fields = [("Name", str(target), False),
                          ("ID", target.id, False),
                          (f"Roles", "No roles", False),
                          ("Created at", f"Created at <t:{str(target.created_at.timestamp()).split('.')[0]}>", False),
                          ("Joined at", f"Joined at <t:{str(target.joined_at.timestamp()).split('.')[0]}>", False)]

            else:
                fields = [("Name", str(target), False),
                          ("ID", target.id, False),
                          (f"Roles ({len(roles)})", " ".join([role.mention for role in roles]), False),
                          ("Created at", f"Created at <t:{str(target.created_at.timestamp()).split('.')[0]}>", False),
                          ("Joined at", f"Joined at <t:{str(target.joined_at.timestamp()).split('.')[0]}>", False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=discord.Embed(title=f'You have to ping someone from this server and this server only',
                                               color=discord.Color.random()))

    @cog_ext.cog_slash(name="userinfo",
                       description="Gives the  information of the member specified...",
                       options=[create_option(name="target",
                                              description="Person who you want to stalk",
                                              option_type=6,
                                              required=False
                                              )
                                ]
                       )
    async def _userinfo(self, ctx: SlashContext, target: nextcord.Member = None):
        if target is None:
            target = ctx.author

        if target in ctx.guild.members:
            roles = [role for role in target.roles if role != ctx.guild.default_role]
            if not roles:
                roles = None
            embed = nextcord.Embed(title="User Information", color=target.top_role.color,
                                   timestamp=datetime.utcnow())
            try:
                embed.set_author(name=target.name, icon_url=target.avatar.url)

                embed.set_thumbnail(url=target.avatar.url)

                embed.set_footer(text=f"Requested by {ctx.author.display_name}",
                                 icon_url=ctx.author.avatar.url)

            except:
                embed.set_author(name=target.name)

                embed.set_footer(text=f"Requested by {ctx.author.display_name}")

            if roles is None:
                fields = [("Name", str(target), False),
                          ("ID", target.id, False),
                          (f"Roles", "No roles", False),
                          ("Created at", f"Created at <t:{str(target.created_at.timestamp()).split('.')[0]}>", False),
                          ("Joined at", f"Joined at <t:{str(target.joined_at.timestamp()).split('.')[0]}>", False)]

            else:
                fields = [("Name", str(target), False),
                          ("ID", target.id, False),
                          (f"Roles ({len(roles)})", " ".join([role.mention for role in roles]), False),
                          ("Created at", f"Created at <t:{str(target.created_at.timestamp()).split('.')[0]}>", False),
                          ("Joined at", f"Joined at <t:{str(target.joined_at.timestamp()).split('.')[0]}>", False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=discord.Embed(title=f'You have to ping someone from this server and this server only',
                                               color=discord.Color.random()))

    @commands.command(aliases=['server', 'sinfo', 'si'])
    @commands.guild_only()
    async def serverinfo(self, ctx):
        format = "%a, %d %b %Y | %H:%M:%S %UTC"
        count = 0
        for member in ctx.guild.members:
            if member.bot:
                count += 1
        embed = nextcord.Embed(
            color=ctx.guild.owner.top_role.color
        )
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        categories = len(ctx.guild.categories)
        channels = text_channels + voice_channels
        try:
            embed.set_thumbnail(url=str(ctx.guild.icon.url))
        except:
            pass
        embed.add_field(name=f"Information About **{ctx.guild.name}**: ",
                        value=f":white_small_square: ID: **{ctx.guild.id}** \n:white_small_square: Owner: **{ctx.guild.owner}** \n:white_small_square: Location: **{str(ctx.guild.region).capitalize()}** \n:white_small_square: Creation: Created on <t:{str(ctx.guild.created_at.timestamp()).split('.')[0]}> \n:white_small_square: Members: **{ctx.guild.member_count}** of which **{count}** members are bots \n:white_small_square: Channels: **{channels}** Channels; **{text_channels}** Text, **{voice_channels}** Voice, **{categories}** Categories \n:white_small_square: Verification: **{str(ctx.guild.verification_level).upper()}** \n:white_small_square: Features: {', '.join(f'**{x}**' for x in ctx.guild.features)} \n:white_small_square: Splash: {ctx.guild.splash}")
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="serverinfo", description="Provides the information about the server")
    async def _serverinfo(self, ctx: SlashContext):
        count = 0
        for member in ctx.guild.members:
            if member.bot:
                count += 1
        embed = nextcord.Embed(
            color=ctx.guild.owner.top_role.color
        )
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        categories = len(ctx.guild.categories)
        channels = text_channels + voice_channels
        try:
            embed.set_thumbnail(url=str(ctx.guild.icon.url))
        except:
            pass
        embed.add_field(name=f"Information About **{ctx.guild.name}**: ",
                        value=f":white_small_square: ID: **{ctx.guild.id}** \n:white_small_square: Owner: **{ctx.guild.owner}** \n:white_small_square: Location: **{str(ctx.guild.region).capitalize()}** \n:white_small_square: Creation: Created on <t:{str(ctx.guild.created_at.timestamp()).split('.')[0]}> \n:white_small_square: Members: **{ctx.guild.member_count}** of which **{count}** members are bots \n:white_small_square: Channels: **{channels}** Channels; **{text_channels}** Text, **{voice_channels}** Voice, **{categories}** Categories \n:white_small_square: Verification: **{str(ctx.guild.verification_level).upper()}** \n:white_small_square: Features: {', '.join(f'**{x}**' for x in ctx.guild.features)} \n:white_small_square: Splash: {ctx.guild.splash}")
        await ctx.send(embed=embed)

    @commands.command(aliases=['robemoji', 'remoji', 'robmo', 'rm'])
    async def robmoji(self, ctx, emoji: nextcord.PartialEmoji, *, name=None):
        if ctx.author.guild_permissions.manage_emojis:
            emoji_url = emoji.url
            if name is None:
                name = emoji.name

            async with aiohttp.ClientSession() as session:
                async with session.get(str(emoji_url)) as response:
                    img = await response.read()
            new_emoji = await ctx.guild.create_custom_emoji(name=name, image=img)
            embed = nextcord.Embed(title="Emoji Added Pog!",
                                   description=f"Name is:\"{name}\", your emoji is {new_emoji}",
                                   color=nextcord.Color.random())
            await ctx.send(embed=embed)

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!",
                                     description="You require to have manage emojis permission!",
                                     color=nextcord.Color.random()))

    """
    @cog_ext.cog_slash(name="robmoji",
                       description="Basically takes an emoji from any server and uploads it in this server so everyone can use it!",
                       options=[create_option(name="emoji",
                                              description="The emoji you want to rob",
                                              option_type=3,
                                              required=True
                                              ),
                                  create_option(name="name",
                                              description="Name of the emoji",
                                              option_type=3,
                                              required=False
                                              )
                                ]
                       )
    async def _robmoji(self, ctx: SlashContext, emoji: nextcord.PartialEmoji, *, name=None):
        if ctx.author.guild_permissions.manage_emojis:
            emoji_url = emoji.url
            if name is None:
                name = emoji.name

            async with aiohttp.ClientSession() as session:
                async with session.get(str(emoji_url)) as response:
                    img = await response.read()
            new_emoji = await ctx.guild.create_custom_emoji(name=name, image=img)
            embed = nextcord.Embed(title="Emoji Added Pog!",
                                   description=f"Name is:\"{name}\", your emoji is {new_emoji}",
                                   color=nextcord.Color.random())
            await ctx.send(embed=embed)

        else:
            await ctx.send(
                embed=nextcord.Embed(title="Stop right there!",
                                     description="You require to have manage emojis permission!",
                                     color=nextcord.Color.random()))"""

    @commands.command(aliases=['n'])
    async def nick(self, ctx, member=None, *, nick=None):
        if member is None and nick is None:
            if ctx.author.guild_permissions.change_nickname:
                await ctx.author.edit(nick=None)
                embed = nextcord.Embed(title=f"Your nickname has been removed",
                                       description=f"Your name is now displayed as {ctx.author.display_name}",
                                       color=nextcord.Color.random())
                await ctx.send(embed=embed)
                return

            else:
                await ctx.send(
                    embed=nextcord.Embed(title="I refuse", description="You require the change nickname permission.",
                                         color=nextcord.Color.random()))
                return

        if member is not None:
            try:
                member = await commands.MemberConverter().convert(ctx, member)
            except:
                pass

        if isinstance(member, str) or (isinstance(member, nextcord.Member) and ctx.author == member):
            if ctx.author.guild_permissions.change_nickname:
                if type(member) is not nextcord.Member:
                    if nick is None:
                        nick = str(member)
                    else:
                        nick = str(member) + " " + nick
                if len(nick) > 48:
                    embed = nextcord.Embed(title=f"That nickname is TOO LONG",
                                           description=f" I'd probably get bored changing it.\nTry a nickname that has less then 32 characters.",
                                           color=nextcord.Color.random())
                    await ctx.send(embed=embed)
                    return
                await ctx.author.edit(nick=nick)
                embed = nextcord.Embed(title=f"Your nickname has been changed",
                                       description=f"Your name is now displayed as {nick}",
                                       color=nextcord.Color.random())
                await ctx.send(embed=embed)
                return
            else:
                await ctx.send(
                    embed=nextcord.Embed(title="I refuse", description="You require the change nickname permission.",
                                         color=nextcord.Color.random()))
                return

        elif isinstance(member, nextcord.Member):
            if ctx.author.guild_permissions.manage_nicknames:
                if nick is None:
                    await member.edit(nick=member.name)
                    embed = nextcord.Embed(title=f"Nickname removed for {member.name}",
                                           description=f"Their name is now displayed as {member.name}",
                                           color=nextcord.Color.random())
                    await ctx.send(embed=embed)
                    return

                elif len(nick) > 48:
                    embed = nextcord.Embed(title=f"That nickname is TOO LONG",
                                           description=f" I'd probably get bored changing it.\nTry a nickname that has less then 48 characters.",
                                           color=nextcord.Color.random())
                    await ctx.send(embed=embed)
                    return

                await member.edit(nick=nick)
                embed = nextcord.Embed(title=f"Nickname changed for {member.name}",
                                       description=f"Their name is now displayed as {nick}",
                                       color=nextcord.Color.random())
                await ctx.send(embed=embed)
                return

            else:
                await ctx.send(
                    embed=nextcord.Embed(title="I refuse", description="You require the manage nicknames permission.",
                                         color=nextcord.Color.random()))


    @cog_ext.cog_slash(name="nick",
                       description="Change nicknames in the server by using this feature",
                       options=[create_option(name="member",
                                              description="The person whose nick you wanna change",
                                              required=False,
                                              option_type=6),
                                create_option(name="nick",
                                              description="The nick you want to change it to",
                                              required=False,
                                              option_type=3)])
    async def _nick(self, ctx: SlashContext, member=None, *, nick=None):
        if member is None and nick is None:
            if ctx.author.guild_permissions.change_nickname:
                await ctx.author.edit(nick=None)
                embed = nextcord.Embed(title=f"Your nickname has been removed",
                                       description=f"Your name is now displayed as {ctx.author.display_name}",
                                       color=nextcord.Color.random())
                await ctx.send(embed=embed)
                return
            else:
                await ctx.send(
                    embed=nextcord.Embed(title="I refuse", description="You require the change nickname permission.",
                                         color=nextcord.Color.random()))
                return

        if member is not None:
            try:
                member = await commands.MemberConverter().convert(ctx, member)
            except:
                pass

        if isinstance(member, str) or (isinstance(member, nextcord.Member) and ctx.author == member):
            if ctx.author.guild_permissions.change_nickname:
                if type(member) is not nextcord.Member:
                    if nick is None:
                        nick = str(member)
                    else:
                        nick = str(member) + " " + nick
                if len(nick) > 48:
                    embed = nextcord.Embed(title=f"That nickname is TOO LONG",
                                           description=f" I'd probably get bored changing it.\nTry a nickname that has less then 32 characters.",
                                           color=nextcord.Color.random())
                    await ctx.send(embed=embed)
                    return
                await ctx.author.edit(nick=nick)
                embed = nextcord.Embed(title=f"Your nickname has been changed",
                                       description=f"Your name is now displayed as {nick}",
                                       color=nextcord.Color.random())
                await ctx.send(embed=embed)
                return
            else:
                await ctx.send(
                    embed=nextcord.Embed(title="I refuse", description="You require the change nickname permission.",
                                         color=nextcord.Color.random()))
                return

        elif isinstance(member, nextcord.Member):
            if ctx.author.guild_permissions.manage_nicknames:
                if nick is None:
                    await member.edit(nick=member.name)
                    embed = nextcord.Embed(title=f"Nickname removed for {member.name}",
                                           description=f"Their name is now displayed as {member.name}",
                                           color=nextcord.Color.random())
                    await ctx.send(embed=embed)
                    return

                elif len(nick) > 48:
                    embed = nextcord.Embed(title=f"That nickname is TOO LONG",
                                           description=f" I'd probably get bored changing it.\nTry a nickname that has less then 48 characters.",
                                           color=nextcord.Color.random())
                    await ctx.send(embed=embed)
                    return

                await member.edit(nick=nick)
                embed = nextcord.Embed(title=f"Nickname changed for {member.name}",
                                       description=f"Their name is now displayed as {nick}",
                                       color=nextcord.Color.random())
                await ctx.send(embed=embed)
                return

            else:
                await ctx.send(
                    embed=nextcord.Embed(title="I refuse", description="You require the manage nicknames permission.",
                                         color=nextcord.Color.random()))

    @commands.command()
    async def afk(self, ctx, *, reason=None):
        if reason is None:
            embed = nextcord.Embed(title="Give ME A REASON",
                                   description="You can't be afk for no reason",
                                   color=nextcord.Color.random())
            embed.set_footer(text="That's Louis' job")
            await ctx.send(embed=embed)
            return

        if len(reason) > 50:
            embed = nextcord.Embed(title="I'm sorry.",
                                   description="I got bored reading your LONG reason.\nSo I ignored it.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Nothing more than 50 characters please")
            await ctx.send(embed=embed)
            return

        db = TinyDB('databases/afk.json')
        db.insert({'afk_user': ctx.author.id, 'reason': reason})

        await ctx.send(embed=nextcord.Embed(title=f"Ok {ctx.author.display_name}.",
                                            description=f"I have set your status as afk for {reason}.",
                                            color=nextcord.Color.random()))

    @cog_ext.cog_slash(name="afk",
                       description="Shows your friends that you are afk for some reason.",
                       options=[
                           create_option(name="reason",
                                         description="The reason which people see when they @you",
                                         required=True,
                                         option_type=3)
                       ])
    async def _afk(self, ctx: SlashContext, *, reason=None):
        if reason is None:
            embed = nextcord.Embed(title="Give ME A REASON",
                                   description="You can't be afk for no reason!",
                                   color=nextcord.Color.random())
            embed.set_footer(text="That's Louis' job")
            await ctx.send(embed=embed)
            return

        if len(reason) > 50:
            embed = nextcord.Embed(title="I'm sorry.",
                                   description="I got bored reading your LONG reason.\nSo I ignored it.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Nothing more than 50 characters please")
            await ctx.send(embed=embed)
            return

        db = TinyDB('databases/afk.json')
        db.insert({'afk_user': ctx.author.id, 'reason': reason})

        await ctx.send(embed=nextcord.Embed(title=f"Ok {ctx.author.display_name}.",
                                            description=f"I have set your status as afk for {reason}.",
                                            color=nextcord.Color.random()))

    @commands.command(aliases=['remind'])
    async def reminder(self, ctx, duration, *, reminder):
        embed = nextcord.Embed(color=0x55a7f7, timestamp=datetime.utcnow())
        seconds = 0
        if reminder is None:
            embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.')
        if duration.lower().endswith("d"):
            seconds += int(duration[:-1]) * 60 * 60 * 24
            counter = f"{seconds // 60 // 60 // 24} days"
        if duration.lower().endswith("h"):
            seconds += int(duration[:-1]) * 60 * 60
            counter = f"{seconds // 60 // 60} hours"
        elif duration.lower().endswith("m"):
            seconds += int(duration[:-1]) * 60
            counter = f"{seconds // 60} minutes"
        elif duration.lower().endswith("s"):
            seconds += int(duration[:-1])
            counter = f"{seconds} seconds"

        if len(reminder) > 200:
            embed = nextcord.Embed(title="I'm sorry.",
                                   description="I got bored reading your LONG reason.\nSo I ignored it.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Nothing more than 200 characters please")
            await ctx.send(embed=embed)
            return

        elif seconds == 0:
            embed.add_field(name='Warning',
                            value='Please specify a proper duration')

        elif seconds < 120:
            embed.add_field(name='Warning',
                            value='You have specified too short a duration!\nMinimum duration is 2 minutes.')

        elif seconds > 7776000:
            embed.add_field(name='Warning',
                            value='You have specified too long a duration!\nMaximum duration is 90 days.')

        else:
            await ctx.send(embed=nextcord.Embed(title=f"I wish I had a title for this embed",
                                                description=f"But I will remind you about {reminder} in {counter}.",
                                                color=nextcord.Color.random()))
            await asyncio.sleep(seconds)
            await ctx.send(f"{ctx.author.mention} Hi, you asked me to remind you to \"{reminder}\" {counter} ago.")
            return

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="reminder", description="Reminds you to do something after sometime...", options=[
        create_option(name="duration", description="Time for reminder(Eg: 1h or 5m)", required=True,
                      option_type=3),
        create_option(name="reminder", description="What you wanted to be reminded about", required=True,
                      option_type=3)
    ])
    async def _reminder(self, ctx: SlashContext, duration, *, reminder):
        embed = nextcord.Embed(color=0x55a7f7, timestamp=datetime.utcnow())
        seconds = 0
        if reminder is None:
            embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.')
        if duration.lower().endswith("d"):
            seconds += int(duration[:-1]) * 60 * 60 * 24
            counter = f"{seconds // 60 // 60 // 24} days"
        if duration.lower().endswith("h"):
            seconds += int(duration[:-1]) * 60 * 60
            counter = f"{seconds // 60 // 60} hours"
        elif duration.lower().endswith("m"):
            seconds += int(duration[:-1]) * 60
            counter = f"{seconds // 60} minutes"
        elif duration.lower().endswith("s"):
            seconds += int(duration[:-1])
            counter = f"{seconds} seconds"

        if len(reminder) > 200:
            embed = nextcord.Embed(title="I'm sorry.",
                                   description="I got bored reading your LONG reason.\nSo I ignored it.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Nothing more than 200 characters please")
            await ctx.send(embed=embed)
            return

        elif seconds == 0:
            embed.add_field(name='Warning',
                            value='Please specify a proper duration')

        elif seconds < 120:
            embed.add_field(name='Warning',
                            value='You have specified too short a duration!\nMinimum duration is 2 minutes.')

        elif seconds > 7776000:
            embed.add_field(name='Warning',
                            value='You have specified too long a duration!\nMaximum duration is 90 days.')

        else:
            await ctx.send(embed=nextcord.Embed(title=f"I wish I had a title for this embed",
                                                description=f"But I will remind you about {reminder} in {counter}.",
                                                color=nextcord.Color.random()))
            await asyncio.sleep(seconds)
            await ctx.send(f"{ctx.author.mention} Hi, you asked me to remind you to \"{reminder}\" {counter} ago.")
            return

        await ctx.send(embed=embed)

    @commands.command(aliases=['sf'])
    async def snowflake(self, ctx, user_id: int):
        created = nextcord.utils.snowflake_time(user_id)
        await ctx.send(embed=nextcord.Embed(title=f"ID {user_id}",
                                            description=f"Was created on <t:{str(created.timestamp()).split('.')[0]}>",
                                            color=nextcord.Color.random()))

    @cog_ext.cog_slash(name="snowflake", description="Find out the creation date of ANYTHING with its ID", options=[
        create_option(name="user_id", description="The ID which im supposed to find creation date of", required=True,
                      option_type=3)
    ])
    async def _snowflake(self, ctx: SlashContext, user_id):
        created = nextcord.utils.snowflake_time(int(user_id))
        await ctx.send(embed=nextcord.Embed(title=f"ID {user_id}",
                                            description=f"Was created on <t:{str(created.timestamp()).split('.')[0]}>",
                                            color=nextcord.Color.random()))

    """@commands.command(aliases=['ab'])
    async def about(self, ctx):
        about_embed = nextcord.Embed(title="About ME!", color=nextcord.Color.green())
        about_embed.add_field(name="Bot Developed by:", value=f"ZeroAndOne, [My epic devs!](https://zeroandone.ml)")
        about_embed.add_field(name="Created to:", value=f"Make discord a better place. :angel:")
        about_embed.add_field(name="Features:", value=f"Use {ctx.prefix}help", inline=True)
        about_embed.add_field(
            name="Give me feedback and complains here. Help me improve myself!\nAlso useful for finding out about the latest Chad updates!!",
            value=f"[Support Server](https://discord.gg/wTsj4DZhyZ)", inline=True)
        about_embed.add_field(name="Vote for me and make me POPULAR!!",
                              value=f"[I'm on top.gg](https://top.gg/bot/864010316424806451/vote)", inline=True)
        user = self.bot.get_user(864010316424806451)
        about_embed.add_field(name="Vote for me here too!",
                              value=f"[I'm on the Discord Bot List](https://discordbotlist.com/bots/chad-6621/upvote)",
                              inline=True)
        about_embed.set_thumbnail(url=user.avatar.url)
        await ctx.send(embed=about_embed)

    @cog_ext.cog_slash(name="about", description="Tells you something more about ME!")
    async def _about(self, ctx: SlashContext):
        about_embed = nextcord.Embed(title="About ME!", color=nextcord.Color.green())
        about_embed.add_field(name="Bot Developed by:", value=f"ZeroAndOne, [My epic devs!](https://zeroandone.ml)")
        about_embed.add_field(name="Created to:", value=f"Make discord a better place. :angel:")
        about_embed.add_field(name="Features:", value=f"Use /help", inline=True)
        about_embed.add_field(
            name="Give me feedback and complains here. Help me improve myself!\nAlso useful for finding out about the latest Chad updates!!",
            value=f"[Support Server](https://discord.gg/wTsj4DZhyZ)", inline=True)
        about_embed.add_field(name="Vote for me and make me POPULAR!!",
                              value=f"[I'm on top.gg](https://top.gg/bot/864010316424806451/vote)", inline=True)
        user = self.bot.get_user(864010316424806451)
        about_embed.add_field(name="Vote for me here too!",
                              value=f"[I'm on the Discord Bot List](https://discordbotlist.com/bots/chad-6621/upvote)",
                              inline=True)
        about_embed.set_thumbnail(url=user.avatar.url)
        await ctx.send(embed=about_embed)

    @commands.command(aliases=['v'])
    async def vote(self, ctx):
        vote = nextcord.Embed(title="Vote for me buckaroo!", color=nextcord.Color.random())
        vote.add_field(name="1", value=f"[top.gg](https://top.gg/bot/864010316424806451/vote)")
        vote.add_field(name="2", value=f"[discordbotlist.com](https://discordbotlist.com/bots/chad-6621/upvote)")
        vote.set_thumbnail(url="https://i.imgur.com/QICgRpf.png")
        await ctx.send(embed=vote)

    @cog_ext.cog_slash(name="vote", description="Gives link to vote for me!")
    async def _vote(self, ctx: SlashContext):
        vote = nextcord.Embed(title="Vote for me buckaroo!", color=nextcord.Color.random())
        vote.add_field(name="1", value=f"[top.gg](https://top.gg/bot/864010316424806451/vote)")
        vote.add_field(name="2", value=f"[discordbotlist.com](https://discordbotlist.com/bots/chad-6621/upvote)")
        vote.set_thumbnail(url="https://i.imgur.com/QICgRpf.png")
        await ctx.send(embed=vote)"""

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.bot.sniped_messages[message.guild.id] = (
            message.content, message.author, message.channel.name, message.created_at)

    """@commands.command(aliases=['inv'])
    async def invite(self, ctx):
        embed = nextcord.Embed(
            title="Invite",
            description=f"To invite me to your own server [click here](https://discord.com/api/oauth2/authorize?client_id=864010316424806451&permissions=9600003159&scope=applications.commands%20bot)")

        embed.set_footer(text="Invite requested by: {}".format(ctx.author.display_name))
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.color = nextcord.Color.green()
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="invite", description="Gives you the link to invite me to your servers!")
    async def _invite(self, ctx: SlashContext):
        embed = nextcord.Embed(
            title="Invite",
            description=f"To invite me to your own server [click here](https://discord.com/api/oauth2/authorize?client_id=864010316424806451&permissions=9600003159&scope=applications.commands%20bot)")

        embed.set_footer(text="Invite requested by: {}".format(ctx.author.display_name))
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.color = nextcord.Color.green()
        await ctx.send(embed=embed)

    @commands.command(aliases=['sup'])
    async def support(self, ctx):
        embed = nextcord.Embed(title="Support Server",
                               description="To visit our support server, click [here](https://discord.gg/wTsj4DZhyZ).\nNow you can see the latest updates!!",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Support Server requested by {ctx.author.name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="support", description="Gives you link for support server")
    async def _support(self, ctx: SlashContext):
        embed = nextcord.Embed(title="Support Server",
                               description="To visit our support server, click [here](https://discord.gg/wTsj4DZhyZ).\nNow you can see the latest updates!!",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Support Server requested by {ctx.author.name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 3600, commands.cooldowns.BucketType.user)
    @commands.command(aliases=['suggestion', 'sug'])
    async def suggest(self, ctx, *, suggestion=None):
        if suggestion is None:
            embed = nextcord.Embed(title=f"We are open to suggestions",
                                   description=f"This, however, does not mean we can use empty suggestions",
                                   color=nextcord.Color.random())
            embed.set_footer(text=f"So try not to do that...")
            await ctx.channel.send(embed=embed)
            return

        elif len(suggestion) > 768:
            embed = nextcord.Embed(title=f"A suggestion can only be of 768 characters or less",
                                   description=f"This is two prevent random wierdos from spamming our suggestions channel",
                                   color=nextcord.Color.random())
            embed.set_footer(text=f"I wish people weren't that evil sometimes")
            await ctx.channel.send(embed=embed)
            return
        channel = self.bot.get_channel(869173309865070592)
        embed = nextcord.Embed(title=f"Suggestion from {ctx.guild.name}",
                               description=f"{suggestion}",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"-by {ctx.author}")
        await channel.send(embed=embed)
        embed = nextcord.Embed(title=f"Your suggestion has been received",
                               description=f"The devs has seen `{suggestion}` as your suggestion!",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Thank you for your response")
        await ctx.send(embed=embed)

    @commands.cooldown(1, 3600, commands.cooldowns.BucketType.user)
    @commands.command(aliases=['complaint', 'comp'])
    async def complain(self, ctx, *, complaint=None):
        if complaint is None:
            embed = nextcord.Embed(title=f"We are open to complaints",
                                   description=f"This, however, does not mean we can use empty complaints",
                                   color=nextcord.Color.random())
            embed.set_footer(text=f"So try not to do that...")
            await ctx.channel.send(embed=embed)
            return

        elif len(complaint) > 768:
            embed = nextcord.Embed(title=f"A complaint can only be of 768 characters or less",
                                   description=f"This is two prevent random wierdos from spamming our complaints channel",
                                   color=nextcord.Color.random())
            embed.set_footer(text=f"I wish people weren't that evil sometimes")
            await ctx.channel.send(embed=embed)
            return
        channel = self.bot.get_channel(869173386465673226)
        embed = nextcord.Embed(title=f"Complaint from {ctx.guild.name}",
                               description=f"{complaint}",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"-by {ctx.author}")
        await channel.send(embed=embed)
        embed = nextcord.Embed(title=f"Your complaint has been received",
                               description=f"The devs has seen `{complaint}` as your suggestion!",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Thank you for your response")
        await ctx.send(embed=embed)

    @commands.command(aliases=['web', 'site', 'www', 'zo'])
    async def website(self, ctx):
        embed = nextcord.Embed(title="Link for our website",
                               color=nextcord.Color.dark_magenta(),
                               description="This is our main [website](https://zeroandone.netlify.app/)\nClick [here](https://www.youtube.com/channel/UCF0DZYNiHcIGZKBoPWfc0lg) to see our YouTube Channel.")
        embed.set_footer(text=f"Website requested by {ctx.author.name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="website", description="Takes you to my devs' website!")
    async def _website(self, ctx: SlashContext):
        embed = nextcord.Embed(title="Link for our website",
                               color=nextcord.Color.dark_magenta(),
                               description="This is our main [website](https://zeroandone.netlify.app/)\nClick [here](https://www.youtube.com/channel/UCF0DZYNiHcIGZKBoPWfc0lg) to see our YouTube Channel.")
        embed.set_footer(text=f"Website requested by {ctx.author.name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['pat', 'donate'])
    async def patreon(self, ctx):
        embed = nextcord.Embed(title="Here is our patreon.",
                               description="Donate to us [here](https://www.patreon.com/TheChadBot) to show your love for Chad!",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Patreon requested by {ctx.author.name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="donate", description="Gives you the Patreon link so u can donate to my cause!")
    async def _donate(self, ctx: SlashContext):
        embed = nextcord.Embed(title="Here is our patreon.",
                               description="Donate to us [here](https://www.patreon.com/TheChadBot) to show your love for Chad!",
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Patreon requested by {ctx.author.name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)"""

    @cog_ext.cog_slash(name="serverlink", description="Use this to make me create an invite link to your server!")
    async def _serverlink(self, ctx: SlashContext):
        link = await ctx.channel.create_invite()
        embed = nextcord.Embed(title="Here's a link for your server.",
                               description=link,
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Server link requested by {ctx.author.name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['sl'])
    async def serverlink(self, ctx):
        link = await ctx.channel.create_invite()
        embed = nextcord.Embed(title="Here's a link for your server.",
                               description=link,
                               color=nextcord.Color.random())
        embed.set_footer(text=f"Server link requested by {ctx.author.name}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.channel)
    @commands.command(aliases=['sn'])
    async def snipe(self, ctx):
        try:
            contents, author, channel_name, duration = self.bot.sniped_messages[ctx.guild.id]

        except:
            await ctx.send(
                embed=nextcord.Embed(title="Couldn't find a message to snipe!", color=nextcord.Color.random()))
            return

        embed = nextcord.Embed(description=contents, color=nextcord.Color.random(), timestamp=duration)
        try:
            embed.set_author(
                name=f"{author.name}#{author.discriminator} has been head-shotted by our glorious snipe command",
                icon_url=author.avatar.url)
        except:
            embed.set_author(
                name=f"{author.name}#{author.discriminator} has been head-shotted by our glorious snipe command")
        embed.set_footer(text=f"Deleted in : #{channel_name} Sniper: {ctx.author.display_name}")

        await ctx.channel.send(embed=embed)

    @cog_ext.cog_slash(name="Snipe", description="Find out what the last deleted message in your server was.")
    async def _snipe(self, ctx: SlashContext):
        try:
            contents, author, channel_name, duration = self.bot.sniped_messages[ctx.guild.id]

        except:
            await ctx.send(
                embed=nextcord.Embed(title="Couldn't find a message to snipe!", color=nextcord.Color.random()))
            return

        embed = nextcord.Embed(description=contents, color=nextcord.Color.random(), timestamp=duration)
        try:
            embed.set_author(
                name=f"{author.name}#{author.discriminator} has been head-shotted by our glorious snipe command",
                icon_url=author.avatar.url)
        except:
            embed.set_author(
                name=f"{author.name}#{author.discriminator} has been head-shotted by our glorious snipe command")
        embed.set_footer(text=f"Deleted in : #{channel_name} Sniper: {ctx.author.display_name}")
        await ctx.send(embed=embed)

    """@robmoji.error
    async def robmoji_error(self, ctx, error):
        member = ctx.author
        membervar = member.display_name
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=nextcord.Embed(title="You're kidding right?",
                                                description=f"{membervar} Please mention an emoji to steal\n That way, I won't need to steal thin air!!",
                                                color=nextcord.Color.random()))

        elif isinstance(error, commands.errors.PartialEmojiConversionFailure):
            error = getattr(error, "original", error)
            the_error_arg = error.argument
            embed = nextcord.Embed(title="Whoops",
                                   description=f"Could not convert {the_error_arg} to an emoji",
                                   color=nextcord.Color.random())
            embed.set_footer(
                text="If this is not you being dumb and a genuine error in the code, let us know [here](https://discord.gg/TeRyp9JWbg)")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(embed=nextcord.Embed(title="You're kidding right?",
                                                description=f"{membervar} give it a name from 2 to 32 characters **ONLY**\nAnd NO SPACES PLS \n this is an emoji name not a train",
                                                color=nextcord.Color.random()))

        else:
            raise error"""

    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed = nextcord.Embed(title="Did you know...",
                                   description="That it is an EXCELLENT idea to actually gime me a person who exists and not use your non existant brain to make up an imaginary person!!",
                                   color=nextcord.Color.random())
            embed.set_footer(text="I mean, common sense people")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title="At least try to...",
                                   description="Wish you'd actually try to tell me who to get info from.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Sigh")
            await ctx.send(embed=embed)

        else:
            raise error

    @makerole.error
    async def make_role_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title="Hmmmm...",
                                   description="Why haven't you mentioned the NAME OF THE ROLE YOU WANT TO CREATE\nA role with the name ___ is pretty stupid.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Think about it")
            await ctx.send(embed=embed)

        else:
            raise error

    @addrole.error
    async def add_role_error(self, ctx, error):
        member = ctx.author
        member_var = member.display_name

        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title="How do you do these things...",
                                   description="You gotta mention both the user and the role.\nI can't just randomly place roles!",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Not in my job description")
            await ctx.send(embed=embed)

        elif isinstance(error, nextcord.errors.Forbidden):
            embed = nextcord.Embed(title="I can't do that!",
                                   description=f"{member_var} you will have to place my role above that role.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="It is a necessity")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MemberNotFound):
            embed = nextcord.Embed(title="I couldn't find this member",
                                   description="How have you tried to add roles to someone not in the server??",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Common sense just ain't common anymore...")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.RoleNotFound):
            embed = nextcord.Embed(title="I didn't find this role.",
                                   description=f"Apparently this role doesn't even EXIST in your server.\nTry making the role with {ctx.prefix}makerole first.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="That would be great")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.errors.CommandInvokeError):
            embed = nextcord.Embed(title="I can't do that!",
                                   description=f"{member_var} you will have to place my role above that role.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="It is a necessity")
            await ctx.send(embed=embed)

        else:
            raise error

    @editrole.error
    async def edit_error(self, ctx, error):
        member = ctx.author
        member_var = member.display_name

        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title="I didn't find this role.",
                                   description=f"{member_var} please mention the role to edit **AND** the new name or color.",
                                   color=nextcord.Color.random())
            embed.set_footer(
                text="Imagine being able to write bot commands properly...")
            await ctx.send(embed=embed)

        elif isinstance(error, nextcord.errors.Forbidden):
            embed = nextcord.Embed(title="I can't do that!",
                                   description=f"{member_var} you will have to place my role above that role.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="It is a necessity")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.RoleNotFound):
            embed = nextcord.Embed(title="I didn't find this role.",
                                   description=f"{member_var} Mentioning a valid role couldn't HURT you know...",
                                   color=nextcord.Color.random())
            embed.set_footer(text="The validity check never ends...")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.errors.CommandInvokeError):
            embed = nextcord.Embed(title="I can't do that!",
                                   description=f"{member_var} you will have to place my role above that role.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="It is a necessity")
            await ctx.send(embed=embed)

        else:
            raise error

    @removerole.error
    async def remove_role_error(self, ctx, error):
        member = ctx.author
        member_var = member.name

        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title="I didn't find this role. (Again...)",
                                   description=f"{member_var} please mention the role to remove.(Again)",
                                   color=nextcord.Color.random())
            embed.set_footer(
                text="Imagine being able to write bot commands properly... (Again...)")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.RoleNotFound):
            embed = nextcord.Embed(title="I didn't find this role.",
                                   description=f"{member_var} Mentioning a valid role couldn't HURT you know...\nBut its sad I gotta repeat stuff I said be4.\n Didn't you guys see this is in the mistake of role edits?",
                                   color=nextcord.Color.random())
            embed.set_footer(text="Once again, the validity check never ends...")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MemberNotFound):
            embed = nextcord.Embed(title="That username... is not in this server?",
                                   description=f"{member_var} I didn't find this so-called user name you mentioned.",
                                   color=nextcord.Color.random())
            embed.set_footer(
                text="I can only remove the role of people who exist in the server.")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.errors.CommandInvokeError):
            embed = nextcord.Embed(title="I do not have the permission!",
                                   description=f"{member_var} my place is currently BELOW that role.\nTry placing me above.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="It is a necessity")
            await ctx.send(embed=embed)

        else:
            raise error

    @deleterole.error
    async def delete_role_error(self, ctx, error):
        member = ctx.author

        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(title="Ok cool",
                                   description=f"**Intense Concentration** There!\nI have deleted a non-existent role.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="No need to thank me...")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.RoleNotFound):
            embed = nextcord.Embed(title=f"Dear {member.name}",
                                   description=f"I assure you that I will do my best to delete a role that I couldn't find in this server.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="I exist to serve")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.errors.CommandInvokeError):
            embed = nextcord.Embed(title="I do not have the permission!",
                                   description=f"{member.name} my place is currently BELOW that role.\nTry placing me above.",
                                   color=nextcord.Color.random())
            embed.set_footer(text="It is a necessity")
            await ctx.send(embed=embed)

        else:
            raise error

    @nick.error
    async def nick_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            embed = nextcord.Embed(title=f"Nope, the member is more powerful than me",
                                   description=f"Maybe put my role above him :pleading_face:",
                                   color=nextcord.Color.random())
            embed.set_footer(text="I feel weak")
            await ctx.send(embed=embed)

        raise error

    @reminder.error
    async def rem_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=nextcord.Embed(title=f"{ctx.author.display_name} please give me time and the thing i have to remind you for",
                                                description=f"PLEASE? DO I REALLY HAVE TO ASK IN THE FIRST PLACE?",
                                                color=nextcord.Color.random()))

        elif isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(embed=nextcord.Embed(title=f"{ctx.author.display_name} That is an invalid time",
                                                color=nextcord.Color.random()))

        else:
            raise error

    @_snowflake.error
    async def snowflake_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(embed=nextcord.Embed(title="The given ID **NOTHING**",
                                                description="Was never created.",
                                                color=nextcord.Color.random()))
        elif isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(embed=nextcord.Embed(title="Pls gimme a valid ID man",
                                                description="Why you do tht to me\n \nMy friend David lost his ID... Now we call him Dav",
                                                color=nextcord.Color.random()))
        else:
            raise error

    @_snowflake.error
    async def snowflake_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(embed=nextcord.Embed(title="The given ID **NOTHING**",
                                                description="Was never created.",
                                                color=nextcord.Color.random()))
        elif isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(embed=nextcord.Embed(title="Pls gimme a valid ID man",
                                                description="Why you do tht to me\n \nMy friend David lost his ID... Now we call him Dav",
                                                color=nextcord.Color.random()))
        else:
            raise error

    """@suggest.error
    async def suggest_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=nextcord.Embed(title=f"Slow down bro. Try after {round(error.retry_after)} seconds",
                                                description=f"We have a one hour cooldown per user",
                                                color=nextcord.Color.random()))

        else:
            raise error

    @complain.error
    async def complain_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=nextcord.Embed(title=f"Slow down bro. Try after {round(error.retry_after)} seconds",
                                                description=f"We have a one hour cooldown per user",
                                                color=nextcord.Color.random()))

        else:
            raise error"""

    @snipe.error
    async def sn_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=nextcord.Embed(title=f"Slow down bro. Try after {round(error.retry_after)} seconds",
                                                color=nextcord.Color.random()))

        else:
            raise error


def setup(bot):
    bot.add_cog(Utils(bot))
