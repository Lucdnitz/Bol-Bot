import random
import discord
from discord.ext import commands, tasks
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from youtube_search import YoutubeSearch
import traceback, json
import sqlite3
import asyncio
import spotipy
import spotipy.oauth2 as oauth2

class Music(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['j'], brief='Faz o bot se juntar a chamada')
    async def join(self, ctx):
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
            cursor.execute("DELETE FROM skipvote WHERE id = (?)", (ctx.message.guild.id,))
            cursor.execute("DELETE FROM stopvote WHERE id = (?)", (ctx.message.guild.id,))
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
        
    @commands.command(aliases=['tocar', 'p', 'PLAY', 'P'], brief='Faz o bot tocar uma música.')
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
            musica = cursor.fetchall()
            cursor.execute("DELETE FROM skipvote WHERE id = (?)", (ctx.message.guild.id,))
            db.commit()
            cursor.close()
            db.close()
            try:
                db = sqlite3.connect('./db/music.sqlite')
                cursor = db.cursor()
                cursor.execute("SELECT pessoa FROM main WHERE id = (?)", (str(ctx.message.guild.id),))
                pessoa = cursor.fetchall()
                cursor.execute("SELECT shuffle FROM shuffle WHERE id = (?)", (str(ctx.message.guild.id),))
                shuffle = str(cursor.fetchone())[1:-2]
                if shuffle=='1':
                  rdm = random.randint(0,len(musica)-1)
                  urlQue = str(musica[rdm])[2:-3]
                  pessoa = str(pessoa[rdm])[2:-3]
                else:
                  urlQue = str(musica[0])[2:-3]
                  pessoa = str(pessoa[0])[2:-3]
                cursor.execute("DELETE FROM main WHERE musica=(?) AND id=(?)", (urlQue, str(ctx.message.guild.id)))
                db.commit()
                cursor.close()
                db.close()
                bol = True
                yt = YoutubeSearch(urlQue, max_results=1).to_json()
                urlQue = 'https://www.youtube.com'+str(json.loads(yt)['videos'][0]['url_suffix'])
                while bol:
                    try:
                        if urlQue != '':
                          with YoutubeDL(YDL_OPTIONS) as ydl:
                            info = ydl.extract_info(urlQue, download=False)
                        bol = False
                    except:
                        embed=discord.Embed(description="Não foi possível extrair o vídeo.", colour=discord.Colour.orange())
                        asyncio.run_coroutine_threadsafe(ctx.send(embed=embed), self.client.loop)
                        bol=False
                        break
                if not voice.is_playing() and voice:
                  URLQUE = info['formats'][0]['url']
                  voice.play(FFmpegPCMAudio(URLQUE, **FFMPEG_OPTIONS), after=lambda e: check_queue())
                  embed=discord.Embed(title=f"{info['title']}", url=f"{urlQue}", description=f"(Duração: {int(info['duration'])//60} minutos e {int(info['duration'])%60} segundos) || Vídeo pedido por: {pessoa}", colour=discord.Colour.orange())
                  asyncio.run_coroutine_threadsafe(ctx.send(embed=embed), self.client.loop)
                  voice.is_playing()
                  db = sqlite3.connect('./db/music.sqlite')
                  cursor = db.cursor()
                  cursor.execute("SELECT loop FROM loop WHERE id = (?)", (str(ctx.message.guild.id),))
                  loop = str(cursor.fetchone())[1:-2]
                  if loop == '1':
                    cursor.execute('INSERT INTO main(id,musica,pessoa) VALUES (?,?,?)', (str(ctx.message.guild.id),info['title'],'Vídeo em loop.'))
                  db.commit()
                  cursor.close()
                  db.close()
            except:
                if len(musica)<=0:
                  embed=discord.Embed(description="Não há mais nenhuma música na fila.\n\nSe está gostando do bot, vote em https://top.gg/bot/771628845530087444/vote \nE siga nossa página no twitter: https://twitter.com/BolBot_", colour=discord.Colour.orange())
                  asyncio.run_coroutine_threadsafe(ctx.send(embed=embed), self.client.loop)
                else:
                  check_queue()
        auth_manager = oauth2.SpotifyClientCredentials(client_id='529300a5a9b340ef838bff39a33376b0', client_secret='947505f8c3b34258a8f8d2509e86d8b8')
        sp = spotipy.Spotify(auth_manager=auth_manager)
        spotify=False
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
        elif ("https://open.spotify.com/track/") in url: 
            url = url[31:]
            track_info=sp.track(url)
            url = track_info['artists'][0]['name']+' - '+track_info['name']
            yt = YoutubeSearch(url, max_results=1).to_json()
            url = 'https://www.youtube.com'+str(json.loads(yt)['videos'][0]['url_suffix'])
        elif ("https://open.spotify.com/playlist/") in url:
          spotify=True
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
        if spotify:
          db = sqlite3.connect('./db/music.sqlite')
          cursor = db.cursor()
          url = url[34:]
          track_info=sp.playlist(url)
          for i in range(len(track_info['tracks']['items'])):
            try:
              url = track_info['tracks']['items'][i]['track']['artists'][0]['name']+' - '+track_info['tracks']['items'][i]['track']['name']
            except:
              url = track_info['tracks']['items'][i]['track']['name']
            cursor.execute("INSERT INTO main(musica, id, pessoa) VALUES (?,?,?)", (url, str(ctx.message.guild.id), ctx.message.author.name))
          db.commit()
          cursor.close()
          db.close()
          check_queue()
          embed=discord.Embed(description=f"Foram adicionadas {len(track_info['tracks']['items'])} músicas pelo spotify.\nPedido por {ctx.message.author.name}.", colour=discord.Colour.orange())
          await ctx.send(embed=embed)
        else:
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
          print(info)          
          try:
            if info!=None:
              if not voice.is_playing():
                URL = info['formats'][0]['url']
                voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda  e: check_queue())
                db = sqlite3.connect('./db/music.sqlite')
                cursor = db.cursor()
                cursor.execute("SELECT loop FROM loop WHERE id = (?)", (str(ctx.message.guild.id),))
                loop = str(cursor.fetchone())[1:-2]
                if loop == '1':
                  cursor.execute('INSERT INTO main(id,musica,pessoa) VALUES (?,?,?)', (str(ctx.message.guild.id),info['title'],'Vídeo em loop.'))
                db.commit()
                cursor.close()
                db.close()
                embed=discord.Embed(title=f"{info['title']}", url=f"{url}", description=f"(Duração: {int(info['duration'])//60} minutos e {int(info['duration'])%60} segundos) || Vídeo pedido por: {ctx.message.author.name}", colour=discord.Colour.orange())
                try:
                  await msgVideos.edit(embed=embed)
                except:
                  await ctx.send(embed=embed)
              else:
                db = sqlite3.connect('./db/music.sqlite')
                cursor = db.cursor()
                cursor.execute("INSERT INTO main(musica, id, pessoa) VALUES (?,?,?)", (info['title'], str(ctx.message.guild.id), ctx.message.author.name))
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
                      db = sqlite3.connect('./db/music.sqlite')
                      cursor = db.cursor()
                      cursor.execute("SELECT loop FROM loop WHERE id = (?)", (str(ctx.message.guild.id),))
                      loop = str(cursor.fetchone())[1:-2]
                      db.commit()
                      cursor.close()
                      db.close()
                      embed=discord.Embed(title=f"{infoIn['formats'][i]['title']}", url=f"{URL}", description=f"(Duração: {int(infoIn['formats'][i]['duration'])//60} minutos e {int(infoIn['formats'][i]['duration'])%60} segundos) || Vídeo pedido por: {ctx.message.author.name}", colour=discord.Colour.orange())
                      try:
                        await msgVideos.edit(embed=embed)
                      except:
                        await ctx.send(embed=embed)
                    except:
                      pass
                  elif i<350:
                    try:
                      db = sqlite3.connect('./db/music.sqlite')
                      cursor = db.cursor()
                      cursor.execute("INSERT INTO main(musica, id, pessoa) VALUES (?,?,?)", (str(info['entries'][i]['title']), str(ctx.message.guild.id), ctx.message.author.name))
                      db.commit()
                    except:
                      pass
                  else:
                    break
                if loop == '1':
                  cursor.execute('INSERT INTO main(id,musica,pessoa) VALUES (?,?,?)', (str(ctx.message.guild.id),str(info['entries'][0]['title']),'Vídeo em loop.'))
                  db.commit()
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
      channel = ctx.message.author.voice.channel
      voice = get(self.client.voice_clients, guild=ctx.guild)
      db = sqlite3.connect('./db/music.sqlite')
      cursor = db.cursor()
      cursor.execute('SELECT skipvote FROM skip WHERE id = (?)', (str(ctx.message.guild.id),))
      skip=str(cursor.fetchone())[1:-2]
      if skip == 'o' or skip=='0':
        if voice and voice.is_playing():
            voice.stop()
            embed=discord.Embed(description="Tocando a próxima música.", colour=discord.Colour.orange())
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(description="Nenhuma música está tocando.", colour=discord.Colour.orange())
            await ctx.send(embed=embed)
      elif skip == '1':
        if voice and voice.is_playing():
          cursor.execute('SELECT vote FROM skipvote WHERE id = (?)', (str(ctx.message.guild.id),))
          skipList=cursor.fetchall()
          skipNum=len(skipList)
          autorMsg = "('"+str(ctx.message.author)+"',)"
          check = False
          for i in range(skipNum):
            if str(skipList[i]) == autorMsg:
              check=True
          if not(check):
            cursor.execute("INSERT INTO skipvote(vote,id) VALUES (?,?)", (str(ctx.message.author),ctx.message.guild.id))
            if skipNum+1 >= ((len(channel.voice_states)-1)*2)//3:
              voice.stop()
              embed=discord.Embed(description="Tocando a próxima música.", colour=discord.Colour.orange())
              await ctx.send(embed=embed)
              cursor.execute("DELETE FROM skipvote WHERE id = (?)", (ctx.message.guild.id,))
            else:
              embed=discord.Embed(description=f"Votação de skip ({skipNum+1}/{((len(channel.voice_states)-1)*2)//3})", colour=discord.Colour.orange())
              await ctx.send(embed=embed)
          else:
            cursor.execute("DELETE FROM skipvote WHERE id = (?) AND vote = (?)", (ctx.message.guild.id,str(ctx.message.author)))
            if skipNum-1 >= ((len(channel.voice_states)-1)*2)//3:
              voice.stop()
              embed=discord.Embed(description="Tocando a próxima música.", colour=discord.Colour.orange())
              await ctx.send(embed=embed)
              cursor.execute("DELETE FROM skipvote WHERE id = (?)", (ctx.message.guild.id,))
            else:
              embed=discord.Embed(description=f"Votação de skip ({skipNum-1}/{((len(channel.voice_states)-1)*2)//3})", colour=discord.Colour.orange())
              await ctx.send(embed=embed)
        else:
          embed=discord.Embed(description="Nenhuma música está tocando.", colour=discord.Colour.orange())
          await ctx.send(embed=embed)
      db.commit()
      cursor.close()
      db.close()


    @commands.command(pass_context=True, aliases=['s', 'parar'], brief='Para a música.')
    async def stop(self, ctx):
      voice = get(self.client.voice_clients, guild=ctx.guild)
      if ctx.message.author.guild_permissions.administrator:
        db = sqlite3.connect('./db/music.sqlite')
        cursor = db.cursor()
        cursor.execute("DELETE FROM main WHERE id = (?)", (str(ctx.message.guild.id),))
        db.commit()
        cursor.close()
        db.close()
        voice.stop()
      else:
        channel = ctx.message.author.voice.channel
        if voice and voice.is_playing():
          db = sqlite3.connect('./db/music.sqlite')
          cursor = db.cursor()
          cursor.execute('SELECT vote FROM stopvote WHERE id = (?)', (str(ctx.message.guild.id),))
          stopList=cursor.fetchall()
          stopNum=len(stopList)
          autorMsg = "('"+str(ctx.message.author)+"',)"
          check = False
          for i in range(stopNum):
            if str(stopList[i]) == autorMsg:
              check=True
          if not(check):
            cursor.execute("INSERT INTO stopvote(vote,id) VALUES (?,?)", (str(ctx.message.author),ctx.message.guild.id))
            if stopNum+1 >= ((len(channel.voice_states)-1)*2)//3:
              cursor.execute("DELETE FROM main WHERE id = (?)", (str(ctx.message.guild.id),))
              cursor.execute("DELETE FROM stopvote WHERE id = (?)", (ctx.message.guild.id,))
              db.commit()
              cursor.close()
              db.close()
              voice.stop()
            else:
              embed=discord.Embed(description=f"Votação de stop ({stopNum+1}/{((len(channel.voice_states)-1)*2)//3})", colour=discord.Colour.orange())
              await ctx.send(embed=embed)
          else:
            cursor.execute("DELETE FROM stopvote WHERE id = (?) AND vote = (?)", (ctx.message.guild.id,str(ctx.message.author)))
            if stopNum-1 >= ((len(channel.voice_states)-1)*2)//3:
              cursor.execute("DELETE FROM main WHERE id = (?)", (str(ctx.message.guild.id),))
              cursor.execute("DELETE FROM stopvote WHERE id = (?)", (ctx.message.guild.id,))
              db.commit()
              cursor.close()
              db.close()
              voice.stop()
            else:
              embed=discord.Embed(description=f"Votação de stop ({stopNum-1}/{((len(channel.voice_states)-1)*2)//3})", colour=discord.Colour.orange())
              await ctx.send(embed=embed)
        else:
          embed=discord.Embed(description="Nenhuma música está tocando.", colour=discord.Colour.orange())
          await ctx.send(embed=embed)
        
        try:
          db.commit()
          cursor.close()
          db.close()
        except:
          pass
    @commands.command(aliases=['que'], brief="Lista as músicas da fila.")
    async def queue(self, ctx):
          try:
            db = sqlite3.connect('./db/music.sqlite')
            cursor = db.cursor()
            cursor.execute("SELECT pessoa FROM main WHERE id = (?)", (str(ctx.message.guild.id),))
            pessoas = cursor.fetchall()
            cursor.execute("SELECT musica FROM main WHERE id = (?)", (str(ctx.message.guild.id),))
            musica = cursor.fetchall()
            cursor.execute("SELECT loop FROM loop WHERE id = (?)", (str(ctx.message.guild.id),))
            loop = str(cursor.fetchone())[1:-2]
            cursor.execute("SELECT shuffle FROM shuffle WHERE id = (?)", (str(ctx.message.guild.id),))
            shuffle = str(cursor.fetchone())[1:-2]
            pages=[]
            rang = 0
            if len(musica)%5==0:
              rang = (len(musica)//5)
            else:
              rang = (len(musica)//5)+1
            if loop=='1':
              strLoop="\n\nPlaylist em loop"
            else:
              strLoop=""
            if shuffle=='1':
              strShuffle="\n\nPlaylist no modo aleatório"
            else:
              strShuffle=""
            for i in range(rang):
                page=discord.Embed(
                    title = f'Página {i+1}/{(rang)}',
                    description= f'Lista das músicas presentes na fila.{strLoop}{strShuffle}',
                    colour=discord.Colour.orange()
                  )
                try:
                  for j in range(5):
                      page.add_field(name=f'{5*i+j+1}. {str(musica[5*i+j])[2:-3]}',value=f'Pedido por: {str(pessoas[5*i+j])[2:-3]}', inline=False)
                except:
                  print('Ok')
                pages.append(page)
            if len(pages)<1:
              embed=discord.Embed(description=f"Não há nenhuma música na fila.{strLoop}{strShuffle}", colour=discord.Colour.orange())
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

    @commands.command(pass_context=True)
    async def loop(self, ctx):
      voice = get(self.client.voice_clients, guild=ctx.guild)
      db = sqlite3.connect('./db/music.sqlite')
      cursor = db.cursor()
      cursor.execute('SELECT loop FROM loop WHERE id = (?)', (str(ctx.message.guild.id),))
      loop=str(cursor.fetchone())[1:-2]
      if loop == 'o':
        cursor.execute("INSERT INTO loop(loop,id) VALUES (?,?)", (1,str(ctx.message.guild.id)))
        embed=discord.Embed(description="A playlist foi colocada em loop.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)
        if voice and voice.is_playing():
          embed=discord.Embed(description="A música atual não entrará no loop. Para que ela seja adicionada, coloque-a novamente.", colour=discord.Colour.orange())
          await ctx.send(embed=embed)
      elif loop == '1':
        cursor.execute("UPDATE loop SET loop = (?) WHERE id = (?)", (0,str(ctx.message.guild.id)))
        cursor.execute("DELETE FROM main WHERE id = (?) AND pessoa = (?)", (str(ctx.message.guild.id),'Vídeo em loop.'))
        embed=discord.Embed(description="A playlist foi tirada do loop.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)
      else:
        cursor.execute("UPDATE loop SET loop = (?) WHERE id = (?)", (1,str(ctx.message.guild.id)))
        embed=discord.Embed(description="A playlist foi colocada em loop.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)
        if voice and voice.is_playing():
          embed=discord.Embed(description="A música atual não entrará no loop. Para que ela seja adicionada, coloque-a novamente.", colour=discord.Colour.orange())
          await ctx.send(embed=embed)

      db.commit()
      cursor.close()
      db.close()

    @commands.command(pass_context=True, aliases=['fs'])
    async def forceskip(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 164390451045072896:
          if voice and voice.is_playing():
              voice.stop()
              embed=discord.Embed(description="Tocando a próxima música.", colour=discord.Colour.orange())
              await ctx.send(embed=embed)
          else:
              embed=discord.Embed(description="Nenhuma música está tocando.", colour=discord.Colour.orange())
              await ctx.send(embed=embed)
        else:
          embed=discord.Embed(description="Você não possui permissões suficientes (permissão necessária: administrador).", colour=discord.Colour.orange())
          await ctx.send(embed=embed)
    
    @commands.command(pass_context=True, aliases=['vs'])
    async def voteskip(self, ctx):
      if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 164390451045072896:
        db = sqlite3.connect('./db/music.sqlite')
        cursor = db.cursor()
        cursor.execute('SELECT skipvote FROM skip WHERE id = (?)', (str(ctx.message.guild.id),))
        skip=str(cursor.fetchone())[1:-2]
        if skip == 'o':
          cursor.execute("INSERT INTO skip(skipvote,id) VALUES (?,?)", (1,str(ctx.message.guild.id)))
          embed=discord.Embed(description="O voteskip foi ativado.", colour=discord.Colour.orange())
          await ctx.send(embed=embed)
        elif skip == '1':
          cursor.execute("UPDATE skip SET skipvote = (?) WHERE id = (?)", (0,str(ctx.message.guild.id)))
          embed=discord.Embed(description="O voteskip foi desativado.", colour=discord.Colour.orange())
          await ctx.send(embed=embed)
        else:
          cursor.execute("UPDATE skip SET skipvote = (?) WHERE id = (?)", (1,str(ctx.message.guild.id)))
          embed=discord.Embed(description="O voteskip foi ativado.", colour=discord.Colour.orange())
          await ctx.send(embed=embed)
        db.commit()
        cursor.close()
        db.close()
      else:
        embed=discord.Embed(description="Você não possui permissões suficientes (permissão necessária: administrador).", colour=discord.Colour.orange())
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def shuffle(self, ctx):
      db = sqlite3.connect('./db/music.sqlite')
      cursor = db.cursor()
      cursor.execute('SELECT shuffle FROM shuffle WHERE id = (?)', (str(ctx.message.guild.id),))
      shuffle=str(cursor.fetchone())[1:-2]
      if shuffle == 'o':
        cursor.execute("INSERT INTO shuffle(shuffle,id) VALUES (?,?)", (1,str(ctx.message.guild.id)))
        embed=discord.Embed(description="A playlist foi colocada no modo aleatório.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)
      elif shuffle == '1':
        cursor.execute("UPDATE shuffle SET shuffle = (?) WHERE id = (?)", (0,str(ctx.message.guild.id)))
        embed=discord.Embed(description="A playlist foi tirada do modo aleatório.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)
      else:
        cursor.execute("UPDATE shuffle SET shuffle = (?) WHERE id = (?)", (1,str(ctx.message.guild.id)))
        embed=discord.Embed(description="A playlist foi colocada no modo aleatório.", colour=discord.Colour.orange())
        await ctx.send(embed=embed)
      db.commit()
      cursor.close()
      db.close()

def setup(client):
    client.add_cog(Music(client)) 