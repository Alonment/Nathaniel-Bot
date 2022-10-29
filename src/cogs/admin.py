import datetime
import time
import pandas as pd
import discord

from io import BytesIO
from discord.ext import commands

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.is_owner()
    @commands.command(hidden=True)
    async def scrape(self, ctx):
        """
        Scrapes the entire message history of the current server and exports
        each message and relevent metadata as a single csv file.
        """

        start = time.time()
        
        columns = [
            "message", "authorId", "authorRoles", "channel", "created", 
            "reactions", "userMentions", "roleMentions", "isEdited", "isPinned", "hasAttachments"
        ]
        dataDict = {label: [] for label in columns}

        parsedChannels = []
        for channel in ctx.guild.text_channels:
            parsedChannels.append(channel.name)
            async for message in channel.history(limit=None):

                dataDict["message"].append(message.content)
                dataDict["authorId"].append(message.author.id)

                try:
                    roles = [role.name for role in message.author.roles if role.name != "@everyone"]
                except:
                    roles = []

                dataDict["authorRoles"].append(roles)
                dataDict["channel"].append(channel.name)
                dataDict["created"].append(message.created_at)
                dataDict["reactions"].append([reaction.emoji for reaction in message.reactions])
                dataDict["userMentions"].append([mention.name for mention in message.mentions])
                dataDict["roleMentions"].append([mention.name for mention in message.role_mentions])
                dataDict["isEdited"].append(message.edited_at != None)
                dataDict["isPinned"].append(message.pinned)
                dataDict["hasAttachments"].append(message.attachments != [])


        df = pd.DataFrame.from_dict(dataDict)
        df = df.sort_values(by="created").reset_index(drop=True)
        
        totalSeconds = time.time() - start

        try:
            csvFile = BytesIO()
            df.to_csv(csvFile)
            csvFile.seek(0) # Reset file pointer to the start of the dataframe

            await ctx.send(
                f"Server: {ctx.guild.name}\n"
                f"Channels Parsed: {', '.join(parsedChannels)}\n"
                f"Number of Messages: {len(df)}\n"
                f"Seconds: {totalSeconds:.2f} ({totalSeconds/60:.2f} minutes)\n"
                f"Date Executed: {datetime.datetime.now()}\n"
                f"Executed By: <@{ctx.author.id}>\n"
            )
            
            await ctx.send(f"It took {totalSeconds/60:.2f} minutes to scrape all {len(df)} messages I had access to.")
            await ctx.send(file=discord.File(csvFile, filename="test.csv"))

        except Exception as err:
            print(f"Error: {err}")
            await ctx.send("There was an error processing this server's logs.")

async def setup(bot):
    await bot.add_cog(Admin(bot))