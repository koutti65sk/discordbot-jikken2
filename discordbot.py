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

@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    return

@bot.listen('on_message')
async def on_message_dm(message):
    if message.author.bot:
        return
    elif type(message.channel) == discord.DMChannel and bot.user == message.channel.me:
        channels = bot.get_channel(dmchannel)
        contents = message.content
        await channels.send(contents)
        return
        
    else:
        return

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)