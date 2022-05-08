import discord
from discord.ext import commands

class divulgacao(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['arts'], brief="Artistas do BOL")
    async def artistas(self, ctx):
        await ctx.send(f'PHC ARTS: https://www.instagram.com/phc.arts/?hl=pt-br \nMAT ARTS: https://www.instagram.com/mat_artz/?hl=pt-br')



def setup(client):
    client.add_cog(divulgacao(client))