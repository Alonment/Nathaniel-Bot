import discord
import asyncio
from discord.ext import commands
import datetime
import random

from discord.ext.commands.core import Command, command

emojis = ["1️⃣", "2⃣", "3⃣", "4⃣", "5⃣",
                   "6⃣", "7⃣", "8⃣", "9⃣", "🔟"]

"""
Main command class for Nathaniel bot where the majority of
QoL commands are stored.
"""
class Nathaniel(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
    
    @commands.command(usage = ": ) ping")
    async def ping(self, ctx):
        """Fetchs your current latency."""

        await ctx.send(f"{round(self.bot.latency * 1000)} ms")

    @commands.command(usage = ": ) erase <number of messages to erase>")
    @commands.has_permissions(manage_messages=True)
    async def erase(self, ctx, n=1):
        """Deletes the last n messages in the channel."""

        if n > 50:
            await ctx.send("Woah woah woah, slow down there buddy. You really tryna erase all of time. And for what. \
                            The limit is 50 messages...")
            return
            
        await ctx.channel.purge(limit=n+1)

    @commands.command(usage = ": ) help roll")
    async def flip(self, ctx):
        """Sends the result of flipping a coin."""

        outcomes = ["H", "T"] * 3000
        outcomes.append("S")

        result = random.choice(outcomes)

        if result == "S":
            await ctx.send("It landed on its side! This has a 1/6000 chance of happening...")

        await ctx.send("You got Heads.") if result == "H" else await ctx.send("You Got Tails.")

    @commands.command(usage = ": ) roll <number of sides on the die>")
    async def roll(self, ctx, n=6):
        """Sends the result of a single n-sided dice roll."""

        if type(n) != int:
            await ctx.send("You gotta give me a number man.")
            return

        # Initializes a list of values from 1 to 6 and randomely sends a single value
        outcomes = [i + 1 for i in range(n)]
        result = random.choice(outcomes)

        await ctx.send("You rolled a {:d}.".format(result))

    @commands.command(usage = ": ) nroll <number of dice> <number of sides on a die>")
    async def nroll(self, ctx, *args):
        """Sends the result of multiple n-sided dice rolls."""

        if len(args) > 2:
            await ctx.send("Proper command: -nroll <number of dice> <number of sides on each dice>")
            return

        for arg in args:
            if not arg.isdigit():
                await ctx.send("You gotta give me a number man.")
                return

        dice = 2 if len(args) == 0 else int(args[0])
        sides = 6 if len(args) == 1 else int(args[1])

        outcomes = [i + 1 for i in range(sides)]
        results = []
        for i in range(dice):

            results.append(random.choice(outcomes))

        await ctx.send("Here are the rolls in order: {}".format(results))

    @commands.command(usage = ": ) timer <number> <unit of time> <optonal: event description>")
    async def timer(self, ctx, *args):
        """Creates a timer that pings you once time is up. (Only seconds, minutes, and hours)"""

        # Different aliases for conveinence of user command input
        aliases = [["s", "seconds"], ["m", "mi", "min", "minutes"], ["h", "hr", "hrs", "hours"]]

        if len(args) < 2:
            await ctx.send("Missing Arguments: <Number> <Unit> Optional:[Event] \nEx. -timer 360 seconds")
            return

        # Ensures that the proper unit of time is stored 
        unit = ""
        for i in range(3):
            if args[1] in aliases[i]:
                unit = aliases[i][-1]
                break

        n = int(args[0])
        await ctx.send(f"A timer has been set to go off {n} {unit} from now.")
        
        if unit == "hours":
            n = n * 60 * 60
        elif unit == "minutes":
            n = n * 60

        await asyncio.sleep(n)

        if len(args) > 2:

            event = " ".join(args[2:])
            await ctx.send("It is time.... for {} {}".format(event, ctx.author.mention))
            return

        await ctx.send("It is time.... {}".format(ctx.author.mention))

    @commands.command(usage = ': ) poll "<question>" <choice 1> <choice 2> ... <choice 10>')
    async def poll(self, ctx, question: str, *choices):
        """Sends out an interactive poll that discord users can react to."""
        
        if len(choices) > 10:
            await ctx.send("You can only have 10 options.")
            return

        embed = discord.Embed(
            title = "Poll",
            description = question,
            colour = ctx.author.colour,
            timestamp = datetime.datetime.utcnow()
        )

        options = "\n\n".join(["{}\t{}".format(emojis[i], choice) for i, choice in enumerate(choices)])

        embed.add_field(name = "Options: \n", value = options, inline = False)
        embed.set_footer(text="React to this message to vote!")

        msg = await ctx.send(embed=embed)
        for reaction in emojis[:len(choices)]:
            await msg.add_reaction(reaction)

    @commands.command(hidden=True)
    async def die(self, ctx):
        """Bot die."""

        if ctx.author.id != 205030030911209474:
            await ctx.send("Nice try bud.")
            return

        await ctx.send("As you wish sir...")
        await self.bot.logout()

    @commands.command(hidden=True)
    async def sayd(self, ctx, *args):
        """He is I and I am he."""
        if ctx.author.id != 205030030911209474:
            return

        await ctx.channel.purge(limit=1)
        await ctx.send(" ".join(args))


async def setup(bot):
    await bot.add_cog(Nathaniel(bot))
