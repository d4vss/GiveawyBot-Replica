import disnake, os, sys, asyncio, time, random
from disnake.ext import commands
from disnake.ext.commands import has_permissions
from datetime import datetime

class CreateCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def messagereq(self, ctx):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            msg = await self.client.wait_for('message', timeout=120, check=check)
        except asyncio.TimeoutError:
            await ctx.send(f"💥 Uh oh! You took longer than 2 minutes to respond, {ctx.author.mention}!\n\n``Giveaway creation has been cancelled.``")
            return "cancel"
        
        if msg.content.lower() == "cancel":
            await ctx.send("💥 Alright, I guess we're not having a giveaway after all...\n\n``Giveaway creation has been cancelled.``")

        return msg.content

    async def step(self, numb : int, ctx, question):
        await ctx.send(question)
        
        if numb == 1:
            channel = None
            while channel == None:
                msg = await self.messagereq(ctx)
                if msg.lower() == "cancel":
                    return None
                try:
                    channel = await commands.TextChannelConverter().convert(ctx, msg)
                except:
                    await ctx.send(f"💥 Uh oh, I couldn't find any channels called '{msg}'! Try again!\n\n``Please type the name of a channel in this server.``")
            return channel

        elif numb == 2:
            duration = None
            while duration == None:
                msg = await self.messagereq(ctx)
                if msg.lower() == "cancel":
                    return
                try:
                    time_convert = {"s" : 1, "m" : 60, "h" : 3600, "d" : 86400, "w": 604800}
                    amount = "".join(c for c in msg if c.isdigit())
                    key = "".join(c for c in msg if not c.isdigit())
                    duration = int(amount) * time_convert[key]
                    if key == "s":
                        addon = "second"
                    elif key == "m":
                        addon = "minute"
                    elif key == "h":
                        addon = "hour"
                    elif key == "d":
                        addon = "day"
                    elif addon == "w":
                        addon = "week"

                except:
                    await ctx.send("💥 Hm. I can't seem to get a number from that. Can you try again?\n\n``Please enter the duration of the giveaway in seconds.\nAlternatively, enter a duration in minutes and include an M at the end, or days and include a D.``")
            return duration, amount, addon
        elif numb == 3:        
            winners = None

            while winners == None:
                msg = await self.messagereq(ctx)
                if msg == "cancel":
                    return
                
                if msg.isnumeric():
                    if 1 <= int(msg) <= 20:
                        return int(msg)
                await ctx.send("💥 Hey! I can only support 1 to 20 winners!\nNeed to host more giveaways, giveaways with longer durations, or giveaways with more winners? Check out <https://giveawaybot.party/donate>! \n\n``Please enter a number of winners between 1 and 20.``")

        elif numb == 4:
            msg = await self.messagereq(ctx)
            if msg == "cancel":
                return
            return msg    

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def gcreate(self, ctx):
        channel = await self.step(1, ctx, "🎉 Alright! Let's set up your giveaway! First, what channel do you want the giveaway in?\nYou can type ``cancel`` at any time to cancel creation.\n\n``Please type the name of a channel in this server.``")
        if channel == None:
            return

        payload = await self.step(2, ctx, f"🎉 Sweet! The giveaway will be in {channel.mention}! Next, how long should the giveaway last?\n\n``Please enter the duration of the giveaway in seconds.\nAlternatively, enter a duration in minutes and include an M at the end, or days and include a D.``")
        if payload == None:
            return
        
        duration = payload[0]
        endtime = round(time.time())+duration
        numb = payload[1]
        text = payload[2]
        if numb != 1:
            text += "s"

        
        winners = await self.step(3, ctx, f"🎉 Neat! This giveaway will last **{numb}** {text}! Now, how many winners should there be?\n\n``Please enter a number of winners between 1 and 20.``")
        if winners == None:
            return

        winner_amount = winners.split("w")[0]
        if winners == "1w":
            winnertext = ""
        else:
            winnertext = f"{winner_amount} winners | "

        prize = await self.step(4, ctx, f"🎉 Ok! {winners} {winner_s} it is! Finally, what do you want to give away?\n\n``Please enter the giveaway prize. This will also begin the giveaway.``")

        if prize == None:
            return

        embed = disnake.Embed(title=prize, description=f"React with 🎉 to enter!\nEnds: <t:{endtime}:R> (<t:{endtime}:f>) \nHosted by: {ctx.author.mention}", timestamp=datetime.utcfromtimestamp(endtime), color=0x7289DA)
        embed.set_footer(text=f"{winnertext}Ends at ")
        msg = await channel.send("🎉 **GIVEAWAY** 🎉", embed=embed)
        await msg.add_reaction("🎉")
        await ctx.send(f"🎉 Done! The giveaway for the ``{prize}`` is starting in {channel.mention}!")

def setup(client):
    client.add_cog(CreateCommand(client))