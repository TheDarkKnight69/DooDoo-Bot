import discord
from discord import app_commands
from discord.ext import commands
import datetime
import asyncio
import re 
import sys
import traceback



time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600, "s":1, "m":60, "d":86400}

class TimeConverter(commands.Converter):
  async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k]*float(v)
            except KeyError:
                raise commands.BadArgument("{} is an invalid time-key! h/m/s/d are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time




class Moderation(commands.Cog):
  """Contains all the moderation flex commands.""" 
  COG_EMOJI = "<:moderator:994972019856769074>"
  def __init__(self, bot):
    self.bot: commands.Bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
        print('Moderation.py is loaded.')


  
  @commands.hybrid_command()
  @commands.guild_only()
  @commands.has_guild_permissions(manage_messages = True)
  async def purge(self, ctx, amount: int):
    """Delete a number of messages"""
    await ctx.channel.purge(limit=amount)

  @commands.hybrid_command()
  @commands.guild_only()
  @commands.has_guild_permissions(kick_members = True)
  async def kick(self, ctx, member: discord.Member, *, reason=None):
    """Yeet a member"""
    await member.kick(reason=reason)
    await ctx.send(f"{member} was successfully kicked! \n\nReason: {reason}")

  @commands.hybrid_command()
  @commands.guild_only()
  @commands.has_guild_permissions(ban_members = True)
  async def ban(self, ctx, member: discord.Member, *, reason=None):
    """Use the ban hammer"""
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} was successfully banned! \n\nReason: {reason}")
    
  @commands.hybrid_command()
  @commands.guild_only()
  @commands.has_guild_permissions(ban_members = True)
  async def unban(self, ctx, *, member):
    """Retract Ban Hammer"""
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
      user = ban_entry.user

    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send(f'Successfully unbanned {user.mention}')
      return

  @purge.error
  async def clear_error(self, ctx, error):
      if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify the amount of messages to delete.")


  @commands.hybrid_command(aliases = ['cr', 'makerole', 'crole'])
  @commands.guild_only()
  @commands.has_guild_permissions(manage_roles = True)
  async def createrole(self, ctx, name , color):
    """ This command creates a role. 
    Only takes hex codes. go to https://g.co/kgs/NuRqog to get hex codes. 
    Permissions are not yet implemented and neither is positioning."""
    
    guild = ctx.guild
    color = color
    color = color[1:] # removing the initial `#`
    color = int(color, 16) # pass this as the colour kwarg
    await guild.create_role(name = name, color = discord.Colour(color)) 
    createrole = discord.Embed(title = "Role Created", description = f"{name} created successfully with basic permissions. Please edit it further if you want", color = discord.Color.random(), timestamp = datetime.datetime.utcnow())
    await ctx.send(embed = createrole)

  @commands.Cog.listener()
  async def on_message(self, message):
    badwords = ['fuck']
    if message.content in badwords:
      await message.channel.send(embed = discord.Embed(title = "Language", description = "Mind your language you little fuck", timestamp = datetime.datetime.utcnow()), delete_after=15)
      await message.delete(delay = 15)
    else: 
      return


  @commands.hybrid_command()
  @commands.guild_only()
  @commands.has_guild_permissions(manage_roles=True)
  async def mute(self, ctx, member : discord.Member, *, time : TimeConverter = None):
        """Mutes a member for the specified time- time in 2d 10h 3m 2s format
        Usage:
        ```.mute {member} {time}```"""
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        guild = ctx.guild
        if not role:
          mutedRole = await guild.create_role(name="Muted", color = discord.Color.red)
          for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)
        if member.top_role.position > ctx.author.top_role.position:
          await ctx.send("You cannot mute this person, they're more cool.")
          return
        elif member.top_role.position > ctx.guild.me.top_role.position:
          await ctx.send("I cannot mute this person, they're too cool.")
          return
        elif member == ctx.author:
          await ctx.send("You cannot mute yourself.")
        elif role in member.roles:
          await ctx.send("They're already muted, chill out.")
        elif member != ctx.author:
          await member.add_roles(role)
          await ctx.send(("Muted {} for {}s" if time else "Muted {} indefinetly").format(member, time))
          await asyncio.sleep(time)
          await member.remove_roles(role)
        elif member == self.bot:
          await ctx.send("r u mad")
        
        

  @commands.hybrid_command()
  @commands.guild_only()
  @commands.has_guild_permissions(manage_roles = True)
  async def unmute(self, ctx, member: discord.Member):
    """Unmutes a person."""
    role = discord.utils.get(ctx.guild.roles, name = "Muted")
    if role in member.roles:
      await member.remove_roles(role)
      unmute = discord.Embed(title = "Member Unmuted", description = f"{ctx.author.mention} has unmuted {member.mention}.", color = ctx.author.color, timestamp = datetime.datetime.utcnow())
      await ctx.send(embed = unmute)
    elif role not in member.roles:
      unmutefail = discord.Embed(title = "Unmute failed", description = f"I could not unmute {member.mention}. The member is not muted.", color = ctx.author.color, timestamp = datetime.datetime.utcnow())
      unmutefail.set_footer(text = "Did you mean `.mute`?")
      await ctx.send(embed = unmutefail)

  @unmute.error
  async def unmute_error(self, ctx, error):
    member = discord.Member
    if isinstance(error, commands.MissingPermissions):
      unmutefailperm = discord.Embed(title = "Unmute failed", description = f"I could not unmute {member.mention}. You lack required permissions", color = ctx.author.color, timestamp = datetime.datetime.utcnow())
      await ctx.send(embed = unmutefailperm)
        

   
  
  
  
  

  
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Moderation(bot))



