import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from youtube_search import YoutubeSearch
import traceback, json
import sqlite3
import asyncio
import os
import random
from difflib import SequenceMatcher

class quiz(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['qadd'], brief="Adiciona uma música ao quiz.")
    async def quizAdd(self, ctx):
        embed=discord.Embed(description="Comando desativado para manutenção.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)

    @commands.command(aliases=['qrem'], brief="Remove uma música do quiz.")
    async def quizRemove(self, ctx):
        embed=discord.Embed(description="Comando desativado para manutenção.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)

    @commands.command(aliases=['qlis'], brief="Lista as músicas do quiz.")
    async def quizLista(self, ctx):
        embed=discord.Embed(description="Comando desativado para manutenção.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)

    @commands.command(aliases=['qs','qstart'], brief="Inicia o quiz.")
    async def quizStart(self,ctx,*,numMus: int):
        embed=discord.Embed(description="Comando desativado para manutenção.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)
'''
    @commands.command()
    async def playMusic(self, ctx, *, url):
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True', 'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
        }]}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn -ss 00:30 -to 00:50'}
        voice = get(self.client.voice_clients, guild=ctx.guild)
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        url = info['formats'][0]['url']
        voice.play(FFmpegPCMAudio(url, **FFMPEG_OPTIONS))
'''


def setup(client):
    client.add_cog(quiz(client))


