import discord
from discord.ext import commands
from discord import app_commands
from keep_alive import keep_alive
import asyncio
import random
import os
from pretty_help import PrettyHelp, PrettyMenu
import logging



MY_GUILD = discord.Object(id=894451313818099783)  # replace with your guild id



class MyClient(commands.Bot):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(
          command_prefix = commands.when_mentioned_or("."),
          status = discord.Status.dnd,
          case_sensitive = False,
          intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
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
        


intents = discord.Intents().all()
client = MyClient(intents=intents)


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')





@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')





keep_alive()
client.run(os.environ.get('TOKEN'), log_handler=handler, log_level=logging.INFO)
  

