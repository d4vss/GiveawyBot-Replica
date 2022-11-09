import disnake, os, sys, json, asyncio, time, datetime, glob, psutil, aiosqlite
from disnake import Embed
from disnake.ext import commands
from disnake.ext.commands import has_permissions, MissingPermissions
start_time = time.time()
class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.process = psutil.Process()

    async def connect_db(self):
        db = await aiosqlite.connect("data/database.sqlite", timeout=3)
        cursor = await db.cursor()
        return db, cursor

    async def close_db(self, cursor):
        await cursor[1].close()
        await cursor[0].commit()
        await cursor[0].close()

    @commands.command(aliases=["r"])
    @ommands.is_owner()
    @commands.guild_only()
    async def reload(self, ctx):
        embed1=disnake.Embed(title="Reload", description="Reloading...")
        embed2=disnake.Embed(title="Reload", description="Done.")
        try:
            await ctx.message.delete()
        except:
            pass
        message = await ctx.send(embed=embed1, delete_after=1.5)
        for ex in os.listdir("cogs"):
            if ex.endswith(".py"): 
                self.client.reload_extension(f'cogs.{ex.split(".")[0]}')
        await message.edit(embed=embed2)
        
    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx):
        api_time = time.time()
        message = await ctx.send("Loading...")
        end_time = time.time()
        botping = round(self.client.latency * 1000)
        apiping = round((end_time - api_time) * 1000)
        await message.edit(f"Ping: {botping}ms | Websocket: {apiping}ms")

    @commands.command()
    async def about(self, ctx):
        embed = disnake.Embed(title="Hold giveaways quickly and easily!", description="Hello! I'm GiveawayBot, and I'm here to make it as easy as possible to hold giveaways on your Discord server! I was created by **jagrosh#4824** using the **JDA** library (4.2.1_41c8f3e) and **JDA-Utilities** (3.0.5). Check out my commands by typing !ghelp, and checkout my website at **<https://giveawaybot.party/>**.")
        await ctx.send(":tada: All about **GiveawayBot** :tada:", embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandNotFound):
            return
        else:
            raise(error)

    @commands.command()
    async def help(self, ctx):
        await ctx.message.add_reaction("🎉")
        try:
            await ctx.author.send('''
:tada: __**GiveawayBot** commands__:

**!gabout** - shows info about the bot
**!ginvite** - shows how to invite the bot
**!gping** - checks the bot's latency

  __Giveaway__:

**!gcreate** - creates a giveaway (interactive setup)
**!gstart <time> [winners]w [prize]** - starts a giveaway (quick setup)
**!gend [messageId]** - ends (picks a winner for) the specified or latest giveaway in the current channel
**!greroll [messageId]** - re-rolls the specified or latest giveaway in the current channel
**!glist** - lists active giveaways on the server

Do not include <> nor [] - <> means required and [] means optional.
For additional help, contact jagrosh#4824 or check out <https://giveawaybot.party/>
To help keep the bot online, please consider donating at <https://giveawaybot.party/donate>
        ''')
        except disnake.Forbidden:
            await ctx.send("💥 Help could not be sent because you are blocking Direct Messages")

def setup(client):
    client.add_cog(Misc(client))