import disnake, asyncio, sqlite3, json, random
from disnake.ext import commands, tasks

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.change_presence.start()

    @commands.Cog.listener()
    async def on_ready(self):
        config = json.load(open("data/config.json", encoding='utf8'))
        print(f"------\nBot name: {config['name']}\nDescription: {config['desc']}\nDV: {disnake.__version__}\n------")

    @tasks.loop(seconds=30)
    async def change_presence(self):
        await self.client.wait_until_ready()
        config = json.load(open("data/config.json", encoding='utf8'))
        await self.client.change_presence(activity=disnake.Activity(type=disnake.ActivityType.playing, name=(random.choice(config["status"])).format(name=config["name"])))
        await asyncio.sleep(30)

def setup(client):
    client.add_cog(Events(client))