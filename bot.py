import time
import discord
from discord.ext import commands
import response
from DiscordBotToken import TOKEN as botTK
from discord.commands import Option
from discord import FFmpegPCMAudio
import jokesfile
import random

"""
For now, the VC-related commands are going to stay as prefix, not slashes.
Reason? I hate using a slash command to make a bot join VCs. Takes too much time of our precious lives :)
"""


def runDiscordBot():  # runs my bot
    try:
        TOKEN = botTK  # Token stored in a local file for... Well, safety! (duh)
        intents = discord.Intents.default()
        intents.message_content = True
        botPrefix = commands.Bot(command_prefix="$", intents=intents)  #prefix... Kinda broken rn. Makes the bot send private messages.


        async def sendMessage(message, userMessage, isPrivate):  # I'll need to leave this one, as she is important for other funcs
            try:
                if message.author != botPrefix.user:
                    responses = response.handlingMessages(userMessage)
                    await message.author.send(responses) if isPrivate else await message.channel.send(responses)

            except Exception as erro:
                print(erro)

        @botPrefix.event  # warns if the bot is on!
        async def on_ready():
            print(f"{botPrefix.user} is running... It's a miracle...- Ahem, of course it is! I have a big brain myself!")
            async for guild in botPrefix.fetch_guilds(limit=150):
                print(f"Guild Name: {guild.name} / Guild ID: {guild.id}")

        """
        Now, the actual bot functions. I'll send this one to another file later on!
        But, for now, they'll be stored in here.
        """

        @botPrefix.slash_command(
            name="whoami", description=f"You are..."  # I'll turn this into a list, since it will change as she joins new servers
        )
        async def whoami(ctx):  # Just testing (for now)
            try:
                await ctx.respond(f"You are... Yourself ?! Nice to meet you.")  # Respond is better for slash commands.
            except Exception as erro:
                await ctx.respond(f"I am sorry! But something went wrong... {erro}")
                print(erro)

        @botPrefix.slash_command(description=f"Calculator for noobies :)")
        async def calculate(ctx, expression: Option(str, "write in your expression:")):
            try:
                await ctx.respond(eval(expression))
            except ZeroDivisionError:
                await ctx.respond("You can't divide by 0")
                pass

        @botPrefix.slash_command(description=f"Tells a random joke.")
        async def telljoke(ctx):
            await ctx.respond(jokesfile.AmadeusJokes())
            await ctx.respond("Hope that's funny enough.")

        @botPrefix.slash_command(description=f"Random number from 1-6, twice.")
        async def diceroll(ctx):
            try:
                x = random.randint(1,6)
                y = random.randint(1,6)
                await ctx.respond(f"• First roll: {x} \n\n• Second roll: {y}\n\n> Total: {x+y}")
            except Exception as ex:
                await ctx.respond("Something went wrong. Sorry!")
                print(f"{ex}")

        @botPrefix.slash_command(description=f"Plays Fatima, Amadeus or Hacking To The Gate!")
        async def play(ctx, song: Option(str, "Write in one of the three:")):
            try:
                song = str(song).lower().strip()
                if ctx.author.voice:
                    channel = ctx.author.voice.channel
                    voice = await channel.connect()
                    src = FFmpegPCMAudio(f'musics/{song}.mp3')
                    player = voice.play(src)
                    await ctx.respond(f"Currently playing {song}")
                else:  # if the user isn't in a voice chat
                    await ctx.respond(f"{ctx.author} Sorry, my dear friend... I can't play that song, since I'm not in a VC. (Or you aren't in a VC)")
            except Exception as erro:
                print(erro)

        @botPrefix.slash_command(description=f"Just joins the VC, no music or anything.")
        async def join(ctx):
            try:
                if ctx.author.voice:  # If the author/user is in a vc
                    channel = ctx.author.voice.channel
                    await channel.connect()
                    await ctx.respond("I've joined the voice chat, Mad Scientist.")
                else:
                    await ctx.respond("Join a voice chat, human.")
            except Exception as erro:
                await ctx.respond(f"Something went wrong {erro}")

        @botPrefix.slash_command(description=f"Leaves the VC")
        async def leave(ctx):
            try:
                if ctx.voice_client:  # if user is in channel
                    await ctx.guild.voice_client.disconnect()
                    await ctx.respond(f"I left the voice channel because {ctx.author} told me to do so. El Psy Congroo ")
                else:  # If user isn't in a channel.
                    await ctx.respond("I'm not in a voice channel, filthy human.")
            except Exception as erro:
                print(erro)

        @botPrefix.event  # Just so I can monitor my server from far away (this one only will work if Amadeus has Admin privileges)
        async def on_message(message):  # Worth mentioning, I'll remove this one... Eventually.
            userName = str(message.author)
            userMessage = str(message.content)
            channel = str(message.channel)
            guildUsr = str(message.guild)

            print(f"\n User {userName} sent message \"{userMessage}\" in {channel} / Time the message was sent: {time.strftime('%H : %M : %S') } / It was in {guildUsr}  \n")  # just so I can check messages :>

            if userMessage[0] == "$":  # every function must be here, here only... If related to the bot commands
                userMessage = userMessage[1:]
                await sendMessage(message, userMessage, isPrivate=True)
            else:
                await sendMessage(message, userMessage, isPrivate=False)

            await botPrefix.process_commands(message)

        botPrefix.run(TOKEN)

    except Exception as error:
        print(error)
