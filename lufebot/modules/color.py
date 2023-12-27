from __future__ import annotations

import random

from loguru import logger
from twitchio.ext.commands import Bot
from twitchio.ext.commands import Cog as Module
from twitchio.ext.commands import command
from twitchio.ext.commands import Context

TWITCH_COLORS = {
    'Blue': 'blue', 'BlueViolet': 'blue_violet',
    'CadetBlue': 'cadet_blue', 'Chocolate': 'chocolate',
    'Coral': 'coral', 'DodgerBlue': 'dodger_blue',
    'Firebrick': 'firebrick', 'GoldenRod': 'golden_rod',
    'Green': 'green', 'HotPink': 'hot_pink',
    'OrangeRed': 'orange_red', 'Red': 'red',
    'SeaGreen': 'sea_green', 'SpringGreen': 'spring_green',
    'YellowGreen': 'yellow_green',
}


def _get_random_color():
    random_value = random.choice(list(TWITCH_COLORS.values()))
    return random_value


class Color(Module):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def cog_check(self, ctx: Context):
        return ctx.author.name in self.bot.owners

    @command(name='cor', aliases=['color'])
    async def _color(self, ctx: Context, color: str | None):
        if color is None or color not in TWITCH_COLORS:
            await ctx.send(
                f'cores disponíveis: {", ".join(TWITCH_COLORS.keys())}',
            )
        else:
            await self.bot.update_chatter_color(
                token=self.bot.token,
                user_id=self.bot.user_id,
                color=TWITCH_COLORS.get(color),
            )
            await ctx.reply(f'cor alterada para: {color}')

    @command(
        name='coraleatoria',
        aliases=['rngcolor', 'rngcor', 'rngc', 'randcolor', 'randomcolor'],
    )
    async def _rand_color(self, ctx: Context):
        color = _get_random_color()

        await self.bot.update_chatter_color(
            token=self.bot.token,
            user_id=self.bot.user_id,
            color=color,
        )
        await ctx.reply(f'cor alterada para: {color}')


def prepare(bot: Bot):
    bot.add_cog(Color(bot))
    logger.success('módulo [color] carregado com successo')
