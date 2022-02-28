import discord
from discord.ext import commands
import os
import datetime
import math
import random

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='//',intents = intents)

logchannel = 944578561413619712
delchannel = 944579014054514748

def jst():
    now = datetime.datetime.utcnow()
    now = now + datetime.timedelta(hours=9)
    return now

@bot.event
async def on_ready():
    now = jst()
    channel = bot.get_channel(logchannel)
    await channel.send(f'ログインしたよ。\n時刻({now: %y / %m / %d  %H : %M : %S})')
    return

@bot.event
async def on_message_delete(message):
    now = jst()
    if message.author.bot:
        return
    embed = discord.Embed(title="メッセージ削除ログ", color=discord.Color.red())
    if message.content:
        embed.add_field(name="メッセージ内容", value=message.content, inline=False)
    else:
        embed.add_field(name="メッセージ内容", value='コンテンツなし', inline=False)
    if message.attachments:
        embed.add_field(name="ファイルの有無", value=message.attachments, inline=False)
    else:
        embed.add_field(name="ファイルの有無", value='ファイルなし', inline=False)
    embed.add_field(name="時刻", value=now.strftime('%y / %m / %d  %H : %M : %S'), inline=False)
    embed.add_field(name="チャンネル", value=message.channel.mention, inline=False)
    embed.set_footer(icon_url=message.author.avatar_url, text=message.author.display_name)
    channel = bot.get_channel(delchannel)
    await channel.send(embed=embed)
    return

token = os.environ["DISCORD_BOT_TOKEN"]
bot.run(token)
