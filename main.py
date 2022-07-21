import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random
import json
import os
import logging



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
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.client instead of discord.client, the client will
        # maintain its own tree instead.
      

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
        await client.load_extension("jishaku")
        for filename in os.listdir("./cogs"):
	        if filename.endswith(".py"):
		        await client.load_extension(f"cogs.{filename[:-3]}")
        


intents = discord.Intents.default()
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






client.run(os.environ.get('TOKEN'), log_handler=handler, log_level=logging.INFO)
  

