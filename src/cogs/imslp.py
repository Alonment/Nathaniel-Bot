import discord
from discord.ext import commands

from imslp import client


class SheetMusic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.source = client.ImslpClient()

    @commands.command(usage = ": ) piece <query>")
    async def piece(self, ctx, *args):
        """Returns search results for the location of sheet music in IMSLP. Be as specific as possible."""
        
        if not args:
            await ctx.send("Missing arguments: -piece <Title of Piece> <Composer>")
            return

        if len("".join(args)) < 5:
            await ctx.send("You gotta give me more info")
            return

        search = self.source.search_works(" ".join(args))

        if len(search) == 0:
            await ctx.send("das tuff, I couldn't find the piece.")
            return

        results = list(search)
        items = '\n'.join('{}:\n{} '.format(work["id"], work['permlink']) for work in results)

        embed = discord.Embed(
            title='Piece List:',
            description=items,
            colour=discord.Colour.red()
        )
        embed.set_thumbnail(url="https://cdn.dribbble.com/users/807834/screenshots/2819480/imslp.png")

        await ctx.send(embed=embed)

    @commands.command(usage = ": ) composer <name of composer>")
    async def composer(self, ctx, *, name):
        """Returns a link to all of a composer's works. Be as specific as possible."""

        search = self.source.search_people(name)
        if len(search) == 0:
            await ctx.send("das tuff, I couldn't find your guy")
            return

        results = list(search)
        items = '\n'.join('{}\n{} '.format(work["id"][9:], work['permlink']) for work in results)

        embed = discord.Embed(
            title='Composer List:',
            description=items,
            colour=discord.Colour.red()
        )
        embed.set_thumbnail(url="https://cdn.dribbble.com/users/807834/screenshots/2819480/imslp.png")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(SheetMusic(bot))
