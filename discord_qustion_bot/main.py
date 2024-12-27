import io
import json
import csv
import os
import asyncio
import logging

import aiohttp
from pathlib import Path
import configparser
from datetime import datetime  # 現在時刻を取得するためにインポート

import discord
from discord.ext import commands
from discord.ext.commands import Bot


class UserHelp(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()
        self.commands_heading = 'コマンド: '
        self.no_category = 'other'
        self.command_attrs['help'] = 'コマンド一覧と簡単な説明を表示'

    def command_not_found(self, string: str):
        return f'{string} というコマンドは見つかりませんでした'

    def get_ending_note(self):
        return (
            "質問箱Bot\n",
            "BotのDMにメッセージや画像を送ると、指定されたチャンネルに匿名化されて送信されます。"
        )


async def periodic_log():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    while True:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 現在時刻をフォーマット
        logger.info(f"Bot is still running... Current time: {current_time}")
        await asyncio.sleep(300)  # 5分ごとにログを出力


async def main():
    TOKEN = os.getenv("DISCORD_TOKEN")
    prefix = '~'

    intents = discord.Intents.default()
    intents.messages = True  # 必要なインテントを有効化

    bot = Bot(
        command_prefix=prefix,
        help_command=UserHelp(),
        activity=discord.Game(name=f"send DM or {prefix}help"),
        intents=intents,
    )

    await bot.load_extension('cog')  # 非同期で拡張をロード

    asyncio.create_task(periodic_log())  # ログタスクを実行
    await bot.start(TOKEN)  # Botを開始


if __name__ == "__main__":
    asyncio.run(main())
