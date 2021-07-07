import discord
from discord.ext import commands
from discord.ext.commands import errors
import requests
from pantheon import pantheon
import asyncio

class lolTournament(commands.Cog):

    def __init__(self, client):
        self.client = client

    

    @commands.command(aliases=['lc'])
    async def lolCreate(self, ctx):
        serverAm = 'americas'
        api_key = 'RGAPI-07babde7-357e-4e86-9889-0339ce6b6349'
        panth = pantheon.Pantheon(serverAm, api_key)

        embed=discord.Embed(title=f"Escolha o modo de jogo", colour=discord.Colour.orange())
        embed.add_field(name="5v5 Summoner's Rift", value="Aperte 1", inline=False)
        embed.add_field(name="3v3 Summoner's Rift", value="Aperte 2", inline=False)
        embed.add_field(name="3v3 ARAM", value="Aperte 3", inline=False)
        embed.add_field(name="1v1 ARAM", value="Aperte 4", inline=False)
        msg=await ctx.send(embed=embed)

        await msg.add_reaction('\u0031\u20e3')
        await msg.add_reaction('\u0032\u20e3')
        await msg.add_reaction('\u0033\u20e3')
        await msg.add_reaction('\u0034\u20e3')

        emoji=''
        def check(reaction, user):
            return (str(reaction.emoji) in ["\u0031\u20e3", "\u0032\u20e3", "\u0033\u20e3", "\u0034\u20e3"]) and (user.id != self.client.user.id) and (user == ctx.message.author)
        while True:
            if emoji=='\u0031\u20e3':
                i=0
                break
            if emoji=='\u0032\u20e3':
                i=1
                break
            if emoji=='\u0033\u20e3':
                i=2
                break
            if emoji=='\u0034\u20e3':
                i=3
                break
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout = 60.0, check = check)
            except asyncio.TimeoutError:
                print('Timeout')
                break
            else:
                await msg.remove_reaction(reaction.emoji,user)
                emoji=reaction.emoji

        if i==0:
            mapa="SUMMONERS_RIFT"
            teamSize=5
            pickType="TOURNAMENT_DRAFT"
            spectator="ALL"
        elif i==1:
            mapa="SUMMONERS_RIFT"
            teamSize=3
            pickType="TOURNAMENT_DRAFT"
            spectator="ALL"
        elif i==2:
            mapa="HOWLING_ABYSS"
            teamSize=3
            pickType="TOURNAMENT_DRAFT"
            spectator="ALL"
        elif i==3:
            mapa="HOWLING_ABYSS"
            teamSize=1
            pickType="TOURNAMENT_DRAFT"
            spectator="ALL"

        response = await panth.registerProvider('BR', "http://test.com", stub=True)
        response2 = await panth.registerTournament(response, 'Bol Bot', stub=True)

        data={
  "mapType": mapa,
  "pickType": pickType,
  "spectatorType": spectator,
  "teamSize": teamSize
}

        response3 = await panth.createTournamentCode(response2, data, nb_codes=1, stub=True)
        await msg.remove_reaction('\u0034\u20e3', self.client.user)
        await msg.remove_reaction('\u0033\u20e3', self.client.user)
        await msg.remove_reaction('\u0032\u20e3', self.client.user)
        await msg.remove_reaction('\u0031\u20e3', self.client.user)
        embed = discord.Embed(title=f"Partida {teamSize}v{teamSize} criada",description=f"Código da partida: {response3[0]}", colour=discord.Colour.orange())
        await msg.edit(embed=embed)

def setup(client):
    client.add_cog(lolTournament(client))