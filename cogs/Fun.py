import discord
from discord.ext import commands
from discord import app_commands
import random
from typing import Optional
import datetime
import os
import aiohttp
from peepee import (
    generate_puzzle_embed,
    update_embed,
    random_puzzle_id,
    is_game_over,
    is_valid_word
)


   
class Meme(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx

    async def on_timeout(self):
      for item in self.children:
        item.disabled = True
        await self.message.edit(view=self) 

    @discord.ui.button(label='Next Meme', style=discord.ButtonStyle.green)
    async def meme(self, interaction: discord.Interaction, button: discord.ui.Button):
      async with aiohttp.ClientSession() as d:
        async with d.get('https://meme-api.herokuapp.com/gimme/memes') as get_meme:
          memes = await get_meme.json()  # returns dict
          meme = discord.Embed(title=memes['title'], url = memes['postLink'], color=discord.Color.random())
          meme.set_image(url=memes['url'])
          meme.set_footer(text=f"Powered by r/memes | Requested by {self.ctx.author}")
          await interaction.response.edit_message(embed=meme)


    @discord.ui.button(label='End Interaction', style=discord.ButtonStyle.grey)
    async def endint(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=self.clear_items())
        self.stop()

class Fun(commands.Cog):
  """Contains all the entertainment commands."""
  COG_EMOJI = "🎮"
  def __init__(self, client: commands.Bot) -> None:
    self.client = client

  testServerid = 894451313818099783

  @commands.Cog.listener()
  async def on_ready(self):
    print('Fun.py is loaded.')

  @commands.hybrid_command(name = '8ball', description="Ask the 8ball what you want.")
  @commands.guild_only()
  async def _8ball(self, ctx, *, question : str):
    """Ask the magic 8ball anything!!
       Usage: 
        ```.8ball <question>```
    """
    responses = ["It is certain.",
                  "It is decidedly so.", 
                  "Without a doubt.",
                  "Yes - definitely.", 
                  "You may rely on it.", 
                  "As I see it, yes.",
                  "Most likely.", 
                  "Outlook good.",
                  "Yes.", 
                  "Signs point to yes.",
                  "Reply hazy, try again.",
                  "Ask again later.",
                  "Better not tell you now.", 
                  "Cannot predict now.",
                  "Concentrate and ask again.",
                  "Don't count on it.", 
                  "My reply is no.",
                  "My sources say no.", 
                  "Outlook not so good.", 
                  "Very doubtful."
                ]
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

  @commands.hybrid_command(name = 'insult')
  @commands.guild_only()
  async def insult(self, ctx, *, member:Optional[discord.Member]):
    """Insult anyone :D
       Usage: 
        ```.insult <mention someone here>```"""
    async with aiohttp.ClientSession() as a:
      async with a.get('https://evilinsult.com/generate_insult.php?lang=en&type=json') as get_insult:
        insult = await get_insult.json()  # returns dict
        if member == None:
          member = ctx.author
        await ctx.send(f'{member.mention}, {insult["insult"]}')

  @commands.hybrid_command(name = 'compliment')
  @commands.guild_only()
  async def compliment(self, ctx, *, member:discord.Member = None):
    """Compliment anyone ^-^ 
       Usage: 
        ```.compliment <mention someone here>```"""
    async with aiohttp.ClientSession() as b:
      async with b.get('https://complimentr.com/api') as get_compliment:
        compliment = await get_compliment.json()  # returns dict
        if member == None:
          member = ctx.author
        await ctx.send(f"{member.mention},  {compliment['compliment'].capitalize()}")
    
  @commands.hybrid_command(name = 'doggo')
  @commands.guild_only()
  async def doggie(self, ctx):
    """Get a dog pic!! 
        Usage: 
        ```.doggo```"""
    async with aiohttp.ClientSession() as c:
      async with c.get('https://dog.ceo/api/breeds/image/random') as get_dog:
        dog = await get_dog.json()  # returns dict
        doggie = discord.Embed(title="Woof Woof", url=dog['message'], color = discord.Color.random())
    doggie.set_image(url=dog['message'])
    await ctx.send(embed=doggie)
    
  
  @commands.hybrid_command(name = 'meme')
  @commands.guild_only()
  async def meme(self, ctx):
    """Gets the hottest memes from r/memes.
      Usage: 
      ```.meme```
    Note: Using the slash command will allow you to have a choice from the same command"""
    async with aiohttp.ClientSession() as d:
      async with d.get('https://meme-api.herokuapp.com/gimme/memes') as get_meme:
        view = Meme(ctx)
        memes = await get_meme.json()  # returns dict
        meme = discord.Embed(title=memes['title'], url = memes['postLink'], color=discord.Color.random())
        meme.set_image(url=memes['url'])
        meme.set_footer(text=f"Powered by r/memes | Requested by {ctx.author}")
        view.message = await ctx.send(embed=meme, view = view)
        
        
        
  @commands.hybrid_command(name = 'wholesomememe')
  @commands.guild_only()
  async def wholesome(self, ctx):  
    """Gets the hottest memes from r/wholesomememes.
      Usage: 
      ```.wholesomememe```
    Note: Using the slash command will allow you to have a choice from the same command"""
    async with aiohttp.ClientSession() as e:
      async with e.get('https://meme-api.herokuapp.com/gimme/wholesomememes') as get_nicememe:
        nicememe = await get_nicememe.json()
        meme = discord.Embed(title=nicememe['title'], url=nicememe['postLink'], color=discord.Color.random())
        meme.set_image(url=nicememe['url'])
        meme.set_footer(text=f"Powered by r/wholesomememes | Requested by {ctx.author}")
        await ctx.send(embed=meme, view = Meme(ctx))
        
  @commands.hybrid_command(name = 'holup')
  @commands.guild_only()
  async def holup(self, ctx): 
    """Ayo, Hol UP!
    Gets the hottest memes from r/HolUp. 
      Usage: 
      ```.holup```
    Note: Using the slash command will allow you to have a choice from the same command"""
    async with aiohttp.ClientSession() as e:
      async with e.get('https://meme-api.herokuapp.com/gimme/HolUp') as get_holup:
        holup = await get_holup.json()
    meme = discord.Embed(title=holup['title'], url=holup['postLink'], colour=discord.Color.random())
    meme.set_image(url=holup['url'])
    meme.set_footer(text=f"Powered by r/HolUp | Requested by {ctx.author}")
    await ctx.send(embed=meme, view = Meme(ctx))

  @commands.hybrid_command(name = 'meow')
  @commands.guild_only()
  async def cat(self, ctx):
    """Gives a cute cat picture :D
      Usage: 
        ```.cat```
    """  
    async with aiohttp.ClientSession() as e:
      async with e.get(f'https://api.thecatapi.com/v1/images/search?api_key={os.getenv("api-key")} as get_cat') as get_cat:
        meow = await get_cat.json()
        cat = discord.Embed(title = "Meow~", url = meow[0]["url"], colour=discord.Color.random())
        cat.set_image(url = meow[0]["url"])
        cat.set_footer(text=f"Powered by CatAPI | Requested by {ctx.author}")
        await ctx.send(embed=cat)
  
  @commands.hybrid_command(name = 'joke')
  @commands.guild_only()
  async def joke(self, ctx):
    """Gives you a funny joke.
      Usage: 
    ```.joke```
    """
    async with aiohttp.ClientSession() as e:
      async with e.get('https://v2.jokeapi.dev/joke/Any?type=twopart') as get_joke:
        joke = await get_joke.json()
        joke = discord.Embed(title = joke['setup'], color = discord.Color.random(), description=joke['delivery'])
        await ctx.send(embed=joke)

  @commands.hybrid_command(name = 'darkjoke')
  @commands.guild_only()
  async def darkjoke(self, ctx):
    """Gives you a dark joke 💀
     Usage: 
    ```.darkjoke```"""
    async with aiohttp.ClientSession() as e:
      async with e.get('https://v2.jokeapi.dev/joke/Dark?') as get_darkjoke:
        darkjoke = await get_darkjoke.json()
        djoke = discord.Embed(title = darkjoke['setup'], color = discord.Color.random(), description=darkjoke['delivery'])
        await ctx.send(embed=djoke)

  @commands.hybrid_command(name = 'activity')
  @commands.guild_only()
  async def activity(self, ctx):
    """Idek why I added this"""
    async with aiohttp.ClientSession() as e:
      async with e.get('http://www.boredapi.com/api/activity/') as get_activity:
        activity = await get_activity.json()
        activity = activity['activity']+"."+"\n"+"\n"+"Type: "+activity['type'].capitalize()
        await ctx.send(activity)



  @commands.hybrid_command(name = 'wordle')
  @commands.guild_only()
  async def wordle(self, ctx):
    """A wordle clone for you to play in discord. It has over 30k words!!! \n To play, reply to the embed with your guess.
    Usage: 
    ```.wordle```"""
    puzzle_id = random_puzzle_id()
    puzzle = generate_puzzle_embed(ctx.author, puzzle_id)
    await ctx.send(embed = puzzle)
  
  @commands.Cog.listener()
  async def on_message(self, message: discord.Message):
    """
    When a message is sent, process it as a guess.
    Then, process any commands in the message if it's not a guess.
    """
    ref = message.reference
    if not ref or not isinstance(ref.resolved, discord.Message):
        return False
    parent = ref.resolved

    # if the parent message is not the client's message, ignore it
    if parent.author.id != self.client.user.id:
        return False

    # check that the message has embeds
    if not parent.embeds or embed.title != "Wordle Clone":
        return False

    embed = parent.embeds[0]

    guess = message.content.lower()

    # check that the member is the one playing
    if embed.author.name == message.author.name:
      pass
    else:
        reply = "Start a new game with .play"
        if embed.author:
          reply = f"This game was started by {embed.author.name}. " + reply
        await message.reply(reply, delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # check that the game is not over
    if is_game_over(embed):
        await message.reply(
            "The game is already over. Start a new game with .play", delete_after=5
        )
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # check that a single word is in the message
    if len(message.content.split()) > 1:
        await message.reply(
            "Please respond with a single 5-letter word.", delete_after=5
        )
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # check that the word is valid
    if not is_valid_word(guess):
        await message.reply("That is not a valid word", delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # update the embed
    embed = update_embed(embed, guess)
    await parent.edit(embed=embed)

    # attempt to delete the message
    try:
        await message.delete()
    except Exception:
        pass

    return True
  
async def setup(client: commands.Bot) -> None:
  await client.add_cog(Fun(client))