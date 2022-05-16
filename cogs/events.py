import nextcord
from nextcord.ext import commands, tasks
import os
from datetime import datetime
import pytz
from tinydb import TinyDB, Query
import csv
dbl_token = os.getenv('dbl_token')

class events(commands.Cog):
    """A couple of simple commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot    

    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged in as')
        print(f'Time:{datetime.now()}')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('.....')
        await self.bot.change_presence(
            status=nextcord.Status.idle,
            activity=nextcord.Activity(
                type=nextcord.ActivityType.listening,
                name=f"-help || Im back... kinda!"))


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        prefix = await self.bot.get_prefix(message)
        prefix = "".join(prefix)

        if message.content == "<@!864010316424806451>":
            if prefix == "!":
                embed = nextcord.Embed(title="I have been summoned!!", color=nextcord.Color.random(),
                                       description=f"My prefix on this server is `{prefix}`\n Simply do `{prefix}help` to see all my commands!\n(If there are too many '!'s then blame me not...)")
                embed.set_footer(text='I was chilling until you disturbed me :(')
            else:
                embed = nextcord.Embed(title="I have been summoned!!", color=nextcord.Color.random(),
                                       description=f"My prefix on this server is `{prefix}`\n Simply do `{prefix}help` to see all my commands!")
                embed.set_footer(text='I was chilling until you disturbed me :(')
            await message.channel.send(embed=embed)

        if message.content.startswith(f'{prefix}afk'):
            return

        db = TinyDB('databases/blacklist.json')
        member = message.author.id
        try:
            query = Query()
            blacklisted_guild = db.search(query['guild_id'] == message.guild.id)
            blacklisted_peeps = None
            for i in range(0, len(blacklisted_guild)):
                if str(member) in str(blacklisted_guild[i]):
                    blacklisted_peeps = blacklisted_guild[i]
            if blacklisted_peeps is not None:
                return
        except:
            print("It's a DM")

        db2 = TinyDB('databases/afk.json')
        query = Query()

        for member in message.mentions:
            if db2.search(query['afk_user'] == member.id):
                value = str(
                    list(
                        map(lambda entry: entry["reason"],
                            db2.search(query['afk_user'] == member.id)))[0])
                await message.channel.send(
                    embed=nextcord.Embed(title=f"{member.display_name} is currently afk",
                                        description=f"Afk note is: {value}",
                                        color=nextcord.Color.random()))

        member = message.author
        if db2.search(query['afk_user'] == member.id):
            await message.channel.send(embed=nextcord.Embed(
                title=f"{member.display_name} You typed a message!",
                description=f"That means you ain't afk!\nWelcome back buddy.",
                color=nextcord.Color.random()))

            query = Query()
            db2.remove(query.afk_user == member.id)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        pos = sum(m.joined_at < member.joined_at for m in member.guild.members
                  if m.joined_at is not None)
        if member.guild.id == 869173101131337748 or member.guild.id == 819870399310594088:
            member_var = member.display_name

            embed = nextcord.Embed(
                description=f"Welcome {member_var} to **{member.guild.name}**\nYou are the {pos}th member in the server.",
                color=0xe74c3c)
            embed.set_thumbnail(url=member.avatar.url)
            if not member.bot:
                try:
                    await member.send(f'Welcome to {member.guild.name}')
                except:
                    print("Could not DM")
                if not channel:
                    pass
                else:
                    await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild = channel.guild
        muted_role = nextcord.utils.get(guild.roles, name="Is Muted")
        if muted_role is None:
            perms = nextcord.Permissions(speak=False,
                                        send_messages=False,
                                        read_message_history=True,
                                        read_messages=True)
            try:
                await guild.create_role(name="Is Muted",
                                        color=nextcord.Color.dark_gray(),
                                        permissions=perms)

            except:
                print("New channel made, cant sync mute perms")
            try:
                muted_role = nextcord.utils.get(guild.roles, name="Is Muted")
            except:
                print("Couldnt get role :(")
        try:
            await channel.set_permissions(muted_role,
                                          send_messages=False,
                                          speak=False)
        except:
            print("Couldnt get role :(")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system_channel
        if member.guild.id == 869173101131337748 or member.guild.id == 819870399310594088:
            embed = nextcord.Embed(
                description=f"{member.name} left **{member.guild.name}**",
                color=0xe74c3c)
            embed.set_thumbnail(url=member.avatar.url)
            try:
                await channel.send(embed=embed)
            except:
                print("Could not get channel")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        db1 = TinyDB('databases/lockdown.json')
        db1.insert({'guild': guild.id, 'unaffected_channels': [], 'state': False})

        embed = nextcord.Embed(title="Guild join",
                              description=guild.name,
                              color=0x00FF00)
        embed.add_field(name=f"Members", value=str(len(guild.members)))
        embed.add_field(name=f"Owner", value=guild.owner)
        a = self.bot.get_guild(869173101131337748)
        channel = a.get_channel(869447409237897256)
        embed.set_footer(text=f"Chad is currently in {len(self.bot.guilds)} servers")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        db1 = TinyDB('databases/lockdown.json')
        db1q = Query()
        db1.remove(db1q.guild == guild.id)
        db2 = TinyDB('databases/blacklist.json')
        db2q = Query()
        db2.remove(db2q.guild_id == guild.id)
        db3 = TinyDB('databases/warnings.json')
        db3q = Query()
        db3.remove(db3q.guild_id == guild.id)
        db4 = TinyDB('databases/prefix.json')
        db4q = Query()
        db4.remove(db4q.guild_id == guild.id)

        embed = nextcord.Embed(title="Guild leave",
                              description=guild.name,
                              color=0xFF0000)
        embed.add_field(name=f"Members", value=str(len(guild.members)))
        embed.add_field(name=f"Owner", value=guild.owner)
        a = self.bot.get_guild(869173101131337748)
        channel = a.get_channel(869447409237897256)
        await channel.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(events(bot))
