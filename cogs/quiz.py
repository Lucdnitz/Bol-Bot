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
    async def quizAdd(self, ctx, *, url):
        if ("www.youtube.com/" in url) or ("youtu.be" in url):
            url = url
        else:
            print('Erro 1')
            yt = YoutubeSearch(url, max_results=5).to_json()
            try:
                videosLista=discord.Embed(title="Vídeos", description="Para selecionar uma música digite o número correspondente do vídeo (1 a 5)", colour=discord.Colour.orange())
                for i in range(5):
                    videosLista.add_field(name=f"{i+1}. {str(json.loads(yt)['videos'][i]['title'])} ({str(json.loads(yt)['videos'][i]['duration'])})", value=f"https://www.youtube.com{str(json.loads(yt)['videos'][i]['url_suffix'])}", inline=False)
                msgVideo = await ctx.send(embed=videosLista)
            except:
                embed=discord.Embed(description="Não foi possível realizar a pesquisa.", colour=discord.Colour.orange())
                await ctx.send(embed=embed)
            msg = await self.client.wait_for('Message', check=lambda message: message.author == ctx.author)
            try:
                if int(msg.content) >= 1 and int(msg.content) <= 5:
                    num = int(msg.content)-1
                    url = 'https://www.youtube.com'+str(json.loads(yt)['videos'][num]['url_suffix'])
                else:
                    embed=discord.Embed(description="Número inválido.", colour=discord.Colour.orange())
                    await msgVideo.edit(embed=embed)
            except:
                embed=discord.Embed(description="Caractere inválido.", colour=discord.Colour.orange())
                await msgVideo.edit(embed=embed)
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True', 'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
        }]}
        bol = True
        db = sqlite3.connect('./db/quiz.sqlite')
        cursor = db.cursor()
        cursor.execute("SELECT link FROM main WHERE id = (?)", (str(ctx.message.guild.id),))
        links = cursor.fetchall()
        cursor.execute("SELECT musica FROM main WHERE id = (?)", (str(ctx.message.guild.id),))
        listaMusicas = cursor.fetchall()
        cursor.execute("SELECT artista FROM main WHERE id = (?)", (str(ctx.message.guild.id),))
        listaArtistas = cursor.fetchall()
        db.commit()
        cursor.close()
        db.close()
        var=0
        print(url)
        while bol and var<3:
          try:
            with YoutubeDL(YDL_OPTIONS) as ydl:
              info = ydl.extract_info(url, download=False)
            bol = False
          except:
            if var==2 and (("www.youtube.com/" in url) or ("youtu.be" in url)):
                embed = discord.Embed(description="Não foi possível extrair o vídeo.", colour=discord.Colour.orange())
                await ctx.send(embed=embed)
            var+=1
            print('Erro...')
        if var < 3:
            embed=discord.Embed(description="Digite o nome do autor:", colour=discord.Colour.orange())
            await ctx.send(embed=embed)
            autor = await self.client.wait_for('Message', check=lambda message: message.author == ctx.author)
            embed=discord.Embed(description="Digite o nome da música:", colour=discord.Colour.orange())
            await ctx.send(embed=embed)
            musica = await self.client.wait_for('Message', check=lambda message: message.author == ctx.author)
            bolMus = True
            for i in range(len(links)):
                if (str(url) == str(links[i])[2:-3]) or ((str(musica.content).lower() == str(listaMusicas[i])[2:-3]) and (str(autor.content).lower() == str(listaArtistas[i])[2:-3])):
                    bolMus = False
            if(bolMus):
                try:
                    db = sqlite3.connect('./db/quiz.sqlite')
                    cursor = db.cursor()
                    cursor.execute("INSERT INTO main(link, id, nome, artista, musica) VALUES (?,?,?,?,?)", (url, str(ctx.message.guild.id), info['title'], str(autor.content).lower(), str(musica.content).lower()))
                    db.commit()
                    cursor.close()
                    db.close()
                    print('a')
                    embed=discord.Embed(description=f"Adicionada a música {info['title']} com sucesso.", colour=discord.Colour.orange())
                    await ctx.send(embed=embed)
                except:
                    embed=discord.Embed(description="Não foi possível adicionar a música.", colour=discord.Colour.orange())
                    await ctx.send(embed=embed)
            else:
                embed=discord.Embed(description="Já existe uma música com esse nome.", colour=discord.Colour.orange())
                await ctx.send(embed=embed)
    @commands.command(aliases=['qrem'], brief="Remove uma música do quiz.")
    async def quizRemove(self, ctx, *, nome):
          try:
              db = sqlite3.connect('./db/quiz.sqlite')
              cursor = db.cursor()
              cursor.execute("DELETE FROM main WHERE nome=(?) AND id=(?)", (nome, str(ctx.message.guild.id)))
              db.commit()
              cursor.close()
              db.close()
              embed=discord.Embed(description=f"Removida a música {nome} com sucesso.", colour=discord.Colour.orange())
              await ctx.send(embed=embed)
          except:
              embed=discord.Embed(description="Não foi possível remover a música", colour=discord.Colour.orange())
              await ctx.send(embed=embed)

    @commands.command(aliases=['qlis'], brief="Lista as músicas do quiz.")
    async def quizLista(self, ctx):
            db = sqlite3.connect('./db/quiz.sqlite')
            cursor = db.cursor()
            cursor.execute("SELECT nome FROM main WHERE id = (?)", (str(ctx.message.guild.id),))
            nomes = cursor.fetchall()
            cursor.execute("SELECT link FROM main WHERE id = (?)", (str(ctx.message.guild.id),))
            links = cursor.fetchall()
            pages=[]
            for i in range((len(nomes)//5)+1):
                page=discord.Embed(
                    title = f'Page {i+1}/{(len(nomes)//5)+1}',
                    description= 'Lista das músicas presentes no quiz.',
                    colour=discord.Colour.orange()
                )
                try:
                  for j in range(5):
                      page.add_field(name=f'{5*i+j+1}. {str(nomes[5*i+j])[2:-3]}',value=f'{str(links[5*i+j])[2:-3]}', inline=False)
                except:
                  print('Ok')
                pages.append(page)

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
            

            cursor.close()
            db.close()

    @commands.command(aliases=['qs','qstart'], brief="Inicia o quiz.")
    async def quizStart(self,ctx,*,numMus: int):
        async def afkSystem(self, ctx):
          voice = get(self.client.voice_clients, guild=ctx.guild)
          db = sqlite3.connect('./db/afk.sqlite')
          cursor = db.cursor()
          cursor.execute("SELECT afkSystem FROM main WHERE id = (?)", (str(ctx.message.guild.id),))
          afk = cursor.fetchone()
          if afk is None:
            cursor.execute("INSERT INTO main(id, afkSystem) VALUES (?,?)", (str(ctx.message.guild.id),'1',))
            db.commit()
            cursor.close()
            db.close()
            while(True):
              await asyncio.sleep(290)
              if (voice and not(voice.is_playing())) or not(voice):
                  await asyncio.sleep(10)
                  if (voice and not(voice.is_playing())) or not(voice):
                    if voice:
                      await voice.disconnect()
                    db = sqlite3.connect('./db/afk.sqlite')
                    cursor = db.cursor()
                    cursor.execute("DELETE FROM main WHERE id = (?)", (str(ctx.message.guild.id),))
                    db.commit()
                    cursor.close()
                    db.close()
                    break
          else:
            db.commit()
            cursor.close()
            db.close()
        
        self.client.loop.create_task(afkSystem(self, ctx))
        ch = ctx.message.channel
        db = sqlite3.connect('./db/quiz.sqlite')
        cursor = db.cursor()
        cursor.execute("INSERT INTO info(OnOff, musInt, contagem, id) VALUES (?,?,?,?)", (1, 0, 0, ctx.message.guild.id))
        db.commit()
        cursor.close()
        db.close()
        resp = []

        def check_music(numM: int, title: str, link: str):
            resp.clear()
            db = sqlite3.connect('./db/quiz.sqlite')
            cursor = db.cursor()
            cursor.execute("SELECT contagem FROM info WHERE id = (?)", ((ctx.message.guild.id),))
            contagem = int(str(cursor.fetchone())[1:-2])
            cursor.execute("SELECT pontos FROM pontuacao WHERE id = (?) ORDER BY pontos DESC", ((ctx.message.guild.id),))
            pontos = cursor.fetchall()
            cursor.execute("SELECT nome FROM pontuacao WHERE id = (?) ORDER BY pontos DESC", ((ctx.message.guild.id),))
            nome = cursor.fetchall()
            db.commit()
            cursor.close()
            db.close()
            if contagem < numM:
                try: 
                    if contagem != 0:
                        if len(nome)!=0:
                            page=discord.Embed(
                                title = f'{title}',
                                url=f'{link}',
                                colour=discord.Colour.orange()
                            )
                            for i in range(len(nome)):
                                page.add_field(name=f"{i+1}. Nome: {str(nome[i])[2:-3]}", value=f"{str(pontos[i])[1:-2]} pontos.", inline=False) 
                            asyncio.run_coroutine_threadsafe(ctx.send(embed=page), self.client.loop)
                        else:
                            page=discord.Embed(
                                title = f'{title}',
                                url=f'{link}',
                                colour=discord.Colour.orange()
                            )
                            page.add_field(name=f"Ninguém pontuou", value=f":(", inline=False) 
                            asyncio.run_coroutine_threadsafe(ctx.send(embed=page), self.client.loop)
                except:
                    pass
                passar=True
                while passar:
                    bolMusPast = True
                    tem = False
                    musInt = random.randint(0,len(links)-1)
                    while bolMusPast:
                        for j in range(len(musIntPast)):
                            if musInt == musIntPast[j]:
                                tem = True
                        if tem:
                            musInt = random.randint(0,len(links)-1)
                            tem = False
                        else:
                            bolMusPast = False

                    bol = True
                    i=0
                    while bol and i<4:
                        try:
                            with YoutubeDL(YDL_OPTIONS) as ydl:
                                info = ydl.extract_info(str(links[musInt])[2:-3], download=False)
                            bol = False
                        except:
                            print('Erro...')
                            i+=1
                    if i>3:
                        db = sqlite3.connect('./db/quiz.sqlite')
                        cursor = db.cursor()
                        cursor.execute("DELETE FROM main WHERE id = (?) AND link = (?)", (ctx.message.guild.id, str(links[musInt])[2:-3]))
                        db.commit()
                        cursor.close()
                        db.close()
                        embed=discord.Embed(description=f"A música com o link {str(links[musInt])[2:-3]} foi removida devido a problemas ao baixá-la.\n\nTocando a próxima música...", colour=discord.Colour.orange())
                        asyncio.run_coroutine_threadsafe(ctx.send(embed=embed), self.client.loop)
                        musIntPast.append(musInt)
                    else:
                        passar=False

                musIntPast.append(musInt)
                db = sqlite3.connect('./db/quiz.sqlite')
                cursor = db.cursor()
                cursor.execute("UPDATE info SET musInt = (?) WHERE id = (?)", (musInt, ctx.message.guild.id))
                db.commit()
                cursor.close()
                db.close()


                url = info['formats'][0]['url']
                titleAnt = info['title']
                db = sqlite3.connect('./db/quiz.sqlite')
                cursor = db.cursor()
                cursor.execute("UPDATE info SET contagem = (?) WHERE id = (?)", (contagem+1, ctx.message.guild.id))
                db.commit()
                cursor.close()
                db.close()
                tempo=random.randint(0,info['duration'])
                if(tempo-20>=0):
                    minFin = int(tempo)//60
                    secFin = int(tempo)%60
                    minIni = int(tempo-20)//60
                    secIni = int(tempo-20)%60
                else:
                    minFin = int(tempo+20)//60
                    secFin = int(tempo+20)%60
                    minIni = int(tempo)//60
                    secIni = int(tempo)%60

                FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': f'-vn -ss {minIni}:{secIni} -to {minFin}:{secFin}'}
                voice.play(FFmpegPCMAudio(url, **FFMPEG_OPTIONS), after=lambda e: check_music(numM, titleAnt, str(links[musInt])[2:-3]))
            else:
                db = sqlite3.connect('./db/quiz.sqlite')
                cursor = db.cursor()
                cursor.execute("SELECT pontos FROM pontuacao WHERE id = (?) ORDER BY pontos DESC",((ctx.message.guild.id),))
                pontos = cursor.fetchall()
                cursor.execute("SELECT nome FROM pontuacao WHERE id = (?) ORDER BY pontos DESC",((ctx.message.guild.id),))
                nome = cursor.fetchall()
                if len(nome)!=0:
                    page=discord.Embed(
                        title = f'{title}',
                        description='Quiz finalizado',
                        url=f'{link}',
                        colour=discord.Colour.orange()
                    )
                    for i in range(len(nome)):
                        page.add_field(name=f"{i+1}. Nome: {str(nome[i])[2:-3]}", value=f"{str(pontos[i])[1:-2]} ponto(s).", inline=False) 
                    asyncio.run_coroutine_threadsafe(ctx.send(embed=page), self.client.loop)
                    print('quiz finalizado')
                else:
                    page=discord.Embed(
                        title = f'{title}',
                        description='Quiz finalizado',
                        url=f'{link}',
                        colour=discord.Colour.orange()
                    )
                    page.add_field(name=f"Ninguém pontuou", value=f":(", inline=False) 
                    asyncio.run_coroutine_threadsafe(ctx.send(embed=page), self.client.loop)
                    print('quiz finalizado')
                cursor.execute("DELETE FROM info WHERE id = (?)", ((ctx.message.guild.id),))
                cursor.execute("DELETE FROM pontuacao WHERE id = (?)", ((ctx.message.guild.id),))
                db.commit()
                cursor.close()
                db.close()
                
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        
        db = sqlite3.connect('./db/quiz.sqlite')
        cursor = db.cursor()
        cursor.execute("SELECT link FROM main WHERE id = (?)", (str(ctx.message.guild.id),))
        links = cursor.fetchall()
        cursor.execute("SELECT musica FROM main WHERE id = (?)", (str(ctx.message.guild.id),))
        musicas = cursor.fetchall()
        cursor.execute("SELECT artista FROM main WHERE id = (?)", (str(ctx.message.guild.id),))
        artistas = cursor.fetchall()
        db.commit()
        cursor.close()
        db.close()
        if(numMus<=len(links) and numMus!=1):
            db = sqlite3.connect('./db/music.sqlite')
            cursor = db.cursor()
            cursor.execute("DELETE FROM main WHERE id = (?)", (str(ctx.message.guild.id),))
            db.commit()
            cursor.close()
            db.close()
            voice.stop()
            YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True', 'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
            }]}
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            bol = True
            while bol:
                try:
                    with YoutubeDL(YDL_OPTIONS) as ydl:
                        info = ydl.extract_info('https://www.youtube.com/watch?v=fZdvcRTE7FQ&ab_channel=WBREdition', download=False)
                    bol = False
                except:
                    pass
            url = info['formats'][0]['url']
            voice.play(FFmpegPCMAudio(url, **FFMPEG_OPTIONS), after=lambda e: check_music(numMus, '', ''))
            db = sqlite3.connect('./db/quiz.sqlite')
            cursor = db.cursor()
            cursor.execute("SELECT OnOff FROM info WHERE id = (?)", ((ctx.message.guild.id),))
            OnOff = int(str(cursor.fetchone())[1:-2])
            db.commit()
            cursor.close()
            db.close()
            musIntPast = []
            def check(message):
              return message.author.id != self.client.user.id
            while OnOff!="o":
                msg = await self.client.wait_for('Message', check=check)
                db = sqlite3.connect('./db/quiz.sqlite')
                cursor = db.cursor()
                cursor.execute("SELECT OnOff FROM info WHERE id = (?)", ((ctx.message.guild.id),))
                OnOff = str(cursor.fetchone())[1:-2]
                if OnOff!='o':
                    cursor.execute("SELECT musInt FROM info WHERE id = (?)", ((ctx.message.guild.id),))
                    musInt = int(str(cursor.fetchone())[1:-2])
                    cursor.execute("SELECT pontos FROM pontuacao WHERE id = (?) AND nome = (?) ORDER BY pontos",(ctx.message.guild.id, msg.author.name))
                    pontos = cursor.fetchall()
                    teste = True
                    for i in range(len(resp)):
                        if msg.content == resp[i]:
                            teste = False
                    
                    if (teste == True) and (SequenceMatcher(a=(msg.content).lower(),b=str(artistas[musInt])[2:-3]).ratio() >= 0.85 or SequenceMatcher(a=(msg.content).lower(),b=str(musicas[musInt])[2:-3]).ratio() >= 0.85) and (msg.channel == ch) and voice.is_playing():
                        testeBol = True
                        for j in range(len(resp)):
                            if SequenceMatcher(a=(msg.content).lower(),b=resp[j]).ratio() >= 0.85:
                                testeBol=False
                        if testeBol:
                            if(len(pontos)!=0):
                                cursor.execute('UPDATE pontuacao SET pontos = pontos + 1 WHERE id = (?) AND nome = (?)', (ctx.message.guild.id, msg.author.name))
                            else:
                                cursor.execute('INSERT INTO pontuacao(nome, pontos, id) VALUES (?,?,?)', (msg.author.name, 1, ctx.message.guild.id))
                            if SequenceMatcher(a=(msg.content).lower(),b=str(artistas[musInt])[2:-3]).ratio() >= 0.85:
                                resp.append((str(artistas[musInt])[2:-3]).lower())
                            if SequenceMatcher(a=(msg.content).lower(),b=str(musicas[musInt])[2:-3]).ratio() >= 0.85:
                                resp.append((str(musicas[musInt])[2:-3]).lower())
                            await msg.add_reaction('\u2705')
                    elif msg.channel == ch and voice.is_playing():
                        await msg.add_reaction('\u274c')
                    if((str(artistas[musInt])[2:-3] in resp) and (str(musicas[musInt])[2:-3] in resp)):
                        voice.stop()

                db.commit()
            cursor.close()
            db.close()
        else:
            await ctx.send('Erro: deve conter pelo menos 2 músicas ou o número solicitado é maior do número de músicas na lista do quiz.')
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