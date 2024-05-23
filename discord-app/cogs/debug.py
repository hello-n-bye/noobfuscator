import discord
from discord.ext import commands

class Debug(commands.Cog):
   def __init__(self, bot):
      self.bot = bot

   @commands.Cog.listener()
   async def on_ready(self):
      print(f"✅ Loaded debug cog")

   @commands.command(aliases=["latency", "ms", "delay"])
   async def ping(self, ctx: commands.Context):
      delay = round((self.bot.latency * 1000), 1)
      
      embed = discord.Embed(title="🏓  Pong!", description=f"Noobfuscator delivered a reply!", color=0x2b2d31)
      embed.add_field(name="Response Time", value=f"{delay} ms", inline=False)

      await ctx.reply(embed=embed)

   @commands.command(aliases=["dircheck", "dir", "isdir"])
   async def checkdir(self, ctx: commands.Context):
      import os

      directory = "discord-app/source-files"
      if not os.path.exists(directory):
         embed = discord.Embed(title="Directory Check", description="The directory does not exist.", color=0x2b2d31)

         await ctx.reply(embed=embed)
      else:
         embed = discord.Embed(title="Directory Check", description="The directory exists.", color=0x2b2d31)

         await ctx.reply(embed=embed)

async def setup(bot):
   await bot.add_cog(Debug(bot))