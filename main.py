import discord as disc
import os
from discord.ext import commands

bot = commands.Bot(command_prefix='.', help_command=None)

@bot.command()
async def load(ctx, extension):
    if ctx.message.author.id == 164390451045072896:
        bot.unload_extension(f'cogs.Desativado{extension}')
        bot.load_extension(f'cogs.{extension}')
        embed=disc.Embed(description=f"Ativado a extensão {extension} com sucesso.", colour=disc.Colour.orange())
        await ctx.send(embed=embed)
    else:
        embed=disc.Embed(description="Permissão insuficiente.", colour=disc.Colour.orange())
        await ctx.send(embed=embed)

        
@bot.command()
async def unload(ctx, extension):
    if ctx.message.author.id == 164390451045072896:
        bot.unload_extension(f'cogs.{extension}')
        bot.load_extension(f'cogs.Desativado{extension}')
        embed=disc.Embed(description=f"Desativado a extensão {extension} com sucesso.", colour=disc.Colour.orange())
        await ctx.send(embed=embed)
    else:
        embed=disc.Embed(description="Permissão insuficiente.", colour=disc.Colour.orange())
        await ctx.send(embed=embed)


@bot.command()
async def help(context):
    embed= disc.Embed(title="Comando de ajuda", description="Comandos relacionados ao bot", colour=disc.Colour.orange())
    embed.add_field(name="Música", value=".play [musica] - Adiciona uma música a fila de músicas, caso não coloque um link, o bot pesquisará automaticamente no youtube.\n.stop - Para todas as músicas.\n.skip - Passa a música que está tocando.\n.queue - Mostra todas as músicas na fila.\n.volume [volume] - Aumenta ou diminui o volume da música.\n.pause - Pausa a música atual.\n.resume - Despausa a música atual.\n.join - Faz com que o bot entre na chamada\n.leave - Faz com que o bot saia da chamada\n.src - Altera o número de itens ao pesquisar pelo vídeo, se alterado para 1, o vídeo será escolhido automaticamente.\n.loop - Coloca a playlist em loop.\n.shuffle - Coloca a playlist no modo aleatório.\n.vs - Desativa e ativa o vote skip\n.fs - Força o skip da música"
    , inline=False)
    embed.add_field(name="8ball", value=".addr [resposta] - Adiciona uma resposta para o 8ball\n.remr [resposta] - Remove uma resposta do 8ball\n.lisr - Lista as respostas que estão no 8ball\n.8ball [pergunta] - Realiza uma pergunta e o universo responderá de acordo com as respostas colocadas."
    , inline=False)
    embed.add_field(name="Quiz", value=".qadd [musica] - Adiciona uma música para o quiz, o bot perguntará também o nome do artista e o nome da música para a música ser adicionada ao banco de dados\n.qrem [musica] - Remove uma música do banco de dados do quiz, para que funcione o nome da música precisa ser idêntico ao vídeo presente no youtube.\n.qlis - Lista todas as músicas presentes no quiz.\n.qs [número de músicas para iniciar o quiz] - Inicia o quiz com a quantidade de músicas que o usuário colocou."
    , inline=False)
    embed.add_field(name="League of Legends", value=".lsts [nome de invocador] - Verifica o status de um determinado jogador\n.ig [nome de invocador] - Verifica se o invocador está em uma partida."
    , inline=False)
    embed.add_field(name="Vote", value=".vote - Você receberá o link para votar.\n.ranking ou .rank - Lista os melhores colocados no sistema de votos."
    , inline=False)
    embed.add_field(name="Experimental", value=".eplay - Você tocará uma música do banco de dados\n.upload - Você dará upload em uma música."
    , inline=False)
    await context.send(embed=embed)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and 'Desativado' not in filename:
        bot.load_extension(f'cogs.{filename[:-3]}')



bot.run('NzcxNjI4ODQ1NTMwMDg3NDQ0.X5u5XA.A7uovHW0zaDzbTibmRtE4ahXMBA')
