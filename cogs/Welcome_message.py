import discord
from discord.ext import commands

class Welcome_message(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot está pronto")
        await self.client.change_presence(activity=discord.Game('.help para os comandos'))



def setup(client):
    client.add_cog(Welcome_message(client))