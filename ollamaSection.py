import discord
from discord.ext import commands
from discord.commands import Option
import requests


class OllamaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ollama_url = "http://localhost:11434/api/generate"

    @commands.slash_command(name="question", description="Asks Amadeus a question!")
    async def question(self, ctx, prompt: Option(str, "What is your question to the great Makise Kurisu herself?")):
        await ctx.defer()

        # I know this SHOULDN'T be in here. But, for now, I'll add it for the lols.
        kurisu_prompt = f"Respond like Kurisu Makise from Steins;Gate. She is sarcastic, witty, intelligent, and sometimes tsundere. Make sure to show these traits when answering. The user asks: {prompt}"

        payload = {
            "model": "mistral",
            "prompt": kurisu_prompt,
            "stream": False
        }

        try:
            response = requests.post(self.ollama_url, json=payload)
            data = response.json()

            if "response" in data:
                await ctx.respond(f"{data['response']}")
            else:
                await ctx.respond("Uhm... I couldn't help you this time—maybe try asking Darou?")
        except Exception as e:
            await ctx.respond(f"Something went wrong: {e}")

def setup(bot):
    bot.add_cog(OllamaCog(bot))
