from __future__ import annotations

import os
import re

from loguru import logger
from openai import AsyncOpenAI
from twitchio import Message
from twitchio.ext.commands import Bot
from twitchio.ext.commands import Cog as Module
from twitchio.ext.commands import command
from twitchio.ext.commands import Context

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL')

client = AsyncOpenAI(
    api_key=OPENAI_API_KEY,
)


async def _chat_completion(system_msg: str, user_msg: str | None):
    response = await client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {'role': 'system', 'content': system_msg},
            {'role': 'user', 'content': user_msg},
        ],
    )

    return response.choices[0].message.content


class ChatGPT(Module):
    def __init__(self, bot: Bot):
        self.bot = bot

    # async def cog_check(self, ctx: Context):
    #     return ctx.author.name in self.bot.owners

    @Module.event()
    async def event_message(self, message: Message) -> None:
        if message.echo:
            return

        ctx = await self.bot.get_context(message)
        if f'@{self.bot.nick}' in ctx.message.content.lower():
            system_msg = '''
                I want you to answer only in portuguese with 90 characters.
                '''
            user_input = str(ctx.message.content)
            user_msg = re.sub(f'@{self.bot.nick}', '', user_input)

            response = await _chat_completion(system_msg, user_msg)
            await ctx.reply(response)

        await self.bot.handle_commands(message)

    @command(name='tellme', aliases=['mediga', 'meconte'])
    async def _tellme(self, ctx: Context, *, user_input: str | None):
        system_msg = '''\
        I want you to answer only in portuguese with 90 characters.
        '''
        response = await _chat_completion(system_msg, user_input)
        await ctx.reply(response)

    @command(name='tellmetts', aliases=['medigatts', 'mecontetts'])
    async def _tellmetts(self, ctx: Context, *, user_input: str | None):
        system_msg = '''\
        I want you to answer only in portuguese with 90 characters.
        '''
        response = await _chat_completion(system_msg, user_input)
        await ctx.reply(response)

    @command(name='translate', aliases=['traduz', 'traduzir'])
    async def _translate(self, ctx: Context, *, text: str):
        system_msg = '''\
        You will act as a translator between portuguese and the language identified
        in the prompt. Whenever you receive a prompt in either language, you
        will translate the text into the opposite language and provide the
        translated output as your response. Please ensure that your response
        contains only the translated text. No additional descriptions or
        explanations, No tags or comments to indicate language direction. and
        no exceeding the maximum of 500 characters.
        '''
        response = await _chat_completion(system_msg, text)
        await ctx.reply(response)


def prepare(bot: Bot):
    bot.add_cog(ChatGPT(bot))
    logger.info('módulo [chatgpt] carregado com successo')
