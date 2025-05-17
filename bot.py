import time
import discord
from discord.ext import commands
import response
from DiscordBotToken import TOKEN as botTK
from discord.commands import Option
from discord import FFmpegPCMAudio
import jokesfile
import random

def runDiscordBot():
    try:
        TOKEN = botTK  # Token stored in a local file for... Well, safety! (duh)
        intents = discord.Intents.default()
        intents.message_content = True
        botPrefix = commands.Bot(command_prefix="$", intents=intents)  #prefix... Kinda broken rn. Makes the bot send private messages.

        botPrefix.load_extension("gelbooruAPI")
        botPrefix.load_extension("ollamaSection")
        botPrefix.load_extension("musicSection")

        print("-> Gelbooru cog loaded.")
        print("-> Ollama cog loaded.")
        print("-> Music cog loaded.")

        async def sendMessage(message, userMessage, isPrivate):  # I'll need to leave this one, as she is important for other funcs
            try:
                if message.author != botPrefix.user:
                    responses = response.handlingMessages(userMessage)
                    await message.author.send(responses) if isPrivate else await message.channel.send(responses)

            except Exception as erro:
                print(erro)

        @botPrefix.event  # warns if the bot is on!
        async def on_ready():
            await botPrefix.sync_commands()
            print(f"{botPrefix.user} is running... It's a miracle...- Ahem, of course it is! I have a big brain myself!")
            async for guild in botPrefix.fetch_guilds(limit=150):
                print(f"Guild Name: {guild.name} / Guild ID: {guild.id}")
            await botPrefix.sync_commands()

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


        @botPrefix.slash_command(description=f"Random number from 1-6, twice.")
        async def diceroll(ctx):
            try:
                x = random.randint(1,6)
                y = random.randint(1,6)
                await ctx.respond(f"• First roll: {x} \n\n• Second roll: {y}\n\n> Total: {x+y}")
            except Exception as ex:
                await ctx.respond("Something went wrong. Sorry!")
                print(f"{ex}")

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
