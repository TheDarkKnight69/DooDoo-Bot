import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random
import json
import os
import logging
import datetime
from keep_alive import keep_alive
from difflib import get_close_matches


MY_GUILD = discord.Object(id=894451313818099783)  # replace with your guild id

def get_prefix(client, message):
  with open('prefix.json', 'r') as p:
    prefixes = json.load(p)

  return prefixes[str(message.guild.id)]

class MyClient(commands.Bot):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(
          command_prefix = get_prefix,
          status = discord.Status.dnd,
          case_sensitive = False,
          intents=intents)
        
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
        await client.load_extension("jishaku")
        for filename in os.listdir("./cogs"):
          if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
        


intents = discord.Intents().all()
intents.members = True
intents.message_content = True
client = MyClient(intents=intents)

client.remove_command('about')
client.remove_command('uptime')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')





@client.event
async def on_ready():
  print(f'Logged in as {client.user} (ID: {client.user.id})')
  print('------')
  client.start_time = datetime.datetime.now(datetime.timezone.utc)
    
  
@client.event
async def on_guild_join(guild):
  with open('prefix.json', 'r') as p:
    prefixes = json.load(p)

  prefixes[str(guild.id)] = "."

  with open('prefix.json', 'w') as p:
    json.dump(prefixes, p , indent = 4)


@client.event
async def on_guild_remove(guild):
  with open('prefix.json', 'r') as p:
    prefixes = json.load(p)

  prefixes.pop(str(guild.id))

  with open('prefix.json', 'w') as p:
    json.dump(prefixes, p , indent = 4)
  


@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')

  




keep_alive()
client.run(os.environ.get('TOKEN'), log_handler=handler, log_level=logging.INFO)
  

