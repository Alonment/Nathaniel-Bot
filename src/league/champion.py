import os

from riotwatcher import LolWatcher

class Champion:


    def __init__(self, name):

        source = LolWatcher(os.environ["LOL_API_KEY"])
        version = source.data_dragon.versions_for_region('na1')['n']['champion']
        champInfo = source.data_dragon.champions(version, full=True)['data'][name]

        self.id = champInfo['id']
        self.name = champInfo['name']
        self.title = champInfo['title']
        self.image = champInfo['image']
        self.lore = champInfo['lore']
        self.types = champInfo['tags']
        self.spells = champInfo['spells']
        self.passive = champInfo['passive']

    @staticmethod
    def exists(champion: str) -> bool:
        """
        Static method to determine if the name input is even valid.
        """

        source = LolWatcher(os.environ["LOL_API_KEY"])
        version = source.data_dragon.versions_for_region('na1')['n']['champion']
        champions = source.data_dragon.champions(version, full=True)
        
        if not champion in champions['data']:
            return False

        return True

    def getFullTitle(self) -> str:
        """
        Returns a champion's name concatenated with their title.
        """

        return f"{self.name} {self.title}"
    
    def getIconUrl(self) -> str:
        """
        Returns the data dragon endpoint containing the champs default splash icon.
        """

        return f"http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{self.id}_0.jpg"
    
    def getAbilities(self) -> list:
        """
        Parses the champion's ability information into a readable string.
        """

        passive = self.passive
        ret = [(f"Passive: {passive['name']}", f"**Description:** {passive['description']}")]

        prefixes = {0: "Q", 1: "W", 2: "E", 3: "R"}
        abilities = self.spells
        for i in range(len(abilities)):
            name = f"{prefixes[i]}: {abilities[i]['name']}"
            info = f"**Description:** {abilities[i]['description']}\n"\
                   f"**Cooldown:** {'/'.join([str(cooldown) for cooldown in abilities[i]['cooldown']])}\n"\
                   f"**Range:** {'/'.join([str(range) for range in abilities[i]['range']])}\n"

            ret.append((name, info))

        return ret