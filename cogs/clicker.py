import discord
from discord.ext import commands
import random
import sqlite3
import asyncio
from discord.utils import get

class clicker(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.group()
    async def clicker(self,ctx):
        if ctx.invoked_subcommand is None:
            embed= discord.Embed(title="Comando de ajuda", colour=discord.Colour.orange())
            embed.add_field(name="Comandos relacionados ao clicker\n", value=".clicker start - inicia o clicker.\n.clicker stop - para o clicker.\n.clicker shop - mostra a loja do clicker.\n.clicker buy <numero> - compra o objeto indicado pelo numero da loja.\n.clicker rank - mostra o ranking do clicker."
            , inline=False)
            await ctx.send(embed=embed)

    @clicker.command()
    async def start(self,ctx):
        db = sqlite3.connect('./db/clicker.sqlite')
        cursor = db.cursor()
        cursor.execute("SELECT clicker FROM main WHERE user = (?)", (str(ctx.message.author.id),))
        clickerOn= cursor.fetchone()
        if clickerOn is not None:
            clickerOn = int(str(clickerOn)[1:-2])
        cursor.close()
        db.close()
        if clickerOn is None or not clickerOn:
            db = sqlite3.connect('./db/clicker.sqlite')
            cursor = db.cursor()
            cursor.execute("SELECT bolas FROM main WHERE user = (?)", (str(ctx.message.author.id),))
            bolas = cursor.fetchone()
            if bolas is None:
                bolas = 0
                cursor.execute("INSERT INTO main(user,bolas,clicker,seg) VALUES (?,?,?,?)", (ctx.message.author.id, bolas, 1, 0))
            else:
                bolas = int(str(bolas)[1:-2])
                cursor.execute("UPDATE main SET clicker = (?) WHERE user = (?)", (1,str(ctx.message.author.id)))
            db.commit()
            cursor.execute("SELECT seg FROM main WHERE user = (?)", (str(ctx.message.author.id),))
            seg = int(str(cursor.fetchone())[1:-2])
            cursor.close()
            db.close()

            async def clickerGame(msg):
                db = sqlite3.connect('./db/clicker.sqlite')
                cursor = db.cursor()
                cursor.execute("SELECT clicker FROM main WHERE user = (?)", (str(ctx.message.author.id),))
                clickerOn = int(str(cursor.fetchone())[1:-2])
                cursor.close()
                db.close()
                while clickerOn:
                    await asyncio.sleep(1)
                    db = sqlite3.connect('./db/clicker.sqlite')
                    cursor = db.cursor()
                    cursor.execute("SELECT clicker FROM main WHERE user = (?)", (str(ctx.message.author.id),))
                    clickerOn = int(str(cursor.fetchone())[1:-2])
                    cursor.execute("SELECT seg FROM main WHERE user = (?)", (str(ctx.message.author.id),))
                    seg = int(str(cursor.fetchone())[1:-2])
                    cursor.close()
                    db.close()
                    if clickerOn:
                        try:
                            db = sqlite3.connect('./db/clicker.sqlite')
                            cursor = db.cursor()
                            cursor.execute("SELECT bolas FROM main WHERE user = (?)", (str(ctx.message.author.id),))
                            bolas = int(str(cursor.fetchone())[1:-2])
                            cursor.execute("UPDATE main SET bolas = (?) WHERE user = (?)", (bolas+seg,str(ctx.message.author.id)))
                            db.commit()
                            cursor.close()
                            db.close()
                            embed=discord.Embed(title="Clicker Bol Bot", colour=discord.Colour.orange())
                            embed.add_field(name="Bolas\n", value=f"{bolas+seg}", inline=False)
                            embed.add_field(name="Bolas por segundo\n", value=f"{seg}", inline=False)
                            await msg.edit(embed=embed)
                        except:
                            pass


            embed=discord.Embed(title="Clicker Bol Bot", colour=discord.Colour.orange())
            embed.add_field(name="Bolas\n", value=f"{bolas}", inline=False)
            embed.add_field(name="Bolas por segundo\n", value=f"{seg}", inline=False)

            msg = await ctx.send(embed=embed)
            self.client.loop.create_task(clickerGame(msg))
            await msg.add_reaction('\u26BD')

            emoji=''
            def check(reaction, user):
                return (str(reaction.emoji) in ["\u26BD"]) and (user.id != self.client.user.id) and (user == ctx.message.author)
            while True:
                if emoji=='\u26BD':
                    db = sqlite3.connect('./db/clicker.sqlite')
                    cursor = db.cursor()
                    cursor.execute("SELECT bolas FROM main WHERE user = (?)", (str(ctx.message.author.id),))
                    bolas = int(str(cursor.fetchone())[1:-2])
                    bolas+=1
                    cursor.execute("UPDATE main SET bolas = (?) WHERE user = (?)", (bolas,str(ctx.message.author.id)))
                    db.commit()
                    cursor.close()
                    db.close()
                    await msg.remove_reaction('\u26BD', self.client.user)
                    await asyncio.sleep(2)
                    await msg.add_reaction('\u26BD')
                try:
                    reaction, user = await self.client.wait_for("reaction_add", timeout = 60.0, check = check)
                except asyncio.TimeoutError:
                    db = sqlite3.connect('./db/clicker.sqlite')
                    cursor = db.cursor()
                    cursor.execute("SELECT clicker FROM main WHERE user = (?)", (str(ctx.message.author.id),))
                    clickerOn=int(str(cursor.fetchone())[1:-2])
                    cursor.execute("UPDATE main SET clicker = (?) WHERE user = (?)", (0,str(ctx.message.author.id)))
                    cursor.execute("SELECT bolas FROM main WHERE user = (?)", (str(ctx.message.author.id),))
                    bolas = int(str(cursor.fetchone())[1:-2])
                    if clickerOn==1:
                        embed=discord.Embed(title="Clicker Bol Bot", colour=discord.Colour.orange())
                        embed.add_field(name="Bolas\n", value=f"{bolas}\n\nFinalizado")
                        cursor.execute("UPDATE main SET clicker = (?) WHERE user = (?)", (0,str(ctx.message.author.id)))
                        await msg.edit(embed=embed)
                    db.commit()
                    cursor.close()
                    db.close()
                    break
                else:
                    await msg.remove_reaction(reaction.emoji,user)
                    emoji=reaction.emoji
        else:
            embed=discord.Embed(description="Clicker já iniciado anteriormente.", colour=discord.Colour.orange())
            await ctx.send(embed=embed)

    @clicker.command()
    async def shop(self,ctx):
        db= sqlite3.connect('./db/clicker.sqlite')
        cursor = db.cursor()
        cursor.execute("SELECT estadio FROM shop WHERE user = (?)", (str(ctx.message.author.id),))
        estadio = cursor.fetchone()
        if estadio is None:
            estadio = 0
            precEstadio=100
            cursor.execute("INSERT INTO shop(user,estadio) VALUES (?,?)", (ctx.message.author.id,0))
        else:
            estadio = int(str(estadio)[1:-2])
            precEstadio=100+(estadio*50)
        embed=discord.Embed(title="Loja do clicker", colour=discord.Colour.orange())
        embed.add_field(name=f'1. Estádio - {precEstadio} bolas', value='1 click por segundo')
        await ctx.send(embed=embed)
        db.commit()
        cursor.close()
        db.close()
    
    @clicker.command()
    async def buy(self,ctx,*,compra):
        db= sqlite3.connect('./db/clicker.sqlite')
        cursor = db.cursor()
        cursor.execute("SELECT bolas FROM main WHERE user = (?)", (str(ctx.message.author.id),))
        bolas = cursor.fetchone()
        cursor.execute("SELECT estadio FROM shop WHERE user = (?)", (str(ctx.message.author.id),))
        estadio = cursor.fetchone()
        if bolas is None:
            bolas = 0
            cursor.execute("INSERT INTO main(user,bolas,clicker,seg) VALUES (?,?,?,?)", (ctx.message.author.id, bolas, 0, 0))
        else:
            bolas = int(str(bolas)[1:-2])
        if estadio is None:
            estadio = 0
            precEstadio=100
            cursor.execute("INSERT INTO shop(user,estadio) VALUES (?,?)", (ctx.message.author.id,0))
        else:
            estadio = int(str(estadio)[1:-2])
            precEstadio=100+(estadio*50)
        db.commit()
        cursor.close()
        db.close()
        try:
            compra = int(compra)
            if compra==1 and bolas>=precEstadio:
                db= sqlite3.connect('./db/clicker.sqlite')
                cursor = db.cursor()
                bolas -= precEstadio
                estadio+=1
                cursor.execute("UPDATE main SET bolas = (?) WHERE user = (?)", (bolas,str(ctx.message.author.id)))
                cursor.execute("SELECT seg FROM main WHERE user = (?)", (str(ctx.message.author.id),))
                seg = int(str(cursor.fetchone())[1:-2])
                cursor.execute("UPDATE main SET seg = (?) WHERE user = (?)", (seg+1,str(ctx.message.author.id)))
                cursor.execute("UPDATE shop SET estadio = (?) WHERE user = (?)", (estadio,str(ctx.message.author.id)))
                db.commit()
                cursor.close()
                db.close()
                embed=discord.Embed(description="Foi comprado 1 estádio com sucesso.", colour=discord.Colour.orange())
                await ctx.send(embed=embed)
            elif compra==1 and bolas<precEstadio:
                embed=discord.Embed(description="Bolas insuficiente.", colour=discord.Colour.orange())
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(description="Caractere inválido.", colour=discord.Colour.orange())
                await ctx.send(embed=embed)
        except:
            embed=discord.Embed(description="Caractere inválido.", colour=discord.Colour.orange())
            await ctx.send(embed=embed)
    @clicker.command()
    async def stop(self,ctx):
        try:
            db = sqlite3.connect('./db/clicker.sqlite')
            cursor = db.cursor()
            cursor.execute("SELECT clicker FROM main WHERE user = (?)", (str(ctx.message.author.id),))
            clickerOn=int(str(cursor.fetchone())[1:-2])
            if clickerOn is None or clickerOn ==0:
                embed=discord.Embed(description="Não há nenhum clicker iniciado.", colour=discord.Colour.orange())
                await ctx.send(embed=embed)
            else:
                cursor.execute("UPDATE main SET clicker = (?) WHERE user = (?)", (0,str(ctx.message.author.id)))
                embed=discord.Embed(description="Clicker finalizado.", colour=discord.Colour.orange())
                await ctx.send(embed=embed)
            db.commit()
            cursor.close()
            db.close()
        except:
            embed=discord.Embed(description="Clicker finalizado.")
            await ctx.send(embed=embed)
        
    @clicker.command()
    async def rank(self, ctx):
        try:
            db = sqlite3.connect('./db/clicker.sqlite')
            cursor = db.cursor()
            cursor.execute("SELECT user FROM main ORDER BY bolas DESC")
            users = cursor.fetchall()
            cursor.execute("SELECT bolas FROM main ORDER BY bolas DESC")
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
                      page.add_field(name=f'{5*i+j+1}. {str(user)[:-5]}',value=f"{str(qtd[5*i+j])[1:-2]} bola(s).", inline=False)
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
    client.add_cog(clicker(client))
