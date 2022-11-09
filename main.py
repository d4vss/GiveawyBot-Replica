import disnake, json, sqlite3
from disnake.ext import commands
from loader import Loader

config = json.load(open("data/config.json"))
loader = Loader()
client = commands.Bot(command_prefix="g!", intents = disnake.Intents.all(), case_insensitive=True)
client.remove_command('help')
loader.load("cogs", client, [])

client.run(config["token"])