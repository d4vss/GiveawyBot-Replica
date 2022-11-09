import disnake, os, sys, asyncio, time, random
from disnake.ext import commands
from disnake.ext.commands import has_permissions
from datetime import datetime

class ListCommand(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def glist(self, ctx):
        running_giveaways = 0
        giveaways = ""
        for channel in ctx.guild.text_channels:
            async for message in channel.history():
                if len(message.embeds) == 1:
                    if "React with 🎉 to enter!" in message.embeds[0].description:
                        if "GIVEAWAY" in message.content:
                            title = message.embeds[0].description.split("\n")[0]
                            desc = message.embeds[0].description
                            footer = message.embeds[0].footer.text
                            if footer.split(" ")[0] == "Ends":
                                winner_amount = 1
                                winner_text = "winner"
                            else:
                                winner_amount = footer.split(" ")[0]
                                winner_text = "winners"
                            timestamp = desc.split("\n")[1].split(" ")[1]
                            running_giveaways += 1
                            if title == "React with 🎉 to enter!":
                                title = "No prize specified"
                            giveaways += f"``{message.id}`` | {message.channel.mention} | **{winner_amount}** {winner_text} | Prize: {title} | Ends {timestamp}\n"
        if running_giveaways == 0:
            return await ctx.send("💥 There are no giveaways running on the server!")
        
        await ctx.send(f"🎉 __Active Giveaways on **{ctx.guild.name}**__:\n\n{giveaways}")
def setup(client):
    client.add_cog(ListCommand(client))