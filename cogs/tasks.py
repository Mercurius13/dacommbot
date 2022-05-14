import nextcord
import asyncio
import csv
from nextcord.ext import commands, tasks
from datetime import datetime
import os
#yeet!
class Loops(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.csv_update.start()
        self.statusandfiles.start()
    




    @tasks.loop(seconds=60)
    async def csv_update(self):
        await self.bot.wait_until_ready()
        now = datetime.now()
        dt_string = now.strftime("%H %M")
        if dt_string == "12 00":
            date1 = datetime.strftime(datetime.now(), "%a, %d/%m/%Y")
            data = [date1, len(self.bot.users)]
            with open("databases/members.csv", 'a+', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(data)

            date2 = datetime.strftime(datetime.now(), "%a, %d/%m/%Y")
            data = [date2, len(self.bot.guilds)]
            with open("databases/servers.csv", 'a+', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(data)

    @tasks.loop(seconds=300)
    async def statusandfiles(self):
        await self.bot.wait_until_ready()
        directory = 'images'
        for f in os.listdir(directory):
            os.remove(os.path.join(directory, f))

        guild_count = len(self.bot.guilds)

        await self.bot.change_presence(
            status=nextcord.Status.idle,
            activity=nextcord.Activity(
                type=nextcord.ActivityType.listening,
                name=f"!help | {len(self.bot.users)} members in {guild_count} servers and I'm still playing with Louis"))

        channel = self.bot.get_channel(878503565369442375)
        mymsg = await channel.fetch_message(878506421484945479)
        guilds = self.bot.guilds
        member_count = 0
        for guild in guilds:
            for _ in guild.members:
                member_count += 1
        embed = nextcord.Embed(title="Stats of the Chad Bot(Me!)", color=nextcord.Color.random())
        embed.add_field(name="Servers", value=str(len(self.bot.guilds)), inline=False)
        embed.add_field(name="Unique users", value=str(len(self.bot.users)), inline=False)
        embed.add_field(name="Total users(contains common members)", value=str(member_count), inline=False)
        await mymsg.edit(embed=embed)
        
def setup(bot):
    bot.add_cog(Loops(bot))
