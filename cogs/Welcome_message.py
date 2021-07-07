import discord
from discord.ext import commands

class Welcome_message(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot está pronto")
        await self.client.change_presence(activity=discord.Game('.help para os comandos'))

    @commands.Cog.listener()
    async def on_member_join(self, ctx, member):
        await ctx.send(f'{member} entrou no servidor.')

    @commands.Cog.listener()
    async def on_member_remove(self, ctx, member):
        await ctx.send(f'{member} saiu do servidor.')



def setup(client):
    client.add_cog(Welcome_message(client))