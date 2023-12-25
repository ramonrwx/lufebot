from __future__ import annotations

import os
from pathlib import Path

from loguru import logger
from twitchio import Message
from twitchio.ext.commands import Bot
from twitchio.ext.commands import Context

TWITCH_ACCESS_TOKEN = os.getenv('TWITCH_ACCESS_TOKEN')
TWITCH_INIT_CHANNELS = os.getenv('TWITCH_INIT_CHANNELS')


class Lufe(Bot):
    def __init__(self):
        self.modules: list[str] = [
            module.stem for module in Path('./lufebot/modules').glob('*.py')
        ]
        self.token = TWITCH_ACCESS_TOKEN
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
        logger.error(f'{ctx.channel.name} -> {error}')

    async def event_message(self, message: Message) -> None:
        if message.echo:
            return

        ctx = await self.get_context(message)
        logger.info(
            f'[{ctx.author.name}] em [{ctx.channel.name}]: {message.content}',
        )

        await self.handle_commands(message)

    def setup_modules(self) -> None:
        for module in self.modules:
            logger.info(f'carregando módulo [{module}]')
            self.load_module(f'lufebot.modules.{module}')

    def run(self) -> None:
        self.setup_modules()
        super().run()
