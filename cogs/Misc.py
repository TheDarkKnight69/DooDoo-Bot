from discord.ext import commands, menus
import discord
from discord import app_commands
import os
import asyncio

class Counter(discord.ui.View):

    # Define the actual button
    # When pressed, this increments the number displayed until it hits 5.
    # When it hits 5, the counter button is disabled and it turns green.
    # note: The name of the function does not matter to the library
    @discord.ui.button(label='0', style=discord.ButtonStyle.red)
    async def count(self, interaction: discord.Interaction, button: discord.ui.Button):
        number = int(button.label) if button.label else 0
        button.label = str(number + 1)
        # Make sure to update the message with our updated selves
        await interaction.response.edit_message(view=self)

class Misc(commands.Cog):
  """Contains all the commands which have no place elsewhere."""
  COG_EMOJI = "<:misc:994972267899535431>"
  def __init__(self, bot):
    self.bot: commands.Bot = bot
    

  @commands.Cog.listener()
  async def on_ready(self):
    print('Misc.py is loaded.')

  @commands.Cog.listener()
  async def on_member_join(self, member):
    channel = self.bot.get_channel(904397226292424775)
    print(channel)
    print('work')
    await channel.send(f"{member.mention} has joined")

  @commands.Cog.listener()
  async def on_member_leave(self, member):
    channel = self.bot.get_channel(904397226292424775)
    print(channel)
    print('work')
    await channel.send(f"{member} has left")

   
  @commands.hybrid_command(aliases = ['ui'])
  async def info(self, ctx, *, member: discord.Member = None):
        """Shows a ton of info about the member in the server.
          Usage:
    ```.info <member>```"""

        member = member or ctx.author
        guild = ctx.guild
        e = discord.Embed()
        roles = [role.name.replace('@', '@\u200b') for role in getattr(member, 'roles', [])]
        e.set_author(name=str(member))
        e.add_field(name='ID', value=member.id, inline=False)
        e.add_field(name='Joined', value="<t:{}>".format(int(member.joined_at.timestamp())), inline=True)
        e.add_field(name='Created', value="<t:{}>".format(int(member.created_at.timestamp())), inline=True)
        voice = getattr(member, 'voice', None)
        if voice is not None:
            vc = voice.channel
            other_people = len(vc.members) - 1
            voice = f'{vc.name} with {other_people} others' if other_people else f'{vc.name} by themselves'
            e.add_field(name='Voice', value=voice, inline=False)
        if roles:
            roles = " ".join([role.mention for role in member.roles if role.name != "@everyone"])
            e.add_field(name='Roles', value= f"{roles}", inline=False)

        colour = member.colour
        if colour.value:
            e.colour = colour

        e.set_thumbnail(url=member.avatar)
        await ctx.send(embed=e)

  @commands.hybrid_command(aliases = ['remoji', 'emoji-id'], hidden = True)
  async def rawemoji(self, ctx, *, emoji: discord.Emoji) -> None:
    await ctx.send(f"{str(emoji.url)}")

  @commands.hybrid_command()
  async def ping(self, ctx):
    """Ping Pong. Checks the round latency to the API. You wouldn't need this. Used to test the bot."""
    await ctx.send(f"Pong! Latency: `{round(self.bot.latency * 1000)}ms`")


    
  @commands.hybrid_command(aliases = ['ss'])
  async def screenshot(self, ctx, *, site: str):
    """Feeling too lazy to go to a website on your own? Fear not, here is screenshot.
    Screenshots a website lmao
    Usage: 
    ```.screenshot <website url>```"""
    ss= discord.Embed(title = f"`{site}`", url = site, color = discord.Color.random())
    ss.set_image(url = f"https://image.thum.io/get/width/1200/crop/1200/allowJPG/{site}")
    ss.set_footer(text = f"Requested by {ctx.author}")
    await ctx.send(embed = ss)

  @commands.hybrid_command()
  async def randomnumber(self, ctx, num1: int = None, num2: int = None):
    """Gives a random number from your arguments. 
    Usage: 
    ```.randomnumber <num1><num2>```"""
    if num1 == None:
      num1 = 1
    if num2 == None:
      num2 = 99999
    randomnumber = randint(num1, num2)
    await ctx.reply(f"{randomnumber}")

  
  @commands.hybrid_command()
  async def count(self, ctx):
    """Press a button lol\n\n
    Usage: 
    ```.count```"""
    await ctx.send(embed = discord.Embed(title = "Press the button", color = discord.Color.random()), view = Counter())

    
    
 
async def setup(client: commands.Bot) -> None:
  await client.add_cog(Misc(client))      