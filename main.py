import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='?', intents=intents)

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    swears = {"shit", "fuck", "bitch", "ass", "dick", "penis"}
    badstuff = {'67', '6 or 7', '6 + 7', '6 7'}

    # Swear filter
    if any(word in message.content.lower() for word in swears):
        await message.delete()
        await message.channel.send(f"{message.author.mention} Please do not use that word!")

        log_channel = discord.utils.get(message.guild.text_channels, name="logs")
        if log_channel:
            role = discord.utils.get(message.guild.roles, name="Moderators")
            if role:
                await log_channel.send(
                    f"⚠️ {role.mention} — {message.author} used a swear in {message.channel.mention}"
                )
            else:
                await log_channel.send(
                    f"⚠️ {message.author} used a swear in {message.channel.mention}"
                )

    # Badstuff filter
    if any(word in message.content.lower() for word in badstuff):
        await message.channel.send(f"{message.author.mention} said 67!")

        log_channel = discord.utils.get(message.guild.text_channels, name="logs")
        role = discord.utils.get(message.guild.roles, name="Moderators")
        if log_channel:
            await log_channel.send(
                f"⚠️ {role.mention} - {message.author} said 67 in {message.channel.mention}"
            )

    # Always process commands
    await bot.process_commands(message)
import webserver
webserver.keep_alive
bot.run(token, log_handler=handler, log_level=logging.DEBUG)