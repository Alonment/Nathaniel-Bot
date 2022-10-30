from discord.ext import commands

class Weather(commands.Cog):

    @commands.command(usage = "weather <zipcode> or <town>")
    async def weather(self, ctx, *args):
        pass

async def setup(bot):
    await bot.add_cog(Weather(bot))