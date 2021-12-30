import discord
from discord.ext import commands
from discord.ext.commands import errors
import requests
import asyncio
import sqlite3

class vote(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=[])
    async def vote(self, ctx):
        embed=discord.Embed(description="Para votar entre no site:\nhttps://top.gg/bot/771628845530087444/vote", colour=discord.Colour.orange())
        await ctx.send(embed=embed)

    @commands.command(aliases=[])
    async def clearVoteRanking(self, ctx):
        try:
            if ctx.message.author.id == 164390451045072896:
                db = sqlite3.connect('//var//www//FlaskApp//FlaskApp//static//vote.sqlite')
                cursor = db.cursor()
                cursor.execute("DELETE FROM main")
                db.commit()
                cursor.close()
                db.close()
                embed=discord.Embed(description="Limpado o ranking com sucesso.", colour=discord.Colour.orange())
                await ctx.send(embed=embed)
        except:
            pass

    @commands.command(aliases=['rank','ranking','top'])
    async def voteRanking(self, ctx):
        try:
            db = sqlite3.connect('//var//www//FlaskApp//FlaskApp//static//vote.sqlite')
            cursor = db.cursor()
            cursor.execute("SELECT user FROM main ORDER BY qtd DESC")
            users = cursor.fetchall()
            cursor.execute("SELECT qtd FROM main ORDER BY qtd DESC")
            qtd = cursor.fetchall()
            pages=[]
            rang = 0
            if len(users)%5==0:
              rang = (len(users)//5)
            else:
              rang = (len(users)//5)+1
            for i in range(rang):
                page=discord.Embed(
                    title = f'Página {i+1}/{(rang)}',
                    description= f'Lista do ranking:',
                    colour=discord.Colour.orange()
                  )
                try:
                  for j in range(5):
                      user = await self.client.fetch_user(int(str(users[5*i+j])[1:-2]))
                      page.add_field(name=f'{5*i+j+1}. {str(user)[:-5]}',value=f"{str(qtd[5*i+j])[1:-2]} voto(s).", inline=False)
                except:
                  print('Ok')
                pages.append(page)
            if len(pages)<1:
              embed=discord.Embed(description=f"Não há nenhuma pessoa no ranking.", colour=discord.Colour.orange())
              await ctx.send(embed=embed)
            else:
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
            pass
        cursor.close()
        db.close()



def setup(client):
    client.add_cog(vote(client))