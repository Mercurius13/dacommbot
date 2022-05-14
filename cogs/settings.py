import nextcord
import asyncio
from nextcord.ext import commands, tasks
from tinydb import TinyDB, Query
from datetime import datetime


class settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['pref', 'pre', 'pr'])
    async def prefix(self, ctx, *, prefix=None):
        if ctx.author.guild_permissions.administrator:
            db = TinyDB('databases/prefix.json')
            query = Query()
            guild_id_var = ctx.guild.id
            if prefix is None:
                await ctx.send(embed=nextcord.Embed(title=f"My prefix is `{ctx.prefix}`",
                                                    color=ctx.guild.owner.top_role.color))

            else:
                if db.search(query.guild_id == str(guild_id_var)):
                    db.update({'prefix': prefix}, query.guild_id == str(guild_id_var))
                    await ctx.send(embed=nextcord.Embed(title=f"Updated prefix of \"{ctx.guild.name}\" to {prefix}",
                                                        color=nextcord.Color.random()))
                else:
                    db.insert({'guild_id': str(guild_id_var), 'prefix': str(prefix)})
                    await ctx.send(embed=nextcord.Embed(title=f"Changed prefix of \"{ctx.guild.name}\" to {prefix}",
                                                        color=nextcord.Color.random()))

        else:
            embed = discord.Embed(title="Hold up",
                                  description="You can't do that, your not an admin!",
                                  color=nextcord.Color.random())
            await ctx.send(embed=embed)

    @commands.command()
    async def stats(self, ctx):
        if ctx.author.id == 815555652780294175 or ctx.author.id == 723032217504186389:
            active_servers = self.bot.guilds
            for guild in active_servers:
                await ctx.send(f"{str(guild)} has {len(guild.members)} members")

        else:
            await ctx.send(embed=nextcord.Embed(title="Imagine trying to see stats of someone else's bot",
                                                color=nextcord.Color.random()))

    @commands.command(aliases=["voteremind", "remindvote"])
    async def vote_reminder(self, ctx):
        if ctx.guild.id != 869173101131337748:
            await ctx.send(embed=nextcord.Embed(title=f"{ctx.author.name} You are an idiot. ",
                                                description="I do this only [here](https://discord.gg/h3Mg4CD7)",
                                                color=nextcord.Color.random()))
        role = nextcord.utils.find(lambda r: r.name == 'voteping', ctx.message.guild.roles)
        await ctx.author.add_roles(role)
        await ctx.send(
            embed=discord.Embed(title=f"Ok {ctx.author.name}. I shall remind you to vote for me every 12 hours!",
                                description="Forgetful boi",
                                color=nextcord.Color.random()))

    @commands.command(aliases=['welcmsg', 'wm', 'welcomemsg', 'welcmessage'])
    async def welcomemessage(self, ctx, *, message=None):
        if ctx.author.guild_permissions.administrator:
            db = TinyDB('databases/welcome.json')
            query = Query()
            guild_id_var = ctx.guild.id
            if message is None:
                try:
                    db.remove(query.guild_id == str(guild_id_var))
                    await ctx.send(embed=nextcord.Embed(title="Welcome message removed.",
                                                        description="I will not bother new comers again",
                                                        color=nextcord.Color.random()))
                except:
                    await ctx.send(embed=nextcord.Embed(title="You don't even have a welcome message",
                                                        description="And if you don't type anything, then my job is to remove your welcome message."
                                                                    "So either try to add a welcome message properly, or chill, your message doesn't exist.",
                                                        color=nextcord.Color.random()))

            else:
                if db.search(query.guild_id == str(guild_id_var)):
                    db.update({'message': message}, query.guild_id == str(guild_id_var))
                    await ctx.send(embed=nextcord.Embed(title=f"Updated your servers welcome message is now:",
                                                        description=f"{message}",
                                                        color=nextcord.Color.random()))
                else:
                    db.insert({'guild_id': str(guild_id_var), 'message': str(message)})
                    await ctx.send(embed=nextcord.Embed(title=f"Your welcome message is now:",
                                                        description=f"{message}",
                                                        color=nextcord.Color.random()))

        else:
            embed = discord.Embed(title="Hold up",
                                  description="You can't do that, your not an admin!",
                                  color=nextcord.Color.random())
            await ctx.send(embed=embed)

    @commands.command(aliases=['leavemsg', 'lm'])
    async def leavemessage(self, ctx, *, message=None):
        if ctx.author.guild_permissions.administrator:
            db = TinyDB('databases/leave.json')
            query = Query()
            guild_id_var = ctx.guild.id
            if message is None:
                try:
                    db.remove(query.guild_id == str(guild_id_var))
                    await ctx.send(embed=nextcord.Embed(title="Leave message removed.",
                                                        description="I will not bother those leaving betrayers again",
                                                        color=nextcord.Color.random()))
                except:
                    await ctx.send(embed=nextcord.Embed(title="You don't even have a leave message",
                                                        description="And if you don't type anything, then my job is to remove your leave message."
                                                                    "So either try to add a leave message properly, or chill, your message doesn't exist.",
                                                        color=nextcord.Color.random()))

            else:
                if db.search(query.guild_id == str(guild_id_var)):
                    db.update({'message': message}, query.guild_id == str(guild_id_var))
                    await ctx.send(embed=nextcord.Embed(title=f"Updated your servers leave message is now:",
                                                        description=f"{message}",
                                                        color=nextcord.Color.random()))
                else:
                    db.insert({'guild_id': str(guild_id_var), 'message': str(message)})
                    await ctx.send(embed=nextcord.Embed(title=f"Your leave message is now:",
                                                        description=f"{message}",
                                                        color=nextcord.Color.random()))

        else:
            embed = discord.Embed(title="Hold up",
                                  description="You can't do that, your not an admin!",
                                  color=nextcord.Color.random())
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(settings(bot))
