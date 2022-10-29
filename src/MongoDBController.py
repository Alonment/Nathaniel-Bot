import os
import pymongo  
import datetime

class MongoDBController():

    def __init__(self):

        client = pymongo.MongoClient(os.environ["MONGO_URI"])
        self.client = client
        self.cluster = client["discord_test"]

    def createUser(self, user):

        collection = self.cluster["discord_test"]

        # Basic user schema for adding to user collection
        userDocument = {
            "_id": user.id,
            "name": user.name,
            "tracking_since": datetime.datetime.today(),
            "guilds": { guild.name : {"Level": 1, "Exp": 0, "guild_id": guild.id} for guild in user.mutual_guilds},
            "top_five": {}
        }

        user = collection.insert_one(userDocument)
        
        return userDocument
        
    def getUser(self, ID):

        collection = self.cluster["discord_test"]
        collection.read_preference
        user = collection.find_one({"_id": ID})

        return user

    def giveExp(self, ID, guild, msg):
        
        collection = self.cluster["discord_test"]
        user = collection.find_one({"_id": ID})

        # Ensures that the guild exists within the user's guilds
        if not guild.name in user["guilds"]:
            collection.update_one(
                {"_id": ID}, 
                {"$set": { f"guilds.{guild.name}": {"Level": 1, "Exp": 0, "guild_id": guild.id}}}
                )

        expGain = 10
        if len(msg) > 10:
            expGain += 3 * len(msg[10:])

        # XP formula: (5n^3)/4  + 5 where n = level
        currentLevel = user["guilds"][guild.name]["Level"]
        requiredExp = (5 * pow(currentLevel, 3)) // 4 + 5 
        currentExp = user["guilds"][guild.name]["Exp"] + expGain

        collection.update_one(
                {"_id": ID},
                {"$set": {f"guilds.{guild.name}.Exp": currentExp}}
                )

        while currentExp >= requiredExp:

            currentExp -= requiredExp
            collection.update_one(
                {"_id": ID},
                {
                    "$inc": {f"guilds.{guild.name}.Level": 1},
                    "$set": {f"guilds.{guild.name}.Exp": currentExp}
                })

            currentLevel += 1
            requiredExp = (5 * pow(currentLevel, 3)) // 4 + 5 

    def updateUser(self, ID, updateExpressions):

        collection = self.cluster["discord_test"]
        
        response = collection.find_one_and_update({"_id": ID}, updateExpressions)
        return response
