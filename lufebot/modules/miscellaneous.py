from __future__ import annotations

import time
from urllib import parse

import httpx
from loguru import logger
from twitchio.ext.commands import Bot
from twitchio.ext.commands import Cog as Module
from twitchio.ext.commands import command
from twitchio.ext.commands import Context


class Miscellaneous(Module):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def cog_check(self, ctx: Context):
        return ctx.author.name in self.bot.owners

    async def cog_command_error(self, ctx: Context, error: Exception):
        logger.error(error)
        await ctx.reply('você não tem permissão para usar esse comando!')

    @command(name='data', aliases=['date', 'dia', 'today'])
    async def date(self, ctx: Context):
        today = time.strftime('%d/%m/%Y')
        await ctx.reply(f'hoje é: {today}')

    @command(name='clima', aliases=['weather', 'tempo'])
    async def _weather(self, ctx: Context, *, local: str = 'Brasil'):
        local_encoded = parse.quote(local)
        url = f'https://wttr.in/{local_encoded}?format=4'

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                await ctx.send(response.text.strip())
            except httpx.HTTPStatusError:
                await ctx.reply('não foi possível saber o clima deste local.')


def prepare(bot: Bot):
    bot.add_cog(Miscellaneous(bot))
    logger.success('módulo [miscellaneous] carregado com successo')
