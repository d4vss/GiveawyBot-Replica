import disnake, os, sys, asyncio, time, random
from disnake.ext import commands
from disnake.ext.commands import has_permissions
from datetime import datetime

class EndCommand(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def gend(self, ctx, message_id = None):
        if message_id == None:
            return
        if not message_id.isnumeric():
            return
        message = await ctx.fetch_message(message_id)
        if len(message.embeds) == 1:
            if "React with 🎉 to enter!" in message.embeds[0].description:
                if "GIVEAWAY" in message.content:
                    title = message.embeds[0].title
                    desc = message.embeds[0].description
                    footer = message.embeds[0].footer.text
                    hosted_by = desc.split('\n')[2]
                    timestamp = int((desc.split("\n")[1].split(" ")[1].replace("<t:", "").replace(":R>", "")))
                    winners = int(footer.split(" ")[0])

                    users = await message.reactions[0].users().flatten()
                    try:
                        users.pop(users.index(self.client.user))
                    except:
                        pass
                    loop = len(users) if len(users) < winners else int(winners)
                    if loop == 1:
                        text = "Winner"
                    else:
                        text = "Winners"
                    if len(users) == 0:
                        embed = disnake.Embed(title=title, description=f'Not enough entrants to determine a winner!\n{hosted_by}', timestamp=datetime.now())
                        embed.set_footer(text=f"{winners} {text} | Ended at:")
                        try:
                            await message.edit("🎉 **GIVEAWAY ENDED** 🎉", embed=embed)
                        except:
                            return
                        embed = disnake.Embed(description=f"**{len(users)}** entrants ↗")
                        return await message.reply("No valid entrants, so a winner could not be determined!", embed=embed)
                    
                    winnerlist = []

                    for i in range(loop):
                        user_choice = random.choice(users)
                        while user_choice in winnerlist:
                            user_choice = random.choice(users)
                        winnerlist.append(user_choice.mention)
                    
                    winnerlist = ", ".join(winnerlist)
                    if title == disnake.Embed.Empty:
                        prize = ""
                        title = ""
                    else:
                        prize = f" the **{title}**"
                    embed = disnake.Embed(title=title, description=f'{text}: {winnerlist}\n{hosted_by}', timestamp=datetime.now())
                    embed.set_footer(text="Ended at:")
                    try:
                        await message.edit("🎉 **GIVEAWAY ENDED** 🎉", embed=embed)
                    except:
                        return
                    if len(users) > 1: s= "s"
                    else: s= ""
                    embed = disnake.Embed(description=f"**{len(users)}** entrant{s} ↗")
                    await message.reply(f"Congratulations {winnerlist}! You won{prize}!",embed=embed)

def setup(client):
    client.add_cog(EndCommand(client))