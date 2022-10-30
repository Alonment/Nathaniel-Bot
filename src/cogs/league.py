import discord
import os

from discord.ext import commands
from riotwatcher import LolWatcher
from src.league.summoner import Summoner
from src.league.champion import Champion
from requests import HTTPError

class League(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        self.watcher = LolWatcher(os.environ["LOL_API_KEY"])
        self.regions = ['na1']
        self.version = self.watcher.data_dragon.versions_for_region('na1')
        self.championStats = self.watcher.data_dragon.champions(self.version['n']['champion'], True)

    @commands.command(usage="profile <summoner name>")
    async def profile(self, ctx, *args):
        """
        Returns a snapshot of the summoner's account stats.
        
        Sends a Discord embed object containing a Summoner's information, 
        or nothing in case that the summoner could not be found.
        """

        name = " ".join(args)
        try:
            account = Summoner(name)

        except HTTPError: # Ends function in the event that the summoner could not be found

            await ctx.send("That ain't your summoner name b or you just don't exist")
            return

        # Initializes embed with summoner name and color
        embed = discord.Embed(
            title="{}'s Profile".format(account.name),
            colour=discord.Colour.dark_green()
        )

        embed.add_field(name="Level", value=account.level, inline=False)

        queues = {"RANKED_SOLO_5x5": "Ranked Solo", "RANKED_FLEX_SR": "Ranked Flex"}
        ranked = account.rankedStats
        mastery = account.mastery

        # Iterates through an account's ranked stats and parses it into a readable string
        for info in sorted(ranked, key = lambda x: x['wins'] + x['losses'], reverse = True):

            rankedQueue = queues[info['queueType']]
            rankedInfo = f"{info['tier']} {info['rank']}  {info['leaguePoints']} LP\n" \
                         f" Winrate: {info['wr']}\n{info['wins']} W {info['losses']} L\n"
            embed.add_field(name=rankedQueue, value = rankedInfo, inline=True)

        # Iterates through an account's champion stats and parses it into a readable string
        # where only their top 3 champions are displayed (in terms of mastery)
        masteryStats = ""
        for champ in mastery[:3]:
            masteryStats = masteryStats + \
                f"[{champ['championLevel']}] **{self.championStats['keys'][str(champ['championId'])]}:** " + \
                "{:,}\n".format(champ['championPoints'])

        if masteryStats == "":
            masteryStats = "Mans really has 0 mastery."

        embed.add_field(name = "Top Champions", value = masteryStats, inline=False)
        embed.add_field(name="Live Game", value = account.getLiveGame())

        # Inserts relative icon information and retrieves it from the DD api.
        url = f"https://ddragon.leagueoflegends.com/cdn/{self.version['n']['profileicon']}" \
              f"/img/profileicon/{account.profileIconId}.png"

        embed.set_thumbnail(url = url)

        await ctx.send(embed = embed)

    @commands.command(usage="champion <champion_name>", aliases=["champ"])
    async def champion(self, ctx, *args):
        """
        Returns a detailed embed of a champions information.
        """
        
        name = " ".join(args)

        # Formats the user inputted name properly by removing all punctuation
        championName = self.removePunctuation(name).lower().title().replace(" ", "")

        if championName == "Wukong": championName = "MonkeyKing" # Handles wukong special case...

        if not Champion.exists(championName):
            await ctx.send("Unfortunately that champion either doesn't exist or you ain't spelling its name right...")
            return
        
        champ = Champion(championName)
        embed = discord.Embed(title=champ.getFullTitle(), colour=discord.Color.dark_gold())
        embed.set_thumbnail(url=champ.getIconUrl())
        embed.add_field(name="Roles", value = ", ".join(champ.types))
        embed.add_field(name="Lore", value=champ.lore, inline=False)
        
        for ability in champ.getAbilities():
            embed.add_field(name=ability[0], value=ability[1], inline=False)
        
        url = f"https://app.mobalytics.gg/lol/champions/{champ.name}/build\n"\
              f"https://probuildstats.com/champion/{champ.name}"
        embed.add_field(name="Winrate, Builds, Runes, etc.:", value=url)

        await ctx.send(embed=embed)

    @commands.command(usage="item <item_name>")
    async def item(self, ctx, *args):
        """
        Returns a detailed embed of an item's information.
        """
        
        name = " ".join(args)
        
    
    def removePunctuation(self, string: str) -> str:
        """
        Helper function to remove all punctuation from a string.
        """

        ret = ""
        for letter in string:
            if letter not in string.punctuation:
                ret += letter
        
        return ret

async def setup(bot):
    await bot.add_cog(League(bot))
