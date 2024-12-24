import discord
from discord.ext import commands
import os

class QuestionBotCog(commands.Cog, name="QuestionBox"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channel_id: int = int(os.getenv('DISCORD_CHANNEL_ID'))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if str(message.channel.type) != 'private':
            return
        to_send_channel: discord.TextChannel = self.bot.get_channel(self.channel_id)
        if not to_send_channel:
            return await message.author.send('転送対象のテキストチャンネルが見つかりません。転送したいチャンネルで`/set`と送信してください。')
        text = message.content
        if text:
            # CSVに保存する処理
            await to_send_channel.send(text)
        for file_ in message.attachments:
            file_url = file_.url
            file_name = file_.filename
            # 添付ファイルを処理する部分
            async with aiohttp.ClientSession() as session:
                async with session.get(file_url) as resp:
                    if resp.status != 200:
                        return await to_send_channel.send('ファイルを取得できませんでした')
                    data = io.BytesIO(await resp.read())
                    await to_send_channel.send(file=discord.File(data, file_name))

    @commands.command(name='set')
    async def _set(self, ctx: commands.Context):
        "質問を転送するチャンネルを設定します"
        channel_id: int = ctx.channel.id
        self.channel_id = channel_id
        await ctx.send('メッセージを転送するチャンネルをこのチャンネルに変更しました')

def setup(bot: commands.Bot):
    return bot.add_cog(QuestionBotCog(bot))
