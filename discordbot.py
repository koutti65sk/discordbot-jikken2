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

#2点間の距離を求める関数
def calc_distance(pos1, pos2):
    diff_x = pos1[0] - pos2[0]
    diff_y = pos1[1] - pos2[1]
    
    return math.sqrt(diff_x**2 + diff_y**2)

#位置決めの関数
def generate_position(size):
    x = random.randrange(0, size)
    y = random.randrange(0, size)
    return (x, y)

#プレイヤー移動の関数
def move_position(direction, pos):
    current_x, current_y = pos
    if direction == "n":
        current_y = current_y - 1
    elif direction == "s":
        current_y = current_y + 1
    elif direction == "w":
        current_x = current_x - 1
    elif direction == "e":
        current_x = current_x + 1
    return (current_x, current_y)

@bot.command()
async def suika_wari(ctx):
    BOARD_SIZE = 5  # ボードの初期サイズ
    suika_pos = await generate_position(BOARD_SIZE)
    player_pos = await generate_position(BOARD_SIZE)

    # スイカとプレイヤーの位置が異なる間、処理を繰り返す
    while (suika_pos != player_pos):
        # スイカとプレイヤーの距離を表示する
        distance = await calc_distance(suika_pos, player_pos)
        await ctx.send("スイカへの距離:", distance)

        # キー入力に応じて、プレイヤーを移動する
        c = await(input("n:北に移動 s:南に移動 e:東に移動 w:西に移動"))
        player_pos = await move_position(c, player_pos)
    await ctx.send('スイカを割りました！')



token = os.environ["DISCORD_BOT_TOKEN"]
bot.run(token)
