import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

bot = commands.Bot(command_prefix="-", intents=discord.Intents.all())
cogs_dir = os.path.join(os.path.dirname(__file__), "cogs")

for filename in os.listdir(cogs_dir):
   if filename.endswith(".py"):
      asyncio.run(bot.load_extension(f"cogs.{filename[:-3]}"))

@bot.event
async def on_ready():
   print(f"✅ Signed in: {bot.user}")

load_dotenv()

token = os.getenv("TOKEN")
bot.run(token)