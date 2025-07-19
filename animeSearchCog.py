import discord
from discord.ext import commands
from discord import Option  # Corrected import for slash commands
import aiohttp

JIKAN_BASE_URL = "https://api.jikan.moe/v4"  # Unofficial MAL REST API- My friend told me it was good, so... There it is!
# It always follows the same logic: Search, Extract and then Build + send


class AnimeSearchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def jikan_fetch(self, endpoint: str):  # Fetches our desired JSON file to be used later on by Amadeus
        url = f"{JIKAN_BASE_URL}/{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return None
                return await resp.json()

    @commands.slash_command(name="anime", description="Searches for anime titles")
    async def anime(self, ctx: discord.ApplicationContext, query: Option(str, "Type the anime's title: ")):
        await ctx.defer()  # search

        data = await self.jikan_fetch(f"anime?q={query.lower()}&limit=1")
        if not data or not data.get("data"):
            return await ctx.respond(f"No results have been found for {query.lower()}... Must've been Okabe.")

        a = data["data"][0]  #extract
        title = a.get("title")
        score = a.get("score")
        episodes = a.get("episodes")
        status = a.get("status")
        synopsis = a.get("synopsis", "No synopsis available.")[:600] + "..."
        img = a.get("images", {}).get("jpg", {}).get("image_url")

        embed = discord.Embed(title=title, url=a.get("url"), description=synopsis, color=0xff66cc)  # build and send
        embed.add_field(name="Score / Episodes / Status", value=f"{score} / {episodes} / {status}", inline=False)
        if img:
            embed.set_thumbnail(url=img)
        await ctx.respond(embed=embed)

    @commands.slash_command(name="manga", description="Searches for manga titles")
    async def manga(self, ctx: discord.ApplicationContext, query: Option(str, "Type manga name to search")):
        await ctx.defer()

        data = await self.jikan_fetch(f"manga?q={query}&limit=1")
        if not data or not data.get("data"):
            return await ctx.respond(f"No manga found for '{query}'. Even Steins;Gate can't help.")

        m = data["data"][0]

        title = m.get("title")
        score = m.get("score")
        chapters = m.get("chapters")
        volumes = m.get("volumes")
        status = m.get("status")
        synopsis = m.get("synopsis", "No synopsis available.")[:600] + "..."
        img = m.get("images", {}).get("jpg", {}).get("image_url")

        # Build a visual embed response
        embed = discord.Embed(title=title, url=m.get("url"), description=synopsis, color=0xff66cc)
        embed.add_field(name="Score / Chapters / Volumes", value=f"{score} / {chapters} / {volumes}", inline=False)
        embed.add_field(name="Status", value=status, inline=False)
        if img:
            embed.set_thumbnail(url=img)

        await ctx.respond(embed=embed)

    @commands.slash_command(name="character", description="Search for information about an anime character")
    async def character(self, ctx: discord.ApplicationContext, query: Option(str, "Character name to search")):
        await ctx.defer()

        data = await self.jikan_fetch(f"characters?q={query}&limit=1")
        if not data or not data.get("data"):
            return await ctx.respond(f"Character '{query}' not found. Probably not in the lab.")

        c = data["data"][0]

        name = c.get("name")
        about = c.get("about", "No description available.").split("\n")[0][:600] + "..."
        anime_list = ", ".join([entry["anime"]["title"] for entry in c.get("anime", [])][:5]) or "—"
        img = c.get("images", {}).get("jpg", {}).get("image_url")

        embed = discord.Embed(title=name, description=about, color=0xff66cc)
        embed.add_field(name="Appears in", value=anime_list, inline=False)
        if img:
            embed.set_thumbnail(url=img)

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(AnimeSearchCog(bot))