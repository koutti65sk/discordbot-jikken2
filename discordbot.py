import discord
from discord.ext import commands
from os import getenv
import traceback

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/',intents = intents)

errorchannel = 931445563654815776
logchannel = 928951765867585536
dmchannel = 931445891481624626


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    channel = bot.get_channel(errorchannel)
    await channel.send(error_msg)
    return


@bot.event
async def on_ready():
    channel = bot.get_channel(logchannel)
    await channel.send('login')
    return


@bot.listen('on_message')
async def on_message_dm(message):
    if message.author.bot:
        return
    elif type(message.channel) == discord.DMChannel and bot.user == message.channel.me:
        channels = bot.get_channel(dmchannel)
        image_url = [x.url for x in message.attachments]
        
        embed = discord.Embed(title = "DMを受け取りました。",color = 0x4682B4,url = message.jump_url
        )
        embed.set_author(name = bot.user,icon_url = bot.user.avatar_url
        )
        if not message.content:
            embed.add_field(name="匿名すこん部",value = "画像のみ")
        else:
            embed.add_field(name="匿名すこん部",value = message.content)
        embedimg.append(embed)
        for x in image_url:
            embed = discord.Embed()
            embed.set_image(
            url=x
            )
            embedimg.append(embed)
        await channels.send(embed = embed)
        return
    else:
        return


token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)