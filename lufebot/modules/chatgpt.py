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

from lufebot._database import get_default_command

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

    @Module.event()
    async def event_message(self, message: Message) -> None:
        if message.echo:
            return

        ctx = await self.bot.get_context(message)

        channel_commands = get_default_command(channel=ctx.channel.name)
        disabled_cmds = [
            cmd
            for cmd, enabled in channel_commands.items()
            if not enabled
        ]

        commands = [
            cmd
            for cmd in self.bot.commands.keys()
            if cmd not in self.bot.hidden_cmds
        ]

        if 'chatgpt' in commands and 'chatgpt' in disabled_cmds:
            return

        if f'@{self.bot.nick}' in ctx.message.content.lower():
            system_msg = '''
                I want you to answer only in portuguese with 90 characters.
                '''
            user_input = str(ctx.message.content)
            user_msg = re.sub(f'@{self.bot.nick}', '', user_input)

            response = await _chat_completion(system_msg, user_msg)
            await ctx.reply(response)

    @command(name='chatgpt')
    async def _chatgpt(self, ctx: Context):
        logger.debug('uma gambiarra')

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

    @command(name='traduzir', aliases=['translate', 'tradutor'])
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
    logger.success('módulo [chatgpt] carregado com successo')
