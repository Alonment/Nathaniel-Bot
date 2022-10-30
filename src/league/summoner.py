import requests
import shutil
import time
import os

from requests.models import HTTPError
from riotwatcher import LolWatcher


class Summoner:
    """
    A Summoner object represents a League of Legends player's account
    and all of its respective information. Several functions are provided
    in querying basic information and data from a single person's account.
    """
    
    def __init__(self, name):

        source = LolWatcher(os.environ["LOL_API_KEY"])
        self.source = source
        summonerInfo = source.summoner.by_name('na1', name)
        rankedStats = source.league.by_summoner('na1', summonerInfo['id'])
        mastery = source.champion_mastery.by_summoner('na1', summonerInfo['id'])
        versions = source.data_dragon.versions_for_region('na1')

        self.name = summonerInfo['name']
        self.summoner_id = summonerInfo['id']
        self.account_id = summonerInfo['accountId']
        self.profileIconId = summonerInfo['profileIconId']
        self.level = summonerInfo['summonerLevel']

        #Instantiates rankedStats attribute based on each ranked queue
        for queue in rankedStats:

            queue['tier'] = queue['tier'].lower().capitalize()
            wins = queue['wins']
            losses = queue['losses']
            wr = round(wins/(wins+losses) * 100)
            queue['wr'] = f"{wr}%"

        self.rankedStats = rankedStats
        self.mastery = mastery
        self.version = versions['n']
    
    def getProfileIcon(self) -> str:
        """
        Retrieves a summoner's active profile icon.
        """

        version = self.source.data_dragon.versions_for_region('na1')['n']['profileicon']
        req = requests.get(
            f"http://ddragon.leagueoflegends.com/cdn/{version}/img/profileicon/{self.profileIconID}.png"
            )
            
        if req.status_code == 200:
            path = "/Users/natha/OneDrive/Nathaniel/LeagueofLegends/assets/{}.png".format(self.profileIconId)
            with open(path, "wb") as f:
                req.raw.decode_content = True
                shutil.copyfileobj(req.raw, f)

            return path

        return ""

    def getLiveGame(self) -> str:
        """Returns whether or not a summoner is currently in a game."""

        try:
            info = self.source.spectator.by_summoner('na1', self.summoner_id)
        except HTTPError:
            return "Currently not in game."
        
        mapInfo = self.source.data_dragon.maps(self.version['map'])['data']
        gameMode = mapInfo[f"{info['mapId']}"]["MapName"]

        # Specate client is delayed by 3 minutes
        seconds = info['gameLength'] + 150 
        return f"Playing in a **{gameMode}** match for"\
               f" **{seconds// 60}** minutes and **{seconds % 60}** seconds now."

    def getChampionInfo(self, champion: str) -> dict:
        """
        Returns all information regarding a particular champion.
        """

        champions = self.source.data_dragon.champions(self.version['champion'])['data']

        if not champion in champions['data']:
            return None

        return champions['data'][champion]

    def getMatchHistory(self):
        start = time.time()
        startIndex = 0
        endIndex = 100
        totalGames = 100
        matches = []
        # while(startIndex < totalGames):

        #     response = self.source.match.matchlist_by_account(
        #         region='na1',
        #         encrypted_account_id= self.account_id,
        #         begin_index=startIndex,
        #         end_index=endIndex
        #         )
        #     matches += response['matches']
        #     if totalGames < response['totalGames']:
        #         totalGames = response['totalGames']
            
        #     startIndex += 100
        #     endIndex += 100
        # print(time.time() - start)
        # print(len(matches))
        # print(matches[0].keys())
        matchInfo = self.source.match.by_id('na1', 3117900180)
        print(matchInfo.keys())
        print(matchInfo['participants'])
        print(matchInfo['participantIdentities'])


