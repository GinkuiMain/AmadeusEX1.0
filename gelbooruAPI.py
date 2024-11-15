import time
import discord
from discord.ext import commands
import response
from DiscordBotToken import TOKEN as botTK
from discord.commands import Option
from discord.commands import slash_command
import requests

class gelbooruCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

        @bot.slash_command(name="gelbooru-search", description="Searches on Gelbooru for images. (I.E. : 'cat_girl' or 'dog_boy' -- Add a ' _ ' instead of space.) ")
        async def gelbooruSearch(ctx, tags: Option(str, "Write/Type the tags you want to search for (white spaces = '_')):",
                                                   required=True)):
            await ctx.defer()

            url = "https://gelbooru.com/index.php" # https://gelbooru.com/index.php?page=wiki&s=view&id=18780
            params = {
                "page": "dapi",
                "s": "post",
                "q": "index",
                "tags": tags,
                "json": 1,
                "limit": 10  # Change the number for whatever number of 'random' posts you want when usnig the command
            }

            try:
                response = requests.get(url, params=params)

                # Log the response for debugging
                print(f"Response Status Code: {response.status_code}")
                print(f"Response Content: {response.text}")

                # Ensure we got a 200 OK response before proceeding -- This was made with Reddit's help
                if response.status_code != 200:
                    await ctx.respond("Failed to retrieve data from Gelbooru. Please try again later. I think it might've been SERN...")
                    return

                data = response.json()
                posts = data.get("post", []) # Access the 'post' array inside the JSON response
                if posts:
                    # Fetch the first post
                    post = posts[0]
                    post_url = post.get("file_url", "")
                    if post_url:
                        await ctx.respond(f"Here, mad scientist, is what I've found!! \n `{tags}`:\n {post_url}")
                    else:
                        await ctx.respond("Nothing was found... Must've been SERN's fault. (No result error)")
                else:
                    await ctx.respond("Nothing was found... Must've been SERN. (No data error)")

            except Exception as e:
                await ctx.respond("Something went fairly wrong-- Not my fault! I blame Okabe.")
                print(f"Error occurred: {e}")
def setup(bot):
    bot.add_cog(gelbooruCog(bot))