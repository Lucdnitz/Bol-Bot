import discord
from discord.ext import commands, tasks
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from youtube_search import YoutubeSearch
import traceback, json
import sqlite3
import asyncio

class Music(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['j'], brief='Faz o bot se juntar a chamada')
    async def join(self, ctx):
        embed=discord.Embed(description="Comando desativado para manutenção.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)
          
    @commands.command(aliases=['l'], brief='Faz o bot sair da chamada(caso o quiz ou o player derem problema, utilize este comando)')
    async def leave(self, ctx):
        embed=discord.Embed(description="Comando desativado para manutenção.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)
        
    @commands.command(aliases=['tocar'], brief='Faz o bot tocar uma música.')
    async def play(self, ctx):
        embed=discord.Embed(description="Comando desativado para manutenção.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['pa', 'pau'], brief='Pausa a música.')
    async def pause(self, ctx):

      embed=discord.Embed(description="Comando desativado para manutenção.", colour=discord.Colour.orange())
      await ctx.send(embed=embed)


    @commands.command(pass_context=True, aliases=['r', 'res'], brief='Retoma a música.')
    async def resume(self, ctx):
        embed=discord.Embed(description="Comando desativado para manutenção.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['next', 'proxima'], brief='Toca a próxima música.')
    async def skip(self, ctx):
        embed=discord.Embed(description="Comando desativado para manutenção.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['s', 'parar'], brief='Para a música.')
    async def stop(self, ctx):
        embed=discord.Embed(description="Comando desativado para manutenção.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)

    @commands.command(aliases=['que'], brief="Lista as músicas da fila.")
    async def queue(self, ctx):
        embed=discord.Embed(description="Comando desativado para manutenção.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['vol', 'v'])
    async def volume(self, ctx):
      embed=discord.Embed(description="Comando desativado para manutenção.", colour=discord.Colour.orange())
      await ctx.send(embed=embed)



def setup(client):
    client.add_cog(Music(client)) 