import disnake, os, sys, asyncio, time, random
from disnake.ext import commands
from disnake.ext.commands import has_permissions
from datetime import datetime

class RerollCommand(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def greroll(self, ctx, message_id = None):
        if message_id == None:
            return 
        if not message_id.isnumeric():
            return
        
        message = await ctx.fetch_message(message_id)

        if len(message.embeds) == 1:
            pass

def setup(client):
    client.add_cog(RerollCommand(client))