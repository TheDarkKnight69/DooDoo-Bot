from discord.ext import commands
from help_structure import HelpCommand


class Help(commands.Cog, name = "Help"):
  """Stop it, get some help"""
  COG_EMOJI = "❓"
  def __init__(self, client):
    self._original_help_command = client.help_command
    client.help_command = HelpCommand()
    client.help_command.cog = self

  def cog_unload(self):
    self.client.help_command = self._original_help_command


async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Help(bot))