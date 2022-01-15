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

async def set_embed(message):
    embed = discord.Embed(title = "DMを受け取りました。",color = 0x4682B4,url = message.jump_url,timestamp=message.created_at
        )
    embed.set_author(name = bot.user,icon_url = bot.user.avatar_url
        )
    embed.add_field(name="匿名すこん部",value = message.content)
    if message.attachments and message.attachments[0].proxy_url:
        embed.set_image(
            url=message.attachments[0].proxy_url
        )
    return embed

@bot.listen('on_message')
async def on_message_dm(message):
    if message.author.bot:
        return
    elif type(message.channel) == discord.DMChannel and bot.user == message.channel.me:
        fin_message = []
        channels = bot.get_channel(dmchannel)
        if message.content or message.attachments:
            embeds = await set_embed(message)
            fin_message.append(embeds)
            for attachment in message.attachments[1:]:
                embed = discord.Embed()
                embed.set_image(
                url = attachment.proxy_url
                )
                fin_message.append(embed)
        for embed in message.embeds:
            fin_message.append(embed)
        await channels.send(embeds = fin_message)
        return
    else:
        return

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)