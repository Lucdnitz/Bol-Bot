import discord
from discord.ext import commands
from discord.ext.commands import errors
import requests

class lol(commands.Cog):

    def __init__(self, client):
        self.client = client

    

    @commands.command(aliases=['lsts','lolstatus'])
    async def lolStatus(self, ctx, *, nomeSum):
        api_key = 'RGAPI-07babde7-357e-4e86-9889-0339ce6b6349'
        nome = nomeSum.replace(' ','%20')
        sumInfo = requests.get(f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{nome}?api_key={api_key}')
        try:
            lvl = sumInfo.json()['summonerLevel']
            sumId = sumInfo.json()['id']
            nomeSumOfi = sumInfo.json()['name']
            embed= discord.Embed(title=f"Status de '{nomeSumOfi}' no lol", description=f"Level do invocador: {lvl}", colour=discord.Colour.orange())
            iconId = sumInfo.json()['profileIconId']
            embed.set_thumbnail(url=f'http://ddragon.leagueoflegends.com/cdn/11.15.1/img/profileicon/{iconId}.png')
            sumInfoRanked = requests.get(f'https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{sumId}?api_key={api_key}')
            try:
                for i in range(len(sumInfoRanked.json())):
                    if(sumInfoRanked.json()[i]['queueType'] == 'RANKED_SOLO_5x5'):
                        tier = sumInfoRanked.json()[i]['tier']
                        rank = sumInfoRanked.json()[i]['rank']
                        pdl = sumInfoRanked.json()[i]['leaguePoints']
                        wins = sumInfoRanked.json()[i]['wins']
                        losses = sumInfoRanked.json()[i]['losses']
                        embed.add_field(name="Ranqueada Solo/Duo", value=f"\nRank: {tier} {rank} com {pdl} pontos\nNúmero total de jogos: {wins+losses}\nTaxa de vitória: {round((wins/(wins+losses))*100,1)}% ({wins}V/{losses}D)", inline=False)
                    elif(sumInfoRanked.json()[i]['queueType'] == 'RANKED_FLEX_SR'):
                        tier = sumInfoRanked.json()[i]['tier']
                        rank = sumInfoRanked.json()[i]['rank']
                        pdl = sumInfoRanked.json()[i]['leaguePoints']
                        wins = sumInfoRanked.json()[i]['wins']
                        losses = sumInfoRanked.json()[i]['losses']
                        embed.add_field(name="Ranqueada Flex", value=f"\nRank: {tier} {rank} com {pdl} pontos\nNúmero total de jogos: {wins+losses}\nTaxa de vitória: {round((wins/(wins+losses))*100,1)}% ({wins}V/{losses}D)", inline=False)
            except:
                pass
            await ctx.send(embed=embed)
        except:
            embed= discord.Embed(description=f'Não foi possível encontrar o invocador.', colour=discord.Colour.orange())
            await ctx.send(embed=embed)

    @commands.command(aliases=['ig','lig','lolingame','LOLINGAME'])
    async def lolInGame(self, ctx, *, nomeSum):
        try:
            api_key = 'RGAPI-07babde7-357e-4e86-9889-0339ce6b6349'
            nome = nomeSum.replace(' ','%20')
            sumInfo = requests.get(f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{nome}?api_key={api_key}')
            sumId = sumInfo.json()['id']
            nomeSumOfi = sumInfo.json()['name']
            matchInfo = requests.get(f'https://br1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{sumId}?api_key={api_key}')

            try:
                matchInfo.json()['status']['status_code']
                embed=discord.Embed(description=f"O invocador {nomeSumOfi} não está em partida.", colour=discord.Colour.orange())
                await ctx.send(embed=embed)
            except:
                matchInfo = matchInfo.json()
                dicTimeAzul={
                    'nome':[],
                    'championId':[],
                    'elo':[]
                }
                dicTimeVermelho={
                    'nome':[],
                    'championId':[],
                    'elo':[]
                }


                for i in range(len(matchInfo['participants'])):
                    if(matchInfo['participants'][i]['teamId'] == 100):
                        dicTimeAzul['nome'].append(matchInfo['participants'][i]['summonerName'])
                        nomeTemp = matchInfo['participants'][i]['summonerName'].replace(' ','%20')
                        sumInfoTemp=requests.get(f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{nomeTemp}?api_key={api_key}')
                        idTemp = sumInfoTemp.json()['id']
                        sumRankedInfo = requests.get(f'https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{idTemp}?api_key={api_key}').json()
                        if len(sumRankedInfo)==2:
                            for i in range(len(sumRankedInfo)):
                                if(sumRankedInfo[i]['queueType'] == 'RANKED_SOLO_5x5'):
                                    tier = sumRankedInfo[i]['tier']
                                    rank = sumRankedInfo[i]['rank']
                                    pdl = sumRankedInfo[i]['leaguePoints']
                                    wins = sumRankedInfo[i]['wins']
                                    losses = sumRankedInfo[i]['losses']
                            dicTimeAzul['elo'].append(f' - {tier} {rank} com {pdl} - Taxa de vitória: {round((wins/(wins+losses))*100,1)}% ({wins}V/{losses}D)')
                        elif len(sumRankedInfo)==1:
                            if(sumRankedInfo[0]['queueType'] == 'RANKED_SOLO_5x5'):
                                tier = sumRankedInfo[0]['tier']
                                rank = sumRankedInfo[0]['rank']
                                pdl = sumRankedInfo[0]['leaguePoints']
                                wins = sumRankedInfo[0]['wins']
                                losses = sumRankedInfo[0]['losses']
                                dicTimeAzul['elo'].append(f' - {tier} {rank} com {pdl} - Taxa de vitória: {round((wins/(wins+losses))*100,1)}% ({wins}V/{losses}D)')
                            else:
                                dicTimeAzul['elo'].append(f' - Não possui partidas ranqueadas Solo/Duo')
                        else:
                            dicTimeAzul['elo'].append(f' - Não possui partidas ranqueadas')
                            

                    else:
                        dicTimeVermelho['nome'].append(matchInfo['participants'][i]['summonerName'])
                        nomeTemp = matchInfo['participants'][i]['summonerName'].replace(' ','%20')
                        sumInfoTemp=requests.get(f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{nomeTemp}?api_key={api_key}')
                        idTemp = sumInfoTemp.json()['id']
                        sumRankedInfo = requests.get(f'https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{idTemp}?api_key={api_key}').json()
                        if len(sumRankedInfo)==2:
                            for i in range(len(sumRankedInfo)):
                                if(sumRankedInfo[i]['queueType'] == 'RANKED_SOLO_5x5'):
                                    tier = sumRankedInfo[i]['tier']
                                    rank = sumRankedInfo[i]['rank']
                                    pdl = sumRankedInfo[i]['leaguePoints']
                                    wins = sumRankedInfo[i]['wins']
                                    losses = sumRankedInfo[i]['losses']
                            dicTimeVermelho['elo'].append(f' - {tier} {rank} com {pdl} pontos - Taxa de vitória: {round((wins/(wins+losses))*100,1)}% ({wins}V/{losses}D)')
                        elif len(sumRankedInfo)==1:
                            if(sumRankedInfo[0]['queueType'] == 'RANKED_SOLO_5x5'):
                                tier = sumRankedInfo[0]['tier']
                                rank = sumRankedInfo[0]['rank']
                                pdl = sumRankedInfo[0]['leaguePoints']
                                wins = sumRankedInfo[0]['wins']
                                losses = sumRankedInfo[0]['losses']
                                dicTimeVermelho['elo'].append(f' - {tier} {rank} com {pdl} pontos - Taxa de vitória: {round((wins/(wins+losses))*100,1)}% ({wins}V/{losses}D)')
                            else:
                                dicTimeVermelho['elo'].append(f' - Não possui partidas ranqueadas Solo/Duo')
                        else:
                            dicTimeVermelho['elo'].append(f' - Não possui partidas ranqueadas')
                    


                embed= discord.Embed(title=f"Status da partida de '{nomeSumOfi}' no lol", colour=discord.Colour.orange())
                iconId = sumInfo.json()['profileIconId']
                embed.set_thumbnail(url=f'http://ddragon.leagueoflegends.com/cdn/11.15.1/img/profileicon/{iconId}.png')
                strAzul=''
                strVerm=''
                for i in range(len(dicTimeAzul['nome'])):
                    strAzul+=f'\n{dicTimeAzul["nome"][i]}{dicTimeAzul["elo"][i]}'
                    strVerm+=f'\n{dicTimeVermelho["nome"][i]}{dicTimeVermelho["elo"][i]}'

                embed.add_field(name="Time azul", value=f"\n{strAzul}", inline=False)
                embed.add_field(name="Time Vermelho", value=f"\n{strVerm}", inline=False)
                await ctx.send(embed=embed)
        except:
            embed= discord.Embed(description="Invocador não encontrado ou o mesmo se encontra em partida contra bots.", colour=discord.Colour.orange())
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(lol(client))