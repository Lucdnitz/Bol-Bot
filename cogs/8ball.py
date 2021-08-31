import discord
from discord.ext import commands
import random
import sqlite3
import asyncio
from discord import FFmpegPCMAudio
from discord.utils import get

class _8Ball(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['8ball'], brief="Comando que poderá dizer seu futuro.")
    async def _8ball(self, ctx, *, perg):
      try:
        db = sqlite3.connect('./db/8ball.sqlite')
        cursor = db.cursor()
        cursor.execute("SELECT respostas FROM main WHERE id = (?) OR id = -1", (str(ctx.message.guild.id),))
        respostas = cursor.fetchall()
        embed=discord.Embed(description=f'Pergunta: {perg}\nResposta: {str(random.choice(respostas))[2:-3]}.', colour=discord.Colour.orange())
        await ctx.send(embed=embed)
        cursor.close()
        db.close()
      except:
        await ctx.send("Não há respostas para o 8ball. Utilize addr para adicionar respostas e remr para remover.")

    @commands.command(aliases=['addr'], brief="Adiciona uma resposta do 8ball.")
    async def adicionarResposta(self, ctx, *, resp):
        try:
            db = sqlite3.connect('./db/8ball.sqlite')
            cursor = db.cursor()
            cursor.execute("INSERT INTO main(respostas, id) VALUES (?,?)", (resp, str(ctx.message.guild.id)))
            db.commit()
            cursor.close()
            db.close()
            embed=discord.Embed(description=f"Adicionada a resposta {resp} com sucesso.", colour=discord.Colour.orange())
            await ctx.send(embed=embed)
        except:
            embed=discord.Embed(description=f"Não foi possível adicionar a resposta", colour=discord.Colour.orange())
            await ctx.send(embed=embed)

    @commands.command(aliases=['remr'], brief="Remove uma resposta do 8ball.")
    async def removerResposta(self, ctx, *, resp):
        try:
            db = sqlite3.connect('./db/8ball.sqlite')
            cursor = db.cursor()
            cursor.execute("DELETE FROM main WHERE respostas=(?) AND id=(?)", (resp, str(ctx.message.guild.id)))
            db.commit()
            cursor.close()
            db.close()
            embed=discord.Embed(description=f"Removida a resposta {resp} com sucesso.", colour=discord.Colour.orange())
            await ctx.send(embed=embed)
        except:
            embed=discord.Embed(description=f"Não foi possível remover a resposta", colour=discord.Colour.orange())
            await ctx.send(embed=embed)
        
    @commands.command(aliases=['lisr'], brief="Lista as respostas do 8ball.")
    async def listaRespostas(self, ctx):
        
        linha = ""
        try:
            db = sqlite3.connect('./db/8ball.sqlite')
            cursor = db.cursor()
            cursor.execute("SELECT respostas FROM main WHERE id = (?) OR id = -1", (str(ctx.message.guild.id),))
            respostas = cursor.fetchall()
            pages=[]
            for i in range((len(respostas)//10)+1):
                page=discord.Embed(
                    title = f'Página {i+1}/{(len(respostas)//10)+1}',
                    colour=discord.Colour.orange()
                )
                try:
                  for j in range(10):
                      linha+=f'{10*i+j+1}. {str(respostas[10*i+j])[2:-3]}\n'
                  page.add_field(name="Lista das respostas presentes no 8ball:", value=linha, inline=False)
                except:
                    if linha!="":
                        page.add_field(name="Lista das respostas presentes no 8ball:", value=linha, inline=False)
                    else:
                        pass
                pages.append(page)
                linha=""

            msg=await ctx.send(embed=pages[0])

            await msg.add_reaction('\u23ee')
            await msg.add_reaction('\u25c0')
            await msg.add_reaction('\u25b6')
            await msg.add_reaction('\u23ed')

            i=0
            emoji=''
            def check(reaction, user):
              return (str(reaction.emoji) in ["\u23ee", "\u25c0", "\u25b6", "\u23ed"]) and (user.id != self.client.user.id) and (user == ctx.message.author)
            while True:
                if emoji=='\u23ee':
                    i=0
                    await msg.edit(embed=pages[i])
                if emoji=='\u25c0':
                    if i>0:
                        i-=1
                        await msg.edit(embed=pages[i])
                if emoji=='\u25b6':
                    if i < len(pages)-1:
                        i+=1
                        await msg.edit(embed=pages[i])
                if emoji=='\u23ed':
                    i=len(pages)-1
                    await msg.edit(embed=pages[i])
                try:
                  reaction, user = await self.client.wait_for("reaction_add", timeout = 60.0, check = check)
                except asyncio.TimeoutError:
                  print('Timeout')
                  break
                else:
                    await msg.remove_reaction(reaction.emoji,user)
                    emoji=reaction.emoji
        except:
          await ctx.send('Sem permissão de edição de mensagem.')


def setup(client):
    client.add_cog(_8Ball(client))
