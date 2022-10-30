import discord
from discord.ext import commands
from google.cloud import translate_v2 as translate
from six import binary_type
import random as rand

class GoogleTranslateAPI(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="translate <target language> <text>")
    async def translate(self, ctx, targetLanguage, *words):
        """
        Translates the inputted text into the specific language.
        """

        if len(words) == 0:
            await ctx.send("You gotta give me something to translate man.")
            return

        text = " ".join(words)

        translateInstance = translate.Client()
        if isinstance(text, binary_type):
            text = text.decode("utf-8")

        languageExists = False
        for la in translateInstance.get_languages():

            if la['name'].lower() == targetLanguage.lower():
                targetLanguage = la['language']
                languageExists = True
                break
            elif la["language"].lower() == targetLanguage.lower():
                languageExists = True

        if not languageExists:
            await ctx.send("Idk what to say bro, either that language doesn't exist or Google is just dumb.")
            return

        result = translateInstance.translate(text, targetLanguage)
        await ctx.send(result["translatedText"])

    @commands.command(usage="language <text>")
    async def language(self, ctx, *words):
        """
        Detects the language of the inputted text.
        """

        translateInstance = translate.Client()
        response = translateInstance.detect_language(" ".join(words))

        language = ""
        for la in translateInstance.get_languages():
            if la["language"] == response["language"]:
                language = la["name"]

        if(response["confidence"] <= 0.6):
            await ctx.send(f"I believe that this is {language}, but I'm not too sure bro.")
            return

        await ctx.send(f"Yeah, pretty sure this is {language}.")

    @commands.command(usage="garble <text>")
    async def garble(self, ctx, *words):
        """
        See and find out.
        """
        
        text = " ".join(words)
        translateInstance = translate.Client()
        languages = translateInstance.get_languages()

        numOfTranslations = rand.randint(10,20)
        languageTrace = f"{numOfTranslations} translations: English "
        for i in range(numOfTranslations):

            choice = rand.choice(languages)
            response = translateInstance.translate(text, choice["language"])
            text = response["translatedText"]
            language = choice["name"]
            languageTrace += f"-> {language} "

            if i % 8 == 0:
                languageTrace += "\n"

        text = translateInstance.translate(text, "en")["translatedText"]
        await ctx.send(f"Here ya go.\n*{languageTrace}-> English*\n{text}")
            
async def setup(bot):
    await bot.add_cog(GoogleTranslateAPI(bot))