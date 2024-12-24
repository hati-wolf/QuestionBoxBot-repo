import json
import os
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


def main():
    # GitHub Secrets から Discord Token を取得
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        raise ValueError("DISCORD_TOKEN is not set in the environment variables")

    # GitHub Secrets から Channel ID を取得
    CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")
    if not CHANNEL_ID:
        raise ValueError("DISCORD_CHANNEL_ID is not set in the environment variables")

    # Bot の設定
    prefix = '~'
    bot = Bot(
        command_prefix=prefix,
        help_command=UserHelp(),
        activity=discord.Game(name=f"send DM or {prefix}help")
    )

    # Cog (質問ボット) をロード
    bot.load_extension('cog')

    # Bot を起動
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
