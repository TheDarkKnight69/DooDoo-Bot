import discord
from discord.ext import commands
from discord import app_commands
import os

intents = discord.Intents.default()
MY_GUILD = discord.Object(id=894451313818099783)

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        self.tree.add_command(ping)
        synced = await self.tree.sync(guild=MY_GUILD)
        print(f"Synced {len(synced)} command(s)")

client = MyBot()

@app_commands.command(name="ping", description="Ping test")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")

client.run("MTM5ODkwOTYzNzI3Njg2MDU1Ng.GqO4pk.j7jJBR5TQlt82ASWEiNlvBo42zh1XemJg8PDvs")
