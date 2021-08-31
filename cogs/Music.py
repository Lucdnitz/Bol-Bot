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
        
        print(len(self.client.guilds))
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


        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
          await voice.move_to(channel)
          embed=discord.Embed(description=f"Eu fui movido para o canal {channel}", colour=discord.Colour.orange())
          await ctx.send(embed=embed)
          self.client.loop.create_task(afkSystem(self, ctx))
        else:
          voice = await channel.connect()
          embed=discord.Embed(description=f"Eu entrei no canal {channel}.", colour=discord.Colour.orange())
          await ctx.send(embed=embed)
          self.client.loop.create_task(afkSystem(self, ctx))
          
    @commands.command(aliases=['l'], brief='Faz o bot sair da chamada(caso o quiz ou o player derem problema, utilize este comando)')
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
          await voice.disconnect()
          embed=discord.Embed(description=f"Eu saí do canal {channel}", colour=discord.Colour.orange())
          await ctx.send(embed=embed)
        else:
          embed=discord.Embed(description="Eu não estou em nenhum canal.", colour=discord.Colour.orange())
          await ctx.send(embed=embed)
        try:          
            db = sqlite3.connect('./db/music.sqlite')
            cursor = db.cursor()
            cursor.execute("DELETE FROM main WHERE id = (?)", (str(ctx.message.guild.id),))
            db.commit()
            cursor.close()
            db.close()

            db = sqlite3.connect('./db/quiz.sqlite')
            cursor = db.cursor()
            cursor.execute("DELETE FROM info WHERE id = (?)", (str(ctx.message.guild.id),))
            cursor.execute("DELETE FROM pontuacao WHERE id = (?)", (str(ctx.message.guild.id),))
            db.commit()
            cursor.close()
            db.close()

            db = sqlite3.connect('./db/afk.sqlite')
            print('a')
            cursor = db.cursor()
            cursor.execute("DELETE FROM main WHERE id = (?)", (str(ctx.message.guild.id),))
            db.commit()
            cursor.close()
            db.close()
        except:
            pass
        
    @commands.command(aliases=['tocar', 'p'], brief='Faz o bot tocar uma música.')
    async def play(self, ctx, *, url):

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

        def check_queue():
            db = sqlite3.connect('./db/music.sqlite')
            cursor = db.cursor()
            cursor.execute("SELECT musica FROM main WHERE id = (?)", (str(ctx.message.guild.id),))
            musica = cursor.fetchone()
            cursor.execute("SELECT pessoa FROM main WHERE id = (?)", (str(ctx.message.guild.id),))
            pessoa = str(cursor.fetchone())[2:-3]
            urlQue = str(musica)[2:-3]
            cursor.execute("DELETE FROM main WHERE musica=(?) AND id=(?)", (urlQue, str(ctx.message.guild.id)))
            try:
                bol = True
                while bol:
                    try:
                        if urlQue != '':
                          with YoutubeDL(YDL_OPTIONS) as ydl:
                            info = ydl.extract_info(urlQue, download=False)
                        bol = False
                    except:
                        embed=discord.Embed(description="Não foi possível extrair o vídeo.", colour=discord.Colour.orange())
                        asyncio.run_coroutine_threadsafe(ctx.send(embed=embed), self.client.loop)
                if not voice.is_playing():
                  URLQUE = info['formats'][0]['url']
                  voice.play(FFmpegPCMAudio(URLQUE, **FFMPEG_OPTIONS), after=lambda e: check_queue())
                  embed=discord.Embed(title=f"{info['title']}", url=f"{urlQue}", description=f"(Duração: {int(info['duration'])//60} minutos e {int(info['duration'])%60} segundos) || Vídeo pedido por: {pessoa}", colour=discord.Colour.orange())
                  asyncio.run_coroutine_threadsafe(ctx.send(embed=embed), self.client.loop)
                  voice.is_playing()
            except:
                embed=discord.Embed(description="Não há mais nenhuma música na fila.", colour=discord.Colour.orange())
                asyncio.run_coroutine_threadsafe(ctx.send(embed=embed), self.client.loop)
            db.commit()
            cursor.close()
            db.close()

        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'False', 'dumpjson':'True','extract_flat':'in_playlist','ignoreerrors':'True', 'continue':'True', 'nooverwrites':'True','postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
        }]}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        db = sqlite3.connect('./db/music.sqlite')
        cursor = db.cursor()
        cursor.execute("SELECT search FROM search WHERE id = (?)", (str(ctx.message.guild.id),))
        search = str(cursor.fetchone())[1:-2]
        cursor.close()
        db.close()
        if search==None or search=="o":
          search=5
        else:
          search=int(search)
        if (("www.youtube.com/" in url) or ("youtu.be" in url)) and "https" in url[0:5]:
            url = url
        else:
            try:
              yt = YoutubeSearch(url, max_results=search).to_json()
            except:
              embed=discord.Embed(description=f"Não foi possível realizar a pesquisa: '{url}'", colour=discord.Colour.orange())
              await ctx.send(embed=embed)
            if search!=1:
              try:
                videosLista=discord.Embed(title="Vídeos", description=f"Para selecionar uma música digite o número correspondente do vídeo (1 a {search})", colour=discord.Colour.orange())
                for i in range(search):
                    videosLista.add_field(name=f"{i+1}. {str(json.loads(yt)['videos'][i]['title'])} ({str(json.loads(yt)['videos'][i]['duration'])})", value=f"https://www.youtube.com{str(json.loads(yt)['videos'][i]['url_suffix'])}", inline=False)
                msgVideos=await ctx.send(embed=videosLista)
              except:
                embed=discord.Embed(description="Não foi possível realizar a pesquisa.", colour=discord.Colour.orange())
                await ctx.send(embed=embed)

              msg = await self.client.wait_for('Message', check=lambda message: message.author == ctx.author)
              try:
                if int(msg.content) >= 1 and int(msg.content) <= search:
                  num = int(msg.content)-1
                  url = 'https://www.youtube.com'+str(json.loads(yt)['videos'][num]['url_suffix'])
                else:
                  embed=discord.Embed(description="Número inválido.", colour=discord.Colour.orange())
                  await msgVideos.edit(embed=embed)
              except:
                  embed=discord.Embed(description="Caractere inválido.", colour=discord.Colour.orange())
                  await msgVideos.edit(embed=embed)
            else:
              url = 'https://www.youtube.com'+str(json.loads(yt)['videos'][0]['url_suffix'])
        bol = True
        while bol:
          try:
            with YoutubeDL(YDL_OPTIONS) as ydl:
              info = ydl.extract_info(url, download=False)
            bol = False
          except:
              try:
                  embed=discord.Embed(description="Não foi possível extrair o vídeo.", colour=discord.Colour.orange())
                  await msgVideos.edit(embed=embed)
                  bol = False
              except:
                  embed=discord.Embed(description="Não foi possível extrair o vídeo.", colour=discord.Colour.orange())
                  await ctx.send(embed=embed)
                  bol = False
                  
        try:
         if info!=None:
          if not voice.is_playing():
            URL = info['formats'][0]['url']
            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda  e: check_queue())
            embed=discord.Embed(title=f"{info['title']}", url=f"{url}", description=f"(Duração: {int(info['duration'])//60} minutos e {int(info['duration'])%60} segundos) || Vídeo pedido por: {ctx.message.author.name}", colour=discord.Colour.orange())
            try:
              await msgVideos.edit(embed=embed)
            except:
              await ctx.send(embed=embed)
          else:
            db = sqlite3.connect('./db/music.sqlite')
            cursor = db.cursor()
            cursor.execute("INSERT INTO main(musica, id, pessoa) VALUES (?,?,?)", (url, str(ctx.message.guild.id), ctx.message.author.name))
            embed=discord.Embed(title=f"{info['title']}", url=f"{url}", description=f"(Duração: {int(info['duration'])//60} minutos e {int(info['duration'])%60} segundos) || Adicionado na fila por: {ctx.message.author.name}", colour=discord.Colour.orange())
            try:
              await msgVideos.edit(embed=embed)
            except:
              await ctx.send(embed=embed)
            db.commit()
            cursor.close()
            db.close()
            return
        except:
         if info != None:
          try:
            for i in range(len(info['entries'])):
              if not voice.is_playing():
                bol = True
                while bol:
                  try:
                    with YoutubeDL(YDL_OPTIONS) as ydl:
                      infoIn = ydl.extract_info(info['entries'][i]['url'], download=False)
                    bol = False
                  except:
                    embed=discord.Embed(description="Não foi possível extrair o vídeo.", colour=discord.Colour.orange())
                    try:
                      await msgVideos.edit(embed=embed)
                    except:
                      await ctx.send(embed=embed)
                try:
                  URL = infoIn['formats'][i]['url']
                  voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda  e: check_queue())
                  embed=discord.Embed(title=f"{infoIn['formats'][i]['title']}", url=f"{URL}", description=f"(Duração: {int(infoIn['formats'][i]['duration'])//60} minutos e {int(infoIn['formats'][i]['duration'])%60} segundos) || Vídeo pedido por: {ctx.message.author.name}", colour=discord.Colour.orange())
                  try:
                    await msgVideos.edit(embed=embed)
                  except:
                    await ctx.send(embed=embed)
                except:
                  pass
              elif i<350:
                try:
                  URL = 'https://www.youtube.com/watch?v='+str(info['entries'][i]['url'])
                  db = sqlite3.connect('./db/music.sqlite')
                  cursor = db.cursor()
                  cursor.execute("INSERT INTO main(musica, id, pessoa) VALUES (?,?,?)", (URL, str(ctx.message.guild.id), ctx.message.author.name))
                  db.commit()
                except:
                  pass
              else:
                break
          except:
            try:
              embed=discord.Embed(description="Vídeo indisponível", colour=discord.Colour.orange())
              await msgVideos.edit(embed=embed)
            except:
              pass
          
          cursor.close()
          db.close()
          embed=discord.Embed(title=f"{info['title']}", url=f"{url}", description=f"({i} vídeos adicionados) || Playlist pedida por: {ctx.message.author.name}", colour=discord.Colour.orange())
          try:
            await msgVideos.edit(embed=embed)
          except:
            await ctx.send(embed=embed)
        try:
          if info == None and msg >= 1 and msg<=10:
            embed=discord.Embed(description='Vídeo indisponível.', colour=discord.Colour.orange())
            await ctx.send(embed=embed)
        except Exception as e:
          if info==None and ((("www.youtube.com/" in url) or ("youtu.be" in url)) and "https" in url[0:5]):
            embed=discord.Embed(description='Vídeo indisponível.', colour=discord.Colour.orange())
            await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['pa', 'pau'], brief='Pausa a música.')
    async def pause(self, ctx):

        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.pause()
            embed=discord.Embed(description="Música pausada.", colour=discord.Colour.orange())
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(description="Não há nenhuma música tocando.", colour=discord.Colour.orange())
            await ctx.send(embed=embed)


    @commands.command(pass_context=True, aliases=['r', 'res'], brief='Retoma a música.')
    async def resume(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_paused():
            voice.resume()
            embed=discord.Embed(description="A música voltou!", colour=discord.Colour.orange())
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(description="A música não está pausada.", colour=discord.Colour.orange())
            await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['next', 'proxima'], brief='Toca a próxima música.')
    async def skip(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.stop()
            embed=discord.Embed(description="Tocando a próxima música.", colour=discord.Colour.orange())
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(description="Nenhuma música está tocando.", colour=discord.Colour.orange())
            await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['s', 'parar'], brief='Para a música.')
    async def stop(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        db = sqlite3.connect('./db/music.sqlite')
        cursor = db.cursor()
        cursor.execute("DELETE FROM main WHERE id = (?)", (str(ctx.message.guild.id),))
        db.commit()
        cursor.close()
        db.close()
        voice.stop()

    @commands.command(aliases=['que'], brief="Lista as músicas da fila.")
    async def queue(self, ctx):
      try:
            db = sqlite3.connect('./db/music.sqlite')
            cursor = db.cursor()
            cursor.execute("SELECT pessoa FROM main WHERE id = (?)", (str(ctx.message.guild.id),))
            pessoas = cursor.fetchall()
            cursor.execute("SELECT musica FROM main WHERE id = (?)", (str(ctx.message.guild.id),))
            musica = cursor.fetchall()
            pages=[]
            rang = 0
            if len(musica)%5==0:
              rang = (len(musica)//5)
            else:
              rang = (len(musica)//5)+1
            for i in range(rang):
                page=discord.Embed(
                    title = f'Página {i+1}/{(rang)}',
                    description= 'Lista das músicas presentes na fila.',
                    colour=discord.Colour.orange()
                )
                try:
                  for j in range(5):
                      page.add_field(name=f'{5*i+j+1}. {str(musica[5*i+j])[2:-3]}',value=f'Pedido por: {str(pessoas[5*i+j])[2:-3]}', inline=False)
                except:
                  print('Ok')
                pages.append(page)
            if len(pages)<1:
              embed=discord.Embed(description="Não há nenhuma música na fila.", colour=discord.Colour.orange())
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
            

            cursor.close()
            db.close()
      except:
        pass
    @commands.command(pass_context=True, aliases=['vol', 'v'])
    async def volume(self, ctx, *, volu: int):
      voice = get(self.client.voice_clients, guild=ctx.guild)
      if voice and voice.is_playing():
        if(volu <= 300 and volu >= 0):
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = (volu/100)
            await ctx.send("Volume alterado para "+str(volu)+"%")
        else:
            await ctx.send("O volume máximo é 300% e o mínimo é 0%")
      else:
          await ctx.send("Nenhuma música tocando.")


    @commands.command(pass_context=True, aliases=['search', 'src'])
    async def searchNum(self, ctx, num:int):

      db = sqlite3.connect('./db/music.sqlite')
      cursor = db.cursor()
      cursor.execute("SELECT search FROM search WHERE id = (?)", (str(ctx.message.guild.id),))
      search = str(cursor.fetchone())[1:-2]
      if search == "o" and num <= 10 and num >= 1:
        cursor.execute("INSERT INTO search(search,id) VALUES (?,?)", (num,str(ctx.message.guild.id)))
        embed=discord.Embed(description=f"O número de pesquisa foi alterado para {num}.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)
      elif num <= 10 and num >= 1:
        cursor.execute("UPDATE search SET search = (?) WHERE id = (?)", (num,str(ctx.message.guild.id)))
        embed=discord.Embed(description=f"O número de pesquisa foi altarado para {num}.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)
      else:
        embed=discord.Embed(description="O número de pesquisa não pode ser maior que 10, nem menor que 1.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)
      db.commit()
      cursor.close()
      db.close()


def setup(client):
    client.add_cog(Music(client)) 