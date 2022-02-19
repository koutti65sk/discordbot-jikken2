import discord
from discord.ext import commands
import os
import datetime

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
    channel = bot.get_channel(logchannel)
    await channel.send('login')
    return

@bot.event
async def on_message_delete(message):
    now = jst()
    embed = discord.Embed(title="メッセージ削除", color=discord.Color.red())
    embed.add_field(name="メッセージ", value=message.content, inline=False)
    embed.add_field(name="時刻", value=now.strftime('%Y /%m / %d　 %H : %M : %S'), inline=False)
    embed.add_field(name="チャンネル", value=message.channel.mention, inline=False)
    embed.set_footer(icon_url=message.author.avatar_url, text=message.author.display_name)
    channel = bot.get_channel(delchannel)
    await channel.send(embed=embed)
    return


token = os.environ["DISCORD_BOT_TOKEN"]
bot.run(token)
