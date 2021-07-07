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
            embed.set_thumbnail(url=f'http://ddragon.leagueoflegends.com/cdn/11.11.1/img/profileicon/{iconId}.png')
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



def setup(client):
    client.add_cog(lol(client))