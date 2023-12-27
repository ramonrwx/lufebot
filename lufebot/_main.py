from __future__ import annotations

import os
from pathlib import Path

from loguru import logger
from twitchio import Message
from twitchio.ext.commands import Bot
from twitchio.ext.commands import Context
from twitchio.ext.commands.errors import ArgumentParsingFailed
from twitchio.ext.commands.errors import CheckFailure
from twitchio.ext.commands.errors import CommandNotFound
from twitchio.ext.commands.errors import MissingRequiredArgument

from lufebot._database import get_default_command

TWITCH_ACCESS_TOKEN = os.getenv('TWITCH_ACCESS_TOKEN')
TWITCH_INIT_CHANNELS = os.getenv('TWITCH_INIT_CHANNELS')
LUFEBOT_OWNERS = os.getenv('LUFEBOT_OWNERS')


class Lufe(Bot):
    def __init__(self):
        self.modules: list[str] = [
            module.stem for module in Path('./lufebot/modules').glob('*.py')
        ]
        self.token = TWITCH_ACCESS_TOKEN
        self.owners = [owner for owner in LUFEBOT_OWNERS.split(',')]

        super().__init__(
            token=TWITCH_ACCESS_TOKEN,
            prefix='!',
            initial_channels=[
                channel for channel in TWITCH_INIT_CHANNELS.split(',')
            ],
        )

    async def event_ready(self) -> None:
        logger.info(f'{self.nick} se conectou a twitch')

    async def event_command_error(self, ctx: Context, error: Exception) -> None:
        if isinstance(error, CommandNotFound):
            return

        elif isinstance(error, ArgumentParsingFailed):
            logger.error(error.message)

        elif isinstance(error, MissingRequiredArgument):
            logger.error(error)
            await ctx.reply(f'ops, está faltando o argumento: {error.name}')

        elif isinstance(error, CheckFailure):
            logger.error(error)
            await ctx.reply(
                'esse comando está desativado ou você não tem permissão para usar!',
            )

        else:
            logger.error(error)

    async def event_message(self, message: Message) -> None:
        if message.echo:
            return

        ctx = await self.get_context(message)

        commands = get_default_command(channel=ctx.channel.name)
        channel_disabled_cmds = [command for command, value in commands.items() if not value]

        bot_commands = self.commands.keys()
        private_cmds = ['coraleatoria', 'cor', 'ativar', 'desativar']
        cmds = [cmd for cmd in bot_commands if cmd not in private_cmds]

        logger.info(
            f'[{message.author.name}] em [{message.channel.name}]: {message.content}',
        )

        if message.content.startswith('!') \
                and ctx.command.name in cmds \
                and ctx.command.name in channel_disabled_cmds:
            return

        await self.handle_commands(message)

    def setup_modules(self) -> None:
        for module in self.modules:
            logger.info(f'carregando módulo [{module}]')
            self.load_module(f'lufebot.modules.{module}')

    def run(self) -> None:
        self.setup_modules()
        super().run()
