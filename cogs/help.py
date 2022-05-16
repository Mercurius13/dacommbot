import nextcord
import asyncio
from nextcord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.utils.manage_components import wait_for_component


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="help",
                       description="Get help. From me of course.",
                       options=[
                           create_option(name="about",
                                         description="The thing I should help you with.",
                                         option_type=3,
                                         required=False
                                         )
                       ])
    async def _help(self, ctx: SlashContext, about=None):
        if about is None:
            embed = nextcord.Embed(title="Help", color=nextcord.Color.random())
            embed.add_field(name="Utilities",
                            value=f"`/help utilities`",
                            inline=True)
            embed.add_field(name="Moderation",
                            value=f"`/help moderation`",
                            inline=True)
            embed.add_field(name="Information",
                            value=f"`/help information`",
                            inline=True)
            embed.add_field(name="Nerd",
                            value=f"`/help nerd`",
                            inline=True)
            embed.add_field(name="Fun", value=f"`/help fun`", inline=True)
            embed.add_field(name="Games", value=f"`/help games`", inline=True)
            embed.add_field(
                name=f"Most Important Commands",
                value=f"Prefix:\n/help prefix\n\nInvite to other servers:\n/help invite\n\nSupport Server:\n/help support\n\nDonations:\n/help patreon",
                inline=False)
            embed.set_thumbnail(url=ctx.author.avatar.url)
            embed.set_footer(text=f"Ping me if u want to know your server prefix!")
            await ctx.send(embed=embed)
            return

        elif about.lower() == "utilities" or about.lower() == "utils":
            page = 1
            pages = 4
            help_utils_1 = nextcord.Embed(title="Utilities")
            help_utils_1.add_field(
                name="Ping",
                value=f"This allows you to check my ping.\n/help ping")
            help_utils_1.add_field(
                name="MakeRole",
                value=f"Makes a new role in the server for you.\n/help makerole",
                inline=False)
            help_utils_1.add_field(
                name="AddRole",
                value=f"Gives a chosen user the required role.\n/help addrole",
                inline=False)
            help_utils_1.add_field(
                name="EditRole",
                value=f"Edits an existing role in the server.\n/help editrole",
                inline=False)
            help_utils_1.add_field(
                name="RemoveRole",
                value=f"Takes away the required role from a chosen user.\n/help removerole",
                inline=False)
            help_utils_1.add_field(
                name="DeleteRole",
                value=f"Takes away the required role from a chosen user.\n/help deleterole",
                inline=False)
            help_utils_1.set_footer(text="Page 1 of 4")
            help_utils_1.color = nextcord.Color.random()

            help_utils_2 = nextcord.Embed(title="Utilities")
            help_utils_2.add_field(
                name="UserInfo",
                value=f"Gives some information about the member specified...\n/help userinfo",
                inline=False)
            help_utils_2.add_field(
                name="ServerInfo",
                value=f"Provides some information about the server.\n/help serverinfo",
                inline=False)
            help_utils_2.add_field(
                name="Robmoji",
                value=f"Robs an emoji! Takes an emoji from any other server and uploads it your own server so everyone else can use it!\n/help robmoji",
                inline=False)
            help_utils_2.add_field(
                name="Nick",
                value=f"Change nicknames in the server by using this feature.\n/help nick",
                inline=False)
            help_utils_2.add_field(
                name="Afk",
                value=f"Shows other people you are afk for some random reason.\n/help afk",
                inline=False)
            help_utils_2.set_footer(text="Page 2 of 4")
            help_utils_2.color = nextcord.Color.random()

            help_utils_3 = nextcord.Embed(title="Utilities")
            help_utils_3.add_field(
                name="Reminder",
                value=f"Remind yourself to do something at a certain time.\n/help remind",
                inline=False)
            help_utils_3.add_field(
                name="Snipe",
                value=f"Allows you to restore the last deleted message of the channel.\n/help snipe",
                inline=False)
            help_utils_3.add_field(
                name="Snowflake",
                value=f"Find out the creation date of ANYTHING with its ID.",
                inline=False)
            help_utils_3.add_field(
                name="About",
                value=f"Tells you more about ME! Totally not conceited.\n/help about",
                inline=False)
            help_utils_3.add_field(
                name="Vote",
                value=f"Alows you to vote for me!\n/help vote",
                inline=False)
            help_utils_3.add_field(
                name="Invite",
                value=f"Helps you invite me to your other servers.\n/help invite",
                inline=False)
            help_utils_3.set_footer(text="Page 3 of 4")
            help_utils_3.color = nextcord.Color.random()

            help_utils_4 = nextcord.Embed(title="Utilities")
            help_utils_4.add_field(
                name="ServerLink",
                value=f"Use this to get an invite link for this server!\n/help serverlink",
                inline=False)
            help_utils_4.add_field(
                name="Suggest",
                value=f"Allows you to make a suggestion on my working.\n/help suggest",
                inline=False)
            help_utils_4.add_field(
                name="Complain",
                value=f"Allows you to complain about my working.\n/help complain",
                inline=False)
            help_utils_4.add_field(
                name="Website",
                value=f"Takes you to my devs' website!\n/help website",
                inline=False)
            help_utils_4.add_field(
                name="Patreon",
                value=f"Gives you my Patreon link so you can donate to my cause!\n/help patreon",
                inline=False)
            help_utils_4.set_footer(text="Page 4 of 4")
            help_utils_4.color = nextcord.Color.random()

            buttons = [
                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                              disabled=False),
                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                              disabled=False),
            ]
            action_row = create_actionrow(*buttons)

            util_message = await ctx.send(embed=help_utils_1, components=[action_row])

            while True:
                try:
                    response: ComponentContext = await wait_for_component(self.bot, messages=util_message,
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
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row = create_actionrow(*buttons_left_disabled)
                            await response.edit_origin(embed=help_utils_1, components=[action_row])

                        except:
                            pass

                    elif page == 2:
                        try:
                            buttons_normal = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row2 = create_actionrow(*buttons_normal)
                            await response.edit_origin(embed=help_utils_2, components=[action_row2])

                        except:
                            pass
                    elif page == 3:
                        try:
                            buttons_normal = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row3 = create_actionrow(*buttons_normal)
                            await response.edit_origin(embed=help_utils_3, components=[action_row3])

                        except:
                            pass
                    elif page == 4:
                        try:
                            buttons_right_disabled = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=True),
                            ]
                            action_row4 = create_actionrow(*buttons_right_disabled)
                            await response.edit_origin(embed=help_utils_4, components=[action_row4])

                        except:
                            pass
                    pass
                except asyncio.TimeoutError:
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=util_message)
                    buttons_all_disabled = [
                        create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                      disabled=True),
                    ]
                    action_row = create_actionrow(*buttons_all_disabled)
                    await response.edit_origin(components=[action_row])

        elif about.lower() == "moderation" or about.lower() == "mod":
            page = 1
            pages = 3
            help_mod_1 = nextcord.Embed(title="Moderation")
            help_mod_1.add_field(
                name="Prefix",
                value=f"Shows you my prefix in this server and allows you to change it.\n/help prefix",
                inline=False)
            help_mod_1.add_field(
                name="Slowmode",
                value=f"Allows moderators to enable/disable slowmode.\n/help slowmode",
                inline=False)
            help_mod_1.add_field(
                name="Blacklist",
                value=f"Blacklists a user.\n/help blacklist",
                inline=False)
            help_mod_1.add_field(
                name="Unblacklist",
                value=f"Unblacklists a user.\n/help unblacklist",
                inline=False)
            help_mod_1.add_field(
                name="Clear",
                value=f"Clears messages in a channel.\n/help clear",
                inline=False)
            help_mod_1.set_footer(text="Page 1 of 3")
            help_mod_1.color = nextcord.Color.random()

            help_mod_2 = nextcord.Embed(title="Moderation")
            help_mod_2.add_field(
                name="Warn",
                value=f"Gives a warning to a user. Better use coming soon!\n/help warn",
                inline=False)
            help_mod_2.add_field(
                name="UserWarn",
                value=f"Displays the history of warnings given to a user.\n/help userwarn",
                inline=False)
            help_mod_2.add_field(
                name="RemoveWarn",
                value=f"Removes one of, or all of, the warnings given to a user.\n/help removewarn",
                inline=False)
            help_mod_2.add_field(
                name="Unmute",
                value=f"Unmutes a user, thus allowing then to type.\n/help unmute",
                inline=False)
            help_mod_2.add_field(
                name="Tempmute",
                value=f"Stops the user from typing in the server TEMPORARILY.\n/help tempmute",
                inline=False)
            help_mod_2.add_field(
                name="Mute",
                value=f"Stops the user from typing in the server PERMANENTLY (or until unmute).\n/help mute",
                inline=False)
            help_mod_2.set_footer(text="Page 2 of 3")
            help_mod_2.color = nextcord.Color.random()

            help_mod_3 = nextcord.Embed(title="Moderation")
            help_mod_3.add_field(
                name="Kick",
                value=f"Kicks the specified user from the server.\n/help kick",
                inline=False)
            help_mod_3.add_field(
                name="Unban",
                value=f"Unbans users, obviously.\n/help unban",
                inline=False)
            help_mod_3.add_field(
                name="Tempban",
                value=f"Bans users, TEMPORARILY.\n/help tempban",
                inline=False)
            help_mod_3.add_field(
                name="Ban",
                value=f"Bans users, like, DUH.\n/help ban",
                inline=False)
            help_mod_3.set_footer(text="Page 3 of 3")
            help_mod_3.color = nextcord.Color.random()

            buttons = [
                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                              disabled=False),
                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                              disabled=False),
            ]
            action_row = create_actionrow(*buttons)

            mod_message = await ctx.send(embed=help_mod_1, components=[action_row])

            while True:
                try:
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=mod_message, timeout=300)
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
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row = create_actionrow(*buttons_left_disabled)
                            await response.edit_origin(embed=help_mod_1, components=[action_row])


                        except:
                            pass
                    elif page == 2:
                        try:
                            buttons_normal = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row2 = create_actionrow(*buttons_normal)
                            await response.edit_origin(embed=help_mod_2, components=[action_row2])

                        except:
                            pass

                    elif page == 3:
                        try:
                            buttons_right_disabled = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=True),
                            ]
                            action_row3 = create_actionrow(*buttons_right_disabled)
                            await response.edit_origin(embed=help_mod_3, components=[action_row3])


                        except:
                            pass
                    pass
                except asyncio.TimeoutError:
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=mod_message)
                    buttons_all_disabled = [
                        create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                      disabled=True),
                    ]
                    action_row = create_actionrow(*buttons_all_disabled)
                    await response.edit_origin(components=[action_row])

        elif about.lower() == "information" or about.lower() == "info":
            page = 1
            pages = 2
            help_info_1 = nextcord.Embed(title="Information")
            help_info_1.add_field(
                name="Dictionary",
                value=f"Finds dictionary meanings, synonyms and antonyms.\n/help dictionary",
                inline=False)
            help_info_1.add_field(
                name="Translate",
                value=f"Translates a word into any language needed. (As long as we have it :sweat_smile:)\n/help translate",
                inline=False)
            help_info_1.add_field(
                name="Google",
                value=f"Allows you to google anything you want.\n/help google",
                inline=False)
            help_info_1.add_field(
                name="Let Me Google That For You",
                value=f"Uses the LMGTFY API to find the answer to your queries.\n/help lmgtfy",
                inline=False)
            help_info_1.set_footer(text="Page 1 of 2")
            help_info_1.color = nextcord.Color.random()

            help_info_2 = nextcord.Embed(title="Information")
            help_info_2.add_field(
                name="Weather",
                value=f"Gives you the present weather of a place.\n/help weather",
                inline=False)
            help_info_2.add_field(
                name="Wiki",
                value=f"Searches up the Wikipedia for you.\n/help wiki",
                inline=False)
            help_info_2.add_field(
                name="UrbanDictionary",
                value=f"Allows you to access the Urban Dictionary.\n/help urban",
                inline=False)
            help_info_2.add_field(
                name="Youtube",
                value=f"Let's you use YouTube through discord itself!\n/help youtube",
                inline=False)
            help_info_2.set_footer(text="Page 2 of 2")
            help_info_2.color = nextcord.Color.random()

            buttons = [
                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                              disabled=False),
                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                              disabled=False),
            ]
            action_row = create_actionrow(*buttons)

            info_message = await ctx.send(embed=help_info_1, components=[action_row])

            while True:
                try:
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=info_message, timeout=300)
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
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row = create_actionrow(*buttons_left_disabled)
                            await response.edit_origin(embed=help_info_1, components=[action_row])


                        except:
                            pass

                    elif page == 2:
                        try:
                            buttons_right_disabled = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=True),
                            ]
                            action_row2 = create_actionrow(*buttons_right_disabled)
                            await response.edit_origin(embed=help_info_2, components=[action_row2])


                        except:
                            pass
                    pass
                except asyncio.TimeoutError:
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=info_message)
                    buttons_all_disabled = [
                        create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                      disabled=True),
                    ]
                    action_row = create_actionrow(*buttons_all_disabled)
                    await response.edit_origin(components=[action_row])

        elif about.lower() == "nerd":
            page = 1
            pages = 4
            help_nerd_1 = nextcord.Embed(title="Nerd")
            help_nerd_1.add_field(
                name="Add",
                value=f"Adds numbers for you.\n/help add",
                inline=False)
            help_nerd_1.add_field(
                name="Subtract",
                value=f"Subtracts numbers for you.\n/help subtract",
                inline=False)
            help_nerd_1.add_field(
                name="Multiply",
                value=f"Multiplies numbers for you.\n/help multiply",
                inline=False)
            help_nerd_1.add_field(
                name="Divide",
                value=f"Divides to numbers for you.\n/help divide",
                inline=False)
            help_nerd_1.set_footer(text="Page 1 of 4")
            help_nerd_1.color = nextcord.Color.random()

            help_nerd_2 = nextcord.Embed(title="Nerd")
            help_nerd_2.add_field(
                name="Square",
                value=f"Gets the square of a number for you.\n/help square",
                inline=False)
            help_nerd_2.add_field(
                name="Cube",
                value=f"Gets the cube of a number for you\n/help cube",
                inline=False)
            help_nerd_2.add_field(
                name="Square Root",
                value=f"Gets the square root of a number for you.\n/help sqrt",
                inline=False)
            help_nerd_2.add_field(
                name="Cube Root",
                value=f"Gets the cube root of a number for you.\n/help cbrt",
                inline=False)
            help_nerd_2.add_field(
                name="Power",
                value=f"Gets any power of any number for you.\n/help power",
                inline=False)
            help_nerd_2.add_field(
                name="Root",
                value=f"Gets any root of any number for you.\n/help root",
                inline=False)
            help_nerd_2.set_footer(text="Page 2 of 4")
            help_nerd_2.color = nextcord.Color.random()

            help_nerd_3 = nextcord.Embed(title="Nerd")
            help_nerd_3.add_field(
                name="Perimeter",
                value=f"Gets the perimeter of certain shapes for you.\n/help perimeter",
                inline=False)
            help_nerd_3.add_field(
                name="Area",
                value=f"Gets the area of certain shapes for you.\n/help area",
                inline=False)
            help_nerd_3.add_field(
                name="Ask A Question",
                value=f"Allows you to ask me any random question.\n/help question",
                inline=False)

            help_nerd_3.set_footer(text="Page 3 of 4")
            help_nerd_3.color = nextcord.Color.random()

            help_nerd_4 = nextcord.Embed(title="Nerd")
            help_nerd_4.add_field(
                name="Trig",
                value=f"Gives you some info about trignometric functions.\n/trig",
                inline=False)
            help_nerd_4.add_field(
                name="Sin",
                value=f"Gives you info about sin.\n/trig sin",
                inline=False)
            help_nerd_4.add_field(
                name="Cos",
                value=f"Gives you info about cos.\n/trig cos",
                inline=False)
            help_nerd_4.add_field(
                name="Tan",
                value=f"Gives you info about tan.\n/trig tan",
                inline=False)
            help_nerd_4.add_field(
                name="Sec",
                value=f"Gives you info about sec.\n/trig sec",
                inline=False)
            help_nerd_4.add_field(
                name="Cosec",
                value=f"Gives you info about cosec.\n/trig cosec",
                inline=False)
            help_nerd_4.add_field(
                name="Cot",
                value=f"Gives you info about cot.\n/trig cot",
                inline=False)

            help_nerd_4.set_footer(text="Page 4 of 4")
            help_nerd_4.color = nextcord.Color.random()

            buttons = [
                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                              disabled=False),
                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                              disabled=False),
            ]
            action_row = create_actionrow(*buttons)

            nerd_message = await ctx.send(embed=help_nerd_1, components=[action_row])

            while True:
                try:
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=nerd_message, timeout=300)
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
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row = create_actionrow(*buttons_left_disabled)
                            await response.edit_origin(embed=help_nerd_1, components=[action_row])


                        except:
                            pass
                    elif page == 2:
                        try:
                            buttons_normal = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row2 = create_actionrow(*buttons_normal)
                            await response.edit_origin(embed=help_nerd_2, components=[action_row2])

                        except:
                            pass
                    elif page == 3:
                        try:
                            buttons_normal = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row3 = create_actionrow(*buttons_normal)
                            await response.edit_origin(embed=help_nerd_3, components=[action_row3])

                        except:
                            pass
                    elif page == 4:
                        try:
                            buttons_right_disabled = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=True),
                            ]
                            action_row4 = create_actionrow(*buttons_right_disabled)
                            await response.edit_origin(embed=help_nerd_4, components=[action_row4])


                        except:
                            pass
                    pass
                except asyncio.TimeoutError:
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=nerd_message)
                    buttons_all_disabled = [
                        create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                      disabled=True),
                    ]
                    action_row = create_actionrow(*buttons_all_disabled)
                    await response.edit_origin(components=[action_row])

        elif about.lower() == "fun":
            page = 1
            pages = 5
            help_fun_1 = nextcord.Embed(title="Fun")
            help_fun_1.add_field(
                name="Ask",
                value=f"Honestly answers any question you may have.\n/help ask",
                inline=False)
            help_fun_1.add_field(
                name="EpicGamerRate",
                value=f"Tells you how EPIC you are at gaming.\n/help epicgamerrate",
                inline=False)
            help_fun_1.add_field(
                name="SimpRate",
                value=f"Tells you how much you are simping (ans sometimes, WHO you are simping :smirk:).\n/help simprate",
                inline=False)
            help_fun_1.add_field(
                name="Poll",
                value=f"Creates a poll for you.\n/help poll",
                inline=False)
            help_fun_1.set_footer(text="Page 1 of 5")
            help_fun_1.color = nextcord.Color.random()

            help_fun_2 = nextcord.Embed(title="Fun")
            help_fun_2.add_field(
                name="Script",
                value=f"Translates the Zero&One script.\n/help script",
                inline=False)
            help_fun_2.add_field(
                name="ASCII",
                value=f"Creates a cool ASCII art for you.\n/help ascii",
                inline=False)
            help_fun_2.add_field(
                name="Binary",
                value=f"Converts a message to binary as zeros and ones are cool.\n/help binary",
                inline=False)
            help_fun_2.add_field(
                name="emojify",
                value=f"Turns your text into emojis!\n/help emojify",
                inline=False)
            help_fun_2.add_field(
                name="Spoilify",
                value=f"Spoils your message just for you! (Its nicer than it sounds)\n/help spoilify",
                inline=False)
            help_fun_2.set_footer(text="Page 2 of 5")
            help_fun_2.color = nextcord.Color.random()

            help_fun_3 = nextcord.Embed(title="Fun")
            help_fun_3.add_field(
                name="Act",
                value=f"Makes me act as though I'm another user...\n/help act",
                inline=False)
            help_fun_3.add_field(
                name="Choose",
                value=f"Helps you choose amongst some tough choices.\n/help choose",
                inline=False)
            help_fun_3.add_field(
                name="Hack",
                value=f"Hacks the required user. WARNING: Only to be used under unavoidable circumstances.\n/help hack",
                inline=False)
            help_fun_3.add_field(
                name="Gif",
                value=f"Allows you to search for GIFs or send random gifs from GIPHY.\n/help gif",
                inline=False)
            help_fun_3.add_field(
                name="ImageMemes",
                value=f"Makes some very funny imagememes for you.\n/help imagememes",
                inline=False)
            help_fun_3.set_footer(text="Page 3 of 5")
            help_fun_3.color = nextcord.Color.random()

            help_fun_4 = nextcord.Embed(title="Fun")
            help_fun_4.add_field(
                name="VCMeme",
                value=f"Lets you have some fun with the people in your VC.\n/help vcmeme",
                inline=False)
            help_fun_4.add_field(
                name="Shoo",
                value=f"Kicks me out of a VC cause bandwith don't come for free.\n/shoo",
                inline=False)
            help_fun_4.add_field(
                name="Pause",
                value=f"Pauses my VC activity.\n/pause",
                inline=False)
            help_fun_4.add_field(
                name="Resume",
                value=f"Resumes my VC shenanigans.\n/resume",
                inline=False)
            help_fun_4.add_field(
                name="Stop",
                value=f"Stop me from doing what I'm doing in a VC.\n/stop",
                inline=False)
            help_fun_4.set_footer(text="Page 4 of 5")
            help_fun_4.color = nextcord.Color.random()

            help_fun_5 = nextcord.Embed(title="Fun")
            help_fun_5.add_field(
                name="Quote",
                value=f"Allows you to quote the sayings of your fellow human beings. (Unless you use a bot name)\n/help quote",
                inline=False)
            help_fun_5.add_field(
                name="Kill",
                value=f"Kill your friends... But minecraft style\n/help kill",
                inline=False)
            help_fun_5.add_field(
                name="Roast",
                value=f"Respect? Nah mate...\n/help roast",
                inline=False)
            help_fun_5.add_field(
                name="Joke",
                value=f"Tells you a joke to lighten your day! (or spoil it :rofl:)\n/help joke",
                inline=False)
            help_fun_5.add_field(
                name="Meme",
                value=f"Gives you memes **cause**.\n/help meme",
                inline=False)
            help_fun_5.set_footer(text="Page 5 of 5")
            help_fun_5.color = nextcord.Color.random()

            buttons = [
                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                              disabled=False),
                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                              disabled=False),
            ]
            action_row = create_actionrow(*buttons)

            fun_message = await ctx.send(embed=help_fun_1, components=[action_row])

            while True:
                try:
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=fun_message, timeout=300)
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
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row = create_actionrow(*buttons_left_disabled)
                            await response.edit_origin(embed=help_fun_1, components=[action_row])


                        except:
                            pass
                    elif page == 2:
                        try:
                            buttons_normal = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row2 = create_actionrow(*buttons_normal)
                            await response.edit_origin(embed=help_fun_2, components=[action_row2])

                        except:
                            pass
                    elif page == 3:
                        try:
                            buttons_normal = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row3 = create_actionrow(*buttons_normal)
                            await response.edit_origin(embed=help_fun_3, components=[action_row3])

                        except:
                            pass

                    elif page == 4:
                        try:
                            buttons_normal = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row4 = create_actionrow(*buttons_normal)
                            await response.edit_origin(embed=help_fun_4, components=[action_row4])

                        except:
                            pass

                    elif page == 5:
                        try:
                            buttons_right_disabled = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=True),
                            ]
                            action_row5 = create_actionrow(*buttons_right_disabled)
                            await response.edit_origin(embed=help_fun_5, components=[action_row5])

                        except:
                            pass
                    pass
                except asyncio.TimeoutError:
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=fun_message)
                    buttons_all_disabled = [
                        create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                      disabled=True),
                    ]
                    action_row = create_actionrow(*buttons_all_disabled)
                    await response.edit_origin(components=[action_row])

        elif about.lower() == "games":
            page = 1
            pages = 3
            help_games_1 = nextcord.Embed(title="Games")
            help_games_1.add_field(
                name="Amogus",
                value=f"Find out if you can get the imposter in time!\n/help amogus",
                inline=False)
            help_games_1.add_field(
                name="Akinator",
                value=f"Check out whether you can defeat our mind-reader.\n/help aki",
                inline=False)
            help_games_1.add_field(
                name="Guess the Movie",
                value=f"Will you be able to guess the movie with the emojis I give you?\n/help guessthemovie",
                inline=False)
            help_games_1.add_field(
                name="Riddle",
                value="Gives you a riddle that you must answer. (Please don't kick me, I like those riddles!)\n/help riddle",
                inline=False)
            help_games_1.add_field(
                name="Who's That Pokémon",
                value=f"Test your knowledge of Pokémon!\n/help whosthatpokemon",
                inline=False)
            help_games_1.set_footer(text="Page 1 of 3")
            help_games_1.color = nextcord.Color.random()

            help_games_2 = nextcord.Embed(title="Games")
            help_games_2.add_field(
                name="Coinflip",
                value=f"Allows you to try your luck with the coin!\n/help coinflip",
                inline=False)
            help_games_2.add_field(
                name="Dice",
                value=f"Rolls a dice, which is useful for bets.\n/help dice",
                inline=False)
            help_games_2.add_field(
                name="Guess",
                value=f"Lets you guess a number within any range.\n/help guess",
                inline=False)
            help_games_2.add_field(
                name="Rps",
                value=f"Lets you play rock paper scissor with me **OR** your friends.\n/help rps",
                inline=False)
            help_games_2.add_field(
                name="OddEve",
                value=f"Lets you play odd eve with me **OR** your friends.\n/help oddeve",
                inline=False)
            help_games_2.set_footer(text="Page 2 of 3")
            help_games_2.color = nextcord.Color.random()

            help_games_3 = nextcord.Embed(title="Games")
            help_games_3.add_field(
                name="Wordhunt",
                value=f"Test your skill in finding hidden words.\n/help wordhunt",
                inline=False)
            help_games_3.add_field(
                name="Extremehunt",
                value=f"A much more difficult version of wordhunt itself!\n/help extremehunt",
                inline=False)
            help_games_3.add_field(
                name="Scramble",
                value=f"Unscramble the word that I have scrambled for you.\n/help scramble",
                inline=False)
            help_games_3.add_field(
                name="Hangman",
                value=f"Save an innocent man by finding the letters in my hidden word!\n/help hangman",
                inline=False)
            help_games_3.add_field(
                name="PassTheBomb",
                value=f"Stop the bomb from exploding in your facing by giving me a suitable word.\n/help passthebomb",
                inline=False)
            help_games_3.add_field(
                name="Typeracer",
                value=f"Race against your friends in a quest to type stuff.\n/help typerace",
                inline=False)
            help_games_3.set_footer(text="Page 3 of 3")
            help_games_3.color = nextcord.Color.random()

            buttons = [
                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                              disabled=False),
                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                              disabled=False),
            ]
            action_row = create_actionrow(*buttons)

            games_message = await ctx.send(embed=help_games_1, components=[action_row])

            while True:
                try:
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=games_message, timeout=300)
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
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row = create_actionrow(*buttons_left_disabled)
                            await response.edit_origin(embed=help_games_1, components=[action_row])

                        except:
                            pass
                    elif page == 2:
                        try:
                            buttons_normal = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row2 = create_actionrow(*buttons_normal)
                            await response.edit_origin(embed=help_games_2, components=[action_row2])

                        except:
                            pass

                    elif page == 3:
                        try:
                            buttons_right_disabled = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=True),
                            ]
                            action_row3 = create_actionrow(*buttons_right_disabled)
                            await response.edit_origin(embed=help_games_3, components=[action_row3])


                        except:
                            pass
                    pass
                except asyncio.TimeoutError:
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=games_message)
                    buttons_all_disabled = [
                        create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                      disabled=True),
                    ]
                    action_row = create_actionrow(*buttons_all_disabled)
                    await response.edit_origin(components=[action_row])

        elif about.lower() == 'ping':
            embed = nextcord.Embed(
                title="Help Ping",
                description="With this command, you can see how fast I am reacting to your messages in milliseconds.",
                color=nextcord.Color.green())
            embed.add_field(name="Usage:", value=f"/ping")
            embed.set_footer(text="I do be very fast u know...")
            await ctx.send(embed=embed)

        elif about.lower() == 'makerole':
            embed = nextcord.Embed(
                title="Help MakeRole",
                description="At last, with just one command, you can make a new role in your server.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/makerole <rolename>\nCause you have the right to be LAZY",
                inline=True
            )
            embed.set_footer(
                text="Only people with manage roles perms can use this so DON'T EVEN TRY, PEASANTS"
            )
            await ctx.send(embed=embed)

        elif about.lower() == 'addrole':
            embed = nextcord.Embed(
                title="Help AddRole",
                description="You can also add roles to your members by just using this one command!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/addrole @<membername> @<rolename>\nSo now you can be LAZIER!",
                inline=True
            )
            embed.set_footer(
                text="Only people with manage roles perms can use this so DON'T EVEN TRY, PEASANTS"
            )
            await ctx.send(embed=embed)


        elif about.lower() == 'editrole':
            embed = nextcord.Embed(
                title="Help EditRole",
                description="Don't like the name of your role?\n Then just use this command to change its name!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/editrole @<fromrolename> <torolename>\n"
                      f"/editrole @<fromrolename> #<hexdecimal>\n"
                      f"/editrole @<fromrolename> <torolename> #<hexdecimal>\n"
                      f"either will do.",
                inline=True
            )
            embed.set_footer(
                text="Color or colour?"
            )
            await ctx.send(embed=embed)

        elif about.lower() == 'removerole':
            embed = nextcord.Embed(
                title="Help RemoveRole",
                description="If your members misuse their roles then there is only one solution:\n Take the role away from them!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/removerole @<membername> @<rolename>\nBasically making you a dictator...",
                inline=True
            )
            embed.set_footer(
                text="Only people with manage roles perms can use this so DON'T EVEN TRY, PEASANTS"
            )
            await ctx.send(embed=embed)

        elif about.lower() == 'deleterole':
            embed = nextcord.Embed(
                title="Help DeleteRole",
                description="You can also delete roles in your server when the role just becomes useless.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/deleterole @<rolename>\nImagine needing to delete roles ANYWAY...",
                inline=True
            )
            embed.set_footer(
                text="Only people with manage roles perms can use this so DON'T EVEN TRY, PEASANTS"
            )
            await ctx.send(embed=embed)

        elif about.lower() == 'support':
            embed = nextcord.Embed(
                title="Help Support",
                description="Need help with the my commands?\nWanna complain about them?\nMaybe make a suggestion?",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/support\nSo you can visit our support server.",
                inline=True)
            embed.set_footer(text="Get support its good for you")
            await ctx.send(embed=embed)

        elif about.lower() == 'patreon' or about.lower() == 'donate':
            embed = nextcord.Embed(
                title="Help Patreon",
                description="Really pleased with my awesomeness?\nWanna show your love?\nGot a lot of money to burn?",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/patreon\nUse this to donate to me, so that I can be better!",
                inline=True)
            embed.set_footer(text="It's worth it, honestly.")
            await ctx.send(embed=embed)

        elif about.lower() == 'userinfo':
            embed = nextcord.Embed(
                title="Help UserInfo",
                description="Find out about the wierdos who join your servers.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/userinfo @<membername>\n#gettingexposed",
                inline=True)
            embed.set_footer(text="Being a stalker eh?")
            await ctx.send(embed=embed)

        elif about.lower() == 'robmoji':
            embed = nextcord.Embed(
                title="Help RobMoji",
                description="Steal an emoji from another server and make it yours. If a name is not given, it will take the emoji's name. Also pls make sure that you give a name from 2 to 32.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/robmoji emoji name_of_new_emoji\n#MINE!",
                inline=True)
            embed.set_footer(text="Should I call the cops?")
            await ctx.send(embed=embed)

        elif about.lower() == 'serverinfo':
            embed = nextcord.Embed(
                title="Help ServerInfo",
                description="For everything you need to know about your server.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/serverinfo\nNever forget your memories, or your server info.",
                inline=True
            )
            embed.set_footer(text="But seriously, how did you forget?")
            await ctx.send(embed=embed)

        elif about.lower() == 'nick':
            embed = nextcord.Embed(
                title="Help Nick",
                description="Nickname your friends anything you want!\nIt is WAY too easy to do so, with this command.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/nick @<membername> <nickname>\nNow see what you can come up with...",
                inline=True
            )
            embed.set_footer(
                text="Nasty surprise for the poor victim's names *sigh*")
            await ctx.send(embed=embed)

        elif about.lower() == 'afk':
            embed = nextcord.Embed(
                title="Help Afk",
                description="Use this to make people know that your are afk when they ping you.\nUseful to warn people about your afkness!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/afk <reason>\nThis will solve a lot of afk problems...",
                inline=True
            )
            embed.set_footer(text="Why didn't we think of this be4?")
            await ctx.send(embed=embed)

        elif about.lower() == 'remind' or about.lower() == 'reminder':
            embed = nextcord.Embed(
                title="Help Reminder",
                description="Nickname your friends anything you want!\nIt is WAY too easy to do so, with this command.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/remind <time> <thingtoremind>\nThis is specially for people who forget what they were doing in like, 2 seconds",
                inline=True
            )
            embed.set_footer(text="Now you cannot forget ANYTHING")
            await ctx.send(embed=embed)

        elif about.lower() == 'about':
            embed = nextcord.Embed(
                title="Help About",
                description="Get to know a little bit more about me!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/about\nPlease use this :pleading_face:\nMy devs think NO ONE wants to know more about me...",
                inline=True
            )
            embed.set_footer(text="I mean, why not?")
            await ctx.send(embed=embed)

        elif about.lower() == 'vote':
            embed = nextcord.Embed(title="Help Vote",
                                   description="Vote me or perish",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/vote\nSupports me a lot :pleading_face:\nMakes me.... **EVEN MORE POPULAR**",
                inline=True
            )
            embed.set_footer(text="I mean, why not?")
            await ctx.send(embed=embed)

        elif about.lower() == 'invite':
            embed = nextcord.Embed(
                title="Help Invite",
                description="Use this to invite me to your other servers.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/invite\nPlease use this :pleading_face:\nYou. Can't. Get. Enough. Of. Me.",
                inline=True
            )
            embed.set_footer(text="I'm the BEST")
            await ctx.send(embed=embed)

        elif about.lower() == 'serverlink' or about.lower() == 'sl':
            embed = nextcord.Embed(
                title="Help ServerLink",
                description="If you feel to lazy to create an invite to your server, just ask me to do it!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/serverlink\nIts ez to use and time-efficient too!",
                inline=True
            )
            embed.set_footer(text="Anyway I was made to do all the work...")
            await ctx.send(embed=embed)

        elif about.lower() == 'suggest' or about.lower() == 'suggestion':
            embed = nextcord.Embed(
                title="Help Suggest",
                description="Use this to make a suggestion about me, which gets magically transported to the devs themselves",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/suggest\nNow you don't have to join the support server.\nUnless you want more info about updates and stuff.",
                inline=True
            )
            embed.set_footer(text="We are open to suggestions. Once per hor")
            await ctx.send(embed=embed)

        elif about.lower() == 'complain' or about.lower() == 'complaint':
            embed = nextcord.Embed(
                title="Help Complain",
                description="Use this to complain about me and the complaint gets magically transported to the devs themselves",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/complain\nNow you don't have to join the support server.\nUnless you want more info about updates and stuff.",
                inline=True
            )
            embed.set_footer(text="You can only complain once per hour tho.")
            await ctx.send(embed=embed)

        elif about.lower() == 'website':
            embed = nextcord.Embed(
                title="Help Website",
                description="My developers have a website. Go check it out.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/website\nPlease use this :pleading_face:\nIt's not really related to me, but its cool anyway.",
                inline=True
            )
            embed.set_footer(text="See you there!")
            await ctx.send(embed=embed)

        elif about.lower() == 'snipe':
            embed = nextcord.Embed(
                title="Help Snipe",
                description="Find out what the last deleted message in your server was.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/snipe\nNow you can catch your sneaky server members in the act!",
                inline=True
            )
            embed.set_footer(text="More stonx for u")
            await ctx.send(embed=embed)

        elif about.lower() == 'snowflake':
            embed = nextcord.Embed(
                title="Help Snowflake",
                description="Use the ID of anything to find out the date of creation!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/snowflake\nUseful for devs and people who want to know how old stuff is.",
                inline=True
            )
            embed.set_footer(text="More stonx for u")
            await ctx.send(embed=embed)

        elif about.lower() == 'slowmode':
            embed = nextcord.Embed(
                title="Help Slowmode",
                description="Allows you to put or remove a slowmode in your channel.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/slowmode <timeinseconds>\nThat will stop the SPAMMERS",
                inline=True
            )
            embed.set_footer(text="Sad life for spammers.")
            await ctx.send(embed=embed)

        elif about.lower() == 'blacklist':
            embed = nextcord.Embed(
                title="Help Blacklist",
                description="This makes the required member unable to use my commands.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/blacklist @<membername>\nThis is one of the most CRUELLEST punishments possible.",
                inline=True
            )
            embed.set_footer(text="Not using CHAD be SAD")
            await ctx.send(embed=embed)

        elif about.lower() == 'unblacklist':
            embed = nextcord.Embed(
                title="Help Unblacklist",
                description="Removes blacklisted users from the list of naughty people...",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/unblacklist @<membername>\nOnly kindness can make you use this command.",
                inline=True
            )
            embed.set_footer(text="Unblacklisters = Saviours")
            await ctx.send(embed=embed)

        elif about.lower() == 'clear':
            embed = nextcord.Embed(
                title="Help Clear",
                description="Clears the required number of messages in a channel. You can also clear messages of a particular member.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/clear <numberofmessages> <optionalmember>\nHelps when your server members just don't want to stop chatting...",
                inline=True
            )
            embed.set_footer(text="Get ERASED")
            await ctx.send(embed=embed)

        elif about.lower() == 'removewarn':
            embed = nextcord.Embed(
                title="Help RemoveWarn",
                description="Used to remove one or all of a users warn.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/lockdown <reason>\nGive the reason to remove, or just type 'all' to remove all warnings.",
                inline=True)
            embed.set_footer(text="Showing mercy gets you killed. You have been warned.")
            await ctx.send(embed=embed)

        elif about.lower() == 'warn':
            embed = nextcord.Embed(title="Help Warn",
                                   description="Gives the rule-breakers a warning!",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/warn <username> <reason>\nOnly for those naughty users who don't like rules.",
                inline=True
            )
            embed.set_footer(text="So you've been warned...")
            await ctx.send(embed=embed)

        elif about.lower() == 'prefix':
            embed = nextcord.Embed(title="Help Prefix",
                                   description="Change dat prefix",
                                   color=nextcord.Color.random())
            embed.add_field(
                name="Usage:",
                value=f"/prefix <newprefix>\nVery handy for big servers!",
                inline=True
            )
            embed.set_footer(text="Just don't forget what your prefix was...")
            await ctx.send(embed=embed)

        elif about.lower() == 'userwarn':
            embed = nextcord.Embed(
                title="Help UserWarn",
                description="Gives a record of why and how many times a user was warned in the server.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/userwarn @<username>\nNow you have a record of their crimes.",
                inline=True
            )
            embed.set_footer(text="*Evil laughter from admins*")
            await ctx.send(embed=embed)

        elif about.lower() == 'unmute':
            embed = nextcord.Embed(title="Help Unmute",
                                   description="Allows you to unmute a user.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/unmute @<username>\nThis makes the able to talk in your server again.",
                inline=True
            )
            embed.set_footer(text="Support Freedom of Speech")
            await ctx.send(embed=embed)

        elif about.lower() == 'tempmute':
            embed = nextcord.Embed(
                title="Help Tempmute",
                description="Allows you to temporarily mute a user.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/tempmute <timeinseconds>s @<username>\nIf you think you may forget to unmute a user, then I do it for you!",
                inline=True
            )
            embed.set_footer(text="That's one less thing to remember...")
            await ctx.send(embed=embed)

        elif about.lower() == 'mute':
            embed = nextcord.Embed(title="Help Mute",
                                   description="Allows you to mute a user.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/mute @<username>\nNow they can't talk until you allow them too!",
                inline=True
            )
            embed.set_footer(text="Sad life for the muted")
            await ctx.send(embed=embed)

        elif about.lower() == 'kick':
            embed = nextcord.Embed(title="Help Kick",
                                   description="Allows you to kick a user.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/kick @<username>\nSo basically they just get yeeted out.",
                inline=True
            )
            embed.set_footer(text="Get rekt lol")
            await ctx.send(embed=embed)

        elif about.lower() == 'unban':
            embed = nextcord.Embed(title="Help Unban",
                                   description="Allows you to unban a user.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/unban @<username>\nSo that they can return to the server.",
                inline=True
            )
            embed.set_footer(text="Oh look, they're back lol")
            await ctx.send(embed=embed)

        elif about.lower() == 'tempban':
            embed = nextcord.Embed(
                title="Help Tempban",
                description="Allows you to temporarily ban a user.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/tempban <timeinseconds>s @<username>\nIf you really hate someone, and may \"accidentally\" forget to unban them...",
                inline=True
            )
            embed.set_footer(text="That's just sus uk")
            await ctx.send(embed=embed)

        elif about.lower() == 'ban':
            embed = nextcord.Embed(title="Help Ban",
                                   description="Allows you to ban a user.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/ban @<username>\nThey can NEVER COME BACK NOW MWA HA HA HA\nJeez I was only joking",
                inline=True
            )
            embed.set_footer(text="Get banished lmao")
            await ctx.send(embed=embed)

        elif about.lower() == 'dictionary':
            embed = nextcord.Embed(
                title="Help Dictionary",
                description="Lets you access a dictionary through discord!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/dictionary <word>\nWhat you can do is get meanings, synonyms and antonyms!\nThen you type either meanings, synonyms or antonyms.",
                inline=True
            )
            embed.set_footer(text="All for geeky lil nerds!")
            await ctx.send(embed=embed)

        elif about.lower() == 'translate':
            embed = nextcord.Embed(
                title="Help Translate",
                description="Translate a word to any language you want.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/translate <wordtotranslate>\nAnd then you enter the language translate to.",
                inline=True
            )
            embed.set_footer(text="Merci!")
            await ctx.send(embed=embed)

        elif about.lower() == 'google' or about.lower() == 'search':
            embed = nextcord.Embed(
                title="Help Google  ",
                description="Lets you google anything you want",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/google <whatyouwanttogoogle>\nGoogles the thing you enter",
                inline=True
            )
            embed.set_footer(text="Perfect for searching through discord instead of your browser")
            await ctx.send(embed=embed)

        elif about.lower() == 'lmgtfy' or about.lower() == 'letmegooglethatforyou':
            embed = nextcord.Embed(
                title="Help Let Me Google That For You",
                description="Kinda self explainatory...",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/lmgtfy <thinguneedtogoogle>\nAgain, pretty obvious why this command exists.",
                inline=True
            )
            embed.set_footer(text="So basically, an obvious command")
            await ctx.send(embed=embed)

        elif about.lower() == 'weather':
            embed = nextcord.Embed(
                title="Help Weather",
                description="Get the real-time weather of any place!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/search <cityname>\nAny city can be searched for!",
                inline=True)
            embed.set_footer(text="Try searching \"Israel\" lol")
            await ctx.send(embed=embed)

        elif about.lower() == 'wiki':
            embed = nextcord.Embed(title="Help Wiki",
                                   description="Search Wikipedia.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/wiki <whatyouwannasearch>\nCause clearly, google wasn't enough.",
                inline=True
            )
            embed.set_footer(text="Wisdom is in DISCORD PPL")
            await ctx.send(embed=embed)

        elif about.lower() == 'urban':
            embed = nextcord.Embed(
                title="Help UrbanDictionary",
                description="Let's you use the Urban Dictionary (like, obviously).",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/urban <whatyouwannasearch>\nAn interesting place of knowledge.",
                inline=True
            )
            embed.set_footer(
                text="The urban dict be lollers (I mean try searching your own name)")
            await ctx.send(embed=embed)

        elif about.lower() == 'youtube':
            embed = nextcord.Embed(
                title="Help Youtube",
                description="Lets you access YouTube itself through discord!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/youtube <thingyouwannasee>\nSo now you lazy folks don't even need to open your browser!",
                inline=True
            )
            embed.set_footer(text="This is for true legends")
            await ctx.send(embed=embed)

        elif about.lower() == 'add':
            embed = nextcord.Embed(title="Help Add",
                                   description="Adds two or more numbers for you.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/math add <number1> <number2> etc...",
                inline=True
            )
            embed.set_footer(text="I can add a lot of stuff tbh")
            await ctx.send(embed=embed)

        elif about.lower() == 'subtract' or about.lower() == 'substract':
            embed = nextcord.Embed(title="Help Subtract",
                                   description="Subtracts only two numbers for you.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/math subtract <number1> <number2>",
                inline=True
            )
            embed.set_footer(text="I can subtract a only two numbers for obvious reasons")
            await ctx.send(embed=embed)

        elif about.lower() == 'multiply' or about.lower() == 'multi':
            embed = nextcord.Embed(title="Help Multiply",
                                   description="Multiplication two or more numbers for you.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/math mulitply <number1> <number2> etc...",
                inline=True
            )
            embed.set_footer(text="I can multiply a lot of stuff tbh")
            await ctx.send(embed=embed)

        elif about.lower() == 'divide' or about.lower() == 'div':
            embed = nextcord.Embed(title="Help Divide",
                                   description="Divides only two numbers for you.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/math divide <number1> <number2>",
                inline=True
            )
            embed.set_footer(text="I can divide a only two numbers for obvious reasons")
            await ctx.send(embed=embed)

        elif about.lower() == 'square':
            embed = nextcord.Embed(title="Help Square",
                                   description="Finds the square of a number for you.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/math square <number>",
                inline=True
            )
            embed.set_footer(text="It's pretty straight forward and ded useful")
            await ctx.send(embed=embed)

        elif about.lower() == 'cube':
            embed = nextcord.Embed(title="Help Cube",
                                   description="Finds the cube of a number for you.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/math cube <number>",
                inline=True
            )
            embed.set_footer(text="It's pretty straight forward and ded useful")
            await ctx.send(embed=embed)

        elif about.lower() == 'sqrt' or about.lower() == 'squareroot':
            embed = nextcord.Embed(title="Help Square Root",
                                   description="Finds the square root of a number for you.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/math squareroot <number>",
                inline=True
            )
            embed.set_footer(text="It's pretty straight forward and ded useful")
            await ctx.send(embed=embed)

        elif about.lower() == 'cbrt' or about.lower() == 'cuberoot':
            embed = nextcord.Embed(title="Help Cube Root",
                                   description="Finds the cube root of a number for you.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/math cuberoot <number>",
                inline=True
            )
            embed.set_footer(text="It's pretty straight forward and ded useful")
            await ctx.send(embed=embed)

        elif about.lower() == 'power':
            embed = nextcord.Embed(title="Help Power",
                                   description="Finds any power of any number for you.\nBasically if you need the power of something more than 2 and 3.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/math power <number> <power>",
                inline=True
            )
            embed.set_footer(text="An OP function if I do say so myself")
            await ctx.send(embed=embed)

        elif about.lower() == 'root':
            embed = nextcord.Embed(title="Help Root",
                                   description="Finds any root of any number for you.\nBasically if you need the root of something more than 2 and 3.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/math root <number> <root>",
                inline=True
            )
            embed.set_footer(text="Another OP function if I do say so myself")
            await ctx.send(embed=embed)

        elif about.lower() == 'perimeter':
            embed = nextcord.Embed(title="Help Perimeter",
                                   description="Finds the perimeters of certain shapes based on the numbers you give.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/perimeter",
                inline=True
            )
            embed.set_footer(text="Its usage is... interesting")
            await ctx.send(embed=embed)

        elif about.lower() == 'area':
            embed = nextcord.Embed(title="Help Area",
                                   description="Finds the areas of certain shapes based on the numbers you give.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/area",
                inline=True
            )
            embed.set_footer(text="Its usage is... interesting")
            await ctx.send(embed=embed)



        elif about.lower() == 'ask':
            embed = nextcord.Embed(title="Help Ask",
                                   description="Ask me a question and I will give you a carefully considered, totally not chance based answer.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/ask <question>\nI am a beacon of honesty.",
                inline=True
            )
            embed.set_footer(text="I have never failed anyone yet")
            await ctx.send(embed=embed)

        elif about.lower() == 'epicgamerrate':
            embed = nextcord.Embed(
                title="Help epicgamerrate",
                description="Now you can find out how epic you are at gaming.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/epicgamerrate\nThis is totally true btw",
                inline=True)
            embed.set_footer(
                text="It's a perfect way of knowing how good you are!")
            await ctx.send(embed=embed)

        elif about.lower() == 'simprate':
            embed = nextcord.Embed(
                title="Help Simprate",
                description="Now you can find out how much you simp.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/simprate\nThis is totally true btw",
                inline=True)
            embed.set_footer(
                text="It's a perfect way of knowing how simpy you are!")
            await ctx.send(embed=embed)

        elif about.lower() == 'poll':
            embed = nextcord.Embed(title="Help Poll",
                                   description="Create a poll to get some votes",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/poll <timeinseconds> <whatyoupollfor>: <optionswithcommas>\nEveryone can just choose what they wanna choose.",
                inline=True
            )
            embed.set_footer(
                text="Use s for seconds, m for mins, h for hours, d for days")
            await ctx.send(embed=embed)



        elif about.lower() == 'script':
            embed = nextcord.Embed(title="Help Script",
                                   description="Translates the ZeroAndOne Script",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/encrypt <stufftoencrypt>\n!decrypt <stufftodecrypt>\nCheck out the way this script works [here](https://secret-message-encoder-decoder.itszeroandone.repl.co/).",
                inline=True
            )
            embed.set_footer(text="You'll love the script.")
            await ctx.send(embed=embed)

        elif about.lower() == 'ascii':
            embed = nextcord.Embed(
                title="Help ASCII",
                description="Turns me into a painter and makes ASCII art.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/ascii <stufftoput>\nI can't really explain it's beauty.",
                inline=True
            )
            embed.set_footer(text="What you put may or may not be what you get")
            await ctx.send(embed=embed)

        elif about.lower() == 'emojify' or about.lower() == 'emo':
            embed = nextcord.Embed(
                title="Help Emojifyy",
                description="Give me TEXT and I will give you emojis",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/emojify <sometext>\nIt's quite creative, really.",
                inline=True
            )
            embed.set_footer(text="It makes quite the statement too!")
            await ctx.send(embed=embed)

        elif about.lower() == 'spoilify' or about.lower() == 'spoil':
            embed = nextcord.Embed(
                title="Help Spoilify",
                description="Annoys your friends if they want to read your message.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/spoilify <stufftoput>\nExcellent command for losing friends!",
                inline=True
            )
            embed.set_footer(text="Jk chill its hilarious tho")
            await ctx.send(embed=embed)

        elif about.lower() == 'act':
            embed = nextcord.Embed(
                title="Help Act",
                description="Use this to make me act like another user!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/act @<usertoactlike> <messagetouse>\nMostly used for fake evidence :smiling_imp:",
                inline=True
            )
            embed.set_footer(text="This is for pure evil purposes")
            await ctx.send(embed=embed)

        elif about.lower() == 'binary':
            embed = nextcord.Embed(title="Help binary",
                                   description="Converts string to binary",
                                   color=nextcord.Color.green())
            embed.add_field(name="Usage:",
                            value=f"/binary <yourstring>",
                            inline=True)
            embed.set_footer(text="Zeros and Ones are awesome.")
            await ctx.send(embed=embed)

        elif about.lower() == 'choose' or about.lower() == 'choose':
            embed = nextcord.Embed(title="Help Choose",
                                   description="Makes a choice for you.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/choose <choices>\nAgain, this bot knows everything.\nIt makes the correct choice.",
                inline=True
            )
            embed.set_footer(text="The bot KNOWS")
            await ctx.send(embed=embed)

        elif about.lower() == 'hack':
            embed = nextcord.Embed(
                title="Help Hack",
                description="Totally hacks the targeted user pc.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/hack @<membername>\nA lot of bad stuff happens.\nUse only in cases of extreme hate or prejudice.",
                inline=True
            )
            embed.set_footer(text="The bad stuff be bad")
            await ctx.send(embed=embed)

        elif about.lower() == 'gif':
            embed = nextcord.Embed(
                title="Help Gif",
                description="Allows you to search giphy for GIFS",
                color=nextcord.Color.random())
            embed.add_field(
                name="Usage:",
                value=f"/gif <nameofgif>\nGifs are cool yay",
                inline=True)
            embed.set_footer(text="Who needs inbuilt GIFs smh")
            await ctx.send(embed=embed)

        elif about.lower() == 'imagememes':
            embed = nextcord.Embed(title="Help ImageMemes",
                                   description="Cool memes with images!",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/imagememes \nGives you a list of image memes. Enjoy!",
                inline=True
            )
            embed.set_footer(text="Cause there can NEVER be enough memes")
            await ctx.send(embed=embed)

        elif about.lower() == 'vcmeme':
            embed = nextcord.Embed(title="Help VCMeme",
                                   description="Prank your friends in your VC.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/vcmeme <chosenvcmeme>\nThe list is long...\nTo check the list, type /vcmeme",
                inline=True
            )
            embed.set_footer(text="I feel sorry for VC users...")
            await ctx.send(embed=embed)

        elif about.lower() == 'quote':
            embed = nextcord.Embed(
                title="Help Quote",
                description="Creates a quote so you can remember your most famous sayings!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/quote <quoter> <quote>\nIt gives you glory.",
                inline=True)
            embed.set_footer(text="Always remember...")
            await ctx.send(embed=embed)

        elif about.lower() == 'kill':
            embed = nextcord.Embed(
                title="Help Kill",
                description="Kill someone with minecraft messages!!!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/kill <Person>\nCoffin Dance Music Plays.",
                inline=True)
            embed.set_footer(text="Yuo Ded")
            await ctx.send(embed=embed)

        elif about.lower() == 'roast':
            embed = nextcord.Embed(
                title="Help Roast",
                description="Roast someone or yourself",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/roast <Person>(Optional)\nDisrespekt",
                inline=True)
            embed.set_footer(text="OOH OOOOOOH")
            await ctx.send(embed=embed)

        elif about.lower() == 'joke':
            embed = nextcord.Embed(
                title="Help Joke",
                description="Gives you jokes.\nYou will either find it funny...\n...or WAY too lame",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/joke",
                inline=True)
            embed.set_footer(text="Jokes be phunny")
            await ctx.send(embed=embed)

        elif about.lower() == 'meme':
            embed = nextcord.Embed(
                title="Help Meme",
                description="Gives you the latest memes... very very phunniez",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/meme",
                inline=True)
            embed.set_footer(text="Cause me wen")
            await ctx.send(embed=embed)

        elif about.lower() == 'riddle' or about.lower() == 'riddles':
            embed = nextcord.Embed(
                title="Help Riddle",
                description="Gives you a cool riddle (that totally isn't lame)",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"Use /riddle\nSee if you can answer 'em or not!",
                inline=True
            )
            await ctx.send(embed=embed)

        elif about.lower() == 'coinflip':
            embed = nextcord.Embed(
                title="Help Coinflip",
                description="Flips a coin for you. But with a lot MORE FUNCTIONALITY (insert pog music here).",
                color=nextcord.Color.green())
            embed.add_field(
                name="Normal:",
                value=f"Use /coinflip\nTo flip a coin. Nothing more, nothing less",
                inline=True
            )
            embed.add_field(
                name="Slightly Better:",
                value=f"Use /coinflip <heads/tails>\nTo flip a coin and see if your luck allows you to win",
                inline=True
            )
            embed.add_field(
                name="Coinflip Fight:",
                value=f"Use /coinflip <membername>\nTo completely humiliate your friends by making them loose in coinflip.\nUnless you loose yourself.",
                inline=True
            )
            embed.set_footer(text="It's so much better now...")
            await ctx.send(embed=embed)

        elif about.lower() == 'dice':
            embed = nextcord.Embed(
                title="Help Dice",
                description="Roles a dice for you! And yes pun intended.\nYou can play either",
                color=nextcord.Color.green())
            embed.add_field(
                name="Normal:",
                value=f"Use /dice\nIf you want to just roll a dice.",
                inline=True
            )
            embed.add_field(
                name="Betting:",
                value=f"Use /dice <lowerlimit> <upper_limit>\nIf you want to, say, place a bet against your friends!",
                inline=True

            )
            embed.set_footer(text="This is the poggy-dice (say it out loud its sounds nice lmao)")
            await ctx.send(embed=embed)

        elif about.lower() == 'amogus':
            embed = nextcord.Embed(
                title="Help Amongus",
                description="The imposters are at it again.\nOnly four people are alive and one of them is the IMPOSTER\nWill you be able to defeat the imposters or will you kill an innocent man?",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/amogus",
                inline=True
            )
            embed.set_footer(text="Amogus go chogers")
            await ctx.send(embed=embed)

        elif about.lower() == 'aki':
            embed = nextcord.Embed(
                title="Help Akinator",
                description="I decided to hire a mind-reader.\nHis job is to ask you questions and figure out what you are think of.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/akihelp",
                inline=True
            )
            embed.set_footer(text="He's pretty great and also slightly UNDEFEATABLE")
            await ctx.send(embed=embed)

        elif about.lower() == 'riddle' or about.lower() == 'riddles':
            embed = nextcord.Embed(
                title="Help Riddle",
                description="Gives you a cool riddle (that totally isn't lame)",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"Use /riddle\nSee if you can answer 'em or not!",
                inline=True
            )
            await ctx.send(embed=embed)

        elif about.lower() == 'guessthemovie' or about.lower() == 'gtm':
            embed = nextcord.Embed(
                title="Help Guess the Movie",
                description="Basically, I give you a bunch of emojis and you gotta guess the movie!\nYes, that must have been so hard to figure out...",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/guessthemovie",
                inline=True
            )
            embed.set_footer(text="I still can't guess the movies tho...")
            await ctx.send(embed=embed)

        elif about.lower() == 'whosthatpokemon' or about.lower() == 'wtp':
            embed = nextcord.Embed(
                title="Help Whos That Pokemon",
                description="Welcome to who's that mutated being.\nWait a minute...\nWhat do you mean those aren't my lines?\nAnyway, you just gotta guess the mutated pokemon I display!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/whosthatpokemon",
                inline=True
            )
            embed.set_footer(text="Stop bothering me I def didn't say anything wrong")
            await ctx.send(embed=embed)

        elif about.lower() == 'guess':
            embed = nextcord.Embed(
                title="Help Guess",
                description="Let's you play guess the number between literally any two numbers.\nBetween 1 and 10000\nLmao",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/guess <lowerboundary> <upperboundary>\nThen you just guess ig...",
                inline=True
            )
            embed.set_footer(text="Bet you can't beat my dev Zero in 1 - 10000")
            await ctx.send(embed=embed)

        elif about.lower() == 'rps':
            embed = nextcord.Embed(title="Help RPS",
                                   description="You can either play:",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Single player:",
                value=f"Use /rps <rock/paper/scissors> to play against me, or",
                inline=True
            )
            embed.add_field(
                name="Multi player:",
                value=f"Use /rps @<useryouwanttodefeat> to play against them.",
                inline=True
            )
            embed.set_footer(text="Its a great game!")
            await ctx.send(embed=embed)

        elif about.lower() == 'oddeve':
            embed = nextcord.Embed(title="Help OddEve",
                                   description="You can either play:",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Single player:",
                value=f"Use /oddeve <odd/even> to play against me.",
                inline=True)
            embed.add_field(
                name="Multi player:",
                value=f"Use /oddeve <useryouwanttodefeat> to play against them.",
                inline=True
            )
            embed.set_footer(text="Its a great game!")
            await ctx.send(embed=embed)

        elif about.lower() == 'wordhunt' or about.lower() == 'wh':
            embed = nextcord.Embed(title="Help Wordhunt",
                                   description="Basically, you get a 9x9 grid with letters and 75 seconds.\nYou need to find as many words as possible.\nThey can be stright, sleeping or even diagnol.\nThe one who finds most words wins!",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"Use /wordhunt",
                inline=True)
            embed.set_footer(text=f"Need something harder? Try /extremehunt")
            await ctx.send(embed=embed)

        elif about.lower() == 'extremehunt' or about.lower() == 'eh':
            embed = nextcord.Embed(title="Help Wordhunt",
                                   description="Basically, you get a 9x9 grid with letters but 60 seconds.\nYou need to find really, really long words.\nThey can be stright, sleeping or even diagnol.\nThe one who finds the longest word wins!",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"Use /extremehunt",
                inline=True)
            embed.set_footer(text=f"Need something easier? Try /wordhunt")
            await ctx.send(embed=embed)

        elif about.lower() == 'scramble':
            embed = nextcord.Embed(title="Help Scramble",
                                   description="An easy game where I give you a scrambled word and you gotta unscramble it.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"Use /scramble",
                inline=True)
            embed.set_footer(text=f"Me wen bored...")
            await ctx.send(embed=embed)

        elif about.lower() == 'hangman' or about.lower() == 'hm':
            embed = nextcord.Embed(title="Help Hangman",
                                   description="I will show you the number of letters in a hidden word.\nYou need to guess which letters it has.\nEverytime you guess correctly, I reveal those letters in the word.\nEverytime you fail, the man comes closer to death.\nYou can only fail 6 times...",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"Use /hangman",
                inline=True)
            embed.set_footer(text=f"Hopefully you succeed")
            await ctx.send(embed=embed)

        elif about.lower() == 'passthebomb' or about.lower() == 'ptb':
            embed = nextcord.Embed(title="Help Pass The Bomb",
                                   description="For some reason, a rando decided to send you and your friends a bomb as a present.\nThe only way to NOT get blown up is typing a word according to what I tell you.\nLast man standing wins.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"Use /passthebomb",
                inline=True)
            embed.set_footer(text=f"Ima be honest with you, not exploding is a very gud idea")
            await ctx.send(embed=embed)

        elif about.lower() == 'typeracer' or about.lower() == 'typerace' or about.lower() == 'tr':
            embed = nextcord.Embed(title="Help Typeracer",
                                   description="Race against your friends to prove your speed.\nYou will be given a sentence to type out.\nOnce the race ends you will get your stats...",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"Use /typerace",
                inline=True)
            embed.set_footer(text=f"Im fast af boi")
            await ctx.send(embed=embed)

        elif about.lower() == 'pingset' or about.lower() == 'pingsettings':
            embed = nextcord.Embed(
                title="Help Ping Settings",
                description="This allows/ stops Chad from using pings in your server.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/pingsettings <trueorfalse>.\nA very, very useful command indeed!",
                inline=True
            )
            embed.set_footer(text="Now no more Chad annoying you with pings eyyy")
            await ctx.send(embed=embed)

        else:
            embed = nextcord.Embed(
                title="Noice",
                description=f"You ask me for help, but I can't help you\nCause {about} isn't a part of my awesome features",
                color=nextcord.Color.green())
            embed.set_footer(text=f"Try /help without anything after it")
            await ctx.send(embed=embed)

    @commands.command(aliases=['welp', 'Help'])
    async def help(self, ctx, command=None):
        if command is None:
            embed = nextcord.Embed(title="Help", color=nextcord.Color.random())
            embed.add_field(name="Utilities",
                            value=f"`{ctx.prefix}help utilities`",
                            inline=True)
            embed.add_field(name="Moderation",
                            value=f"`{ctx.prefix}help moderation`",
                            inline=True)
            embed.add_field(name="Information",
                            value=f"`{ctx.prefix}help information`",
                            inline=True)
            embed.add_field(name="Nerd",
                            value=f"`{ctx.prefix}help nerd`",
                            inline=True)
            embed.add_field(name="Fun", value=f"`{ctx.prefix}help fun`", inline=True)
            embed.add_field(name="Games", value=f"`{ctx.prefix}help games`", inline=True)
            embed.add_field(
                name=f"Most Important Commands",
                value=f"Prefix:\n{ctx.prefix}help prefix\n\nInvite to other servers:\n{ctx.prefix}help invite\n\nSupport Server:\n{ctx.prefix}help support\n\nDonations:\n{ctx.prefix}help patreon",
                inline=False)
            embed.set_thumbnail(url=ctx.author.avatar.url)
            embed.set_footer(text=f"Ping me if u want to know your server prefix!")
            await ctx.send(embed=embed)
            return

        elif command.lower() == "utilities" or command.lower() == "utils":
            page = 1
            pages = 4
            help_utils_1 = nextcord.Embed(title="Utilities")
            help_utils_1.add_field(
                name="Ping",
                value=f"This allows you to check my ping.\n{ctx.prefix}help ping")
            help_utils_1.add_field(
                name="MakeRole",
                value=f"Makes a new role in the server for you.\n{ctx.prefix}help makerole",
                inline=False)
            help_utils_1.add_field(
                name="AddRole",
                value=f"Gives a chosen user the required role.\n{ctx.prefix}help addrole",
                inline=False)
            help_utils_1.add_field(
                name="EditRole",
                value=f"Edits an existing role in the server.\n{ctx.prefix}help editrole",
                inline=False)
            help_utils_1.add_field(
                name="RemoveRole",
                value=f"Takes away the required role from a chosen user.\n{ctx.prefix}help removerole",
                inline=False)
            help_utils_1.add_field(
                name="DeleteRole",
                value=f"Deletes the required role in the server.\n{ctx.prefix}help deleterole",
                inline=False)
            help_utils_1.set_footer(text="Page 1 of 4")
            help_utils_1.color = nextcord.Color.random()

            help_utils_2 = nextcord.Embed(title="Utilities")
            help_utils_2.add_field(
                name="UserInfo",
                value=f"Gives some information about the member specified...\n{ctx.prefix}help userinfo",
                inline=False)
            help_utils_2.add_field(
                name="ServerInfo",
                value=f"Provides some information about the server.\n{ctx.prefix}help serverinfo",
                inline=False)
            help_utils_2.add_field(
                name="Robmoji",
                value=f"Robs an emoji! Takes an emoji from any other server and uploads it your own server so everyone else can use it!\n{ctx.prefix}help robmoji",
                inline=False)
            help_utils_2.add_field(
                name="Nick",
                value=f"Change nicknames in the server by using this feature.\n{ctx.prefix}help nick",
                inline=False)
            help_utils_2.add_field(
                name="Afk",
                value=f"Shows other people you are afk for some random reason.\n{ctx.prefix}help afk",
                inline=False)
            help_utils_2.color = nextcord.Color.random()
            help_utils_2.set_footer(text="Page 2 of 4")

            help_utils_3 = nextcord.Embed(title="Utilities")
            help_utils_3.add_field(
                name="Reminder",
                value=f"Remind yourself to do something at a certain time.\n{ctx.prefix}help remind",
                inline=False)
            help_utils_3.add_field(
                name="Snipe",
                value=f"Allows you to restore the last deleted message of the channel.\n{ctx.prefix}help snipe",
                inline=False)
            help_utils_3.add_field(
                name="Snowflake",
                value=f"Find out the creation date of ANYTHING with its ID.",
                inline=False)
            help_utils_3.add_field(
                name="About",
                value=f"Tells you something more about ME! Totally not conceited.\n{ctx.prefix}help about",
                inline=False)
            help_utils_3.add_field(
                name="Vote",
                value=f"Allows you to vote for me!\n{ctx.prefix}help vote",
                inline=False)
            help_utils_3.add_field(
                name="Invite",
                value=f"Helps you invite me to your other servers.\n{ctx.prefix}help invite",
                inline=False)
            help_utils_3.set_footer(text="Page 3 of 4")
            help_utils_3.color = nextcord.Color.random()

            help_utils_4 = nextcord.Embed(title="Utilities")
            help_utils_4.add_field(
                name="ServerLink",
                value=f"Use this to get an invite link for this server!\n{ctx.prefix}help serverlink",
                inline=False)
            help_utils_4.add_field(
                name="Suggest",
                value=f"Allows you to make a suggestion on my working.\n{ctx.prefix}help suggest",
                inline=False)
            help_utils_4.add_field(
                name="Complain",
                value=f"Allows you to complain about my working.\n{ctx.prefix}help complain",
                inline=False)
            help_utils_4.add_field(
                name="Website",
                value=f"Takes you to my devs' website!\n{ctx.prefix}help website",
                inline=False)
            help_utils_4.add_field(
                name="Patreon",
                value=f"Gives you my Patreon link so you can donate to my cause!\n{ctx.prefix}help patreon",
                inline=False)
            help_utils_4.set_footer(text="Page 4 of 4")
            help_utils_4.color = nextcord.Color.random()

            buttons = [
                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                              disabled=False),
                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                              disabled=False),
            ]
            action_row = create_actionrow(*buttons)

            util_message = await ctx.send(embed=help_utils_1, components=[action_row])

            while True:
                try:
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=util_message, timeout=300)
                    while response.author != ctx.author:
                        await response.reply("This ain't your button fool", hidden=True)
                        response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                              timeout=2)

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
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row = create_actionrow(*buttons_left_disabled)
                            await response.edit_origin(embed=help_utils_1, components=[action_row])

                        except:
                            pass
                    elif page == 2:
                        try:
                            buttons_normal = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row2 = create_actionrow(*buttons_normal)
                            await response.edit_origin(embed=help_utils_2, components=[action_row2])

                        except:
                            pass
                    elif page == 3:
                        try:
                            buttons_normal = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row3 = create_actionrow(*buttons_normal)
                            await response.edit_origin(embed=help_utils_3, components=[action_row3])

                        except:
                            pass
                    elif page == 4:
                        try:
                            buttons_right_disabled = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=True),
                            ]
                            action_row4 = create_actionrow(*buttons_right_disabled)
                            await response.edit_origin(embed=help_utils_4, components=[action_row4])

                        except:
                            pass
                    pass
                except asyncio.TimeoutError:

                    components = util_message.components
                    for row in components:
                        for component in row["components"]:
                            component["disabled"] = True
                        return components

                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=util_message)
                    buttons_all_disabled = [
                        create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                      disabled=True),
                    ]
                    action_row = create_actionrow(*buttons_all_disabled)
                    await response.edit_origin(components=[action_row])

        elif command.lower() == "moderation" or command.lower() == "mod":
            page = 1
            pages = 3
            help_mod_1 = nextcord.Embed(title="Moderation")
            help_mod_1.add_field(
                name="Prefix",
                value=f"Shows you my prefix in this server and allows you to change it.\n{ctx.prefix}help prefix",
                inline=False)
            help_mod_1.add_field(
                name="Slowmode",
                value=f"Allows moderators to enable/disable slowmode.\n{ctx.prefix}help slowmode",
                inline=False)
            help_mod_1.add_field(
                name="Blacklist",
                value=f"Blacklists a user.\n{ctx.prefix}help blacklist",
                inline=False)
            help_mod_1.add_field(
                name="Unblacklist",
                value=f"Unblacklists a user.\n{ctx.prefix}help unblacklist",
                inline=False)
            help_mod_1.add_field(
                name="Clear",
                value=f"Clears messages in a channel.\n{ctx.prefix}help clear",
                inline=False)
            help_mod_1.set_footer(text="Page 1 of 3")
            help_mod_1.color = nextcord.Color.random()

            help_mod_2 = nextcord.Embed(title="Moderation")
            help_mod_2.add_field(
                name="Warn",
                value=f"Gives a warning to a user. Better use coming soon!\n{ctx.prefix}help warn",
                inline=False)
            help_mod_2.add_field(
                name="UserWarn",
                value=f"Displays the history of warnings given to a user.\n{ctx.prefix}help userwarn",
                inline=False)
            help_mod_2.add_field(
                name="RemoveWarn",
                value=f"Removes one of, or all of, the warnings given to a user.\n{ctx.prefix}help removewarn",
                inline=False)
            help_mod_2.add_field(
                name="Unmute",
                value=f"Unmutes a user, thus allowing then to type.\n{ctx.prefix}help unmute",
                inline=False)
            help_mod_2.add_field(
                name="Tempmute",
                value=f"Stops the user from typing in the server TEMPORARILY.\n{ctx.prefix}help tempmute",
                inline=False)
            help_mod_2.add_field(
                name="Mute",
                value=f"Stops the user from typing in the server PERMANENTLY (or until unmute).\n{ctx.prefix}help mute",
                inline=False)
            help_mod_2.set_footer(text="Page 2 of 3")
            help_mod_2.color = nextcord.Color.random()

            help_mod_3 = nextcord.Embed(title="Moderation")
            help_mod_3.add_field(
                name="Kick",
                value=f"Kicks the specified user from the server.\n{ctx.prefix}help kick",
                inline=False)
            help_mod_3.add_field(
                name="Unban",
                value=f"Unbans users, obviously.\n{ctx.prefix}help unban",
                inline=False)
            help_mod_3.add_field(
                name="Tempban",
                value=f"Bans users, TEMPORARILY.\n{ctx.prefix}help tempban",
                inline=False)
            help_mod_3.add_field(
                name="Ban",
                value=f"Bans users, like, DUH.\n{ctx.prefix}help ban",
                inline=False)
            help_mod_3.set_footer(text="Page 3 of 3")
            help_mod_3.color = nextcord.Color.random()

            buttons = [
                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                              disabled=False),
                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                              disabled=False),
            ]
            action_row = create_actionrow(*buttons)

            mod_message = await ctx.send(embed=help_mod_1, components=[action_row])

            while True:
                try:
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=mod_message, timeout=300)
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
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row = create_actionrow(*buttons_left_disabled)
                            await response.edit_origin(embed=help_mod_1, components=[action_row])

                        except:
                            pass
                    elif page == 2:
                        try:
                            buttons_normal = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row2 = create_actionrow(*buttons_normal)
                            await response.edit_origin(embed=help_mod_2, components=[action_row2])

                        except:
                            pass

                    elif page == 3:
                        try:
                            buttons_right_disabled = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=True),
                            ]
                            action_row3 = create_actionrow(*buttons_right_disabled)
                            await response.edit_origin(embed=help_mod_3, components=[action_row3])

                        except:
                            pass
                    pass
                except asyncio.TimeoutError:
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=mod_message)
                    buttons_all_disabled = [
                        create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                      disabled=True),
                    ]
                    action_row = create_actionrow(*buttons_all_disabled)
                    await response.edit_origin(components=[action_row])

        elif command.lower() == "information" or command.lower() == "info":
            page = 1
            pages = 2
            help_info_1 = nextcord.Embed(title="Information")
            help_info_1.add_field(
                name="Dictionary",
                value=f"Finds dictionary meanings, synonyms and antonyms.\n{ctx.prefix}help dictionary",
                inline=False)
            help_info_1.add_field(
                name="Translate",
                value=f"Translates a word into any language needed. (As long as we have it :sweat_smile:)\n{ctx.prefix}help translate",
                inline=False)
            help_info_1.add_field(
                name="Google",
                value=f"Allows you to google anything you want.\n{ctx.prefix}help google",
                inline=False)
            help_info_1.add_field(
                name="Let Me Google That For You",
                value=f"Uses the LMGTFY API to find the answer to your queries.\n{ctx.prefix}help lmgtfy",
                inline=False)
            help_info_1.set_footer(text="Page 1 of 2")
            help_info_1.color = nextcord.Color.random()

            help_info_2 = nextcord.Embed(title="Information")
            help_info_2.add_field(
                name="Weather",
                value=f"Gives you the present weather of a place.\n{ctx.prefix}help weather",
                inline=False)
            help_info_2.add_field(
                name="Wiki",
                value=f"Searches up the Wikipedia for you.\n{ctx.prefix}help wiki",
                inline=False)
            help_info_2.add_field(
                name="UrbanDictionary",
                value=f"Allows you to access the Urban Dictionary.\n{ctx.prefix}help urban",
                inline=False)
            help_info_2.add_field(
                name="Youtube",
                value=f"Let's you use YouTube through discord itself!\n{ctx.prefix}help youtube",
                inline=False)
            help_info_2.set_footer(text="Page 2 of 2")
            help_info_2.color = nextcord.Color.random()

            buttons = [
                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                              disabled=False),
                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                              disabled=False),
            ]
            action_row = create_actionrow(*buttons)

            info_message = await ctx.send(embed=help_info_1, components=[action_row])

            while True:
                try:
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=info_message, timeout=300)
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
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row = create_actionrow(*buttons_left_disabled)
                            await response.edit_origin(embed=help_info_1, components=[action_row])

                        except:
                            pass

                    elif page == 2:
                        try:
                            buttons_right_disabled = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=True),
                            ]
                            action_row2 = create_actionrow(*buttons_right_disabled)
                            await response.edit_origin(embed=help_info_2, components=[action_row2])

                        except:
                            pass
                    pass
                except asyncio.TimeoutError:
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=info_message)
                    buttons_all_disabled = [
                        create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                      disabled=True),
                    ]
                    action_row = create_actionrow(*buttons_all_disabled)
                    await response.edit_origin(components=[action_row])

        elif command.lower() == "nerd":
            page = 1
            pages = 4
            help_nerd_1 = nextcord.Embed(title="Nerd")
            help_nerd_1.add_field(
                name="Add",
                value=f"Adds numbers for you.\n{ctx.prefix}help add",
                inline=False)
            help_nerd_1.add_field(
                name="Subtract",
                value=f"Subtracts numbers for you.\n{ctx.prefix}help subtract",
                inline=False)
            help_nerd_1.add_field(
                name="Multiply",
                value=f"Multiplies numbers for you.\n{ctx.prefix}help multiply",
                inline=False)
            help_nerd_1.add_field(
                name="Divide",
                value=f"Divides to numbers for you.\n{ctx.prefix}help divide",
                inline=False)
            help_nerd_1.set_footer(text="Page 1 of 4")
            help_nerd_1.color = nextcord.Color.random()

            help_nerd_2 = nextcord.Embed(title="Nerd")
            help_nerd_2.add_field(
                name="Square",
                value=f"Gets the square of a number for you.\n{ctx.prefix}help square",
                inline=False)
            help_nerd_2.add_field(
                name="Cube",
                value=f"Gets the cube of a number for you\n{ctx.prefix}help cube",
                inline=False)
            help_nerd_2.add_field(
                name="Square Root",
                value=f"Gets the square root of a number for you.\n{ctx.prefix}help sqrt",
                inline=False)
            help_nerd_2.add_field(
                name="Cube Root",
                value=f"Gets the cube root of a number for you.\n{ctx.prefix}help cbrt",
                inline=False)
            help_nerd_2.add_field(
                name="Power",
                value=f"Gets any power of any number for you.\n{ctx.prefix}help power",
                inline=False)
            help_nerd_2.add_field(
                name="Root",
                value=f"Gets any root of any number for you.\n{ctx.prefix}help root",
                inline=False)
            help_nerd_2.set_footer(text="Page 2 of 4")
            help_nerd_2.color = nextcord.Color.random()

            help_nerd_3 = nextcord.Embed(title="Nerd")
            help_nerd_3.add_field(
                name="Perimeter",
                value=f"Gets the perimeter of certain shapes for you.\n{ctx.prefix}help perimeter",
                inline=False)
            help_nerd_3.add_field(
                name="Area",
                value=f"Gets the area of certain shapes for you.\n{ctx.prefix}help area",
                inline=False)
            help_nerd_3.add_field(
                name="Ask A Question",
                value=f"Allows you to ask me any random question.\n{ctx.prefix}help question",
                inline=False)

            help_nerd_3.set_footer(text="Page 3 of 4")
            help_nerd_3.color = nextcord.Color.random()

            help_nerd_4 = nextcord.Embed(title="Nerd")
            help_nerd_4.add_field(
                name="Trig",
                value=f"Gives you some info about trignometric functions.\n{ctx.prefix}trig",
                inline=False)
            help_nerd_4.add_field(
                name="Sin",
                value=f"Gives you info about sin.\n{ctx.prefix}sin",
                inline=False)
            help_nerd_4.add_field(
                name="Cos",
                value=f"Gives you info about cos.\n{ctx.prefix}cos",
                inline=False)
            help_nerd_4.add_field(
                name="Tan",
                value=f"Gives you info about tan.\n{ctx.prefix}tan",
                inline=False)
            help_nerd_4.add_field(
                name="Sec",
                value=f"Gives you info about sec.\n{ctx.prefix}sec",
                inline=False)
            help_nerd_4.add_field(
                name="Cosec",
                value=f"Gives you info about cosec.\n{ctx.prefix}cosec",
                inline=False)
            help_nerd_4.add_field(
                name="Cot",
                value=f"Gives you info about cot.\n{ctx.prefix}cot",
                inline=False)

            help_nerd_4.set_footer(text="Page 4 of 4")
            help_nerd_4.color = nextcord.Color.random()

            buttons = [
                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                              disabled=False),
                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                              disabled=False),
            ]
            action_row = create_actionrow(*buttons)

            nerd_message = await ctx.send(embed=help_nerd_1, components=[action_row])

            while True:
                try:
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=nerd_message, timeout=300)
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
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row = create_actionrow(*buttons_left_disabled)
                            await response.edit_origin(embed=help_nerd_1, components=[action_row])

                        except:
                            pass
                    elif page == 2:
                        try:
                            buttons_normal = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row2 = create_actionrow(*buttons_normal)
                            await response.edit_origin(embed=help_nerd_2, components=[action_row2])

                        except:
                            pass
                    elif page == 3:
                        try:
                            buttons_normal = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row3 = create_actionrow(*buttons_normal)
                            await response.edit_origin(embed=help_nerd_3, components=[action_row3])

                        except:
                            pass
                    elif page == 4:
                        try:
                            buttons_right_disabled = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=True),
                            ]
                            action_row4 = create_actionrow(*buttons_right_disabled)
                            await response.edit_origin(embed=help_nerd_4, components=[action_row4])

                        except:
                            pass
                    pass
                except asyncio.TimeoutError:
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=nerd_message)
                    buttons_all_disabled = [
                        create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                      disabled=True),
                    ]
                    action_row = create_actionrow(*buttons_all_disabled)
                    await response.edit_origin(components=[action_row])

        elif command.lower() == "fun":
            page = 1
            pages = 5
            help_fun_1 = nextcord.Embed(title="Fun")
            help_fun_1.add_field(
                name="Ask",
                value=f"Honestly answers any question you may have.\n{ctx.prefix}help ask",
                inline=False)
            help_fun_1.add_field(
                name="EpicGamerRate",
                value=f"Tells you how EPIC you are at gaming.\n{ctx.prefix}help epicgamerrate",
                inline=False)
            help_fun_1.add_field(
                name="SimpRate",
                value=f"Tells you how much you are simping (ans sometimes, WHO you are simping :smirk:).\n{ctx.prefix}help simprate",
                inline=False)
            help_fun_1.add_field(
                name="Poll",
                value=f"Creates a poll for you.\n{ctx.prefix}help poll",
                inline=False)
            help_fun_1.set_footer(text="Page 1 of 5")
            help_fun_1.color = nextcord.Color.random()

            help_fun_2 = nextcord.Embed(title="Fun")
            help_fun_2.add_field(
                name="Script",
                value=f"Translates the Zero&One script.\n{ctx.prefix}help script",
                inline=False)
            help_fun_2.add_field(
                name="ASCII",
                value=f"Creates a cool ASCII art for you.\n{ctx.prefix}help ascii",
                inline=False)
            help_fun_2.add_field(
                name="Binary",
                value=f"Converts a message to binary as zeros and ones are cool.\n{ctx.prefix}help binary",
                inline=False)
            help_fun_2.add_field(
                name="Emojify",
                value=f"Turns your text into emojis!\n{ctx.prefix}help emojify",
                inline=False)
            help_fun_2.add_field(
                name="Spoilify",
                value=f"Spoils your message just for you! (Its nicer than it sounds)\n{ctx.prefix}help spoilify",
                inline=False)
            help_fun_2.set_footer(text="Page 2 of 5")
            help_fun_2.color = nextcord.Color.random()

            help_fun_3 = nextcord.Embed(title="Fun")
            help_fun_3.add_field(
                name="Act",
                value=f"Makes me act as though I'm another user...\n{ctx.prefix}help act",
                inline=False)
            help_fun_3.add_field(
                name="Choose",
                value=f"Helps you choose amongst some tough choices.\n{ctx.prefix}help choose",
                inline=False)
            help_fun_3.add_field(
                name="Hack",
                value=f"Hacks the required user. WARNING: Only to be used under unavoidable circumstances.\n{ctx.prefix}help hack",
                inline=False)
            help_fun_3.add_field(
                name="Gif",
                value=f"Allows you to search for GIFs or send random gifs from GIPHY.\n{ctx.prefix}help gif",
                inline=False)
            help_fun_3.add_field(
                name="ImageMemes",
                value=f"Makes some very funny image memes for you.\n{ctx.prefix}help imagememes",
                inline=False)
            help_fun_3.set_footer(text="Page 3 of 5")
            help_fun_3.color = nextcord.Color.random()

            help_fun_4 = nextcord.Embed(title="Fun")
            help_fun_4.add_field(
                name="VCMeme",
                value=f"Lets you have some fun with the people in your VC.\n{ctx.prefix}help vcmeme",
                inline=False)
            help_fun_4.add_field(
                name="Shoo",
                value=f"Kicks me out of a VC cause bandwith don't come for free.\n{ctx.prefix}shoo",
                inline=False)
            help_fun_4.add_field(
                name="Pause",
                value=f"Pauses my VC activity.\n{ctx.prefix}pause",
                inline=False)
            help_fun_4.add_field(
                name="Resume",
                value=f"Resumes my VC shenanigans.\n{ctx.prefix}resume",
                inline=False)
            help_fun_4.add_field(
                name="Stop",
                value=f"Stop me from doing what I'm doing in a VC.\n{ctx.prefix}stop",
                inline=False)
            help_fun_4.set_footer(text="Page 4 of 5")
            help_fun_4.color = nextcord.Color.random()

            help_fun_5 = nextcord.Embed(title="Fun")
            help_fun_5.add_field(
                name="Quote",
                value=f"Allows you to quote the sayings of your fellow human beings. (Unless you use a bot name)\n{ctx.prefix}help quote",
                inline=False)
            help_fun_5.add_field(
                name="Kill",
                value=f"Kill your friends... But minecraft style\n{ctx.prefix}help kill",
                inline=False)
            help_fun_5.add_field(
                name="Roast",
                value=f"Respect? Nah mate...\n{ctx.prefix}help roast",
                inline=False)
            help_fun_5.add_field(
                name="Joke",
                value=f"Tells you a joke to lighten your day! (or spoil it :rofl:)\n{ctx.prefix}help joke",
                inline=False)
            help_fun_5.add_field(
                name="Meme",
                value=f"Gives you memes **cause**.\n{ctx.prefix}help meme",
                inline=False)
            help_fun_5.set_footer(text="Page 5 of 5")
            help_fun_5.color = nextcord.Color.random()

            buttons = [
                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                              disabled=False),
                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                              disabled=False),
            ]
            action_row = create_actionrow(*buttons)

            fun_message = await ctx.send(embed=help_fun_1, components=[action_row])

            while True:
                try:
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=fun_message, timeout=300)
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
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row = create_actionrow(*buttons_left_disabled)
                            await response.edit_origin(embed=help_fun_1, components=[action_row])

                        except:
                            pass
                    elif page == 2:
                        try:
                            buttons_normal = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row2 = create_actionrow(*buttons_normal)
                            await response.edit_origin(embed=help_fun_2, components=[action_row2])

                        except:
                            pass
                    elif page == 3:
                        try:
                            buttons_normal = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row3 = create_actionrow(*buttons_normal)
                            await response.edit_origin(embed=help_fun_3, components=[action_row3])

                        except:
                            pass

                    elif page == 4:
                        try:
                            buttons_normal = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row4 = create_actionrow(*buttons_normal)
                            await response.edit_origin(embed=help_fun_4, components=[action_row4])

                        except:
                            pass

                    elif page == 5:
                        try:
                            buttons_right_disabled = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=True),
                            ]
                            action_row5 = create_actionrow(*buttons_right_disabled)
                            await response.edit_origin(embed=help_fun_5, components=[action_row5])

                        except:
                            pass
                    pass
                except asyncio.TimeoutError:
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=fun_message)
                    buttons_all_disabled = [
                        create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                      disabled=True),
                    ]
                    action_row = create_actionrow(*buttons_all_disabled)
                    await response.edit_origin(components=[action_row])

        elif command.lower() == "games":
            page = 1
            pages = 3
            help_games_1 = nextcord.Embed(title="Games")
            help_games_1.add_field(
                name="Amogus",
                value=f"Find out if you can get the imposter in time!\n{ctx.prefix}help amogus",
                inline=False)
            help_games_1.add_field(
                name="Akinator",
                value=f"Check out whether you can defeat our mind-reader.\n{ctx.prefix}help aki",
                inline=False)
            help_games_1.add_field(
                name="Guess the Movie",
                value=f"Will you be able to guess the movie with the emojis I give you?\n{ctx.prefix}help guessthemovie",
                inline=False)
            help_games_1.add_field(
                name="Riddle",
                value=f"Gives you a riddle that you must answer. (Please don't kick me, I like those riddles!)\n{ctx.prefix}help riddle",
                inline=False)
            help_games_1.add_field(
                name="Who's That Pokémon",
                value=f"Test your knowledge of Pokémon!\n{ctx.prefix}help whosthatpokemon",
                inline=False)
            help_games_1.set_footer(text="Page 1 of 3")
            help_games_1.color = nextcord.Color.random()

            help_games_2 = nextcord.Embed(title="Games")
            help_games_2.add_field(
                name="Coinflip",
                value=f"Allows you to try your luck with the coin!\n{ctx.prefix}help coinflip",
                inline=False)
            help_games_2.add_field(
                name="Dice",
                value=f"Rolls a dice, which is useful for bets.\n{ctx.prefix}help dice",
                inline=False)
            help_games_2.add_field(
                name="Guess",
                value=f"Guess a number within any range.\n{ctx.prefix}help guess",
                inline=False)
            help_games_2.add_field(
                name="Rps",
                value=f"Lets you play rock paper scissor with me **OR** your friends.\n{ctx.prefix}help rps",
                inline=False)
            help_games_2.add_field(
                name="OddEve",
                value=f"Lets you play odd eve with me **OR** your friends.\n{ctx.prefix}help oddeve",
                inline=False)
            help_games_2.set_footer(text="Page 2 of 3")
            help_games_2.color = nextcord.Color.random()

            help_games_3 = nextcord.Embed(title="Games")
            help_games_3.add_field(
                name="Wordhunt",
                value=f"Test your skill in finding hidden words.\n{ctx.prefix}help wordhunt",
                inline=False)
            help_games_3.add_field(
                name="Extremehunt",
                value=f"A much more difficult version of wordhunt itself!\n{ctx.prefix}help extremehunt",
                inline=False)
            help_games_3.add_field(
                name="Scramble",
                value=f"Unscramble the word that I have scrambled for you.\n{ctx.prefix}help scramble",
                inline=False)
            help_games_3.add_field(
                name="Hangman",
                value=f"Save an innocent man by finding the letters in my hidden word!\n{ctx.prefix}help hangman",
                inline=False)
            help_games_3.add_field(
                name="PassTheBomb",
                value=f"Stop the bomb from exploding in your facing by giving me a suitable word.\n{ctx.prefix}help passthebomb",
                inline=False)
            help_games_3.add_field(
                name="Typeracer",
                value=f"Race against your friends in a quest to type stuff.\n{ctx.prefix}help typerace",
                inline=False)
            help_games_3.set_footer(text="Page 3 of 3")
            help_games_3.color = nextcord.Color.random()

            buttons = [
                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                              disabled=True),
                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                              disabled=False),
                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                              disabled=False),
            ]
            action_row = create_actionrow(*buttons)

            games_message = await ctx.send(embed=help_games_1, components=[action_row])

            while True:
                try:
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=games_message, timeout=300)
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
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row = create_actionrow(*buttons_left_disabled)
                            await response.edit_origin(embed=help_games_1, components=[action_row])

                        except:
                            pass
                    elif page == 2:
                        try:
                            buttons_normal = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=False),
                            ]
                            action_row2 = create_actionrow(*buttons_normal)
                            await response.edit_origin(embed=help_games_2, components=[action_row2])

                        except:
                            pass

                    elif page == 3:
                        try:
                            buttons_right_disabled = [
                                create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                              disabled=False),
                                create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                              disabled=True),
                                create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                              disabled=True),
                            ]
                            action_row3 = create_actionrow(*buttons_right_disabled)
                            await response.edit_origin(embed=help_games_3, components=[action_row3])

                        except:
                            pass
                    pass
                except asyncio.TimeoutError:
                    response: ComponentContext = await wait_for_component(self.bot, components=action_row,
                                                                          messages=games_message)
                    buttons_all_disabled = [
                        create_button(style=ButtonStyle.blue, custom_id="big_back", emoji="⏪",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="back", emoji="◀",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="forward", emoji="▶",
                                      disabled=True),
                        create_button(style=ButtonStyle.blue, custom_id="big_forward", emoji="⏩",
                                      disabled=True),
                    ]
                    action_row = create_actionrow(*buttons_all_disabled)
                    await response.edit_origin(components=[action_row])

        elif command.lower() == 'ping':
            embed = nextcord.Embed(
                title="Help Ping",
                description="With this command, you can see how fast I am reacting to your messages in milliseconds.",
                color=nextcord.Color.green())
            embed.add_field(name="Usage:", value=f"{ctx.prefix}ping")
            embed.set_footer(text="I do be very fast u know...")
            await ctx.send(embed=embed)

        elif command.lower() == 'makerole':
            embed = nextcord.Embed(
                title="Help MakeRole",
                description="At last, with just one command, you can make a new role in your server.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}makerole <rolename>\nCause you have the right to be LAZY",
                inline=True
            )
            embed.set_footer(
                text="Only people with manage roles perms can use this so DON'T EVEN TRY, PEASANTS"
            )
            await ctx.send(embed=embed)

        elif command.lower() == 'addrole':
            embed = nextcord.Embed(
                title="Help AddRole",
                description="You can also add roles to your members by just using this one command!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}addrole @<membername> @<rolename>\nSo now you can be LAZIER!",
                inline=True
            )
            embed.set_footer(
                text="Only people with manage roles perms can use this so DON'T EVEN TRY, PEASANTS"
            )
            await ctx.send(embed=embed)


        elif command.lower() == 'editrole':
            embed = nextcord.Embed(
                title="Help EditRole",
                description="Don't like the name of your role?\n Then just use this command to change its name!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"/editrole @<fromrolename> <torolename>\n"
                      f"/editrole @<fromrolename> #<hexdecimal>\n"
                      f"/editrole @<fromrolename> <torolename> #<hexdecimal>\n"
                      f"either will do.",
                inline=True
            )
            embed.set_footer(
                text="Color or colour?"
            )
            await ctx.send(embed=embed)

        elif command.lower() == 'removerole':
            embed = nextcord.Embed(
                title="Help RemoveRole",
                description="If your members misuse their roles then there is only one solution:\n Take the role away from them!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}removerole @<membername> @<rolename>\nBasically making you a dictator...",
                inline=True
            )
            embed.set_footer(
                text="Only people with manage roles perms can use this so DON'T EVEN TRY, PEASANTS"
            )
            await ctx.send(embed=embed)

        elif command.lower() == 'deleterole':
            embed = nextcord.Embed(
                title="Help DeleteRole",
                description="You can also delete roles in your server when the role just becomes useless.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}deleterole @<rolename>\nImagine needing to delete roles ANYWAY...",
                inline=True
            )
            embed.set_footer(
                text="Only people with manage roles perms can use this so DON'T EVEN TRY, PEASANTS"
            )
            await ctx.send(embed=embed)

        elif command.lower() == 'support':
            embed = nextcord.Embed(
                title="Help Support",
                description="Need help with the my commands?\nWanna complain about them?\nMaybe make a suggestion?",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}support\nSo you can visit our support server.",
                inline=True)
            embed.set_footer(text="Get support its good for you")
            await ctx.send(embed=embed)

        elif command.lower() == 'patreon' or command.lower() == 'donate':
            embed = nextcord.Embed(
                title="Help Patreon",
                description="Really pleased with my awesomeness?\nWanna show your love?\nGot a lot of money to burn?",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}patreon\nUse this to donate to me, so that I can be better!",
                inline=True)
            embed.set_footer(text="It's worth it, honestly.")
            await ctx.send(embed=embed)

        elif command.lower() == 'userinfo':
            embed = nextcord.Embed(
                title="Help UserInfo",
                description="Find out about the wierdos who join your servers.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}userinfo @<membername>\n#gettingexposed",
                inline=True)
            embed.set_footer(text="Being a stalker eh?")
            await ctx.send(embed=embed)

        elif command.lower() == 'robmoji':
            embed = nextcord.Embed(
                title="Help RobMoji",
                description="Steal an emoji from another server and make it yours. If a name is not given, it will take the emoji's name. Also pls make sure that you give a name from 2 to 32.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}robmoji emoji name_of_new_emoji\n#MINE!",
                inline=True)
            embed.set_footer(text="Should I call the cops?")
            await ctx.send(embed=embed)

        elif command.lower() == 'serverinfo':
            embed = nextcord.Embed(
                title="Help ServerInfo",
                description="For everything you need to know about your server.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}serverinfo\nNever forget your memories, or your server info.",
                inline=True
            )
            embed.set_footer(text="But seriously, how did you forget?")
            await ctx.send(embed=embed)

        elif command.lower() == 'nick':
            embed = nextcord.Embed(
                title="Help Nick",
                description="Nickname your friends anything you want!\nIt is WAY too easy to do so, with this command.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}nick @<membername> <nickname>\nNow see what you can come up with...",
                inline=True
            )
            embed.set_footer(
                text="Nasty surprise for the poor victim's names *sigh*")
            await ctx.send(embed=embed)

        elif command.lower() == 'afk':
            embed = nextcord.Embed(
                title="Help Afk",
                description="Use this to make people know that your are afk when they ping you.\nUseful to warn people about your afkness!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}afk <reason>\nThis will solve a lot of afk problems...",
                inline=True
            )
            embed.set_footer(text="Why didn't we think of this be4?")
            await ctx.send(embed=embed)

        elif command.lower() == 'remind' or command.lower() == 'reminder':
            embed = nextcord.Embed(
                title="Help Reminder",
                description="Nickname your friends anything you want!\nIt is WAY too easy to do so, with this command.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}remind <time> <thingtoremind>\nThis is specially for people who forget what they were doing in like, 2 seconds",
                inline=True
            )
            embed.set_footer(text="Now you cannot forget ANYTHING")
            await ctx.send(embed=embed)

        elif command.lower() == 'about':
            embed = nextcord.Embed(
                title="Help About",
                description="Get to know a little bit more about me!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}about\nPlease use this :pleading_face:\nMy devs think NO ONE wants to know more about me...",
                inline=True
            )
            embed.set_footer(text="I mean, why not?")
            await ctx.send(embed=embed)

        elif command.lower() == 'vote':
            embed = nextcord.Embed(title="Help Vote",
                                   description="Vote me or perish",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}vote\nSupports me a lot :pleading_face:\nMakes me.... **EVEN MORE POPULAR**",
                inline=True
            )
            embed.set_footer(text="I mean, why not?")
            await ctx.send(embed=embed)

        elif command.lower() == 'invite':
            embed = nextcord.Embed(
                title="Help Invite",
                description="Use this to invite me to your other servers.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}invite\nPlease use this :pleading_face:\nYou. Can't. Get. Enough. Of. Me.",
                inline=True
            )
            embed.set_footer(text="I'm the BEST")
            await ctx.send(embed=embed)

        elif command.lower() == 'serverlink' or command.lower() == 'sl':
            embed = nextcord.Embed(
                title="Help ServerLink",
                description="If you feel to lazy to create an invite to your server, just ask me to do it!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}serverlink\nIts ez to use and time-efficient too!",
                inline=True
            )
            embed.set_footer(text="Anyway I was made to do all the work...")
            await ctx.send(embed=embed)

        elif command.lower() == 'suggest' or command.lower() == 'suggestion':
            embed = nextcord.Embed(
                title="Help Suggest",
                description="Use this to make a suggestion about me, which gets magically transported to the devs themselves",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}suggest\nNow you don't have to join the support server.\nUnless you want more info about updates and stuff.",
                inline=True
            )
            embed.set_footer(text="We are open to suggestions. Once per hor")
            await ctx.send(embed=embed)

        elif command.lower() == 'complain' or command.lower() == 'complaint':
            embed = nextcord.Embed(
                title="Help Complain",
                description="Use this to complain about me and the complaint gets magically transported to the devs themselves",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}complain\nNow you don't have to join the support server.\nUnless you want more info about updates and stuff.",
                inline=True
            )
            embed.set_footer(text="You can only complain once per hour tho.")
            await ctx.send(embed=embed)

        elif command.lower() == 'website':
            embed = nextcord.Embed(
                title="Help Website",
                description="My developers have a website. Go check it out.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}website\nPlease use this :pleading_face:\nIt's not really related to me, but its cool anyway.",
                inline=True
            )
            embed.set_footer(text="See you there!")
            await ctx.send(embed=embed)

        elif command.lower() == 'snipe':
            embed = nextcord.Embed(
                title="Help Snipe",
                description="Find out what the last deleted message in your server was.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}snipe\nNow you can catch your sneaky server members in the act!",
                inline=True
            )
            embed.set_footer(text="More stonx for u")
            await ctx.send(embed=embed)

        elif command.lower() == 'snowflake':
            embed = nextcord.Embed(
                title="Help Snowflake",
                description="Use the ID of anything to find out the date of creation!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}snowflake\nUseful for devs and people who want to know how old stuff is.",
                inline=True
            )
            embed.set_footer(text="More stonx for u")
            await ctx.send(embed=embed)

        elif command.lower() == 'slowmode':
            embed = nextcord.Embed(
                title="Help Slowmode",
                description="Allows you to put or remove a slowmode in your channel.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}slowmode <timeinseconds>\nThat will stop the SPAMMERS",
                inline=True
            )
            embed.set_footer(text="Sad life for spammers.")
            await ctx.send(embed=embed)

        elif command.lower() == 'blacklist':
            embed = nextcord.Embed(
                title="Help Blacklist",
                description="This makes the required member unable to use my commands.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}blacklist @<membername>\nThis is one of the most CRUELLEST punishments possible.",
                inline=True
            )
            embed.set_footer(text="Not using CHAD be SAD")
            await ctx.send(embed=embed)

        elif command.lower() == 'unblacklist':
            embed = nextcord.Embed(
                title="Help Unblacklist",
                description="Removes blacklisted users from the list of naughty people...",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}unblacklist @<membername>\nOnly kindness can make you use this command.",
                inline=True
            )
            embed.set_footer(text="Unblacklisters = Saviours")
            await ctx.send(embed=embed)

        elif command.lower() == 'clear':
            embed = nextcord.Embed(
                title="Help Clear",
                description="Clears the required number of messages in a channel. You can also clear messages of a particular member within a certain number of messages.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}clear <numberofmessages> <optionalmember>\nHelps when your server members just don't want to stop chatting...",
                inline=True
            )
            embed.set_footer(text="Get ERASED")
            await ctx.send(embed=embed)

        elif command.lower() == 'removewarn':
            embed = nextcord.Embed(
                title="Help RemoveWarn",
                description="Used to remove one or all of a users warn.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}lockdown <reason>\nGive the reason to remove, or just type 'all' to remove all warnings.",
                inline=True)
            embed.set_footer(text="Showing mercy gets you killed. You have been warned.")
            await ctx.send(embed=embed)

        elif command.lower() == 'warn':
            embed = nextcord.Embed(title="Help Warn",
                                   description="Gives the rule-breakers a warning!",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}warn <username> <reason>\nOnly for those naughty users who don't like rules.",
                inline=True
            )
            embed.set_footer(text="So you've been warned...")
            await ctx.send(embed=embed)

        elif command.lower() == 'prefix':
            embed = nextcord.Embed(title="Help Prefix",
                                   description="Change dat prefix",
                                   color=nextcord.Color.random())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}prefix <newprefix>\nVery handy for big servers!",
                inline=True
            )
            embed.set_footer(text="Just don't forget what your prefix was...")
            await ctx.send(embed=embed)

        elif command.lower() == 'userwarn':
            embed = nextcord.Embed(
                title="Help UserWarn",
                description="Gives a record of why and how many times a user was warned in the server.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}userwarn @<username>\nNow you have a record of their crimes.",
                inline=True
            )
            embed.set_footer(text="*Evil laughter from admins*")
            await ctx.send(embed=embed)

        elif command.lower() == 'unmute':
            embed = nextcord.Embed(title="Help Unmute",
                                   description="Allows you to unmute a user.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}unmute @<username>\nThis makes the able to talk in your server again.",
                inline=True
            )
            embed.set_footer(text="Support Freedom of Speech")
            await ctx.send(embed=embed)

        elif command.lower() == 'tempmute':
            embed = nextcord.Embed(
                title="Help Tempmute",
                description="Allows you to temporarily mute a user.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}tempmute <timeinseconds>s @<username>\nIf you think you may forget to unmute a user, then I do it for you!",
                inline=True
            )
            embed.set_footer(text="That's one less thing to remember...")
            await ctx.send(embed=embed)

        elif command.lower() == 'mute':
            embed = nextcord.Embed(title="Help Mute",
                                   description="Allows you to mute a user.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}mute @<username>\nNow they can't talk until you allow them too!",
                inline=True
            )
            embed.set_footer(text="Sad life for the muted")
            await ctx.send(embed=embed)

        elif command.lower() == 'kick':
            embed = nextcord.Embed(title="Help Kick",
                                   description="Allows you to kick a user.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}kick @<username>\nSo basically they just get yeeted out.",
                inline=True
            )
            embed.set_footer(text="Get rekt lol")
            await ctx.send(embed=embed)

        elif command.lower() == 'unban':
            embed = nextcord.Embed(title="Help Unban",
                                   description="Allows you to unban a user.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}unban @<username>\nSo that they can return to the server.",
                inline=True
            )
            embed.set_footer(text="Oh look, they're back lol")
            await ctx.send(embed=embed)

        elif command.lower() == 'tempban':
            embed = nextcord.Embed(
                title="Help Tempban",
                description="Allows you to temporarily ban a user.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}tempban <timeinseconds>s @<username>\nIf you really hate someone, and may \"accidentally\" forget to unban them...",
                inline=True
            )
            embed.set_footer(text="That's just sus uk")
            await ctx.send(embed=embed)

        elif command.lower() == 'ban':
            embed = nextcord.Embed(title="Help Ban",
                                   description="Allows you to ban a user.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}ban @<username>\nThey can NEVER COME BACK NOW MWA HA HA HA\nJeez I was only joking",
                inline=True
            )
            embed.set_footer(text="Get banished lmao")
            await ctx.send(embed=embed)

        elif command.lower() == 'dictionary':
            embed = nextcord.Embed(
                title="Help Dictionary",
                description="Lets you access a dictionary through discord!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}dictionary <word>\nWhat you can do is get meanings, synonyms and antonyms!\nThen you type either meanings, synonyms or antonyms.",
                inline=True
            )
            embed.set_footer(text="All for geeky lil nerds!")
            await ctx.send(embed=embed)

        elif command.lower() == 'translate':
            embed = nextcord.Embed(
                title="Help Translate",
                description="Translate a word to any language you want.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}translate <wordtotranslate>\nAnd then you enter the language translate to.",
                inline=True
            )
            embed.set_footer(text="Merci!")
            await ctx.send(embed=embed)

        elif command.lower() == 'google' or command.lower() == 'search':
            embed = nextcord.Embed(
                title="Help Google  ",
                description="Lets you google anything you want",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}google <whatyouwanttogoogle>\nGoogles the thing you enter",
                inline=True
            )
            embed.set_footer(text="Perfect for searching through discord instead of your browser")
            await ctx.send(embed=embed)

        elif command.lower() == 'lmgtfy' or command.lower() == 'letmegooglethatforyou':
            embed = nextcord.Embed(
                title="Help Let Me Google That For You",
                description="Kinda self explainatory...",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}lmgtfy <thinguneedtogoogle>\nAgain, pretty obvious why this command exists.",
                inline=True
            )
            embed.set_footer(text="So basically, an obvious command")
            await ctx.send(embed=embed)

        elif command.lower() == 'weather':
            embed = nextcord.Embed(
                title="Help Weather",
                description="Get the real-time weather of any place!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}search <cityname>\nAny city can be searched for!",
                inline=True)
            embed.set_footer(text="Try searching \"Israel\" lol")
            await ctx.send(embed=embed)

        elif command.lower() == 'wiki':
            embed = nextcord.Embed(title="Help Wiki",
                                   description="Search Wikipedia.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}wiki <whatyouwannasearch>\nCause clearly, google wasn't enough.",
                inline=True
            )
            embed.set_footer(text="Wisdom is in DISCORD PPL")
            await ctx.send(embed=embed)

        elif command.lower() == 'urban':
            embed = nextcord.Embed(
                title="Help UrbanDictionary",
                description="Let's you use the Urban Dictionary (like, obviously).",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}urban <whatyouwannasearch>\nAn interesting place of knowledge.",
                inline=True
            )
            embed.set_footer(
                text="The urban dict be lollers (I mean try searching your own name)")
            await ctx.send(embed=embed)

        elif command.lower() == 'youtube':
            embed = nextcord.Embed(
                title="Help Youtube",
                description="Lets you access YouTube itself through discord!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}youtube <thingyouwannasee>\nSo now you lazy folks don't even need to open your browser!",
                inline=True
            )
            embed.set_footer(text="This is for true legends")
            await ctx.send(embed=embed)

        elif command.lower() == 'add':
            embed = nextcord.Embed(title="Help Add",
                                   description="Adds two or more numbers for you.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}add <number1> <number2> etc...",
                inline=True
            )
            embed.set_footer(text="I can add a lot of stuff tbh")
            await ctx.send(embed=embed)

        elif command.lower() == 'subtract' or command.lower() == 'subs':
            embed = nextcord.Embed(title="Help Subtract",
                                   description="Subtracts only two numbers for you.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}subtract <number1> <number2>",
                inline=True
            )
            embed.set_footer(text="I can subtract a only two numbers for obvious reasons")
            await ctx.send(embed=embed)

        elif command.lower() == 'multiply' or command.lower() == 'multi':
            embed = nextcord.Embed(title="Help Multiply",
                                   description="Multiplication two or more numbers for you.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}mulitply <number1> <number2> etc...",
                inline=True
            )
            embed.set_footer(text="I can multiply a lot of stuff tbh")
            await ctx.send(embed=embed)

        elif command.lower() == 'divide' or command.lower() == 'div':
            embed = nextcord.Embed(title="Help Divide",
                                   description="Divides only two numbers for you.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}divide <number1> <number2>",
                inline=True
            )
            embed.set_footer(text="I can divide a only two numbers for obvious reasons")
            await ctx.send(embed=embed)

        elif command.lower() == 'square':
            embed = nextcord.Embed(title="Help Square",
                                   description="Finds the square of a number for you.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}square <number>",
                inline=True
            )
            embed.set_footer(text="It's pretty straight forward and ded useful")
            await ctx.send(embed=embed)

        elif command.lower() == 'cube':
            embed = nextcord.Embed(title="Help Cube",
                                   description="Finds the cube of a number for you.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}cube <number>",
                inline=True
            )
            embed.set_footer(text="It's pretty straight forward and ded useful")
            await ctx.send(embed=embed)

        elif command.lower() == 'sqrt' or command.lower() == 'squareroot':
            embed = nextcord.Embed(title="Help Square Root",
                                   description="Finds the square root of a number for you.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}squareroot <number>",
                inline=True
            )
            embed.set_footer(text="It's pretty straight forward and ded useful")
            await ctx.send(embed=embed)

        elif command.lower() == 'cbrt' or command.lower() == 'cuberoot':
            embed = nextcord.Embed(title="Help Cube Root",
                                   description="Finds the cube root of a number for you.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}cuberoot <number>",
                inline=True
            )
            embed.set_footer(text="It's pretty straight forward and ded useful")
            await ctx.send(embed=embed)

        elif command.lower() == 'power':
            embed = nextcord.Embed(title="Help Power",
                                   description="Finds any power of any number for you.\nBasically if you need the power of something more than 2 and 3.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}power <number> <power>",
                inline=True
            )
            embed.set_footer(text="An OP function if I do say so myself")
            await ctx.send(embed=embed)

        elif command.lower() == 'root':
            embed = nextcord.Embed(title="Help Root",
                                   description="Finds any root of any number for you.\nBasically if you need the root of something more than 2 and 3.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}root <number> <root>",
                inline=True
            )
            embed.set_footer(text="Another OP function if I do say so myself")
            await ctx.send(embed=embed)

        elif command.lower() == 'perimeter':
            embed = nextcord.Embed(title="Help Perimeter",
                                   description="Finds the perimeters of certain shapes based on the numbers you give.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}perimeter",
                inline=True
            )
            embed.set_footer(text="Its usage is... interesting")
            await ctx.send(embed=embed)

        elif command.lower() == 'area':
            embed = nextcord.Embed(title="Help Area",
                                   description="Finds the areas of certain shapes based on the numbers you give.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}area",
                inline=True
            )
            embed.set_footer(text="Its usage is... interesting")
            await ctx.send(embed=embed)

        elif command.lower() == 'question' or command.lower() == 'aaq':
            embed = nextcord.Embed(title="Help Ask A Question",
                                   description="You ask me a question, I give you it's answer.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}question <question>",
                inline=True
            )
            embed.set_footer(text="Im just wondering how many ppl will fail to use this properly")
            await ctx.send(embed=embed)

        elif command.lower() == 'ask':
            embed = nextcord.Embed(title="Help Ask",
                                   description="Ask me a question and I will give you a carefully considered, totally not chance based answer.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}ask <question>\nI am a beacon of honesty.",
                inline=True
            )
            embed.set_footer(text="I have never failed anyone yet")
            await ctx.send(embed=embed)

        elif command.lower() == 'epicgamerrate':
            embed = nextcord.Embed(
                title="Help epicgamerrate",
                description="Now you can find out how epic you are at gaming.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}epicgamerrate\nThis is totally true btw",
                inline=True)
            embed.set_footer(
                text="It's a perfect way of knowing how good you are!")
            await ctx.send(embed=embed)

        elif command.lower() == 'simprate':
            embed = nextcord.Embed(
                title="Help simprate",
                description="Now you can find out how much you simp.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}simprate\nThis is totally true btw",
                inline=True)
            embed.set_footer(
                text="It's a perfect way of knowing how simpy you are!")
            await ctx.send(embed=embed)

        elif command.lower() == 'poll':
            embed = nextcord.Embed(title="Help Poll",
                                   description="Create a poll to get some votes",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}poll <timeinseconds> <whatyoupollfor>: <optionswithcommas>\nEveryone can just choose what they wanna choose.",
                inline=True
            )
            embed.set_footer(
                text="Use s for seconds, m for mins, h for hours, d for days")
            await ctx.send(embed=embed)


        elif command.lower() == 'script':
            embed = nextcord.Embed(title="Help Script",
                                   description="Translates the ZeroAndOne Script",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}encrypt <stufftoencrypt>\n!decrypt <stufftodecrypt>\nCheck out the way this script works [here](https://secret-message-encoder-decoder.itszeroandone.repl.co/).",
                inline=True
            )
            embed.set_footer(text="You'll love the script.")
            await ctx.send(embed=embed)

        elif command.lower() == 'ascii':
            embed = nextcord.Embed(
                title="Help ASCII",
                description="Turns me into a painter and makes ASCII art.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}ascii <stufftoput>\nI can't really explain it's beauty.",
                inline=True
            )
            embed.set_footer(text="What you put may or may not be what you get")
            await ctx.send(embed=embed)

        elif command.lower() == 'emojify' or command.lower() == 'emo':
            embed = nextcord.Embed(
                title="Help Emojify",
                description="Give me TEXT and I will give you emojis",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}emojify <sometext>\nIt's quite creative, really.",
                inline=True
            )
            embed.set_footer(text="It makes quite the statement too!")
            await ctx.send(embed=embed)

        elif command.lower() == 'spoilify' or command.lower() == 'spoil':
            embed = nextcord.Embed(
                title="Help Spoilify",
                description="Annoys your friends if they want to read your message.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}spoilify <stufftoput>\nExcellent command for losing friends!",
                inline=True
            )
            embed.set_footer(text="Jk chill its hilarious tho")
            await ctx.send(embed=embed)

        elif command.lower() == 'act':
            embed = nextcord.Embed(
                title="Help Act",
                description="Use this to make me act like another user!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}act @<usertoactlike> <messagetouse>\nMostly used for fake evidence :smiling_imp:",
                inline=True
            )
            embed.set_footer(text="This is for pure evil purposes")
            await ctx.send(embed=embed)

        elif command.lower() == 'binary':
            embed = nextcord.Embed(title="Help binary",
                                   description="Converts string to binary",
                                   color=nextcord.Color.green())
            embed.add_field(name="Usage:",
                            value=f"{ctx.prefix}binary <yourstring>",
                            inline=True)
            embed.set_footer(text="Zeros and Ones are awesome.")
            await ctx.send(embed=embed)

        elif command.lower() == 'choose' or command.lower() == 'choose':
            embed = nextcord.Embed(title="Help Choose",
                                   description="Makes a choice for you.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}choose <choices>\nAgain, this bot knows everything.\nIt makes the correct choice.",
                inline=True
            )
            embed.set_footer(text="The bot KNOWS")
            await ctx.send(embed=embed)

        elif command.lower() == 'hack':
            embed = nextcord.Embed(
                title="Help Hack",
                description="Totally hacks the targeted user pc.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}hack @<membername>\nA lot of bad stuff happens.\nUse only in cases of extreme hate or prejudice.",
                inline=True
            )
            embed.set_footer(text="The bad stuff be bad")
            await ctx.send(embed=embed)

        elif command.lower() == 'gif':
            embed = nextcord.Embed(
                title="Help Gif",
                description="Allows you to search giphy for GIFS",
                color=nextcord.Color.random())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}gif <nameofgif>\nGifs are cool yay",
                inline=True)
            embed.set_footer(text="Who needs inbuilt GIFs smh")
            await ctx.send(embed=embed)

        elif command.lower() == 'imagememes':
            embed = nextcord.Embed(title="Help ImageMemes",
                                   description="Cool memes with images!",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}imagememes \nGives you a list of image memes. Enjoy!",
                inline=True
            )
            embed.set_footer(text="Cause there can NEVER be enough memes")
            await ctx.send(embed=embed)

        elif command.lower() == 'vcmeme':
            embed = nextcord.Embed(title="Help VCMeme",
                                   description="Prank your friends in your VC.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}vcmeme <chosenvcmeme>\nThe list is long...\nTo check the list, type {ctx.prefix}vcmeme",
                inline=True
            )
            embed.set_footer(text="I feel sorry for VC users...")
            await ctx.send(embed=embed)

        elif command.lower() == 'quote':
            embed = nextcord.Embed(
                title="Help Quote",
                description="Creates a quote so you can remember your most famous sayings!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}quote <quoter> <quote>\nIt gives you glory.",
                inline=True)
            embed.set_footer(text="Always remember...")
            await ctx.send(embed=embed)

        elif command.lower() == 'kill':
            embed = nextcord.Embed(
                title="Help Kill",
                description="Kill someone with minecraft messages!!!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}kill <Person>\nCoffin Dance Music Plays.",
                inline=True)
            embed.set_footer(text="Yuo Ded")
            await ctx.send(embed=embed)

        elif command.lower() == 'roast':
            embed = nextcord.Embed(
                title="Help Roast",
                description="Roast someone or yourself",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}roast <Person>(Optional)\nDisrespekt",
                inline=True)
            embed.set_footer(text="OOH OOOOOOH")
            await ctx.send(embed=embed)

        elif command.lower() == 'joke':
            embed = nextcord.Embed(
                title="Help Joke",
                description="Gives you jokes.\nYou will either find it funny...\n...or WAY too lame",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}joke",
                inline=True)
            embed.set_footer(text="Jokes be phunny")
            await ctx.send(embed=embed)

        elif command.lower() == 'meme':
            embed = nextcord.Embed(
                title="Help Meme",
                description="Gives you the latest memes... very very phunniez",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}meme",
                inline=True)
            embed.set_footer(text="Cause me wen")
            await ctx.send(embed=embed)

        elif command.lower() == 'blackjack' or command.lower() == 'bj' or command.lower() == '21':
            embed = nextcord.Embed(
                title="Help Blackjack",
                description="An awesome multiplayer card games.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"Use {ctx.prefix}bjhelp\nTells you everything you gotta know about this game.",
                inline=True
            )
            await ctx.send(embed=embed)

        elif command.lower() == 'coinflip':
            embed = nextcord.Embed(
                title="Help Coinflip",
                description="Flips a coin for you. But with a lot MORE FUNCTIONALITY (insert pog music here).",
                color=nextcord.Color.green())
            embed.add_field(
                name="Normal:",
                value=f"Use {ctx.prefix}coinflip\nTo flip a coin. Nothing more, nothing less",
                inline=True
            )
            embed.add_field(
                name="Slightly Better:",
                value=f"Use {ctx.prefix}coinflip <heads/tails>\nTo flip a coin and see if your luck allows you to win",
                inline=True
            )
            embed.add_field(
                name="Coinflip Fight:",
                value=f"Use {ctx.prefix}coinflip <membername>\nTo completely humiliate your friends by making them loose in coinflip.\nUnless you loose yourself.",
                inline=True
            )
            embed.set_footer(text="It's so much better now...")
            await ctx.send(embed=embed)

        elif command.lower() == 'dice':
            embed = nextcord.Embed(
                title="Help Dice",
                description="Roles a dice for you! And yes pun intended.\nYou can play either",
                color=nextcord.Color.green())
            embed.add_field(
                name="Normal:",
                value=f"Use {ctx.prefix}dice\nIf you want to just roll a dice.",
                inline=True
            )
            embed.add_field(
                name="Betting:",
                value=f"Use {ctx.prefix}dice <lowerlimit> <upper_limit>\nIf you want to, say, place a bet against your friends!",
                inline=True

            )
            embed.set_footer(text="This is the poggy-dice (say it out loud its sounds nice lmao)")
            await ctx.send(embed=embed)

        elif command.lower() == 'amogus':
            embed = nextcord.Embed(
                title="Help Amongus",
                description="The imposters are at it again.\nOnly four people are alive and one of them is the IMPOSTER\nWill you be able to defeat the imposters or will you kill an innocent man?",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}amogus",
                inline=True
            )
            embed.set_footer(text="Amogus so chogus")
            await ctx.send(embed=embed)

        elif command.lower() == 'aki':
            embed = nextcord.Embed(
                title="Help Akinator",
                description="I decided to hire a mind-reader.\nHis job is to ask you questions and figure out what you are think of.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}akihelp",
                inline=True
            )
            embed.set_footer(text="He's pretty great and also slightly UNDEFEATABLE")
            await ctx.send(embed=embed)

        elif command.lower() == 'blackjack' or command.lower() == 'bj':
            embed = nextcord.Embed(
                title="Help Blackjack",
                description="A beautiful game of chance, all related to the number 21.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}bjhelp",
                inline=True
            )
            embed.set_footer(text="He's pretty great and also slightly UNDEFEATABLE")
            await ctx.send(embed=embed)

        elif command.lower() == 'guessthemovie' or command.lower() == 'gtm':
            embed = nextcord.Embed(
                title="Help Guess the Movie",
                description="Basically, I give you a bunch of emojis and you gotta guess the movie!\nYes, that must have been so hard to figure out...",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}guessthemovie",
                inline=True
            )
            embed.set_footer(text="I still can't guess the movies tho...")
            await ctx.send(embed=embed)

        elif command.lower() == 'whosthatpokemon' or command.lower() == 'wtp':
            embed = nextcord.Embed(
                title="Help Whos That Pokemon",
                description="Welcome to who's that mutated being.\nWait a minute...\nWhat do you mean those aren't my lines?\nAnyway, you just gotta guess the mutated pokemon I display!",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}whosthatpokemon",
                inline=True
            )
            embed.set_footer(text="Stop bothering me I def didn't say anything wrong")
            await ctx.send(embed=embed)

        elif command.lower() == 'guess':
            embed = nextcord.Embed(
                title="Help Guess",
                description="Let's you play guess the number between literally any two numbers.\nBetween 1 and 10000\nLmao",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}guess <lowerboundary> <upperboundary>\nThen you just guess ig...",
                inline=True
            )
            embed.set_footer(text="Bet you can't beat my dev Zero in 1 - 10000")
            await ctx.send(embed=embed)

        elif command.lower() == 'rps':
            embed = nextcord.Embed(title="Help RPS",
                                   description="You can either play:",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Single player:",
                value=f"Use {ctx.prefix}rps <rock/paper/scissors> to play against me, or",
                inline=True
            )
            embed.add_field(
                name="Multi player:",
                value=f"Use {ctx.prefix}rps @<useryouwanttodefeat> to play against them.",
                inline=True
            )
            embed.set_footer(text="Its a great game!")
            await ctx.send(embed=embed)

        elif command.lower() == 'oddeve':
            embed = nextcord.Embed(title="Help OddEve",
                                   description="You can either play:",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Single player:",
                value=f"Use {ctx.prefix}oddeve <odd/even> to play against me.",
                inline=True)
            embed.add_field(
                name="Multi player:",
                value=f"Use {ctx.prefix}oddeve <useryouwanttodefeat> to play against them.",
                inline=True
            )
            embed.set_footer(text="Its a great game!")
            await ctx.send(embed=embed)

        elif command.lower() == 'wordhunt' or command.lower() == 'wh':
            embed = nextcord.Embed(title="Help Wordhunt",
                                   description="Basically, you get a 9x9 grid with letters and 75 seconds.\nYou need to find as many words as possible.\nThey can be stright, sleeping or even diagnol.\nThe one who finds most words wins!",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"Use {ctx.prefix}wordhunt",
                inline=True)
            embed.set_footer(text=f"Need something harder? Try {ctx.prefix}extremehunt")
            await ctx.send(embed=embed)

        elif command.lower() == 'extremehunt' or command.lower() == 'eh':
            embed = nextcord.Embed(title="Help Wordhunt",
                                   description="Basically, you get a 9x9 grid with letters but 60 seconds.\nYou need to find really, really long words.\nThey can be stright, sleeping or even diagnol.\nThe one who finds the longest word wins!",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"Use {ctx.prefix}extremehunt",
                inline=True)
            embed.set_footer(text=f"Need something easier? Try {ctx.prefix}wordhunt")
            await ctx.send(embed=embed)

        elif command.lower() == 'scramble':
            embed = nextcord.Embed(title="Help Scramble",
                                   description="An easy game where I give you a scrambled word and you gotta unscramble it.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"Use {ctx.prefix}scramble",
                inline=True)
            embed.set_footer(text=f"Me wen bored...")
            await ctx.send(embed=embed)

        elif command.lower() == 'hangman' or command.lower() == 'hm':
            embed = nextcord.Embed(title="Help Hangman",
                                   description="I will show you the number of letters in a hidden word.\nYou need to guess which letters it has.\nEverytime you guess correctly, I reveal those letters in the word.\nEverytime you fail, the man comes closer to death.\nYou can only fail 6 times...",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"Use {ctx.prefix}hangman",
                inline=True)
            embed.set_footer(text=f"Hopefully you succeed")
            await ctx.send(embed=embed)

        elif command.lower() == 'passthebomb' or command.lower() == 'ptb':
            embed = nextcord.Embed(title="Help Pass The Bomb",
                                   description="For some reason, a rando decided to send you and your friends a bomb as a present.\nThe only way to NOT get blown up is typing a word according to what I tell you.\nLast man standing wins.",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"Use {ctx.prefix}passthebomb",
                inline=True)
            embed.set_footer(text=f"Ima be honest with you, not exploding is a very gud idea")
            await ctx.send(embed=embed)

        elif command.lower() == 'typeracer' or command.lower() == 'typerace' or command.lower() == 'tr':
            embed = nextcord.Embed(title="Help Typeracer",
                                   description="Race against your friends to prove your speed.\nYou will be given a sentence to type out.\nOnce the race ends you will get your stats...",
                                   color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"Use {ctx.prefix}typerace",
                inline=True)
            embed.set_footer(text=f"Im fast af boi")
            await ctx.send(embed=embed)

        elif command.lower() == 'pingset' or command.lower() == 'pingsettings':
            embed = nextcord.Embed(
                title="Help Ping Settings",
                description="This allows/ stops Chad from using pings in your server.",
                color=nextcord.Color.green())
            embed.add_field(
                name="Usage:",
                value=f"{ctx.prefix}pingsettings <trueorfalse>.\nA very, very useful command indeed!",
                inline=True
            )
            embed.set_footer(text="Now no more Chad annoying you with pings eyyy")
            await ctx.send(embed=embed)

        else:
            embed = nextcord.Embed(
                title="Noice",
                description=f"You ask me for help, but I can't help you\nCause {command} isn't a part of my awesome features",
                color=nextcord.Color.green())
            embed.set_footer(text=f"Try {ctx.prefix}help without anything after it")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
