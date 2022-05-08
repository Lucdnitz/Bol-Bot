import discord
from discord.ext import commands

class Desativadoclicker(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group()
    async def clicker(self,ctx):
        embed= discord.Embed(title="Comando desativado para manutenção.", colour=discord.Colour.orange())
            

def setup(client):
    client.add_cog(Desativadoclicker(client))
