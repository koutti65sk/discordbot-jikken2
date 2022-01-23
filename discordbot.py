import discord
from discord.ext import commands
import os
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
    embed = discord.Embed(
        title = "DMを受け取りました。",color = 0x4682B4,url = message.jump_url,description = message.content
        )
    embed.set_author(
    name = bot.user,icon_url = bot.user.avatar_url
    )
    return embed

@bot.listen('on_message')
async def on_message_dm(message):
    if message.author.bot:
        return
    elif type(message.channel) == discord.DMChannel and bot.user == message.channel.me:
        channel = bot.get_channel(dmchannel)
        embeds = []
        embed = await set_embed(message)
        embeds.append(embed)
        if message.attachments and message.attachments[0].proxy_url:
            for attachment in message.attachments:
                embed = discord.Embed()
                embed.set_image(
                url=attachment.proxy_url
                )
                embeds.append(embed)
        await channel.send(embeds = embeds)
        return
    else:
        return

token = os.environ("DISCORD_BOT_TOKEN")
bot.run(token)
