import discord
from discord.ext import commands

class Desativado8Ball(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['8ball'], brief="Comando que poderá dizer seu futuro.")
    async def _8ball(self, ctx):
        embed=discord.Embed(description="Comando desativado para manutenção.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)



    @commands.command(aliases=['addr'], brief="Adiciona uma resposta do 8ball.")
    async def adicionarResposta(self, ctx):
        embed=discord.Embed(description="Comando desativado para manutenção.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)

    @commands.command(aliases=['remr'], brief="Remove uma resposta do 8ball.")
    async def removerResposta(self, ctx):
        embed=discord.Embed(description="Comando desativado para manutenção.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)
        
    @commands.command(aliases=['lisr'], brief="Lista as respostas do 8ball.")
    async def listaRespostas(self, ctx):
        embed=discord.Embed(description="Comando desativado para manutenção.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Desativado8Ball(client))
