import discord
from discord.colour import Color
from discord.ext import commands
from MongoDBController import MongoDBController
from datetime import datetime

MDB = MongoDBController()

class Economy(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def account(self, ctx):
        collection = MDB.cluster["discord_test"]
        collection.read_preference
        
        user = collection.find_one({"_id": ctx.author.id})
        level = user["guilds"][ctx.guild.name]["Level"]
        exp = user["guilds"][ctx.guild.name]["Exp"]

        requiredExp = (5 * pow(level, 3)) // 4 + 5 # exp = 5n^3 // 4 + 5
        progress = exp // requiredExp * 100
        bar = [":black_circle:"] * 10

        for i in range(progress // 10):
            bar[i] = "<:shon:740597489538826332>"

        embed = discord.Embed(title = f"{ctx.author.name} - {ctx.guild.name} ", Color = discord.Colour.dark_red())
        embed.add_field(name = "Level:", value = level)
        embed.add_field(name = "Current Exp:", value = exp, inline = True)
        embed.add_field(name = f"Progress to next level: {progress}%", value = "".join(bar), inline=False)
        embed.set_footer(text = f"Tracking Since: {datetime.now().strftime('%-m/%-d/%Y, %-I:%M:%S %p')}")
        embed.set_thumbnail(url=ctx.author.avatar_url)

        await ctx.send(embed = embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))