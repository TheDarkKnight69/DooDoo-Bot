from discord.ext import commands
import discord
from discord import app_commands
import os
import asyncio
import json
import aiohttp
import dateutil
import time
import async_cse
import io
import datetime



class Google(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx

    async def on_timeout(self):
      for item in self.children:
        item.disabled = True
        await self.message.edit(view=self) 

    @discord.ui.button(label='Screeshot Page', style=discord.ButtonStyle.green)
    async def ss(self, interaction: discord.Interaction, button: discord.ui.Button):
      async with aiohttp.ClientSession() as d:
        async with d.get(f'https://image.thum.io/get/width/1200/crop/1200/allowJPG/{j}') as get_ss:
          s = await get_ss.json()  # returns dict
          ss= discord.Embed(title = f"`{site}`", url = site, color = discord.Color.random())
          ss.set_image(url = f"https://image.thum.io/get/width/1200/crop/1200/allowJPG/{j}")
          ss.set_footer(text = f"Requested by {ctx.author}")
          await interaction.response.send_message(embed=ss, ephemeral = True)


    @discord.ui.button(label='End Interaction', style=discord.ButtonStyle.grey)
    async def endint(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=self.clear_items())
        self.stop()
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
  @commands.guild_only()
  async def userinfo(self, ctx, *, member: discord.Member = None):
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
            voice = f'In <#{vc.id}> with {other_people} others' if other_people else f'In <#{vc.id}> by themselves'
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
  @commands.guild_only()
  async def ping(self, ctx):
    """Ping Pong. Checks the round latency to the API. You wouldn't need this. Used to test the bot."""
    await ctx.send(f"Pong! Latency: `{round(self.bot.latency * 1000)}ms`")


    
  @commands.hybrid_command(aliases = ['ss'])
  @commands.guild_only()
  async def screenshot(self, ctx, *, site: str):
    """Feeling too lazy to go to a website on your own? Fear not, here is screenshot.
    Screenshots a website lmao
    Usage: 
    ```.screenshot <website url>```"""
    ss= discord.Embed(title = f"`{site}`", url = site, color = discord.Color.random())
    ss.set_image(url = f"https://image.thum.io/get/width/1200/crop/1200/allowJPG/{site}")
    ss.set_footer(text = f"Requested by {ctx.author}")
    await ctx.send(embed = ss)

 # @commands.hybrid_command()
  #async def randomnumber(self, ctx, num1: int = None, num2: int = None):
 #   """Gives a random number from your arguments. 
 #   Usage: 
 #   ```.randomnumber <num1><num2>```"""
 #   if num1 == None:
 #     num1 = 1
  #  if num2 == None:
 #     num2 = 99999
 #   randomnumber = randint(num1, num2)
 #   await ctx.reply(f"{randomnumber}")

  
  @commands.hybrid_command()
  @commands.guild_only()
  async def count(self, ctx):
    """Press a button lol\n\n
    Usage: 
    ```.count```"""
    await ctx.send(embed = discord.Embed(title = "Press the button", color = discord.Color.random()), view = Counter())

  @commands.command()
  @commands.guild_only()
  async def changeprefix(self, ctx, prefix):
    with open('prefix.json', 'r') as p:
      prefixes = json.load(p)
    prefixes[str(ctx.guild.id)] = prefix
    with open('prefix.json', 'w') as p:
      json.dump(prefixes, p , indent = 4)

    await ctx.send(f"Old prefix was `{ctx.prefix}`\n\nPrefix has successfully been changed to `{prefix}`")


  @commands.command(name='uptime', aliases = ['up'])
  @commands.guild_only()
  @commands.cooldown(1, 3, commands.BucketType.user)
  async def uptime(self, ctx):
    """Gets the uptime of the bot"""
    resolved_full = discord.utils.format_dt(self.bot.start_time, "F")
    resolved_rel = discord.utils.format_dt(self.bot.start_time, "R")
    date = datetime.datetime.utcnow()
    date_resolved = discord.utils.format_dt(date, "F")
    uptime = discord.Embed(color = discord.Color.random())
    uptime.add_field(name = "Launched At", value = resolved_full, inline = False)
    uptime.add_field(name = "Up since", value = resolved_rel)
    uptime.set_author(name = self.bot.user.name, icon_url = self.bot.user.avatar.url)
    uptime.set_footer(text = f"Requested by {ctx.author}" , icon_url = ctx.author.avatar.url)
    uptime.set_thumbnail(url = ctx.author.avatar.url)
    await ctx.send(embed = uptime)




    
        
        

  @commands.command(aliases=['about'])
  @commands.guild_only()
  @commands.cooldown(1, 3, commands.BucketType.user)
  async def info(self, ctx):
    """See information about Doodoo Bot"""
    info = await self.bot.application_info()

    embed = discord.Embed(title=" Doodoo Bot Info", color=discord.Color.random())
    embed.add_field(name="Developer", value=f"```\n{str(info.owner)}```", inline=False)
    embed.add_field(name="Library", value=f"```\ndiscord.py {discord.__version__}```", inline=True)
    embed.add_field(name="Total servers", value=f"```\n{len(self.bot.guilds)}```", inline=True)
    embed.add_field(name="Total members", value=f"```\n{sum([g.member_count for g in self.bot.guilds])}```", inline=True)
    embed.set_thumbnail(url=self.bot.user.avatar.url)
    await ctx.reply(embed=embed, mention_author=False)

  @commands.hybrid_command(aliases = ['g', 'find', 'search'])
  @commands.guild_only()
  @commands.cooldown(1, 30, commands.BucketType.user)
  async def google(self, ctx, *, query):
    client = async_cse.Search(os.environ.get("google_api")) # create the Search client (uses Google by default!)

    results = await client.search(query, safesearch=True) # returns a list of async_cse.Result objects
    google = discord.Embed(title = "Google Search Results", color = discord.Color.random())
    google.add_field(name = results[0].title, value = f"{results[0].url}\n{results[0].description}")
    google.set_thumbnail(url = results[0].image_url)
    await client.close()
    await ctx.send(embed = google)


  @commands.hybrid_command()
  @commands.guild_only()
  @commands.cooldown(1, 3, commands.BucketType.user)
  async def spotify(self, ctx, member: discord.Member=None):
    member = member or ctx.author

    spotify = discord.utils.find(lambda a: isinstance(a, discord.Spotify), member.activities)
    if spotify is None:
      return await ctx.send(f"**{member}** is not listening or connected to Spotify.")

    params = {
      'title': spotify.title,
      'cover_url': spotify.album_cover_url,
      'duration_seconds': spotify.duration.seconds,
      'start_timestamp': spotify.start.timestamp(),
      'artists': spotify.artists
    }
  
    async with aiohttp.ClientSession() as session:
      async with session.get('https://api.jeyy.xyz/discord/spotify', params=params) as response:
        buf = io.BytesIO(await response.read())
        artists = ', '.join(spotify.artists)
        await ctx.send(f"> **{member}** is listening to **{spotify.title}** by **{artists}**", file=discord.File(buf, 'spotify.png'))




  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      seconds = error.retry_after
      seconds = round(seconds, 2)
      hours, remainder = divmod(int(seconds), 3600)
      minutes, seconds = divmod(remainder, 60)
      await ctx.send(f'You are on Cooldown: {minutes}m and {seconds}s remaining.')

    



  
      
    
 
async def setup(client: commands.Bot) -> None:
  await client.add_cog(Misc(client))      