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


@bot.command()
async def hello(ctx):
    await ctx.send(f"hello {ctx.author.name}")

@bot.command()
async def ytp(ctx, *, search: str):

    if not ctx.author.voice:
        await ctx.send("please connect to an audio channel first")
        return

    voice_channel = ctx.author.voice.channel

    #connect to user's voice channel if not connect, or move channel if its not same
    if not ctx.voice_client:
        await voice_channel.connect()
    elif ctx.voice_client.channel != voice_channel:
        await ctx.voice_client.move_to(voice_channel)

    #stop if something is playing
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(search, download=False)

        if info is None:
            await ctx.send("could not fetch video")
            return


        url = info['url']
        title = info.get('title', 'unknown title')

    source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
    ctx.voice_client.play(source, after=lambda e: print(f"done: {e}"))
    await ctx.send(f"now playing **{title}**")


@bot.command()
async def yts(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("disconnected")


bot.run(os.getenv("TOKEN"))


