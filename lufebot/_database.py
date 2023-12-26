from __future__ import annotations

from peewee import Model
from playhouse.sqlite_ext import CharField
from playhouse.sqlite_ext import JSONField
from playhouse.sqlite_ext import SqliteExtDatabase

sqlite_db = SqliteExtDatabase(
    './lufebot.db',
    pragmas={
        'journal_mode': 'wal',
        'cache_size': -1024 * 64,
        'synchronous': 0,
    },
)


class BaseModel(Model):
    class Meta:
        database = sqlite_db


class DefaultCommand(BaseModel):
    class Meta:
        db_table = 'default_commands'

    channel = CharField(unique=True, null=False)
    commands = JSONField()


def get_default_command(channel: str, command: str):
    default_command = DefaultCommand.get_or_none(channel=channel)
    if default_command is None:
        raise ValueError()
    else:
        return default_command.commands.get(command, None)


def set_default_command(channel: str, command: str, value: bool):
    DefaultCommand.update(
        commands=DefaultCommand.commands.update({command: value}),
    ).where(DefaultCommand.channel == channel).execute()


sqlite_db.connect()
sqlite_db.create_tables([DefaultCommand])
