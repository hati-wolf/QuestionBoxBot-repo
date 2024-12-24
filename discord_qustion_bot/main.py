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
    # GitHub Actionsの環境変数からトークンとチャンネルIDを取得
    TOKEN = os.getenv('DISCORD_TOKEN')
    CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

    if not TOKEN or not CHANNEL_ID:
        raise ValueError("DISCORD_TOKEN または DISCORD_CHANNEL_ID が設定されていません。")

    # 必要な intents を設定
    intents = discord.Intents.default()
    intents.messages = True  # メッセージイベントを受信できるように設定
    intents.message_content = True  # メッセージコンテンツにアクセスできるように設定

    prefix = '~'
    bot = Bot(
        command_prefix=prefix,
        help_command=UserHelp(),
        activity=discord.Game(name=f"send DM or {prefix}help"),
        intents=intents  # intentsを指定
    )

    # 通常通りに拡張機能を読み込み
    bot.load_extension('cog')
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
