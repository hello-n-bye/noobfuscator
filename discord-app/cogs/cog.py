import discord
from discord.ext import commands
import random
import time
import os
import json
import re
import subprocess
import datetime
import string
import requests

config = "config.json"

def encrypt_string(str):
    return ''.join(['\\x{:02x}'.format(ord(c)) for c in str])

def get_random_useless_code():
    with open("./ignore-me.json", "r", encoding='utf-8') as file:
      data = json.load(file)

    types = data['code']

    useless_code = random.choice(types)
    variable_name_length = random.randint(5, 15)

    possible_characters = string.ascii_letters

    variable_name = ''.join(random.choice(possible_characters) for _ in range(variable_name_length))

    useless_code = useless_code.replace('_', variable_name)
    useless_code = re.sub(r"(['\"])(.*?)\1", lambda m: f"{m.group(1)}{encrypt_string(m.group(2))}{m.group(1)}", useless_code)

    return useless_code

def obfuscate(lua):
    names_local = re.findall(r"(?<=local )([a-zA-Z_][a-zA-Z0-9_]*)\b", lua)
    names_function = re.findall(r"(?<=function )([a-zA-Z_][a-zA-Z0-9_]*)\b", lua)
    names_start = re.findall(r"^([a-zA-Z_][a-zA-Z0-9_]*)\b", lua)

    names = names_local + names_function + names_start
    
    used = set()
    lua_keywords = ["and", "break", "do", "else", "elseif", "end", "false", "for", "function", "if", "in", "local", "nil", "not", "or", "repeat", "return", "then", "true", "until", "while"]
    
    for name in names:
        if name not in lua_keywords:
            converted = None
            
            while converted is None or converted in used:
                variable_name_length = random.randint(5, 15)
                possible_characters = string.ascii_letters
                converted = ''.join(random.choice(possible_characters) for _ in range(variable_name_length))
            
            used.add(converted)
            
            lua = re.sub(rf"\b{name}\b", lambda m: converted if (m.string[:m.start()].count('"') % 2 == 0 and m.string[m.end():].count('"') % 2 == 0) else m.group(0), lua)

    lines = lua.split('\n')
    for i in range(len(lines)):
        for _ in range(random.randint(1, 1500)):
            lines[i] += ' ' + get_random_useless_code()

    lua = ' '.join(lines)

    lua = re.sub(r'"([^"]*)"', lambda m: f'"{encrypt_string(m.group(1))}"', lua)
    lua = re.sub(r"\b(end|;)\b", lambda m: f"{m.group(0)} {get_random_useless_code()}", lua)

    return lua

class Obfuscate(commands.Cog):
   def __init__(self, bot):
      self.bot = bot

   @commands.Cog.listener()
   async def on_ready(self):
      print(f"✅ Loaded obfuscation cog")

   @commands.command(aliases=["obf", "obfuscate", "ob"])
   async def o(self, ctx: commands.Context):
      file = ctx.message.attachments

      if not file:
         embed = discord.Embed(title="Missing File", description="You're missing the file to obfuscate.", color=0x2b2d31)
         embed.add_field(name="Usage", value="Use **-o**, **-obf** or **-obfuscate** with a file included.", inline=False)
         embed.add_field(name="Supported File Types", value=".Lua, .Luau", inline=False)

         await ctx.reply(embed=embed)
      else:
         cutoutName = file[0].filename.split(".")[0]
         cutoutName = cutoutName.capitalize()

         print(f'✅ Detected file ... "{cutoutName}"')

         fileTypes = [".lua", ".luau"]
         
         try:
            if file[0].filename.endswith(tuple(fileTypes)):
               print(f'✅ Supported file type ... "{cutoutName}"')

               embed = discord.Embed(title = "Noobfuscator's Low-end Obfuscation", description="> Please wait whilst we obfuscate.", color=0x2b2d31, url="https://github.com/hello-n-bye/noobfuscator")
               embed.set_author(name="Noobfuscator", url="https://github.com/hello-n-bye/noobfuscator", icon_url="attachment://logo.png")
               embed.add_field(name="Progress", value="1. Stage 0 of 3", inline=True)
               embed.add_field(name="File Name", value=f"2. {cutoutName}", inline=True)
               embed.add_field(name="Task", value="3. Preparing for Obfuscation...", inline=False)
               embed.set_image(url="attachment://code.png")
               embed.set_footer(text=f"Obfuscation Requested on: {datetime.datetime.now().strftime('%Y-%m-%d')}")

               logo = discord.File("images/logo.png", filename="logo.png")
               code = discord.File("images/code.png", filename="code.png")

               message = await ctx.reply(embed=embed, files=[logo, code])

               unique_identification_code = random.randint(100, 999)
               file_name = f"discord-app/source-files/{cutoutName}_{unique_identification_code}.lua"

               try:
                  with open(file_name, "x") as filed:
                     filed.write("")

                  embed.set_field_at(0, name="Progress", value="1. Stage 1 of 3", inline=True)

                  await message.edit(embed=embed)

                  time.sleep(random.uniform(0.3, 0.65))

                  embed.set_field_at(2, name="Task", value="3. Syncing file contents", inline=False)
                  await message.edit(embed=embed)

                  try:
                     with open(file_name, "w") as filed:
                        with open(file[0].filename, "r") as original_file:
                           filed.write(original_file.read())

                     embed.set_field_at(0, name="Progress", value="1. Stage 2 of 3", inline=True)
                     await message.edit(embed=embed)

                     time.sleep(random.uniform(0.3, 0.65))

                     embed.set_field_at(2, name="Task", value="3. Minifying source-code (Luamin)", inline=False)
                     await message.edit(embed=embed)

                     path = f"discord-app/source-files/{cutoutName}_{unique_identification_code}.lua"

                     if not os.path.exists(path):
                        embed.clear_fields()
                        embed.description = "The current file does not exist, please try again."

                        return
                     else:
                        print(f"✅ Found file ... {path}")

                     with open(config, "r") as f:
                        config_data = json.load(f)

                     try:
                        result = subprocess.run([r"C:\Users\Suno\AppData\Roaming\npm\luamin.cmd", "-f", r"C:\Users\Suno\Downloads\source.lua"], capture_output=True, text=True, check=True)

                        with open(f"discord-app/source-files/{cutoutName}_{unique_identification_code}.lua", "w", encoding="utf8") as file:
                           file.write(result.stdout)

                        print(f"✅ Minified file")
                     except subprocess.CalledProcessError as e:
                        embed.clear_fields()
                        embed.description = "Failed to minify the file, please try again."
                     
                        await message.edit(embed=embed)

                        print(f"⚠️ {e}")
                        return
                     
                     try:
                        with open(path, "r", encoding="utf8") as lua_file:
                           lua = lua_file.read()
                     except FileNotFoundError as e:
                        embed.clear_fields()
                        embed.description = "Failed to read the file, please try again."
                     
                        await message.edit(embed=embed)

                        print(f"⚠️ {e}")
                        return
                     
                     obfuscated = f'([[(_Obfuscated With {config_data['name']}-{config_data['version']}_)]]):gsub("-", (function(...) {obfuscate(lua)} end))' 

                     try:
                        with open(path, "w", encoding="utf8") as lua_file:
                           lua_file.write(obfuscated)
                           lua_file.close()

                        response = requests.post("https://www.cloudbin.org/raw", headers={"Content-Type": "text/plain"}, data=obfuscated)
                        
                        if response.status_code == 200:
                           try:
                              uploadedUrl = f"https://www.cloudbin.org/raw/{response.content.decode("utf-8")}"
                           except Exception as e:
                              print("⚠️ Error occured uploading to Cloudbin, not sending URL.")
                        else:
                           print("⚠️ Error occured uploading to Cloudbin, not sending URL.")

                        print("✅ Obfuscated file")

                        embed.set_field_at(0, name="Progress", value="1. Stage 3 of 3", inline=True)
                        embed.description = "> Obfuscation complete, you'll receive the file shortly."
                        embed.set_field_at(2, name="Task", value="3. Sending obfuscated file", inline=False)

                        await message.edit(embed=embed)

                        time.sleep(random.uniform(0.3, 0.65))

                        embed.clear_fields()
                        embed.add_field(name="Obfuscation Notice", value="1. The obfuscation process has been completed.", inline=False)

                        if uploadedUrl:
                           embed.add_field(name="RAW Url", value=f"2. [View RAW page]({uploadedUrl})", inline=False)

                        await message.edit(embed=embed)
                        await ctx.send(file=discord.File(path, filename=f"Obfuscted_{cutoutName}.lua"))

                        os.remove(file_name)
                     except IOError as e:
                        embed.clear_fields()
                        embed.description = "Failed to send obfuscated file, please try again."
                     
                        await message.edit(embed=embed)

                        os.remove(file_name)

                        print(f"⚠️ {e}")
                        return
                  except Exception as e:
                     print("❌ Error occurred, cancelled.")

                     embed.clear_fields()
                     embed.description = "Failed to obfuscate file, please try again."
                     
                     await message.edit(embed=embed)

                     os.remove(file_name)

                     print(f"⚠️ {e}")
               except Exception as e:
                  print("❌ Error occurred, cancelled.")

                  embed.clear_fields()
                  embed.description = "Failed to create source-file, please try again."
                  
                  await message.edit(embed=embed)

                  os.remove(file_name)

                  print(f"⚠️ {e}")
            else:
               print("❌ Unsupported file type, cancelled.")

               embed.clear_fields()
               embed.description = "Invalid file type, please try again."

               embed.add_field(name="Supported File Types", value=".Lua, .Luau", inline=False)
               
               await message.edit(embed=embed)

               os.remove(file_name)

               await ctx.reply(embed=embed)
         except Exception as e:
            print("❌ Error occurred, cancelled.")

            embed.clear_fields()
            embed.description = "Invalid file type, please try again."
            
            await message.edit(embed=embed)

            os.remove(file_name)

            await ctx.reply(embed=embed)
            print(f"⚠️ {e}")

async def setup(bot):
   await bot.add_cog(Obfuscate(bot))