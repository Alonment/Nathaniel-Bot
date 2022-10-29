
import discord
from discord.ext import commands
from cogwatch import watch

class NathanielBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.help_command = HelpCommand()
    
    async def setup_hook(self) -> None:
        
        extensions = [
            # "src.cogs.economy",
            # "src.cogs.google_translate_api",
            # "src.cogs.league",
            # "src.cogs.sheet_music",
            "src.cogs.tests",
            "src.cogs.admin",
            # "src.cogs.weather"
        ]

        for extension in extensions:
            await self.load_extension(extension)

    @watch(path='src/cogs')
    async def on_ready(self):
        print('And we back')

class HelpCommand(commands.HelpCommand):

    def __init__(self):
        super().__init__()
    
    async def send_bot_help(self, mapping):

        embed = discord.Embed(title="Here ya go :)", description='Use "-help <command>" for more information!', 
                              colour=discord.Colour.dark_red())

        for cog in mapping:
        
            if cog != None and len(mapping[cog]) != 0:

                commandNames = [command.name for command in mapping[cog] if not command.hidden]

                # Ensure embed string is not empty - prevents help command from breaking
                if len(commandNames) == 0:
                    continue

                embed.add_field(name = cog.qualified_name, value = ", ".join(commandNames), inline = False)

        await self.get_destination().send(embed = embed)

    async def send_command_help(self, command):
        
        if command.hidden:
            return 

        embed = discord.Embed(title = command.name, 
                              description = command.help,
                              colour = discord.Colour.dark_red())

        embed.add_field(name = "*usage:* ", value = f"```{command.usage}```")
        return await self.get_destination().send(embed = embed)