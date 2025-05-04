from types import coroutine
from dotenv import load_dotenv
import discord 
import os
from discord.ext import commands 
from yt_dlp import YoutubeDL
import asyncio 

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

queues = {}


YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': 'True',
    'quiet': True,
    'default_search': 'ytsearch',
    'extract_flat': 'in_playlist',
}

FFMPEG_OPTIONS = {
    'before_options' : '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options' : '-vn'
}

class Song:
    def __init__(self, url, title):
        self.url = url
        self.title = title

async def play_next(ctx):

    if ctx.guild.id not in queues or'queue' not in queues[ctx.guild.id]:
        await ctx.send("No queue found for this server.")
        return

    queue = queues[ctx.guild.id]['queue']
    if queue.empty():
        await ctx.send("queue is empty, leaving voice chat")
        await ctx.voice_client.disconnect()
        return

    song = await queue.get()
    source = discord.FFmpegPCMAudio(song.url, **FFMPEG_OPTIONS)

    def after_play(err):
        fut = asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop)
        try:
            fut.result()
        except Exception as e:
            print(f" Error playing song {e}")

    ctx.voice_client.play(source, after=after_play)
    await ctx.send(f"Now playing: {song.title}")


async def add_to_queue(ctx, search: str):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(search, download=False)
        if info is None:
            await ctx.send("could not find video")
            return

        url = info['url']
        title = info.get('title', 'unknown title')
        song = Song(url, title)
        await queues[ctx.guild.id]['queue'].put(song)
        await ctx.send(f"added to queue: **{song.title}**")


@bot.command()
async def hello(ctx):
    await ctx.send(f"hello {ctx.author.name}")

@bot.command()
async def ytp(ctx, *, search: str):

    if not ctx.author.voice:
        await ctx.send("please connect to an audio channel first")
        return

    voice_channel = ctx.author.voice.channel

    if ctx.guild.id not in queues:
        queues[ctx.guild.id] = {'queue': asyncio.Queue()}

    #connect to user's voice channel if not connect, or move channel if its not same
    if not ctx.voice_client:
        await voice_channel.connect()
    elif ctx.voice_client.channel != voice_channel:
        await ctx.voice_client.move_to(voice_channel)

    await add_to_queue(ctx, search)

    #play next if something is not playing
    if not ctx.voice_client.is_playing():
        await play_next(ctx)


@bot.command()
async def ytpause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("paused song")
    else:
        await ctx.send("nothing is playing")

@bot.command()
async def ytresume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("resumed song")
    else:
        await ctx.send("nothing is paused")

@bot.command()
async def ytskip(ctx):
    if ctx.voice_client and (ctx.voice_client.is_playing() or ctx.voice_client.is_paused()):
        ctx.voice_client.stop()
        await ctx.send("skipped song")
    else:
        await ctx.send("nothing to skip")

@bot.command()
async def ytqueue(ctx):
    if ctx.guild.id not in queues or 'queue' not in queues[ctx.guild.id]:
        await ctx.send("queue is empty")
        return

    items = list(queues[ctx.guild.id]['queue']._queue)
    msg = "\n".join([f"{idx+1}. {song.title}" for idx, song in enumerate(items)])
    await ctx.send(f"Queue:\n{msg}")

@bot.command()
async def ytremove(ctx, index: int):
    if ctx.guild.id not in queues or 'queue' not in queues[ctx.guild.id]:
        await ctx.send("queue is empty")
        return

    q = queues[ctx.guild.id]['queue']
    items = list(q._queue)

    if index < 1 or index > len(items):
        await ctx.send("invalid index")
        return

    removed = items.pop(index-1)
    new_q = asyncio.Queue()
    for song in items:
        await new_q.put(song)

    queues[ctx.guild.id]['queue'] = new_q
    await ctx.send(f"removed : **{removed.title}**")


@bot.command()
async def ythelp(ctx):
    embed = discord.Embed(
        title="Music Bot Commands",
        description="Here are the available commands:",
        color=discord.Color.blue()
    )

    embed.add_field(name="$ytp [song name or URL]", value="Play a song or add it to the queue.", inline=False)
    embed.add_field(name="$ytpause", value="Pause the currently playing song.", inline=False)
    embed.add_field(name="$ytresume", value="Resume a paused song.", inline=False)
    embed.add_field(name="$ytskip", value="Skip the current song.", inline=False)
    embed.add_field(name="$ytqueue", value="Show the current queue.", inline=False)
    embed.add_field(name="$ytremove [index]", value="Remove a song from the queue by index.", inline=False)
    embed.add_field(name="$yts", value="Stop and disconnect the bot from the voice channel.", inline=False)
    embed.add_field(name="$hello", value="Say hello to the bot.", inline=False)
    embed.add_field(name="$help", value="Show this help message.", inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def yts(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        queues.pop(ctx.guild.id, None)
        await ctx.send("disconnected")
    else:
        await ctx.send("bot is not connected.")


bot.run(os.getenv("TOKEN"))


