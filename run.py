import discord
import os
import pandas as pd
import time
import datetime
import asyncio

from src.bot import NathanielBot

from discord.colour import Color
from discord.ext import commands

# @bot.listen("on_member_join")
# async def updateUserOnJoin(member):

#     if member.bot:
#         return


#     user = MDB.getUser(member.id)
#     if user == None: # Add user if they are not currently being tracked
#         MDB.createUser(member)
#         return

#     elif member.guild not in user["guilds"]: # Add guild to user document in case it's not already there
#         MDB.updateUser(user.id,
#          {"$set": {f"guilds.{member.guild.name}": {"Level": 1, "Exp": 0}}}
#          )
    

# @bot.listen("on_message")
# async def updateUserStats(msg):

#     # Bot accounts are not stored in MongoDB
#     if msg.author.bot:
#         return

#     ID = msg.author.id
#     guild = msg.guild
#     user = MDB.getUser(ID)

#     if user == None:
#         newUser = await bot.fetch_user(ID)
#         MDB.createUser(newUser)

#     # Processes a user's level and exp given their message's content
#     MDB.giveExp(ID, guild, msg.content.split(" "))

#     # Increments the num of messages tracker for each user
#     MDB.updateUser(ID, {"$inc": {"numOfMesssages": 1, f"guilds.{guild.name}.messages": 1} })


async def main():
    bot = NathanielBot(command_prefix="-", intents=discord.Intents.all())
    await bot.start(os.environ['TOKEN'])

if __name__ == "__main__":
    asyncio.run(main())