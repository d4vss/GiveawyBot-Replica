import disnake, os, sys, asyncio, time, random
from disnake.ext import commands
from disnake.ext.commands import has_permissions
from datetime import datetime

class StartCommand(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def gstart(self, ctx, duration = None, winners = None, prize = None):
        await ctx.message.delete()
        if duration == None:
            return await ctx.send("💥 Please include a length of time, and optionally a number of winners and a prize!\nExample usage: ``!gstart 30m 5w Awesome T-Shirt``")
        
        try:
            time_convert = {"s" : 1, "m" : 60, "h" : 3600, "d" : 86400, "w": 604800}
            amount = "".join(c for c in duration if c.isdigit())
            key = "".join(c for c in duration if not c.isdigit())
            duration = int(amount) * time_convert[key]
        except:
            return await ctx.send(f"💥 Failed to parse time from ``{duration}``\nExample usage: ``!gstart 30m 5w Awesome T-Shirt``")
        
        endtime = round(time.time()) + duration
        numb = 0
        if winners != None:
            if winners[len(winners)-1].lower() == "w":
                numb = winners.lower().split("w")
                numb = int(numb[0])
                if 20 > numb < 1:
                    return await ctx.send("💥 Number of winners must be at least 1 and no larger than 20.")
        if numb == 0:
            if prize != None:
                prize = f"{winners} {prize}"
            elif winners != None:
                prize = winners
            else:
                prize = ""
            winners = "1w"
        else:
            if prize == None:
                prize = ""
        winner_amount = winners.split("w")[0]
        if winners == "1w":
            winnertext = ""
        else:
            winnertext = f"{winner_amount} winners | "

        if prize == "None None":
            prize = ""

        embed = disnake.Embed(title=prize, description=f"React with 🎉 to enter!\nEnds: <t:{endtime}:R> (<t:{endtime}:f>) \nHosted by: {ctx.author.mention}", timestamp=datetime.utcfromtimestamp(endtime), color=0x7289DA)
        embed.set_footer(text=f"{winnertext}Ends at ")
        msg = await ctx.send("🎉 **GIVEAWAY** 🎉", embed=embed)
        await msg.add_reaction("🎉")

def setup(client):
    client.add_cog(StartCommand(client))