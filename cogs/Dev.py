import discord
from discord import app_commands
from discord.ext import commands
import traceback
import io
import textwrap
from contextlib import redirect_stdout
from typing import Any, Optional


class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self._last_result: Optional[Any] = None

    @commands.Cog.listener()
    async def on_ready(self):
        print('Dev.py is loaded.')

    async def is_owner(ctx):
        return ctx.author.id == 785763244890914847

    def cleanup_code(self, content: str) -> str:
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

            # remove `foo`
        return content.strip('` \n')

    @commands.command(name='eval', hidden = True)
    @commands.is_owner()
    async def _eval(self, ctx, *, body: str):
        """Evaluates a piece of code"""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result,
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
                else:
                    self._last_result = ret
                    await ctx.send(f'```py\n{value}{ret}\n```')

    @_eval.error
    async def error(self, ctx, error):
      if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("u suck lol")


async def setup(client: commands.Bot) -> None:
  await client.add_cog(Dev(client))      
