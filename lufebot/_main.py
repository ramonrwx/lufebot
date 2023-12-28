from __future__ import annotations

import os
import sys
from pathlib import Path

from loguru import logger
from twitchio import Message
from twitchio.ext.commands import Bot
from twitchio.ext.commands import Context
from twitchio.ext.commands.errors import ArgumentParsingFailed
from twitchio.ext.commands.errors import CheckFailure
from twitchio.ext.commands.errors import CommandNotFound
from twitchio.ext.commands.errors import MissingRequiredArgument

from lufebot._database import DefaultCommand
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
        self.hidden_cmds = ['ativar', 'desativar', 'cor', 'coraleatoria']
        init_channels = [channel for channel in TWITCH_INIT_CHANNELS.split(',')]

        super().__init__(
            token=TWITCH_ACCESS_TOKEN,
            prefix='!',
            initial_channels=init_channels,
        )

        for channel in init_channels:
            try:
                DefaultCommand.get_or_create(channel=channel, commands={})
            except Exception:
                continue

    async def event_ready(self) -> None:
        logger.success(f'{self.nick} se conectou a twitch')

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

        channel_commands = get_default_command(channel=ctx.channel.name)
        disabled_cmds = [
            cmd
            for cmd, enabled in channel_commands.items()
            if not enabled
        ]

        commands = [
            cmd
            for cmd in self.commands.keys()
            if cmd not in self.hidden_cmds
        ]

        logger.info(
            f'[{message.author.name}] em [{message.channel.name}]: {message.content}',
        )

        if message.content.startswith('!') \
                and ctx.command.name in commands  \
                and ctx.command.name in disabled_cmds:
            return

        await self.handle_commands(message)

    def setup_modules(self) -> None:
        for module in self.modules:
            self.load_module(f'lufebot.modules.{module}')

    def run(self) -> None:
        log_format = '<green>{time:YYYY-MM-DD HH:mm:ss} </green> | <level>{level: <2}</level> | <level>{message}</level>'
        logger.remove()
        logger.add(sys.stdout, format=log_format)
        self.setup_modules()
        super().run()
