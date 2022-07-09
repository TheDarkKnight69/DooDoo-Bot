from discord.ext import commands
import discord
from typing import Optional, Set

import discord
from discord.ext import commands
from typing import Optional, Set, List


class HelpDropdown(discord.ui.Select):
  def __init__(self, help_command: "HelpCommand", options: List[discord.SelectOption]):
    super().__init__(placeholder = "Choose a category...", min_values = 1, max_values = 1, options = options)
    self._help_command = help_command

  async def callback(self, interaction: discord.Interaction):
    embed = (
      await self._help_command.cog_help_embed(self._help_command.context.bot.get_cog(self.values[0]))
      if self.values[0] != self.options[0].value
      else await self._help_command.bot_help_embed(self._help_command.get_bot_mapping())
    )
    await interaction.response.edit_message(embed = embed)




class HelpView(discord.ui.View):
  def __init__(self, help_command: "HelpCommand", options: List[discord.SelectOption], *, timeout: Optional[float] = 120):
    super().__init__(timeout=timeout)
    self.add_item(HelpDropdown(help_command, options))
    self._help_command = help_command
  async def on_timeout(self) -> None:
    self.clear_items()
    await self._help_command.response.edit(view = self)
  async def interaction_check(self, interaction: discord.Interaction) -> bool:
    return self._help_command.context.author == interaction.user


class HelpCommand(commands.MinimalHelpCommand):
  def get_command_signature(self, command):
    return f"{self.context.clean_prefix}{command.qualified_name} {command.signature}"
  async def _cog_select_options(self) -> List[discord.SelectOption]:
    options: List[discord.SelectOption] = []
    options.append(discord.SelectOption(
      label = "Home",
      emoji = "🏠",
      description = "Go Back to the Main Menu",
    ))
    for cog, command_set in self.get_bot_mapping().items():
      filtered = await self.filter_commands(command_set, sort = True)
      if not filtered:
        continue
      emoji = getattr(cog, "COG_EMOJI", None)
      options.append(discord.SelectOption(
        label = cog.qualified_name if cog else "No Category",
        emoji = emoji,
        description = cog.description[:100] if cog and cog.description else None
      ))
    return options 

  async def _help_embed(
    self, title: str, description: Optional[str] = None, mapping: Optional[dict] = None,
    command_set: Optional[Set[commands.Command]] = None
  ) -> discord.Embed:
    embed = discord.Embed(title = title)
    if description:
      embed.description = description
    avatar = self.context.bot.user.avatar 
    embed.set_author(name = self.context.bot.user.name, icon_url = avatar)
    footicon = self.context.author.avatar
    embed.set_footer(text = f"Invoked by {self.context.author}", icon_url = footicon)
    if command_set:
      #show help about all commands in set
      filtered = await self.filter_commands(command_set, sort = True)
      for command in filtered:
        embed.add_field(
          name = self.get_command_signature(command),
          value = command.short_doc or '**....**',
          inline = False
        )
    elif mapping:
      #add a short description of commands in each cog
      for cog, command_set in mapping.items():
        filtered = await self.filter_commands(command_set, sort = True)
        if not filtered:
          continue
        name = cog.qualified_name if cog else "No category"
        emoji = getattr(cog, "COG_EMOJI", None)
        cog_label = f"{emoji} {name}" if emoji else None
        cmd_list = " ".join(
          f"`{self.context.clean_prefix}{cmd.name}`" for cmd in filtered
        )
        value = (
          f"{cog.description}\n{cmd_list}"
          if cog and cog.description
          else cmd_list
        )
        embed.add_field(name = name, value = value)

          
        
        
    return embed
    
  async def send_bot_help(self, mapping: dict):
    embed = await self.bot_help_embed(mapping)
    options = await self._cog_select_options()
    self.response = await self.get_destination().send(embed = embed, view = HelpView(self, options))

  async def send_command_help(self, command: commands.Command):
    emoji = getattr(command.cog, "COG_EMOJI", None)
    embed = await self._help_embed(
      title = f"{emoji} {command.qualified_name.capitalize()}" if emoji else command.qualified_name.capitalize(),
      description = command.help,
      command_set = command.commands if isinstance(command, commands.Group) else None
    )
    await self.get_destination().send(embed = embed)

  async def bot_help_embed(self, mapping: dict) -> discord.Embed:
    return await self._help_embed(
      title = "Bot Commands",
      description = self.context.bot.description,
      mapping = mapping,
    
    )

  async def cog_help_embed(self, cog: commands.Cog) -> discord.Embed:
    emoji = getattr(cog, "COG_EMOJI", None)
    return await self._help_embed(
      title = f"{emoji} {cog.qualified_name.capitalize()}" if emoji else {cog.qualified_name.capitalize()} ,
      description = cog.description,
      command_set = cog.get_commands()
    )
    
  async def send_cog_help(self, cog: commands.Cog):
    embed = await self.cog_help_embed(cog)
    await self.get_destination().send(embed = embed)

  send_group_help = send_command_help