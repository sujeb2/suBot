# # = 주석 아니면 고쳐야하는거임 ㅇ
import discord, asyncio, os
import youtube_dl
import ffmpeg
from discord.ext import commands


game = discord.Game("test")
bot = commands.Bot(command_prefix='p', status=discord.Status.online, activity=game)

#bot logged in
@bot.event
async def on_ready():
    print('logged on:' + bot.user.display_name)

#commands start
@bot.command(aliases=['안녕', 'hi', '안녕하세요'])
async def hello(ctx):
    await ctx.send(f'{ctx.author.mention}님 안녕하세요.')

#need to fix
@bot.command(aliases=['주사위'])
async def roll(ctx, number:int = 6):
    await ctx.send(f'주사위에서 {random.randint(1,int(number))}이가 나왔습니다.')

@roll.error
async def roll(ctx,error):
    await ctx.send(f'{ctx.author.mention} 오류가 났습니다.')

@bot.command(aliases=['도움말', 'h'])
async def 도움(ctx):
    embed = discord.Embed(title="poskBot", description="설명", color=0x4432a8)
    embed.add_field(name="인사하기", value="phello", inline=False)
    embed.add_field(name="주사위", value="proll", inline=False)
    embed.add_field(name="음성채널 입장", value="pplay", inline=False)
    embed.add_field(name="노래 일시중지", value="ppause", inline=False)
    embed.add_field(name="음성채널 나가기", value="pleave", inline=False)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, number:int = 5):
    await ctx.message.delete()
    await ctx.channel.purge(limit=number)
    await ctx.send(f'{ctx.author.mention}님이 메세지를 삭제하였습니다.')

#music
@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.send("음성채널에 접속중")

@join.error
async def join(ctx,error):
    await ctx.send(f'{ctx.author.mention}님이 음성채널에 접속중이 아니야.') #when voice channel doesn't joined(?)

@bot.command()
async def leave(ctx):
    await bot.voice_clients[0].disconnect()
    await ctx.send("음성채널에서 나갔어.")

@leave.error
async def leave(ctx,error):
    await ctx.send(f'{ctx.author.mention} 이미 음성채널에서 나갔어.')

@bot.command()
async def pause(ctx):
    if not bot.voice_clients[0].is_paused():
        bot.voice_clients[0].pause()
    else:
        await ctx.send("이미 일시중지 됐어.")

@bot.command()
async def resume(ctx):
    if bot.voice_clients[0].is_paused():
        bot.voice_clients[0].resume()
    else:
       await ctx.send("이미 재시작 됐어.")

@bot.command()
async def stop(ctx):
    if bot.voice_clients[0].is_playing():
        bot.voice_clients[0].stop()
    else:
        await ctx.send("노래가 플레이중이 아니야.")

@bot.command()
async def play(ctx, url):
    channel = ctx.author.voice.channel
    if bot.voice_clients == []:
    	await channel.connect()
    	await ctx.send("해당 채널에 접속했어 -> " + str(bot.voice_clients[0].channel))

    ydl_opts = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
    voice = bot.voice_clients[0]
    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

@play.error
async def play(ctx,error):
    await ctx.send(f'URL 링크가 잘못되었거나, 다운로드에 오류가 났어.')

bot.run('tokenbtw')
