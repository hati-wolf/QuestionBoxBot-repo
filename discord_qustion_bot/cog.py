import discord
import os
from discord.ext import commands

class QuestionBoxCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        """ヘルプメッセージを表示します"""
        await ctx.send("質問箱Botのコマンドを表示します")

    @commands.Cog.listener()
    async def on_message(self, message):
        """メッセージを処理し、DMから指定されたチャンネルに送信します"""
        if message.author == self.bot.user:
            return

        if isinstance(message.channel, discord.DMChannel):
            # DMから送られたメッセージを指定チャンネルに送信
            channel = self.bot.get_channel(int(os.getenv('DISCORD_CHANNEL_ID')))
            if channel:
                await channel.send(f"匿名メッセージ: {message.content}")
            else:
                print("チャンネルが見つかりませんでした")

# 通常の同期関数に変更
def setup(bot):
    bot.add_cog(QuestionBoxCog(bot))
