from discord.ext import commands
from discord import Option
import discord
import asyncio
from collections import deque
import yt_dlp

SONG_QUEUES = {}


def _extract(query, ydl_opts):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(query, download=False)


async def search_ytdlp_async(query, ydl_opts):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: _extract(query, ydl_opts))


class YouTubeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="play", description="Play a song from YouTube!")
    async def play(
        self,
        ctx: discord.ApplicationContext,
        song_query: Option(str, "Search for a song"),
    ):
        await ctx.defer()

        if not ctx.author.voice:
            await ctx.respond("You're not in a voice channel, Mad Scientist.")
            return

        voice_channel = ctx.author.voice.channel
        voice_client = ctx.guild.voice_client

        if voice_client is None:
            voice_client = await voice_channel.connect()
        elif voice_channel != voice_client.channel:
            await voice_client.move_to(voice_channel)

        ydl_options = { # I'll try to place this and other sections into separate files, so it looks less... Complicated for whoever uses it.
            "format": "bestaudio[abr<=96]/bestaudio",
            "noplaylist": True,
            "youtube_include_dash_manifest": False,
            "youtube_include_hls_manifest": False,
            "nocheckcertificate": True,  # Optional, for SSL issues
            "force_generic_extractor": True,  # As a fallback
        }

        query = "ytsearch1:" + song_query
        results = await search_ytdlp_async(query, ydl_options)
        tracks = results.get("entries", [])

        if not tracks:
            await ctx.respond("No results found... I blame Okabe.")
            return

        first_track = tracks[0]
        audio_url = first_track["url"]
        title = first_track.get("title", "Untitled")

        guild_id = str(ctx.guild_id)
        SONG_QUEUES.setdefault(guild_id, deque()).append((audio_url, title))

        if voice_client.is_playing() or voice_client.is_paused():
            await ctx.respond(f"Added to queue: **{title}**, mad scientist!")
        else:
            await ctx.respond(f"Now playing: **{title}**")
            await self.play_next_song(voice_client, guild_id, ctx.channel)

    async def play_next_song(self, voice_client, guild_id, channel):
        if SONG_QUEUES[guild_id]:
            audio_url, title = SONG_QUEUES[guild_id].popleft()

            ffmpeg_options = {
                "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                "options": "-vn -c:a libopus -b:a 96k",
            }

            source = discord.FFmpegOpusAudio(audio_url, **ffmpeg_options)

            def after_play(error):
                if error:
                    print(f"Error playing {title}: {error}")
                asyncio.run_coroutine_threadsafe(
                    self.play_next_song(voice_client, guild_id, channel),
                    self.bot.loop
                )

            voice_client.play(source, after=after_play)
            await channel.send(f"Now playing: **{title}**")
        else:
            await voice_client.disconnect()
            SONG_QUEUES[guild_id] = deque()

    @commands.slash_command(description=f"Skips the current song")
    async def skip(self, ctx: discord.ApplicationContext):
        try:
            voice_client = ctx.guild.voice_client
            if voice_client and (voice_client.is_playing() or voice_client.is_paused()):
                voice_client.stop()
                await ctx.respond("Skipped the current song. Happy now, Okabe?")
            else:
                await ctx.respond("There's nothing playing... You can't skip silence, you know.")

        except Exception:
            ctx.respond("I couldn't connect to the voice | Or something else went wrong.")
            ctx.respond(f"{Exception}")

    @commands.slash_command(description=f"Pauses the current song")
    async def pause(self, ctx: discord.ApplicationContext):
        try:
            voice_client = ctx.guild.voice_client
            if voice_client is None:
                await ctx.respond("I'm not in a voice chat. Not my fault, blame Darou! That idiot whale.")
                return
            if not voice_client.is_playing():
                await ctx.respond("Nothing to play! Nothing to play!!! Boring...")

            voice_client.pause()
            await ctx.respond("Paused.")

        except Exception:
            await ctx.respond("")

    @commands.slash_command(description=f"Resumes the current song")
    async def resume(self, ctx: discord.ApplicationContext):
        voice_client = ctx.guild.voice_client

        if voice_client is None:
            await ctx.respond("I'm not in a voice channel!!!! Hmph...")
        if not voice_client.is_paused():
            await ctx.respond("The song's not even paused. Are you ok??")

        ctx.respond("Resumed!")
        voice_client.resume()

    @commands.slash_command(description=f"Stops the current song")
    async def stop(self, ctx: discord.ApplicationContext):
        voice_client = ctx.guild.voice_client

        if not voice_client or not voice_client.is_connected():
            await ctx.respond("I'm not connected to any voice channel. Not my fault.")
            return

        guild_id_str = str(ctx.guild.id)
        SONG_QUEUES.get(guild_id_str, deque()).clear()

        if voice_client.is_playing() or voice_client.is_paused():
            voice_client.stop()

        await voice_client.disconnect()
        await ctx.respond("Playback halted, queue cleared, and I’m gone. Just like your common sense.")

    @commands.slash_command(description=f"Leaves the VC")
    async def leave(self, ctx: discord.ApplicationContext):
        try:
            if ctx.voice_client:  # if user is in channel
                await ctx.guild.voice_client.disconnect()
                await ctx.respond(f"I left the voice channel because {ctx.author} told me to do so. El Psy Congroo ")
            else:  # If user isn't in a channel.
                await ctx.respond("I'm not in a voice channel, filthy human.")
        except Exception as erro:
            print(erro)


def setup(bot):
    bot.add_cog(YouTubeCog(bot))

"""
The section below is just a WIP (for me to remember later)

        # @botPrefix.slash_command(description=f"Just joins the VC, no music or anything.")
        # async def join(ctx):
        #     try:
        #         if ctx.author.voice:  # If the author/user is in a vc
        #             channel = ctx.author.voice.channel
        #             await channel.connect()
        #             await ctx.respond("I've joined the voice chat, Mad Scientist.")
        #         else:
        #             await ctx.respond("Join a voice chat, human.")
        #     except Exception as erro:
        #         await ctx.respond(f"Something went wrong {erro}")

        # @botPrefix.slash_command(description=f"Leaves the VC")
        # async def leave(ctx):
        #     try:
        #         if ctx.voice_client:  # if user is in channel
        #             await ctx.guild.voice_client.disconnect()
        #             await ctx.respond(f"I left the voice channel because {ctx.author} told me to do so. El Psy Congroo ")
        #         else:  # If user isn't in a channel.
        #             await ctx.respond("I'm not in a voice channel, filthy human.")
        #     except Exception as erro:
        #         print(erro)

"""