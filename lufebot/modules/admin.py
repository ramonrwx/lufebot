from __future__ import annotations

from loguru import logger
from twitchio.ext.commands import Bot
from twitchio.ext.commands import Cog as Module
from twitchio.ext.commands import command
from twitchio.ext.commands import Context

from lufebot._database import set_default_command


class Admin(Module):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def cog_check(self, ctx: Context):
        return ctx.author.is_mod or ctx.author.name in self.bot.owners

    @command(name='ativar', aliases=['enable', 'ligar'])
    async def _enable(self, ctx: Context, command: str | None):
        commands = self.bot.commands.keys()
        private_cmds = ['coraleatoria', 'cor', 'ativar', 'desativar']
        cmds = [cmd for cmd in commands if cmd not in private_cmds]

        if command is None:
            await ctx.send(f'comandos disponivéis para ativar: {", ".join(cmds)}')
        elif command in cmds:
            set_default_command(ctx.channel.name, command, True)
            await ctx.reply(f'comando {command} foi ativado no canal!')

    @command(name='desativar', aliases=['disable', 'desligar'])
    async def _disable(self, ctx: Context, command: str | None):
        commands = self.bot.commands.keys()
        private_cmds = ['coraleatoria', 'cor', 'ativar', 'desativar']
        cmds = [cmd for cmd in commands if cmd not in private_cmds]

        if command is None:
            await ctx.send(f'comandos disponivéis para desativar: {", ".join(cmds)}')
        elif command in cmds:
            set_default_command(ctx.channel.name, command, False)
            await ctx.reply(f'comando {command} foi desativado no canal!')


def prepare(bot: Bot):
    bot.add_cog(Admin(bot))
    logger.info('módulo [admin] carregado com successo')
