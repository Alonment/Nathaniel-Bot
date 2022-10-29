from logging import error
import discord
from discord.ext import commands

class Test(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ex(self, ctx):
        await ctx.send("Yessir")

    @commands.command()
    async def me(self, ctx):
        await ctx.send(ctx.author.mention)

    @commands.command()
    async def react(self, ctx):

        msg = await ctx.send("test")
        await msg.add_reaction("1️⃣")

    @commands.command()
    async def ethan(self, ctx):
        print("here")
        await ctx.send("bruh shid 5")

async def setup(client):
    await client.add_cog(Test(client))