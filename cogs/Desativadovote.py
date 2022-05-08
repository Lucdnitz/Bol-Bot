import discord
from discord.ext import commands
from discord.ext.commands import errors
import requests

class Desativadovote(commands.Cog):

    def __init__(self, client):
        self.client = client

    

    @commands.command(aliases=['rank','ranking','top'])
    async def voteRanking(self, ctx):
        embed=discord.Embed(description="Comando desativado para manutenção.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)



def setup(client):
    client.add_cog(Desativadovote(client))