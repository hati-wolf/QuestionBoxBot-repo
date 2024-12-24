# main.py
import discord
import asyncio
import os
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


async def main():
    TOKEN = os.getenv('DISCORD_TOKEN')  # GitHub Secretsからトークンを取得
    CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))  # GitHub SecretsからチャンネルIDを取得

    if not TOKEN or not CHANNEL_ID:
        raise ValueError("DISCORD_TOKEN or DISCORD_CHANNEL_ID is not set in the environment variables")

    prefix = '~'
    intents = discord.Intents.default()  # 必要なインテントを設定
    bot = Bot(
        command_prefix=prefix,
        help_command=UserHelp(),
        activity=discord.Game(name=f"send DM or {prefix}help"),
        intents=intents  # インテントを指定
    )

    # 非同期で拡張機能をロード
    await bot.load_extension('discord_qustion_bot.cog')  # 修正箇所
    await bot.start(TOKEN)  # bot.run() の代わりに await bot.start() を使います


if __name__ == "__main__":
    asyncio.run(main())  # 非同期関数を実行
