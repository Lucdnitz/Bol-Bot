import discord
from discord.ext import commands
from discord_components import *
import discord_components

class divulgacao(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(aliases=['arts'], brief="Artistas do BOL")
    async def artistas(self, ctx):
        ddb=DiscordComponents(self.client)
        await ctx.send('a', components=[Button(style=discord_components.ButtonStyle.red, label='a')])
        res = await self.client.wait_for("button_click")
        print('res')


def setup(client):
    client.add_cog(divulgacao(client))