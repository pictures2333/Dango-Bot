import json
from turtle import textinput
def loadset(ggid):
        if ggid == 0:
            with open('settings.json', 'r', encoding = 'utf-8') as f:
                d1 = json.load(f)
        else:
            with open(f'settings/{str(ggid)}.json', 'r', encoding = 'utf-8') as f:
                d1 = json.load(f)
        return d1
def writeset(ggid, ddd1:dict):
    dumpdata = json.dumps(ddd1, ensure_ascii = False)
    with open(f'settings/{str(ggid)}.json', 'w', encoding = 'utf-8') as f:
        f.write(dumpdata)
def gain_money(gid:int):
    if os.path.exists(f'settings/{str(gid)}.json'):
        try:
            wt12 = loadset(gid)
            wt12['guildmon'] += 1
            writeset(gid, wt12)
        except:
            pass
def loadlang(pack:str):
    with open(f'lang/{pack}', 'r', encoding = 'utf-8') as f:
        d1 = json.load(f)
    return d1

with open('settings.json', 'r', encoding = 'utf-8') as f:
    botsetting = json.load(f)

from collections import Counter
import youtube_dl, shutil
import discord, requests, random, os, glob, asyncio, urllib, re, ooxx
from discord.ext import commands, tasks
from discord.ui import Button, View, Select
from datetime import datetime, timezone, timedelta
from time import sleep
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio
from discord.utils import get
import gettime

timezonenames = {-12:"國際換日線",
-11:"美屬薩摩亞標準時間",
-10:"夏威夷-阿留申標準時間",
-9.5:"馬克薩斯群島標準時間",
-9:"阿拉斯加標準時間",
-8:"太平洋標準時間",
-7:"北美山區標準時間",
-6:"北美中部標準時間",
-5:"北美東部標準時間",
-4:"大西洋標準時間",
-3.5:"紐芬蘭島標準時間",
-3:"巴西利亞標準時間",
-2:"費爾南多·迪諾羅尼亞群島標準時間",
-1:"維德角標準時間",
0:"歐洲西部時區，GMT - 格林威治標準時間",
1:"歐洲中部時區",
2:"歐洲東部時區",
3:"莫斯科時區",
3.5:"伊朗標準時間",
4:"海灣標準時間",
4.5:"阿富汗標準時間",
5:"巴基斯坦標準時間",
5.5:"印度標準時間",
5.75:"尼泊爾標準時間",
6:"孟加拉標準時間",
6.5:"緬甸標準時間",
7:"中南半島標準時間",
8:"台灣時間",
9:"日本標準時間",
9.5:"澳洲中部標準時間",
10:"澳洲東部標準時間",
10.5:"豪勳爵群島標準時間",
11:"萬那杜標準時間",
12:"紐西蘭標準時間",
12.45:"查塔姆群島標準時間",
13:"菲尼克斯群島標準時間",
14:"萊恩群島標準時間"}

price = {
    "小麥":10,
    "馬鈴薯":10,
    "胡蘿蔔":10,
    "煤炭":5,
    "鐵礦":10, 
    "黃金":20,
    "鑽石":50,
    "鋁礦":15,
    "山豬肉":10,
    "鹿肉":10,
    "牛肉":10,
    "蟒蛇肉":10,
}

api_key = botsetting['googleapi']
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = botsetting['prefix'], intents = intents, help_command=None)
@bot.event
async def on_ready():
    print('[main1]Bot is ready and online')
    print('[main1]>>Bot is ONLINE<<')
    await asyncio.sleep(1)
    
    thechannel = bot.get_channel(botsetting['restartlog'])
    botguilds = bot.guilds
    gettime.gettime(8, '%Y/%m/%d %H:%M:%S')
    with open('time.txt', 'r', encoding = 'utf-8') as f:
        content1 = f.readlines()
        zoned_time1 = content1[0]
    embed=discord.Embed(title="伺服器重啟日誌", color=0x00bfff)
    embed.add_field(name="伺服器重啟時間", value=f"Asia/Taipei UTC/GMT+8 {zoned_time1}", inline=False)
    embed.add_field(name="伺服器載入分流數量", value="3", inline=False)
    embed.add_field(name="使用團子機器人的伺服器數量", value=f"{str(len(botguilds))}", inline=False)
    embed.set_footer(text=f'愛吃團子的機器人|{botsetting["version"]}')
    await thechannel.send(embed=embed)

    while True:
        game = discord.Game(f'>>help|{botsetting["version"]}')
        await bot.change_presence(status=discord.Status.online, activity=game)

@bot.event
async def on_guild_join(guild):
    gid = guild.id
    gname = str(guild)
    if not os.path.exists(f'settings/{int(gid)}.json'):
        wd1 = {"otz":[], "tickets":[], "ticketnum":0, "leave":{}, "welcome":{}, "rolerrbl":[], "rrbl":[], "rr":[], "tvc":[], "lang":"zh-tw.json", "timearea":"None","guildmon":100, "botexp":0,"channelid": 0, "ytchannelid":[]}
        dumpdata3 = json.dumps(wd1)
        with open(f'settings/{str(gid)}.json', 'w', encoding = 'utf-8') as f:
            f.write(dumpdata3)

@bot.command()
async def fbk(ctx):
    await ctx.send('https://tenor.com/view/shirakami-fubuki-hololive-yabe-vtuber-gif-19227770')

@bot.command()
async def resetup(ctx):
    gid = ctx.guild.id
    try:
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
    except:
        langpack = loadlang('zh-tw.json')
    au = ctx.author
    roles = au.roles
    isa = 0
    for a in roles:
        for c in a.permissions:
            if c[0] == 'administrator' and c[1] == True:
                isa = 1
    if isa == 1:
        try:
            gname  = str(ctx.guild)
            wd1 = {"otz":[], "tickets":[], "ticketnum":0, "leave":{}, "welcome":{}, "rolerrbl":[], "rrbl":[],"rr":[], "tvc":[], "lang":"zh-tw.json", "timearea":"None","guildmon":0, "botexp":0,"channelid": 0, "ytchannelid":[]}
            dumpdata3 = json.dumps(wd1)
            with open(f'settings/{str(gid)}.json', 'w', encoding = 'utf-8') as f:
                f.write(dumpdata3)
            embed=discord.Embed(title=langpack["resetup.success"], color=0xee2f9f)
            embed.add_field(name=langpack["desetup.success.name"], value=f"{gname}", inline=True)
            embed.add_field(name=langpack["desetup.success.id"], value=f"{str(gid)}", inline=True)
            await ctx.send(embed=embed)
        except:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="ERROR!", value=langpack["err.message"], inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name=langpack['resetup.notadmin.title'], value=langpack["notadmin.msg"], inline=True)
        await ctx.send(embed=embed)

@bot.command()
async def addytchannel(ctx, chid:str):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        gid = ctx.guild.id
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
        
        try:
            au = ctx.author
            roles = au.roles
            isa = 0
            for a in roles:
                for c in a.permissions:
                    if c[0] == 'administrator' and c[1] == True:
                        isa = 1
            if isa == 1:
                gid = ctx.guild.id
                wt41 = loadset(gid)

                result3 = requests.get('https://www.googleapis.com/youtube/v3/channels?part=snippet&id={}&key={}'.format(chid, api_key))
                data3 = result3.json()
                chname = data3["items"][0]["snippet"]["title"]

                wt41['ytchannelid'].append(chid)
                writeset(gid, wt41)
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name=langpack["addytchannel.success.title"], value=f"頻道名稱:{chname}({chid})", inline=False)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name=langpack["addytchannel.notadmin.title"], value=langpack['notadmin.msg'], inline=True)
                await ctx.send(embed=embed)
        except:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="ERROR!", value=langpack["err.message"], inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)

@bot.group()
async def guildinfo(ctx):
    gid = ctx.guild.id
    try:
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
    except:
        langpack = loadlang('zh-tw.json')
    try:
        gain_money(gid)
    except:
        pass
    owner = bot.get_user(ctx.guild.owner_id)
    embed=discord.Embed(title=str(ctx.guild), description=f"id:{str(ctx.guild.id)}", color=0xee4f9e)
    embed.set_thumbnail(url=ctx.guild.icon)
    embed.add_field(name=langpack['guildinfo.member'], value=len(ctx.guild.members), inline=True)
    embed.add_field(name=langpack["guildinfo.channel"], value=len(ctx.guild.channels), inline=True)
    embed.add_field(name = '伺服器擁有者', value = f'{str(owner)}({str(owner.id)})', inline = True)
    embed.add_field(name = '伺服器橫幅', value = f'{str(ctx.guild.banner)}', inline = True)
    embed.add_field(name = '身分組數量', value = f'{str(len(ctx.guild.roles))}', inline = True)
    embed.add_field(name = '創建時間', value = f"{str((ctx.guild.created_at).strftime('%Y/%m/%d %H:%M:%S'))} UTC+0", inline = True)
    await ctx.send(embed = embed)
@guildinfo.command()
async def detail(ctx):
    text = f"""Information of {str(ctx.guild)}
AFK Channel:{str(ctx.guild.afk_channel)}
AFK Timeout:{str(ctx.guild.afk_channel)}
伺服器成員上限:{str(ctx.guild.max_members)}
伺服器存在上限:{str(ctx.guild.max_presences)}
伺服器視訊人數上限:{str(ctx.guild.max_video_channel_users)}
伺服器表情符號數量:{str(len(ctx.guild.emojis))}
伺服器敘述:{str(ctx.guild.description)}
mfa等級:{str(ctx.guild.mfa_level)}
驗證等級:{str(ctx.guild.verification_level)}
訊息內容過濾器:{str(ctx.guild.explicit_content_filter)}
伺服器通知設定:{str(ctx.guild.default_notifications)}
加成等級:{str(ctx.guild.premium_tier)}
加成次數:{str(ctx.guild.premium_subscription_count)}
首選語言環境:{str(ctx.guild.preferred_locale)}
大型伺服器:{str(ctx.guild.preferred_locale)}
語音頻道數量:{str(len(ctx.guild.voice_channels))}
舞台頻道數量:{str(len(ctx.guild.stage_channels))}
文字頻道數量:{str(len(ctx.guild.text_channels))}
類別數量:{str(len(ctx.guild.categories))}
系統訊息頻道:{str(ctx.guild.system_channel)}
規則頻道:{str(ctx.guild.rules_channel)}
Discord系統訊息頻道:{str(ctx.guild.public_updates_channel)}
表情符號數量限制:{str(ctx.guild.emoji_limit)}
語音頻道音訊品質限制:{str(ctx.guild.bitrate_limit)}
檔案大小限制:{str(ctx.guild.filesize_limit)}
chunked:{str(ctx.guild.chunked)}"""
            
    with open('guildinfo.txt', 'w', encoding = 'utf8') as f:
        f.write(text)
    file = discord.File('guildinfo.txt')
    await ctx.send(file = file)
    os.remove('guildinfo.txt')
@bot.command()
async def yourinfo(ctx):
    gid = ctx.guild.id
    try:
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
    except:
        langpack = loadlang('zh-tw.json')
    try:
        gain_money(gid)
    except:
        pass
    user = bot.get_user(ctx.author.id)
    embed=discord.Embed(title=str(user), description=f"id:{str(user.id)}", color=0xee4f9e)
    embed.set_thumbnail(url=ctx.author.avatar)
    createtime = user.created_at
    createtime2 = createtime.strftime('%Y/%m/%d %H:%M:%S')
    embed.add_field(name=langpack['yourinfo.time'], value=str(createtime2) + ' UTC+0', inline=False)
    embed.add_field(name='機器人帳戶', value=str(user.bot), inline=False)
    await ctx.send(embed=embed)
    if os.path.exists(f'gamer/{str(ctx.author.id)}.json'):
        with open(f'gamer/{str(ctx.author.id)}.json', 'r', encoding = 'utf8') as f:
            wt1 = json.load(f)
        embed2=discord.Embed(title=f"{str(user)} 的遊戲資訊", color=0xee4f9e)
        embed2.add_field(name="OOXX遊戲", value="統計資料", inline = False)
        embed2.add_field(name="總場數", value = str(wt1['ooxx']['total']))
        embed2.add_field(name="勝場數", value=f"{str(wt1['ooxx']['win'])}")
        if wt1['ooxx']['total'] != 0:
            embed2.add_field(name="勝率", value=f"{str(round(wt1['ooxx']['win']/wt1['ooxx']['total']*100))}%")
        else:
            embed2.add_field(name="勝率", value=f"0%")
        embed2.add_field(name="敗場數",value=f"{str(wt1['ooxx']['lose'])}")
        embed2.add_field(name="平局數",value=f"{str(wt1['ooxx']['tie'])}")
        embed2.add_field(name="中離場數", value=f"{str(wt1['ooxx']['noend'])}")
        await ctx.send(embed = embed2)
@bot.command()
async def userinfo(ctx, tuser):
    gid = ctx.guild.id
    try:
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
    except:
        langpack = loadlang('zh-tw.json')
    try:
        gain_money(gid)
    except:
        pass
    user = bot.get_user(int(str(tuser).replace('<', '').replace('>', '').replace('!', '').replace('@', '')))
    embed=discord.Embed(title=str(user), description=f"id:{str(user.id)}", color=0xee4f9e)
    embed.set_thumbnail(url=user.avatar)
    createtime = user.created_at
    createtime2 = createtime.strftime('%Y/%m/%d %H:%M:%S')
    embed.add_field(name=langpack['yourinfo.time'], value=str(createtime2) + ' UTC+0', inline=False)
    embed.add_field(name='機器人帳戶', value=str(user.bot), inline=False)
    await ctx.send(embed=embed)
    if os.path.exists(f'gamer/{str(user.id)}.json'):
        with open(f'gamer/{str(user.id)}.json', 'r', encoding = 'utf8') as f:
            wt1 = json.load(f)
        embed2=discord.Embed(title=f"{str(user)} 的遊戲資訊", color=0xee4f9e)
        embed2.add_field(name="OOXX遊戲", value="統計資料", inline = False)
        embed2.add_field(name="總場數", value = str(wt1['ooxx']['total']))
        embed2.add_field(name="勝場數", value=f"{str(wt1['ooxx']['win'])}")
        if wt1['ooxx']['total'] != 0:
            embed2.add_field(name="勝率", value=f"{str(round(wt1['ooxx']['win']/wt1['ooxx']['total']*100))}%")
        else:
            embed2.add_field(name="勝率", value=f"0%")
        embed2.add_field(name="敗場數",value=f"{str(wt1['ooxx']['lose'])}")
        embed2.add_field(name="平局數",value=f"{str(wt1['ooxx']['tie'])}")
        embed2.add_field(name="中離場數", value=f"{str(wt1['ooxx']['noend'])}")
        await ctx.send(embed = embed2)

@bot.command()
async def removeytchannel(ctx, id:str):
    if os.path.exists(f'settings/{str(ctx.guild.id) }.json'):
        gid = ctx.guild.id
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
        
        try:
            au = ctx.author
            roles = au.roles
            isa = 0
            for a in roles:
                for c in a.permissions:
                    if c[0] == 'administrator' and c[1] == True:
                        isa = 1
            if isa == 1:
                gid = ctx.guild.id
                wt41 = loadset(gid)
                if wt41['ytchannelid'] != []:
                    tlist = []
                    for wttt in wt41['ytchannelid']:
                        if wttt != id:
                            tlist.append(wttt)
                    if len(wt41['ytchannelid']) > len(tlist):
                        wt41['ytchannelid'] = tlist
                        writeset(ctx.guild.id, wt41)
                        embed=discord.Embed(color=0xee4f9e)
                        result3 = requests.get('https://www.googleapis.com/youtube/v3/channels?part=snippet&id={}&key={}'.format(id, api_key))
                        data3 = result3.json()
                        embed.add_field(name='刪除成功!', value=f'已刪除頻道 {data3["items"][0]["snippet"]["title"]}({id})', inline=False)
                        await ctx.send(embed=embed)
                    else:
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name='錯誤!', value=f'頻道列表中不存在頻道ID {id}', inline=False)
                        await ctx.send(embed=embed)
                else:
                    embed=discord.Embed(color=0xee4f9e)
                    embed.add_field(name="ERROR!", value='沒有任何頻道在列表內!', inline=False)
                    await ctx.send(embed=embed)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name=langpack["removeytchannel.cantdel.title"], value=langpack["notadmin.msg"], inline=True)
                await ctx.send(embed=embed)
        except:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="ERROR!", value=langpack["err.message"], inline=False)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@bot.command()
async def ytchannellist(ctx):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        gid = ctx.guild.id
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
        
        try:
            gid = ctx.guild.id
            wt41 = loadset(gid)
            msg = ""
            for wttt in wt41['ytchannelid']:
                try:
                    result3 = requests.get('https://www.googleapis.com/youtube/v3/channels?part=snippet&id={}&key={}'.format(wttt, api_key))
                    data3 = result3.json()
                    msg += f'{data3["items"][0]["snippet"]["title"]}\nhttps://www.youtube.com/channel/' + wttt + "\n(id:" + wttt + ')\n' 
                except:
                    pass
            if msg == "":
                msg = "清單內沒有Youtube頻道"
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name=langpack["ytchannellist.title"], value=f"{msg}", inline=False)
            await ctx.send(embed=embed)
        except:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="ERROR!", value=langpack["err.message"], inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)

def loadlang(pack:str):
    with open(f'lang/{pack}', 'r', encoding = 'utf-8') as f:
        d1 = json.load(f)
    return d1

@bot.command()
async def ping(ctx):
    gid = ctx.guild.id
    try:
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
    except:
        langpack = loadlang('zh-tw.json')
    try:
        gain_money(gid)
    except:
        pass
    lan_set = loadset(gid)
    langpack = loadlang(lan_set["lang"])
    embed=discord.Embed(color=0xec3cbd)
    embed.add_field(name=langpack["ping.title"], value=f"{round(bot.latency*1000)}ms", inline=True)
    
    button = Button(label = "更新", style = discord.ButtonStyle.green, emoji="🔃")
    async def intwe(interaction):
        embed=discord.Embed(color=0xec3cbd)
        embed.add_field(name=langpack["ping.title"], value=f"{round(bot.latency*1000)}ms", inline=True)
        button = Button(label = "更新", style = discord.ButtonStyle.green, emoji="🔃")
        button.callback = intwe

        view = View(timeout = None)
        view.add_item(button)
        await interaction.response.edit_message(embed = embed, view = view)
    
    button = Button(label = "更新", style = discord.ButtonStyle.green, emoji="🔃")
    button.callback = intwe
    view = View(timeout = None)
    view.add_item(button)
    await ctx.send(embed=embed, view = view)
@bot.command()
async def help(ctx):
    gid = ctx.guild.id
    try:
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
    except:
        langpack = loadlang('zh-tw.json')
    try:
        gain_money(gid)
    except:
        pass
    embed=discord.Embed(title='愛吃團子的機器人', description="bot prefix >>", color=0xec3cbd)
    embed.add_field(name="[廣告投放欄位]", value="""``歡迎私訊申請投放廣告``""", inline=False)

    embed.add_field(name="機器人作者", value='pour33142GX', inline=True)
    embed.add_field(name="機器人版本", value=botsetting["version"], inline=True)
    embed.add_field(name="圖片庫版本", value='v1.5', inline=True)
    embed.add_field(name="程式語言", value='Python 3.10', inline=True)
    embed.add_field(name="模組", value='Discord.py、Pycord、urllib、requests、asyncio、os、random、datetime、glob、json、re、time、collections', inline=True)
    embed.add_field(name="Special Thanks", value='白上主子主推(onion88didi)、【偽聲見習生】呆那、Himeno_hina、鈴木ロータス🍡腦殘vtuber(已安息、墳墓還被基岩壓著)', inline=True)
    embed.set_footer(text=f'愛吃團子的機器人|{botsetting["version"]}')
    
    select = Select(placeholder="Choose a page!",
        options=[
        discord.SelectOption(label="Page1", emoji = "🥳", description='娛樂功能'),
        discord.SelectOption(label="Page2", emoji = "▶️", description='YouTube功能'),
        discord.SelectOption(label="Page3", emoji = "🗑️", description='其他功能'),
        discord.SelectOption(label="Page4", emoji = "🖥️", description='伺服器功能'),
        discord.SelectOption(label="Page5", emoji = "👾", description='RPG'),
        discord.SelectOption(label="Page6", emoji = "🔊", description='暫存語音頻道功能'),
        discord.SelectOption(label="Page7", emoji = "😘", description='Role'),
        discord.SelectOption(label="Page8", emoji = "👋", description='Welcome and Leave'),
        discord.SelectOption(label="Page9", emoji = "🎮", description='Game and Gamer'),
        discord.SelectOption(label="Page10", emoji = "🎵", description='音樂')
    ])
    async def testcallback(interaction):
        if select.values[0] == 'Page1':
            embed=discord.Embed(title=langpack["clist.page1.title.title"], description=langpack["clist.page1.title.msg"], color=0xec3cbd)
            embed.add_field(name=">>funstick", value=langpack["clist.page1.command1"], inline=False)
            embed.add_field(name=">>hi", value=langpack["clist.page1.command2"], inline=False)
            embed.add_field(name=">>hug", value=langpack['clist.page1.command3'], inline=False)
            embed.add_field(name=">>picture <type>", value=langpack['clist.page1.command4.p1'] + "\n" + langpack['clist.page1.command4.p2'], inline=False)
            embed.add_field(name=">>picgoogle <word>", value='用google搜尋圖片\n<word>處可指定關鍵字', inline=False)
            embed.add_field(name=">>愛蓮說", value=langpack['clist.page1.command6'], inline=True)
            embed.add_field(name=">>fbk", value='yep u know:D', inline=True)
            embed.add_field(name=">>pupload <tag>", value = "上傳圖片至團子機器人的圖庫\n<tag>可輸入圖片的分類(目前提供:r18、other、WTF、iruma、yellow-card)\n僅接受jpg、png、gif格式的圖片\n使用指令時將圖片作為訊息附件即可", inline = True)
            await interaction.response.edit_message(embed=embed)
        elif select.values[0] == 'Page2':
            embed=discord.Embed(title=langpack['clist.page2.title.title'], description=langpack['clist.page2.title.msg'], color=0xec3cbd)
            embed.add_field(name=">>newvideo", value=langpack['clist.page2.command1'], inline=False)
            embed.add_field(name=">>channelinfo", value=langpack['clist.page2.command2'], inline=False)
            embed.add_field(name=">>subs guild", value=langpack['clist.page2.command3'], inline=False)
            embed.add_field(name=">>subs other <id>", value=langpack['clist.page2.command3.p1'] + "\n" + langpack['clist.page2.command3.p2'], inline=False)
            embed.add_field(name=">>addytchannel <chid>", value=langpack['clist.page4.command2.p1'], inline=False)
            embed.add_field(name=">>removeytchannel", value=langpack['clist.page4.command3.p1'] + "\n" + langpack['clist.page4.command3.p2'], inline=False)
            embed.add_field(name=">>ytchannellist", value=langpack['clist.page4.command4'], inline=False)
            await interaction.response.edit_message(embed=embed)
        elif select.values[0] == 'Page3':
            embed=discord.Embed(title=langpack['clist.page3.title.title'], description=langpack['clist.page3.title.msg'], color=0xec3cbd)
            embed.add_field(name=">>exam", value="查看112年國中教育會考倒數計時", inline=False)
            embed.add_field(name=">>help", value=langpack['clist.page3.command1'], inline=False)
            embed.add_field(name=">>ping", value=langpack['clist.page3.command2'], inline=False)
            embed.add_field(name=">>time", value=langpack['clist.page3.command3'], inline=False)
            embed.add_field(name=">>time_other <area>", value=langpack['clist.page3.command4.p1'] + "\n" + langpack['clist.page3.command4.p2'], inline=False)
            embed.add_field(name=">>yourinfo", value=langpack['clist.page3.command6'], inline=False)
            embed.add_field(name=">>guildinfo", value=langpack['clist.page3.command7'], inline=False)
            embed.add_field(name=">>guildinfo detail", value='查看更詳細的伺服器資訊', inline=False)
            await interaction.response.edit_message(embed=embed)
        elif select.values[0] == 'Page4':
            embed=discord.Embed(title=langpack['clist.page4.title.title'], description=langpack['clist.page4.title.msg'], color=0xec3cbd)
            embed.add_field(name=">>purge <limit>", value=langpack['clist.page4.command1.p1'] + '\n' + langpack['clist.page4.command1.p2'], inline=False)
            embed.add_field(name=">>timezone", value=langpack['clist.page4.command10'], inline=False)
            embed.add_field(name=">>settimezone", value=langpack['clist.page4.command11'], inline=False)
            embed.add_field(name=">>addtz <zone>", value="添加時區到其他時區列表\n<zone>處可指定時區", inline=False)
            embed.add_field(name=">>deltz <zone>", value="從其他時區列表中刪除指定時區\n<zone>處可指定時區", inline=False)
            embed.add_field(name=">>resetup", value=langpack['clist.page4.command14'], inline=False)
            embed.add_field(name=">>setlang", value=langpack["clist.main.setlang.p1"], inline=False)
            embed.add_field(name=">>timezonelist", value="查看全球時區表(UTC)", inline=False)
            await interaction.response.edit_message(embed=embed)
        elif select.values[0] == 'Page5':
            embed=discord.Embed(title="RPG", description=langpack['clist.page5.title.msg'], color=0xec3cbd)
            embed.add_field(name=">>rpg register", value="註冊RPG玩家身分及選擇職業", inline=False)
            embed.add_field(name=">>rpg me", value="查看自己的狀態/資料", inline=False)
            embed.add_field(name=">>rpg farm", value="農夫/耕作", inline=False)
            embed.add_field(name=">>rpg mine", value="礦工/挖礦", inline=False)
            embed.add_field(name=">>rpg hunt", value="獵人/狩獵", inline=False)
            embed.add_field(name=">>rpg bp", value="查看背包", inline=False)
            embed.add_field(name=">>rpg eat", value="吃東西，可以回復HP", inline=False)
            embed.add_field(name=">>rpg sell <name> <amount>", value="販賣背包內的物品\n<name>填物品名稱，<amount>填數量", inline=False)
            await interaction.response.edit_message(embed=embed)
        elif select.values[0] == 'Page6':
            embed=discord.Embed(title='指令列表-page7', description='Reaction Roles', color=0xec3cbd)
            embed.add_field(name=">>tvc list", value='查看暫存語音頻道列表', inline=False)
            embed.add_field(name=">>tvc create <id>", value='將一個頻道設定為暫存語音頻道的入口\n<id>處指定語音頻道id', inline=False)
            embed.add_field(name=">>tvc delete <id>", value="移除一個頻道做為暫存語音頻道的入口的功能\n<id>處指定語音頻道id", inline=False)
            embed.add_field(name=">>tvc lock", value="將你現在所處的頻道設為私人頻道", inline=False)
            embed.add_field(name=">>tvc unlock", value="解鎖你現在所處的語音頻道", inline=False)
            embed.add_field(name=">>tvc add <member>", value="將一個成員加入白名單，讓那個成員可以加入你的語音頻道\n<member>處tag一個人來指定", inline=False)
            embed.add_field(name=">>tvc kick <member>", value="將一個成員從白名單中移除，讓那個成員不能加入你的語音頻道\n<member>處tag一個人來指定", inline=False)
            await interaction.response.edit_message(embed=embed)
        elif select.values[0] == 'Page7':
            embed=discord.Embed(title='指令列表-page7', description='Role', color=0xec3cbd)
            embed.add_field(name=">>rr list", value='查看Reaction Roles列表', inline=False)
            embed.add_field(name=">>rr new <msgid> <emoji> <role>", value='設定一個訊息的Reaction Roles\n<msgid>處指定訊息id\n<emoji>指定一個表情符號\n<role>處tag一個身分組，點選reaction時就會獲得這個身分組', inline=False)
            embed.add_field(name=">>rr remove <msgid> <emoji>", value="移除一個頻道的Reaction Roles.\n<msgid>處指定一個訊息的id\n<emoji>處指定一個反應(Reaction)", inline=False)
            embed.add_field(name=">>rr userbladd <msgid> <emoji> <user>", value="將一個用戶加入黑名單，讓他不能透過特定訊息上特定的反應取得身分組\n<msgid>處指定一個訊息的id\n<emoji>處指定一個反應(Reaction)\n<user>處指定一個人，可以tag他來指定", inline=False)
            embed.add_field(name=">>rr userbldelete <msgid> <emoji> <user>", value="將一個用戶從黑名單中移除，讓他可以透過特定訊息上特定的反應取得身分組\n<msgid>處指定一個訊息的id\n<emoji>處指定一個反應(Reaction)\n<user>處指定一個人，可以tag他來指定", inline=False)
            embed.add_field(name=">>rr rolebladd <msgid> <emoji> <role>", value="將一個身分組加入黑名單，讓擁有該身分組的人不能透過特定訊息上特定的反應取得身分組\n<msgid>處指定一個訊息的id\n<emoji>處指定一個反應(Reaction)\n<user>處指定一身分組，可以tag身分組來指定", inline=False)
            embed.add_field(name=">>rr rolebldelete <msgid> <emoji> <role>", value="將一個身分組從黑名單中移除，讓擁有該身分組的人可以透過特定訊息上特定的反應取得身分組\n<msgid>處指定一個訊息的id\n<emoji>處指定一個反應(Reaction)\n<user>處指定一身分組，可以tag身分組來指定", inline=False)
            embed.add_field(name = '>>rr bllist', value = '查看Reaction Roles黑名單')
            embed.add_field(name=">>br new <role> <title> <content>", value="設定點擊按鈕獲得身分組的功能\n<role>處指定一身分組，可以tag身分組來指定\n<title>處可填入Embed訊息的標題\n<content>處可填入Embed訊息的內容", inline=False)
            await interaction.response.edit_message(embed=embed)
        elif select.values[0] == 'Page8':
            embed=discord.Embed(title='指令列表-page8', description='Welcome and Leave', color=0xec3cbd)
            embed.add_field(name=">>welcome edit <msg>", value='編輯歡迎訊息\n<msg>處填入訊息內容，可以搭配特殊佔位符', inline=False)
            embed.add_field(name=">>welcome clear", value='清除歡迎訊息', inline=False)
            embed.add_field(name=">>welcome show", value="顯示歡迎訊息", inline=False)
            embed.add_field(name=">>welcome channel", value="將使用指令的頻道設定為歡迎訊息顯示的頻道", inline=False)
            embed.add_field(name=">>welcome showch", value="顯示歡迎訊息頻道", inline=False)
            embed.add_field(name=">>welcome toggle <option>", value="開關歡迎訊息功能\n<option>處可以填入True(開啟)或是False(關閉)", inline=False)
            embed.add_field(name=">>welcome welrole <role>", value="設定成員一進到伺服器就自動領取的身分組\n<role>處可以tag一個身分組或是填入身分組的id", inline=False)
            embed.add_field(name ='>>welcome showrole', value = '查看成員一進去伺服器就自動領取的身分組', inline=False)
            embed.add_field(name ='>>welcome roletoggle <option>', value = '開關成員一進去就自動領取的身分組的功能\n<option>處可以填入True(開啟)或是False(關閉)', inline=False)
            embed.add_field(name ='>>welcome weldm <msg>', value = '設定私人歡迎訊息\n<msg>處可填入歡迎訊息內容', inline=False)
            embed.add_field(name ='>>welcome dmshow', value = '顯示私人歡迎訊息', inline=False)
            embed.add_field(name ='>>welcome dmtoggle <option>', value = '開啟私人歡迎訊息\n<option>處可以填入True(開啟)或是False(關閉)', inline=False)
            embed.add_field(name ='>>leave edit <msg>', value = '編輯離開訊息\n<msg>處填入訊息內容', inline=False)
            embed.add_field(name ='>>leave clear', value = '清除離開訊息', inline=False)
            embed.add_field(name ='>>leave show', value = '顯示離開訊息', inline=False)
            embed.add_field(name ='>>leave channel', value = '將使用指令的頻道設定為離開訊息顯示的頻道', inline=False)
            embed.add_field(name ='>>leave showch', value = '顯示離開訊息頻道', inline=False)
            embed.add_field(name ='>>leave toggle <option>', value = '開關離開訊息功能\n<option>處可以填入True(開啟)或是False(關閉)', inline=False)
            embed.add_field(name ='>>leave dm <msg>', value = '編輯私人離開訊息\n<msg>處可填入私人離開訊息內容', inline=False)
            embed.add_field(name ='>>leave dmshow', value = '顯示私人離開訊息', inline=False)
            embed.add_field(name ='>>leave dmtoggle', value = '開關私人離開訊息功能\n<option>處可以填入True(開啟)或是False(關閉)', inline=False)
            embed.add_field(name ='特殊佔位符', value = '>gname< 顯示伺服器名稱\n>tagm< 在訊息中tag加入/離開的成員\n>mname< 顯示成員帳號名稱\n>tagm<在離開訊息不能使用', inline=False)
            await interaction.response.edit_message(embed=embed)
        elif select.values[0] == 'Page9':
            embed=discord.Embed(title='指令列表-page9', description='Game and Gamer', color=0xec3cbd)
            embed.add_field(name="Gamer", value='玩家指令', inline=False)
            embed.add_field(name=">>gamer self", value='查看自己的玩家資料', inline=False)
            embed.add_field(name=">>gamer search <user>", value="查看他人的玩家資料\n<user>內可以tag一位用戶來查詢", inline=False)
            embed.add_field(name="OOXX", value="井字遊戲指令", inline=False)
            embed.add_field(name=">>ooxx new", value="開啟一場新的井字遊戲", inline=False)
            embed.add_field(name=">>ooxx leave", value="強制結束一場井字遊戲", inline=False)
            embed.add_field(name=">>ooxx view", value="叫出遊戲面板", inline=False)
            await interaction.response.edit_message(embed=embed)
        elif select.values[0] == 'Page10':
            embed=discord.Embed(title='指令列表-page10', description='音樂', color=0xec3cbd)
            embed.add_field(name=">>join", value='加入語音頻道', inline=False)
            embed.add_field(name=">>vleave", value='離開語音頻道', inline=False)
            embed.add_field(name=">>play <url>", value="播放一個歌曲/把一個歌曲加到列表\n<url> - 填入Youtube影片網址", inline=False)
            embed.add_field(name=">>pause", value="暫停音樂", inline=False)
            embed.add_field(name=">>resume", value="繼續播放音樂", inline=False)
            embed.add_field(name=">>loop <mode>", value="切換音樂循環模式\n<mode> - 可填入``n``、``o``、``a``\nn - 關閉 | o - 單曲循環 | a - 播放清單循環", inline=False)
            embed.add_field(name=">>queue", value="查看播放清單", inline=False)
            embed.add_field(name=">>clearqueue", value="清除播放清單", inline=False)
            embed.add_field(name=">>prandom", value="切換隨機播放", inline=False)
            embed.add_field(name=">>stop", value="停止播放音樂", inline=False)
            embed.add_field(name=">>skip", value="跳過現在播放的音樂", inline=False)
            await interaction.response.edit_message(embed=embed)
    select.callback = testcallback
    view = View(timeout = None)
    view.add_item(select)

    view.add_item(Button(label = '官方discord', style = discord.ButtonStyle.url, url = 'https://discord.gg/EEphsxzvvQ'))
    view.add_item(Button(label = '邀請團子機器人', style = discord.ButtonStyle.url, url = 'https://discord.com/api/oauth2/authorize?client_id=891282885007532062&permissions=8&scope=bot'))
    view.add_item(Button(label = '機器人程式碼', style = discord.ButtonStyle.url, url = 'https://github.com/pictures2333/Dango-Bot'))

    await ctx.send(embed=embed, view = view)

@bot.command()
async def time(ctx):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        gid = ctx.guild.id
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
        
        wt45 = loadset(gid)
        try:
            if wt45['timearea'] != "None":
                gettime.gettime(wt45['timearea'], '%Y/%m/%d %H:%M:%S')
                with open('time.txt', 'r', encoding = 'utf-8') as f:
                    content1 = f.readlines()
                    zoned_time1 = content1[0]
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name=langpack['time.success'] + f"{timezonenames[wt45['timearea']]}({str(wt45['timearea'])})", value=f"{zoned_time1}", inline=False)
                tmsg = ""
                for tz in wt45['otz']:
                    gettime.gettime(tz, '%Y/%m/%d %H:%M:%S')
                    with open('time.txt', 'r', encoding = 'utf-8') as f:
                        content1 = f.readlines()
                        zoned_time1 = content1[0]
                    tmsg += f"{timezonenames[tz]}({str(tz)}) => {zoned_time1}\n"
                if tmsg == "":
                    tmsg = "無"
                embed.add_field(name="其他時區", value=f"{tmsg}", inline=False)
                button = Button(label = '更新', style = discord.ButtonStyle.green, emoji="🔃")
                async def refresh(interaction):
                    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
                        gid = ctx.guild.id
                        lan_set = loadset(gid)
                        langpack = loadlang(lan_set["lang"])
                        try:
                            gain_money(gid)
                        except:
                            pass
                        wt45 = loadset(gid)
                        try:
                            if wt45['timearea'] != "None":
                                gettime.gettime(wt45['timearea'], '%Y/%m/%d %H:%M:%S')
                                with open('time.txt', 'r', encoding = 'utf-8') as f:
                                    content1 = f.readlines()
                                    zoned_time1 = content1[0]
                                embed=discord.Embed(color=0xee4f9e)
                                embed.add_field(name=langpack['time.success'] + f"{timezonenames[wt45['timearea']]}({str(wt45['timearea'])})", value=f"{zoned_time1}", inline=False)
                                tmsg = ""
                                for tz in wt45['otz']:
                                    gettime.gettime(tz, '%Y/%m/%d %H:%M:%S')
                                    with open('time.txt', 'r', encoding = 'utf-8') as f:
                                        content1 = f.readlines()
                                        zoned_time1 = content1[0]
                                    tmsg += f"{timezonenames[tz]}({str(tz)}) => {zoned_time1}\n"
                                if tmsg == "":
                                    tmsg = "無"
                                embed.add_field(name="其他時區", value=f"{tmsg}", inline=False)
                                await interaction.response.edit_message(embed=embed)
                            else:
                                embed=discord.Embed(color=0xee4f9e)
                                embed.add_field(name="ERROR!", value=langpack['time.notimezone'], inline=True)
                                await interaction.response.edit_message(embed=embed)
                        except:
                            embed=discord.Embed(color=0xee4f9e)
                            embed.add_field(name="ERROR!", value=langpack['err.message'], inline=True)
                            await interaction.response.edit_message(embed = embed)
                    else:
                        await interaction.response.edit_message(content='設定檔遺失!\n請使用>>resetup建立設定檔')
                button.callback=refresh
                view = View(timeout = None)
                view.add_item(button)
                await ctx.send(embed = embed, view = view)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="ERROR!", value=langpack['time.notimezone'], inline=True)
                await ctx.send(embed=embed)
        except:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="ERROR!", value=langpack['err.message'], inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@bot.command()
async def settimezone(ctx, zone:float):
    if os.path.exists(f"settings/{str(ctx.guild.id)}.json"):
        gid = ctx.guild.id
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
        
        try:
            au = ctx.author
            roles = au.roles
            isa = 0
            for a in roles:
                for c in a.permissions:
                    if c[0] == 'administrator' and c[1] == True:
                        isa = 1
            if isa == 1:
                gid = ctx.guild.id
                wt46 = loadset(gid)
                embed=discord.Embed(color=0xee4f9e)

                cant = False
                for i in timezonenames:
                    if i == zone:
                        cant = True
                if cant == True:
                    wt46['timearea'] = zone
                    writeset(gid, wt46)

                    embed=discord.Embed(color=0xee4f9e)
                    embed.add_field(name='設定完成!', value=f'時區:{timezonenames[zone]}({str(zone)})', inline=True)
                    await ctx.send(embed=embed)
                else:
                    embed=discord.Embed(color=0xee4f9e)
                    embed.add_field(name='錯誤!', value='非正確時區!', inline=True)
                    await ctx.send(embed=embed)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name=langpack['settimezone.notadmin'], value=langpack['notadmin.msg'], inline=True)
                await ctx.send(embed=embed)
        except:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="ERROR!", value=langpack['err.message'], inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)

@bot.command()
async def addtz(ctx, zone:float):
    if os.path.exists(f"settings/{str(ctx.guild.id)}.json"):
        gid = ctx.guild.id
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
        
        try:
            au = ctx.author
            roles = au.roles
            isa = 0
            for a in roles:
                for c in a.permissions:
                    if c[0] == 'administrator' and c[1] == True:
                        isa = 1
            if isa == 1:
                gid = ctx.guild.id
                wt46 = loadset(gid)
                cana = True
                for tz in wt46['otz']:
                    if tz == zone or zone == wt46['timearea']:
                        cana = False
                if cana == True:
                    cant = False
                    for i in timezonenames:
                        if i == zone:
                            cant = True
                    if cant == True:
                        wt46['otz'].append(zone)
                        writeset(gid, wt46)
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name='時區添加成功!', value="時區:" +f"{timezonenames[zone]}({str(zone)})", inline=True)
                        await ctx.send(embed=embed)
                    else:
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name='錯誤!', value='時區不正確', inline=True)
                        await ctx.send(embed=embed)
                else:
                    embed=discord.Embed(color=0xee4f9e)
                    embed.add_field(name='錯誤!', value='此時區已存在於其他時區列表或是此時區是伺服器主時區', inline=True)
                    await ctx.send(embed=embed)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name=langpack['settimezone.notadmin'], value=langpack['notadmin.msg'], inline=True)
                await ctx.send(embed=embed)
        except:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="ERROR!", value=langpack['err.message'], inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@bot.command()
async def deltz(ctx, zone:float):
    if os.path.exists(f"settings/{str(ctx.guild.id)}.json"):
        gid = ctx.guild.id
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
        
        try:
            au = ctx.author
            roles = au.roles
            isa = 0
            for a in roles:
                for c in a.permissions:
                    if c[0] == 'administrator' and c[1] == True:
                        isa = 1
            if isa == 1:
                gid = ctx.guild.id
                cana = True
                tlist = []
                wt46 = loadset(gid)
                for tz in wt46['otz']:
                    if tz == zone:
                        cana = False
                    else:
                        tlist.append(tz)
                if cana == True:
                    embed=discord.Embed(color=0xee4f9e)
                    embed.add_field(name='刪除失敗', value="列表內沒有這個時區", inline=True)
                    await ctx.send(embed=embed)
                else:
                    wt46['otz'] = tlist
                    writeset(gid, wt46)
                    embed=discord.Embed(color=0xee4f9e)
                    embed.add_field(name='刪除成功', value='此時區已被移除', inline=True)
                    await ctx.send(embed=embed)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name=langpack['settimezone.notadmin'], value=langpack['notadmin.msg'], inline=True)
                await ctx.send(embed=embed)
        except:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="ERROR!", value=langpack['err.message'], inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@bot.command()
async def timezone(ctx):
    if os.path.exists(f"settings/{str(ctx.guild.id)}.json"):
        gid = ctx.guild.id
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
        
        gid = ctx.guild.id
        wt47 = loadset(gid)

        tmsg = ""
        for tz in wt47['otz']:
            tmsg += f"{timezonenames[tz]}({str(tz)})\n"
        if tmsg == "":
            tmsg = "無"
        if wt47['timearea'] != "None":
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name=langpack['timezone.success'], value=f"{timezonenames[wt47['timearea']]}({wt47['timearea']})", inline=False)
            embed.add_field(name='其他時區列表:', value=tmsg, inline=True)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="ERROR!", value=langpack['timezone.notimeozne'], inline=False)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@bot.command()
async def time_other(ctx, area:float):
    gid = ctx.guild.id
    try:
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
    except:
        langpack = loadlang('zh-tw.json')
    try:
        gain_money(gid)
    except:
        pass
    try:
        gettime.gettime(area, '%Y/%m/%d %H:%M:%S')
        with open('time.txt', 'r', encoding = 'utf-8') as f:
            content1 = f.readlines()
            zoned_time1 = content1[0]
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name=langpack['timeother.success']+f"{timezonenames[area]} {str(area)})", value=f"{zoned_time1}", inline=True)
        await ctx.send(embed=embed)
    except:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="ERROR!", value=langpack['err.message'], inline=True)
        await ctx.send(embed=embed)
@bot.command()
async def timezonelist(ctx):
    msgs = ""
    for i in timezonenames:
        msgs += f"{timezonenames[i]}({str(i)})\n"
    embed=discord.Embed(color=0xee4f9e)
    embed.add_field(name="時區列表", value=msgs, inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def channelinfo(ctx):
    if os.path.exists(f"settings/{str(ctx.guild.id)}.json"):
        gid = ctx.guild.id
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
        
        try:
            gid = ctx.guild.id
            wt41 = loadset(gid)
            if wt41['ytchannelid'] != []:
                msg = ""
                for wttt in wt41['ytchannelid']:
                    result3 = requests.get('https://www.googleapis.com/youtube/v3/channels?part=snippet&id={}&key={}'.format(wttt, api_key))
                    data3 = result3.json()
                    msg += f'{data3["items"][0]["snippet"]["title"]}\nhttps://www.youtube.com/channel/' + wttt + '\n' 
                embed=discord.Embed(color=0xee4f9e)
                if msg == "":
                    msg = "沒有任何Youtube頻道在清單中!"
                embed.add_field(name=langpack['channelinfo.success'], value=f"{msg}", inline=False)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="ERROR!", value=langpack['channelinfo.nolist.p1'] + "\n" + langpack['channelinfo.nolist.p2'], inline=True)
                await ctx.send(embed=embed)
        except:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="ERROR!", value=langpack['err.message'], inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@bot.command()
async def newvideo(ctx):
    if os.path.exists(f"settings/{ctx.guild.id}.json"):
        gid = ctx.guild.id
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
        gid = ctx.guild.id
        try:
            wt2 = loadset(gid)
            if wt2['ytchannelid'] != []:
                msg = ""
                for chid in wt2['ytchannelid']:
                    result1 = requests.get('https://www.googleapis.com/youtube/v3/channels?part=snippet,contentDetails&id={}&key={}'.format(chid, api_key))
                    data1 = result1.json()
                    try:
                        result2 = requests.get('https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId={}&key={}'.format(data1['items'][0]['contentDetails']['relatedPlaylists']['uploads'], api_key))
                        data2 = result2.json()
                        result3 = requests.get('https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={}&key={}'.format(data2['items'][0]['contentDetails']['videoId'], api_key))
                        data3 = result3.json()
                        msg += f'頻道:{data1["items"][0]["snippet"]["title"]}/id:{chid}) => {data3["items"][0]["snippet"]["title"]}\nhttps://www.youtube.com/watch?v={data3["items"][0]["id"]}\n\n'
                    except:
                        msg += f'頻道:{data1["items"][0]["snippet"]["title"]}/id:{chid} => 無法獲取!\n\n'
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name=langpack['newvideo'], value=msg, inline=True)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="ERROR!", value=langpack['channelinfo.nolist.p1'] + "\n" + langpack['channelinfo.nolist.p2'], inline=True)
                await ctx.send(embed=embed)
        except:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="ERROR", value=langpack['err.message'], inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@bot.command()
async def funstick(ctx):
    gid = ctx.guild.id
    try:
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
    except:
        langpack = loadlang('zh-tw.json')
    try:
        gain_money(gid)
    except:
        pass
    msg = await ctx.send(langpack['funstick.catch'])
    sleep(1)
    await msg.edit(content = f"{langpack['funstick.catch']} {langpack['funstick.catch']}")
    r1 = random.randint(1, 3)
    sleep(1)
    if r1 == 1:
        await msg.edit(content = langpack['funstick.success'])
    else:
        await msg.edit(content = langpack['funstick.fail'])
@bot.command()
async def hi(ctx):
    gid = ctx.guild.id
    try:
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
    except:
        langpack = loadlang('zh-tw.json')
    try:
        gain_money(gid)
    except:
        pass
    r2 = random.randint(1, 3)
    if r2 == 1:
        await ctx.send('hello~')
    elif r2 == 2:
        await ctx.send('ヾ(≧▽≦*)o')
    elif r2 == 3:
        await ctx.send('o(*^▽^*)┛')
@bot.command()
async def hug(ctx):
    gid = ctx.guild.id
    try:
        gain_money(gid)
    except:
        pass
    button = Button(label = '抱抱', style = discord.ButtonStyle.blurple)
    view = View(timeout = None)
    async def inte1(interaction):
        button1 = Button(label = '抱抱', style = discord.ButtonStyle.blurple, disabled=True)
        view1 = View()
        view1.add_item(button1)
        await interaction.response.edit_message(content = "(つ´ω`)つ⊂(・﹏・⊂)", view = view1)
    button.callback = inte1
    view.add_item(button)
    await ctx.send('(つ´ω`)つ', view = view)

@bot.command()
async def setchannel(ctx):
    if os.path.exists(f"settings/{str(ctx.guild.id)}.json"):
        gid = ctx.guild.id
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
        
        au = ctx.author
        roles = au.roles
        isa = 0
        for a in roles:
            for c in a.permissions:
                if c[0] == 'administrator' and c[1] == True:
                    isa = 1
        if isa == 1:
            gid = ctx.guild.id
            if os.path.exists(f'settings/{str(gid)}.json'):
                try:
                    channelid = ctx.channel.id
                    channel = bot.get_channel(channelid)
                    await channel.send('Test message')
                    d10 = loadset(gid)
                    d10['channelid'] = str(channelid)
                    writeset(gid, d10)
                    embed=discord.Embed(title=langpack['setchannel.success.title'], color=0xee4f9e)
                    embed.add_field(name=langpack['setchannel.success.id'], value=f"{channelid}", inline=True)
                    embed.add_field(name=langpack['setchannel.success.name'], value=f"{channel.mention}", inline=True)
                    await ctx.send(embed=embed)
                except:
                    embed=discord.Embed(color=0xee4f9e)
                    embed.add_field(name="ERROR", value=langpack['err.message'], inline=True)
                    await ctx.send(embed=embed)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="此伺服器還沒setup過!", value="使用>>setup以進行setup", inline=True)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name=langpack['setchannel.notadmin'], value=langpack['notadmin.msg'], inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@bot.command()
async def showchannel(ctx):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        gid = ctx.guild.id
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
        
        gid = ctx.guild.id
        if os.path.exists(f'settings/{str(gid)}.json'):
            try:
                d11 = loadset(gid)
                channel = bot.get_channel(int(d11['channelid']))
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name=langpack['printchannel'], value=f"{channel.mention}", inline=True)
                await ctx.send(embed=embed)
            except:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="ERROR", value=langpack['err.message'], inline=True)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="此伺服器還沒setup過!", value="使用>>setup以進行setup", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)

@bot.command()
async def picture(ctx, type:str):
    gid = ctx.guild.id
    try:
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
    except:
        langpack = loadlang('zh-tw.json')
    try:
        gain_money(gid)
    except:
        pass
    try:
        if type == 'r18':
            if ctx.channel.is_nsfw():
                files = glob.glob(f'pictures/{type}/*.*')
                r10 = random.randint(0, len(files)-1)
                pic = discord.File(os.path.abspath(files[r10]))
                await ctx.send(file = pic)
            else:
                awa = random.randint(0, 2)
                if awa == 0:
                    pic = discord.File('不可以瑟瑟.jpg')
                    await ctx.send(file = pic)
                elif awa == 1:
                    pic = discord.File('吃雞雞x不可以色色.jpg')
                    await ctx.send(file = pic)
                elif awa == 2:
                    pic = discord.File('中華電信色情守門員x超能先生迷因.jpg')
                    await ctx.send(file = pic)
        else:
            files = glob.glob(f'pictures/{type}/*.*')
            r10 = random.randint(0, len(files)-1)
            pic = discord.File(os.path.abspath(files[r10]))
            await ctx.send(file = pic)
    except:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="ERROR", value=langpack['err.message'], inline=True)
        await ctx.send(embed=embed)
@bot.command()
async def picgoogle(ctx, *, msg):
    global imageList
    def getHtmlCode(url):
      headers = {
        'User-Agent': 'Mozilla/5.0(Linux; Android 6.0; Nexus 5 Build/MRA58N) \
        AppleWebKit/537.36(KHTML,like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
      }
      url = urllib.request.Request(url,headers=headers)
      page = urllib.request.urlopen(url).read()
      page = page.decode('UTF-8')
      return page
    def getImage(page):
       global imageList
       imageList = re.findall(r'(https:[^\s]*?(jpg|png|gif))"',page)
       x = 0
       while not x>1 :
         try:
           print(imageList)
           x = x + 1
         except:
           continue
       pass
    if __name__ == '__main__':
       encodedStr = f'https://{msg}.com'
       url = urllib.parse.quote(encodedStr).replace('https://', '').replace('.com', '')
       page = getHtmlCode(f'https://www.google.com/search?q={url}&tbm=isch')
       turl = str(imageList[random.randint(0, len(imageList)-1)][0])
       print(turl)
       await ctx.send(f"{msg}\n{turl}")

@bot.command()
async def purge(ctx, num:int):
    gid = ctx.guild.id
    try:
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
    except:
        langpack = loadlang('zh-tw.json')
    try:
        gain_money(gid)
    except:
        pass
    au = ctx.author
    roles = au.roles
    isa = 0
    for a in roles:
        for c in a.permissions:
            if c[0] == 'administrator' and c[1] == True:
                isa = 1
    if isa == 1:
        try:
            await ctx.channel.purge(limit = num+1)
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name=f"{str(num)}"+langpack['purge.success'], value="我們懷念他們。", inline=True)
            await ctx.send(embed=embed)
        except:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="ERROR", value=langpack['err.message'], inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name=langpack['purge.notadmin'], value=langpack['notadmin.msg'], inline=True)
        await ctx.send(embed=embed)

@bot.group()
async def subs(ctx):
    gid = ctx.guild.id
    try:
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
    except:
        langpack = loadlang('zh-tw.json')
    try:
        gain_money(gid)
    except:
        pass
@subs.command()
async def guild(ctx):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        gid = ctx.guild.id
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
        gain_money(gid)
        try:
            wt3 = loadset(gid)
            if wt3['ytchannelid'] != []:
                msg = ""
                for chid in wt3['ytchannelid']:
                    try:
                        result1 = requests.get('https://www.googleapis.com/youtube/v3/channels?part=statistics, snippet&id={}&key={}'.format(str(chid), api_key))
                        wt4 = result1.json()
                        subs = wt4['items'][0]['statistics']['subscriberCount']
                        msg += langpack['subs.guild.success.msg.p1'] + f'{wt4["items"][0]["snippet"]["title"]}'+langpack['subs.guild.success.msg.p2']+f'{str(subs)}\n'
                    except:
                        msg += langpack['subs.guild.success.msg.p1'] + f'{wt4["items"][0]["snippet"]["title"]}'+langpack['subs.guild.success.msg.p2'] + langpack['subs.guild.notdisplay']
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name=langpack['subs.guild.listtitle'], value=msg, inline=True)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="ERROR!", value=langpack['channelinfo.nolist.p1']+langpack['channelinfo.nolist.p2'], inline=True)
                await ctx.send(embed=embed)
        except:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="ERROR", value=langpack['err.message'], inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@subs.command()
async def other(ctx, chid:str):
    gid = ctx.guild.id
    try:
        lan_set= loadset(gid)
        langpack = loadlang(lan_set['lang'])
    except:
        langpack = loadlang('zh-tw.json')
    try:
        result1 = requests.get('https://www.googleapis.com/youtube/v3/channels?part=statistics, snippet&id={}&key={}'.format(str(chid), api_key))
        wt4 = result1.json()
        subs = wt4['items'][0]['statistics']['subscriberCount']
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name= langpack['subs.guild.success.msg.p1'] + f'[{wt4["items"][0]["snippet"]["title"]}]' + langpack['subs.guild.success.msg.p2'], value=f"{str(subs)}", inline=True)
        await ctx.send(embed=embed)
    except:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="ERROR", value=langpack['err.message'], inline=True)
        await ctx.send(embed=embed)

@bot.command()
async def store(ctx):
    gid = ctx.guild.id
    try:
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
    except:
        langpack = loadlang('zh-tw.json')
    try:
        gain_money(gid)
    except:
        pass
    try:
        wt5 = loadset(0)
        msg = "Food Store:\n"
        for i in range (len(wt5['item'])):
            msg += '{}/{}\n'.format(wt5['item'][i], str(wt5['price'][i]))
        user = bot.get_user(ctx.author.id)
        if user is not None:
            if user.dm_channel is None:
                await user.create_dm()
            await user.dm_channel.send(msg)
            await ctx.send('食物商店商品清單已經傳送到DM中')
        else:
            await ctx.send('無法傳送商品清單!')
    except:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="ERROR", value=langpack['err.message'], inline=True)
        await ctx.send(embed=embed)

@bot.group()
async def rpg(ctx):
    pass
@rpg.command()
async def register(ctx):
    select = Select(placeholder="選擇一個職業!",
        options=[
        discord.SelectOption(label="農夫", emoji = "👩‍🌾"),
        discord.SelectOption(label="礦工", emoji = "💎"),
        discord.SelectOption(label="獵人", emoji = "🍖"),
    ])
    async def inte(interaction):
        if not os.path.exists(f'RPG/{str(interaction.user.id)}.json'):
            wt1 = {"job":select.values[0], "money":0, "bp":[], "lev":1, "exp":0, "nextlev":100, "hp":20, "body":20}
            dumpdata = json.dumps(wt1, ensure_ascii = False)
            with open(f'RPG/{str(interaction.user.id)}.json', 'w', encoding = 'utf-8') as f:
                f.write(dumpdata)
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name=f"{str(interaction.user)} 註冊成功!", value=f'職業:{select.values[0]}', inline=True)
            await interaction.response.send_message(embed = embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name=f"{str(interaction.user)} 註冊失敗!", value=f'你已經註冊過了!', inline=True)
            await interaction.response.send_message(embed = embed)
    select.callback = inte
    view = View(timeout = None)
    view.add_item(select)

    embed=discord.Embed(color=0xee4f9e)
    embed.add_field(name=f"註冊RPG帳號", value=f'請選擇一個職業', inline=True)
    
    await ctx.send(embed = embed,view = view)
@rpg.command()
async def me(ctx):
    if os.path.exists(f'RPG/{str(ctx.author.id)}.json'):
        with open(f'RPG/{str(ctx.author.id)}.json', 'r', encoding = 'utf-8') as f:
            d1 = json.load(f)
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name=f"{str(ctx.author)}", value=f'職業:{d1["job"]}', inline=False)
        embed.add_field(name=f"生命值", value=d1["hp"], inline=True)
        embed.add_field(name=f"體力值", value=d1["body"], inline=True)
        embed.add_field(name=f"金錢", value=d1["money"], inline=True)
        embed.add_field(name=f"等級", value=d1["lev"], inline=True)
        embed.add_field(name=f"經驗值", value=d1["exp"], inline=True)
        await ctx.send(embed = embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name=f"你還沒註冊!", value=f'你尚未註冊RPG帳號!\n請使用>>rpg register註冊!', inline=False)
        await ctx.send(embed = embed)
@rpg.command()
async def farm(ctx):
    if os.path.exists(f'RPG/{str(ctx.author.id)}.json'):
        with open(f'RPG/{str(ctx.author.id)}.json', 'r', encoding = 'utf-8') as f:
            d1 = json.load(f)
        if d1['job'] == "農夫":
            if d1['body'] >= 3:
                ranev = random.randint(1, 10)
                if ranev != 1:
                    multiper = 0.9
                    for i in range(d1['lev']):
                        multiper += 0.1
                    d1['exp'] += 3*multiper
                    d1['body'] -= 3
                    a1 = random.randint(1,3)
                    if a1 == 1:
                        a2 = random.randint(1, 3)
                        for i in range(a2):
                            d1['bp'].append('小麥')
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name=f"經過辛苦耕作...", value=f'你獲得了{str(a2)}個小麥!', inline=False)
                        await ctx.send(embed = embed)
                    elif a1 == 2:
                        a2 = random.randint(2, 5)
                        for i in range(a2):
                            d1['bp'].append('胡蘿蔔')
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name=f"經過辛苦耕作...", value=f'你獲得了{str(a2)}個胡蘿蔔!', inline=False)
                        await ctx.send(embed = embed)
                    elif a1 == 3:
                        a2 = random.randint(2, 5)
                        for i in range(a2):
                            d1['bp'].append('馬鈴薯')
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name=f"經過辛苦耕作...", value=f'你獲得了{str(a2)}個馬鈴薯!', inline=False)
                        await ctx.send(embed = embed)

                    if d1['exp'] >= d1['nextlev']:
                        d1['lev'] += 1
                        d1['exp'] -= d1['nextlev']
                        d1['nextlev'] *= 1.4
                else:
                    d1['body'] -= 3
                    event = random.randint(1, 2)
                    if event == 1:
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name=f"你噴農藥時噴到自己", value=f'HP-3, so sad.', inline=False)
                        await ctx.send(embed = embed)
                    elif event == 2:
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name=f"你耕作時跌進水圳", value=f'HP-3, 小心腳邊.', inline=False)
                        await ctx.send(embed = embed)
                dumpdata = json.dumps(d1, ensure_ascii = False)
                with open(f'RPG/{str(ctx.author.id)}.json', 'w', encoding = 'utf-8') as f:
                    f.write(dumpdata)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name=f"體力值不足!", value=f'工作之餘也要休息喔!', inline=False)
                await ctx.send(embed = embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name=f"你的職業不是農夫", value=f'你的職業是:{d1["job"]}', inline=False)
            await ctx.send(embed = embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name=f"你還沒註冊!", value=f'你尚未註冊RPG帳號!\n請使用>>rpg register註冊!', inline=False)
        await ctx.send(embed = embed)
@rpg.command()
async def mine(ctx):
    if os.path.exists(f'RPG/{str(ctx.author.id)}.json'):
        with open(f'RPG/{str(ctx.author.id)}.json', 'r', encoding = 'utf-8') as f:
            d1 = json.load(f)
        if d1['job'] == "礦工":
            if d1['body'] >= 3:
                ranev = random.randint(1, 10)
                if ranev != 1:
                    multiper = 0.9
                    for i in range(d1['lev']):
                        multiper += 0.1
                    d1['exp'] += 3*multiper
                    d1['body'] -= 3
                    a1 = random.randint(1, 100)
                    if a1 > 0 and a1 <= 40:
                        a2 = random.randint(5, 8)
                        for i in range(a2):
                            d1['bp'].append('煤炭')
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name=f"經過辛苦挖掘...", value=f'你獲得了{str(a2)}個煤炭!', inline=False)
                        await ctx.send(embed = embed)
                    elif a1 > 40 and a1 <= 70:
                        a2 = random.randint(2, 5)
                        for i in range(a2):
                            d1['bp'].append('鐵礦')
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name=f"經過辛苦挖掘...", value=f'你獲得了{str(a2)}個鐵礦!', inline=False)
                        await ctx.send(embed = embed)
                    elif a1 > 70 and a1 <= 80:
                        a2 = random.randint(1, 3)
                        for i in range(a2):
                            d1['bp'].append('黃金')
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name=f"經過辛苦挖掘...", value=f'你獲得了{str(a2)}個黃金!', inline=False)
                        await ctx.send(embed = embed)
                    elif a1 > 80 and a1 <= 85:
                        a2 = random.randint(1, 3)
                        for i in range(a2):
                            d1['bp'].append('鑽石')
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name=f"經過辛苦挖掘...", value=f'你獲得了{str(a2)}個鑽石!', inline=False)
                        await ctx.send(embed = embed)
                    elif a1 > 85 and a1 <= 100:
                        a2 = random.randint(1, 3)
                        for i in range(a2):
                            d1['bp'].append('鋁礦')
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name=f"經過辛苦挖掘...", value=f'你獲得了{str(a2)}個鋁礦!', inline=False)
                        await ctx.send(embed = embed)

                    if d1['exp'] >= d1['nextlev']:
                        d1['lev'] += 1
                        d1['exp'] -= d1['nextlev']
                        d1['nextlev'] *= 1.4
                else:
                    d1['body'] -= 3
                    event = random.randint(1, 3)
                    if event == 1:
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name=f"青青石", value=f'HP-3, 青青對不起.', inline=False)
                        await ctx.send(embed = embed)
                    elif event == 2:
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name=f"用稿子砸自己的腳", value=f'HP-3, 下次使用稿子時小心一點.', inline=False)
                        await ctx.send(embed = embed)
                    elif event == 3:
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name=f"被落石砸中", value=f'HP-3, 落石注意.', inline=False)
                        await ctx.send(embed = embed)
                dumpdata = json.dumps(d1, ensure_ascii = False)
                with open(f'RPG/{str(ctx.author.id)}.json', 'w', encoding = 'utf-8') as f:
                    f.write(dumpdata)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name=f"體力值不足!", value=f'工作之餘也要休息喔!', inline=False)
                await ctx.send(embed = embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name=f"你的職業不是礦工", value=f'你的職業是:{d1["job"]}', inline=False)
            await ctx.send(embed = embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name=f"你還沒註冊!", value=f'你尚未註冊RPG帳號!\n請使用>>rpg register註冊!', inline=False)
        await ctx.send(embed = embed)
@rpg.command()
async def hunt(ctx):
    if os.path.exists(f'RPG/{str(ctx.author.id)}.json'):
        with open(f'RPG/{str(ctx.author.id)}.json', 'r', encoding = 'utf-8') as f:
            d1 = json.load(f)
        if d1['job'] == "獵人":
            if d1['body'] >= 3:
                ranev = random.randint(1, 10)
                if ranev != 1:
                    multiper = 0.9
                    for i in range(d1['lev']):
                        multiper += 0.1
                    d1['exp'] += 3*multiper
                    d1['body'] -= 3
                    a1 = random.randint(1, 100)
                    if a1 > 0 and a1 <= 40:
                        a2 = random.randint(1, 3)
                        for i in range(a2):
                            d1['bp'].append('山豬肉')
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name=f"經過辛苦狩獵...", value=f'你獲得了{str(a2)}個山豬肉!', inline=False)
                        await ctx.send(embed = embed)
                    elif a1 > 40 and a1 <= 70:
                        a2 = random.randint(1, 3)
                        for i in range(a2):
                            d1['bp'].append('鹿肉')
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name=f"經過辛苦狩獵...", value=f'你獲得了{str(a2)}個鹿肉!', inline=False)
                        await ctx.send(embed = embed)
                    elif a1 > 70 and a1 <= 80:
                        a2 = random.randint(1, 3)
                        for i in range(a2):
                            d1['bp'].append('牛肉')
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name=f"經過辛苦狩獵...", value=f'你獲得了{str(a2)}個牛肉!', inline=False)
                        await ctx.send(embed = embed)
                    elif a1 > 80 and a1 <= 85:
                        a2 = random.randint(1, 3)
                        for i in range(a2):
                            d1['bp'].append('蟒蛇肉')
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name=f"經過辛苦狩獵...", value=f'你獲得了{str(a2)}個蟒蛇肉!', inline=False)
                        await ctx.send(embed = embed)

                    if d1['exp'] >= d1['nextlev']:
                        d1['lev'] += 1
                        d1['exp'] -= d1['nextlev']
                        d1['nextlev'] *= 1.4
                else:
                    d1['body'] -= 3
                    d1['hp'] -= 3
                    event = random.randint(1, 3)
                    if event == 1:
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name=f"被山豬撞", value=f'HP-3, 偶砸摳ㄟ檳榔加上小米酒，原住民ㄟ山豬丟溪溝溝搂.', inline=False)
                        await ctx.send(embed = embed)
                    elif event == 2:
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name=f"你不尊重狐，狐會生氣", value=f'HP-3, 請尊重狐.', inline=False)
                        await ctx.send(embed = embed)
                    elif event == 3:
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name=f"被蟒蛇咬", value=f'HP-3, 大滿蛇ㄟ.', inline=False)
                        await ctx.send(embed = embed)
                dumpdata = json.dumps(d1, ensure_ascii = False)
                with open(f'RPG/{str(ctx.author.id)}.json', 'w', encoding = 'utf-8') as f:
                    f.write(dumpdata)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name=f"體力值不足!", value=f'工作之餘也要休息喔!', inline=False)
                await ctx.send(embed = embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name=f"你的職業不是獵人", value=f'你的職業是:{d1["job"]}', inline=False)
            await ctx.send(embed = embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name=f"你還沒註冊!", value=f'你尚未註冊RPG帳號!\n請使用>>rpg register註冊!', inline=False)
        await ctx.send(embed = embed)
@rpg.command()
async def bp(ctx):
    if os.path.exists(f'RPG/{str(ctx.author.id)}.json'):
        with open(f'RPG/{str(ctx.author.id)}.json', 'r', encoding = 'utf-8') as f:
            d1 = json.load(f)
        diction = Counter(d1['bp'])
        msg = ""
        for i in diction:
            msg += f'{i} x{str(diction[i])}\n'
        user = bot.get_user(ctx.author.id)
        if user is not None:
            if user.dm_channel is None:
                await user.create_dm()
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name=f"你的背包", value=msg, inline=False)
            await user.dm_channel.send(embed = embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name=f"你還沒註冊!", value=f'你尚未註冊RPG帳號!\n請使用>>rpg register註冊!', inline=False)
        await ctx.send(embed = embed)
@rpg.command()
async def sell(ctx, name:str, amount:int):
    if os.path.exists(f'RPG/{str(ctx.author.id)}.json'):
        tfille = True
        for i in price:
            if i == name:
                tfille = False
        if tfille == False:
            with open(f'RPG/{str(ctx.author.id)}.json', 'r', encoding = 'utf-8') as f:
                d1 = json.load(f)
            diction = Counter(d1['bp'])
            if diction[name] >= amount:
                d1['money'] += price[name] * amount
                diction[name] -= amount
                nbp = []
                for j in diction:
                    for awa in range(diction[j]):
                        nbp.append(j)
                d1['bp'] = nbp
                dumpdata = json.dumps(d1, ensure_ascii = False)
                with open(f'RPG/{str(ctx.author.id)}.json', 'w', encoding = 'utf-8') as f:
                    f.write(dumpdata)
                
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name=f"販賣成功!", value=f'你獲得了{str(d1["money"])}元!', inline=False)
                await ctx.send(embed = embed)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name=f"販賣失敗!", value=f'你的背包沒有{str(amount)}個{name}!', inline=False)
                await ctx.send(embed = embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name=f"你知道這是什麼嗎?", value=f'你知道這個東西其實不能賣嗎?', inline=False)
            await ctx.send(embed = embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name=f"你還沒註冊!", value=f'你尚未註冊RPG帳號!\n請使用>>rpg register註冊!', inline=False)
        await ctx.send(embed = embed)
@rpg.command()
async def eat(ctx):
    if os.path.exists(f'RPG/{str(ctx.author.id)}.json'):
        wt8 = loadset(0)
        options = []
        for i, it in enumerate(wt8['item']):
            options.append(discord.SelectOption(label=it, description=f"價格:{str(wt8['price'][i])}"))
        select = Select(placeholder="選擇一個食物!",
            options=options)
        async def inte(interaction):
            if os.path.exists(f'RPG/{str(interaction.user.id)}.json'):
                with open(f'RPG/{str(interaction.user.id)}.json', 'r', encoding = 'utf-8') as f:
                    d1 = json.load(f)
                itemindex = -1
                for i in wt8['item']:
                    itemindex += 1
                    if i == select.values[0]:
                        break
                if d1['money'] >= wt8['price'][itemindex]:
                    d1['money'] -= wt8['price'][itemindex]
                    d1['hp'] += wt8['hunger'][itemindex]
                    if d1['hp'] > 20:
                        d1['hp'] = 20
                    dumpdata = json.dumps(d1, ensure_ascii = False)
                    with open(f'RPG/{str(ctx.author.id)}.json', 'w', encoding = 'utf-8') as f:
                        f.write(dumpdata)
                    embed=discord.Embed(color=0xee4f9e)
                    embed.add_field(name=f"{str(interaction.user)}:你吃了一個**{select.values[0]}**", value=f'你的生命值(HP)回復到{str(d1["hp"])}\n你花費了{wt8["price"][itemindex]}元', inline=False)
                    await interaction.response.send_message(embed = embed)
                else:
                    embed=discord.Embed(color=0xee4f9e)
                    embed.add_field(name=f"{str(interaction.user)}:購買失敗!", value=f'你的錢不夠買一個**{select.values[0]}**', inline=False)
                    await interaction.response.send_message(embed = embed)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name=f"{str(interaction.user)}:你還沒註冊!", value=f'你尚未註冊RPG帳號!\n請使用>>rpg register註冊!', inline=False)
                await interaction.response.send_message(embed = embed)
        select.callback = inte
        view = View(timeout = None)
        view.add_item(select)

        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name=f"食物選擇", value=f'請選擇你要吃的食物', inline=False)
        await ctx.send(embed = embed, view = view)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name=f"你還沒註冊!", value=f'你尚未註冊RPG帳號!\n請使用>>rpg register註冊!', inline=False)
        await ctx.send(embed = embed)

#@bot.command()
#async def feed(ctx, amount:int, name:str):
#    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
#        gid = ctx.guild.id
#        lan_set = loadset(gid)
#        langpack = loadlang(lan_set["lang"])
#        
#        if amount >= 0:
#            try:
#                gid = int(ctx.guild.id)
#                if os.path.exists(f'settings/{str(gid)}.json'):
#                    wt7 = loadset(gid)
#                    wt8 = loadset(0)
#                    titemt = False
#                    whn = 0
#                    for n in range(len(wt8['item'])):
#                        if wt8['item'][n] == name:
#                            titemt = True
#                            whn = n
#                    if titemt == True:
#                        tprice = wt8['price'][whn] * amount
#                        if int(wt7['guildmon']) >= tprice:
#                            rgmon = int(wt7['guildmon']) - tprice
#                            wt7['guildmon'] = rgmon
#                            writeset(gid, wt7)
#                            embed=discord.Embed(color=0xee4f9e)
#                            embed.add_field(name=langpack['feed.success.deal.title.title'], value=langpack['feed.success.deal.title.msg.p1'] + f"{str(tprice)}"+langpack['feed.success.deal.title.msg.p2']+f"{str(amount)}"+langpack['feed.success.deal.title.msg.p3']+f"{name}\n"+langpack['feed.success.deal.title.msg.p4'], inline=True)
#                            embed.set_footer(text = langpack['feed.success.deal.footer']+f'{str(rgmon)}')
#                            await ctx.send(embed=embed)
#                            await ctx.send(langpack['feed.eating.p1'])
#                            await asyncio.sleep(0.5)
#                            await ctx.send(langpack['feed.eating.p2'])
#                            await asyncio.sleep(3)
#                            await ctx.send(langpack['feed.eating.p3'])
#                            wt10 = loadset(gid)
#                            wt10["botexp"] += tprice
#                            writeset(gid, wt10)
#                            embed=discord.Embed(color=0xee4f9e)
#                            embed.add_field(name=langpack['feed.exp'], value=f"{tprice}", inline=True)
#                            await ctx.send(embed=embed)
#                        else:
#                            embed=discord.Embed(color=0xee4f9e)
#                            embed.add_field(name=langpack['feed.nomoney.title'], value=langpack['feed.nomoney.msg']+f"{str(amount)}"+langpack['feed.success.deal.title.msg.p3']+f"{name}", inline=True)
#                            await ctx.send(embed=embed)
#                    else:
#                        embed=discord.Embed(color=0xee4f9e)
#                        embed.add_field(name=langpack['feed.notfound.title'], value=langpack['feed.notfound.msg'], inline=True)
#                        await ctx.send(embed=embed)
#            except:
#                embed=discord.Embed(color=0xee4f9e)
#                embed.add_field(name="ERROR", value=langpack['err.message'], inline=True)
#                await ctx.send(embed=embed)
#        else:
#            embed=discord.Embed(color=0xee4f9e)
#            embed.add_field(name=langpack['feed.negative.title'], value=langpack['feed.negative.msg'], inline=True)
#            await ctx.send(embed=embed) 
#    else:
#        embed=discord.Embed(color=0xee4f9e)
        #embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        #await ctx.send(embed=embed)
#@bot.command()
#async def botboard(ctx):
#    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
#        gid = ctx.guild.id
#        lan_set = loadset(gid)
#        langpack = loadlang(lan_set["lang"])
#        
#        gid = ctx.guild.id
#        if os.path.exists(f'settings/{str(gid)}.json'):
#            #try:
#                files = glob.glob('settings/*.json')
#                bexps = []
#                tsrank = 0
#                for fi in files:
#                    ff1, ss1 = os.path.split(fi)
#                    f2 = ss1.replace('.json', '')
#                    wt14 = loadset(f2)
#                    bexps.append(int(wt14['botexp']))
#                bexps.sort()
#                bexps.reverse()
#                bexps3 = bexps
#                try:
#                    bexp1 = bexps3[0]
#                except:
#                    bexp1 = 'none'
#                try:
#                    bexp2 = bexps3[1]
#                except:
#                    bexp2 = 'none'
#                try:
#                    bexp3 = bexps[2]
#                except:
#                    bexp3 = 'none'
#                wt16 = loadset(gid)
#                for be3 in range(len(bexps3)):
#                    if int(bexps3[be3]) == int(wt16['botexp']):
#                        tsrank = be3
#                bgid1 = ''
#                bgid2 = ''
#                bgid3 = ''
#                files2 = glob.glob('settings/*.json')
#                for f2 in files2:
#                    fgid, ffgid = os.path.split(f2)
#                    fgid2 = ffgid.replace('.json', '')
#                    tgid = int(fgid2)
#                    wt15 = loadset(tgid)
#                    if int(bexp1) == int(wt15['botexp']):
#                        bgid1 = str(bot.get_guild(tgid))
#                    elif int(bexp2) == int(wt15['botexp']):
#                        bgid2 = str(bot.get_guild(tgid))
#                    elif int(bexp3) == int(wt15['botexp']):
#                        bgid3 = str(bot.get_guild(tgid))
#                if bgid1 == '':
#                    bgid1 = 'none'
#                if bgid2 == '':
#                    bgid2 = 'none'
#                if bgid3 == '':
#                    bgid3 = 'none'
#                embed=discord.Embed(title=langpack['botboard.title.title'], description=langpack['botboard.title.msg']+f"{str(int(len(files)))}", color = 0xee4f9e)
#                embed.add_field(name=langpack['botboard.gold']+f"{str(bgid1)}", value=langpack['botboard.exp']+f"{str(bexp1)}", inline=False)
#                embed.add_field(name=langpack['botboard.sliver']+f"{str(bgid2)}", value=langpack['botboard.exp']+f"{str(bexp2)}", inline=False)
#                embed.add_field(name=langpack['botboard.bronze']+f"{str(bgid3)}", value=langpack['botboard.exp']+f"{str(bexp3)}", inline=False)
#                embed.set_footer(text=langpack['botboard.ranking']+f"{str(tsrank+1)}\n"+langpack['botboard.expguild']+f"{str(wt16['botexp'])}")
#                await ctx.send(embed=embed)
#            #except:
#            #    embed=discord.Embed(color=0xee4f9e)
#            #    embed.add_field(name="ERROR!", value=langpack['err.message'], inline=True)
#            #    await ctx.send(embed=embed) 
#        else:
#            embed=discord.Embed(color=0xee4f9e)
#            embed.add_field(name="此伺服器還沒setup過!", value="使用>>setup以進行設定!", inline=True)
#            await ctx.send(embed=embed)
#    else:
#        embed=discord.Embed(color=0xee4f9e)
        #embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        #await ctx.send(embed=embed)

@bot.command()
async def 愛蓮說(ctx):
    embed=discord.Embed(color=0xee4f9e)
    embed.add_field(name="愛蓮說-周敦頤", value="水陸草木之花，可愛者甚蕃。晉陶淵明獨愛菊。自李唐來，世人甚愛牡丹。予獨愛蓮之出淤泥而不染，濯清漣而不妖；中通外直，不蔓不枝；香遠益清，亭亭淨植，可遠觀而不可褻玩焉。\n予謂：菊，花之隱逸者也；牡丹，花之富貴者也；蓮，花之君子者也。\n噫！菊之愛，陶後鮮有聞。蓮之愛，同予者何人？牡丹之愛，宜乎眾矣！", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def setlang(ctx):
    au = ctx.author
    roles = au.roles
    isa = 0
    for a in roles:
        for c in a.permissions:
            if c[0] == 'administrator' and c[1] == True:
                isa = 1
    if isa == 1:
        if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
            gid = ctx.guild.id
            try:
                select = Select(placeholder="選擇一個語言",
                options=[
                    discord.SelectOption(label='繁體中文'),
                    discord.SelectOption(label='English')
                ])
                async def inte(interaction):
                    wt50 = loadset(gid)
                    if select.values[0] == "繁體中文":
                        pack = "zh-tw"
                    elif select.values[0] == "English":
                        pack = "eng"
                    wt50['lang'] = pack+'.json'
                    writeset(gid, wt50)

                    view = View(timeout = None)
                    view.add_item(Button(label="完成!", style=discord.ButtonStyle.green, disabled=True))

                    await interaction.response.edit_message(view=view)
                
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="選擇語言", value="使用下方的選單選擇語言", inline=True)

                select.callback = inte
                view = View(timeout = None)
                view.add_item(select)

                await ctx.send(embed = embed, view = view)
            except:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="ERROR!", value="I can't run this command.", inline=True)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)

@bot.group()
async def tvc(ctx):
    pass
@tvc.command()
async def create(ctx, id:int):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        au = ctx.author
        roles = au.roles
        isa = 0
        for a in roles:
            for c in a.permissions:
                if c[0] == 'administrator' and c[1] == True:
                    isa = 1
        if isa == 1:
            channel = bot.get_channel(id)
            if str(channel.type) == 'voice':
                wt1 = loadset(ctx.guild.id)
                alexist = False
                for chid in wt1['tvc']:
                    if chid == id:
                        alexist = True
                        break
                if alexist == False:
                    wt1['tvc'].append(id)
                    writeset(ctx.guild.id, wt1)
                    embed=discord.Embed(color=0xee4f9e)
                    embed.add_field(name="設定完成!", value=f"頻道id:{str(id)}", inline=True)
                    await ctx.send(embed=embed)
                else:
                    embed=discord.Embed(color=0xee4f9e)
                    embed.add_field(name="錯誤!", value=f"本頻道已經被設定為暫存語音頻道!", inline=True)
                    await ctx.send(embed=embed)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="錯誤!", value=f"ID指向的頻道不是語音頻道\n請提供語音頻道的id", inline=True)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="抱歉!", value=f"你沒有權限執行這條指令!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@tvc.command()
async def delete(ctx, id:int):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        au = ctx.author
        roles = au.roles
        isa = 0
        for a in roles:
            for c in a.permissions:
                if c[0] == 'administrator' and c[1] == True:
                    isa = 1
        if isa == 1:
            wt1 = loadset(ctx.guild.id)
            exist = False
            tvc2 = []
            for chid in wt1['tvc']:
                if chid == id:
                    exist = True
                    continue
                tvc2.append(chid)
            wt1['tvc'] = tvc2
            writeset(ctx.guild.id, wt1)
            if exist == True:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="刪除成功!", value=f"頻道id:{str(id)}", inline=True)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="錯誤!", value=f"ID指向的頻道不是語音頻道\n請提供語音頻道的id", inline=True)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="抱歉!", value=f"你沒有權限執行這條指令!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@tvc.command()
async def list(ctx):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        wt1 = loadset(ctx.guild.id)
        text = '暫存語音頻道列表\n'
        n = 0
        for chid in wt1['tvc']:
            channel = bot.get_channel(chid)
            text += f'[{str(n)}]{str(channel)}({str(channel.id)})'
            n += 1
        await ctx.send(text)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@tvc.command()
async def lock(ctx):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        voice = ctx.author.voice
        if voice.channel.name == f"{str(ctx.author)}'s private channel":
            if ctx.author.name == voice.channel.name.replace("'s private channel", ''):
                channel = bot.get_channel(voice.channel.id)
                roles = ctx.guild.roles
                overwrite = discord.PermissionOverwrite()
                overwrite.view_channel = True
                for m in channel.members:
                    await channel.set_permissions(m, overwrite = overwrite)
                overwrite2 = discord.PermissionOverwrite()
                overwrite2.view_channel = False
                for r in roles:
                    await channel.set_permissions(r, overwrite = overwrite2)
                await ctx.send('Locked.')
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="抱歉!", value=f"你不是這個私人語音頻道的擁有者!", inline=True)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="錯誤!", value=f"你不在一個私人語音頻道中!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@tvc.command()
async def unlock(ctx):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        voice = ctx.author.voice
        if voice.channel.name == f"{str(ctx.author)}'s private channel":
            if ctx.author.name == voice.channel.name.replace("'s private channel", ''):
                channel = bot.get_channel(voice.channel.id)
                roles = ctx.guild.roles
                overwrite = discord.PermissionOverwrite()
                overwrite.view_channel = True
                for m in channel.members:
                    await channel.set_permissions(m, overwrite = overwrite)
                for r in roles:
                    await channel.set_permissions(r, overwrite = overwrite)
                await ctx.send('Unlocked.')
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="抱歉!", value=f"你不是這個私人語音頻道的擁有者!", inline=True)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="錯誤!", value=f"你不在一個私人語音頻道中!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@tvc.command()
async def add(ctx, tuser):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        voice = ctx.author.voice
        if voice.channel.name == f"{str(ctx.author)}'s private channel":
            if ctx.author.name == voice.channel.name.replace("'s private channel", ''):
                channel = bot.get_channel(voice.channel.id)
                user = bot.get_user(int(tuser.replace('<', '').replace('@', '').replace('!', '').replace('>', '')))
                overwrite = discord.PermissionOverwrite()
                overwrite.view_channel = True
                overwrite.connect = True
                overwrite.priority_speaker = False
                overwrite.speak = True
                overwrite.stream = True
                overwrite.use_voice_activation = True
                overwrite.move_members = False
                overwrite.manage_channels = False
                overwrite.manage_permissions = False
                overwrite.deafen_members = False
                overwrite.mute_members = False
                await channel.set_permissions(user, overwrite = overwrite)
                await ctx.send('Added!')
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="抱歉!", value=f"你不是這個私人語音頻道的擁有者!", inline=True)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="錯誤!", value=f"你不在一個私人語音頻道中!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@tvc.command()
async def kick(ctx, tuser):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        voice = ctx.author.voice
        if voice.channel.name == f"{str(ctx.author)}'s private channel":
            if ctx.author.name == voice.channel.name.replace("'s private channel", ''):
                channel = bot.get_channel(voice.channel.id)
                user = bot.get_user(int(tuser.replace('<', '').replace('@', '').replace('!', '').replace('>', '')))
                overwrite = discord.PermissionOverwrite()
                overwrite.view_channel = False
                await channel.set_permissions(user, overwrite = overwrite)
                await ctx.send('Kicked!')
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="抱歉!", value=f"你不是這個私人語音頻道的擁有者!", inline=True)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="錯誤!", value=f"你不在一個私人語音頻道中!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@bot.event
async def on_voice_state_update(member, before, after):
    ist = False
    if (after.channel != None and before.channel == None):
        ist = True
        gid = after.channel.guild.id
        wt1 = loadset(gid)
        isit = False
        for chid in wt1['tvc']:
            if chid == after.channel.id:
                isit = True
                break
        if isit == True:
            voice = member.guild.channels
            found = False
            for v in voice:
                if v.name == f"{str(member)}'s private channel" and str(v.type) == 'voice':
                    await member.move_to(v)
                    found = True
                    break
            if found == False:
                tcategory = after.channel.category
                tchannel = await after.channel.guild.create_voice_channel(f"{str(member)}'s private channel", category = tcategory)
                await member.move_to(tchannel)
    elif (after.channel != None and before.channel != None):
        if not(after.channel == before.channel):
            ist = True
            gid = after.channel.guild.id
            wt1 = loadset(gid)
            isit = False
            for chid in wt1['tvc']:
                if chid == after.channel.id:
                    isit = True
                    break
            if isit == True:
                voice = member.guild.channels
                found = False
                for v in voice:
                    if v.name == f"{str(member)}'s private channel" and str(v.type) == 'voice':
                        await member.move_to(v)
                        found = True
                        break
                if found == False:
                    tcategory = after.channel.category
                    tchannel = await after.channel.guild.create_voice_channel(f"{str(member)}'s private channel", category = tcategory)
                    await member.move_to(tchannel)
            else:
                if "'s private channel" in before.channel.name:
                    if len(before.channel.members) == 0:
                        await before.channel.delete()
    if ist == False:
        if "'s private channel" in before.channel.name:
            if len(before.channel.members) == 0:
                await before.channel.delete()

@bot.group()
async def rr(ctx):
    pass
@rr.command()
async def new(ctx, msgid:int, emoji, role):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        try:
            au = ctx.author
            roles = au.roles
            isa = 0
            for a in roles:
                for c in a.permissions:
                    if c[0] == 'administrator' and c[1] == True:
                        isa = 1
            if isa == 1:
                message = await ctx.channel.fetch_message(msgid)
                await message.add_reaction(emoji)
                trole = str(role).replace('<', '').replace('>', '').replace('@', '').replace('&', '')
                tdict = {'msgid':int(msgid), "emoji":str(emoji), "role":int(trole)}
                wt1 = loadset(ctx.guild.id)
                wt1['rr'].append(tdict)
                writeset(ctx.guild.id, wt1)
                await ctx.send("Done!")
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="抱歉!", value=f"你沒有權限執行這條指令!", inline=True)
                await ctx.send(embed=embed)
        except:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="錯誤!", value=f"執行指令時發生錯誤!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@rr.command()
async def remove(ctx, msgid:int, emoji):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        try:
            au = ctx.author
            roles = au.roles
            isa = 0
            for a in roles:
                for c in a.permissions:
                    if c[0] == 'administrator' and c[1] == True:
                        isa = 1
            if isa == 1:
                wt1 = loadset(ctx.guild.id)
                rr2 = []
                tf = False
                for r in wt1['rr']:
                    if r['msgid'] == msgid:
                        if r['emoji'] == str(emoji):
                            tf = True
                            continue
                    rr2.append(r)
                if tf == False:
                    embed=discord.Embed(color=0xee4f9e)
                    embed.add_field(name="錯誤!", value=f"指定的訊息與Reaction並沒有被設定reaction roles", inline=True)
                    await ctx.send(embed=embed)
                else:
                    wt1['rr'] = rr2
                    writeset(ctx.guild.id, wt1)
                    embed=discord.Embed(color=0xee4f9e)
                    embed.add_field(name="成功!", value=f"刪除完成", inline=True)
                    await ctx.send(embed=embed)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="抱歉!", value=f"沒有權限執行這條指令!", inline=True)
                await ctx.send(embed=embed)
        except:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="錯誤!", value=f"執行指令時發生錯誤!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@rr.command()
async def list(ctx):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        try:
            au = ctx.author
            roles = au.roles
            isa = 0
            for a in roles:
                for c in a.permissions:
                    if c[0] == 'administrator' and c[1] == True:
                        isa = 1
            if isa == 1:
                wt1 = loadset(ctx.guild.id)
                msg = '訊息id/emoji/身分組名稱\n'
                roles = ctx.guild.roles
                for r in wt1['rr']:
                    for tr in roles:
                        if tr.id == r['role']:
                            role = tr
                            break
                    msg += f'{str(r["msgid"])}/{str(r["emoji"])}/{str(role)}\n'
                await ctx.send(msg)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="抱歉!", value=f"沒有權限執行這條指令!", inline=True)
                await ctx.send(embed=embed)
        except:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="錯誤!", value=f"執行指令時發生錯誤!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@rr.command()
async def userbladd(ctx, msgid, emoji, tag):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        au = ctx.author
        roles = au.roles
        isa = 0
        for a in roles:
            for c in a.permissions:
                if c[0] == 'administrator' and c[1] == True:
                    isa = 1
        if isa == 1:
            userid = str(tag).replace('<', '').replace('@', '').replace('!', '').replace('>', '')
            wt1 = loadset(ctx.guild.id)
            tf22 = False
            for r in wt1['rr']:
                if str(r['msgid']) == str(msgid) and str(r['emoji']) == str(emoji):
                    tf22 = True
                    break
            if tf22 == False:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="錯誤!", value=f"指定的訊息與Reaction並沒有被設定reaction roles!", inline=True)
                await ctx.send(embed=embed)
            else:
                wt1['rrbl'].append({'msgid':msgid, 'emoji':str(emoji), 'userid':userid})
                writeset(ctx.guild.id, wt1)
                await ctx.send(f'已成功將用戶id{str(userid)}加入指定訊息的Reaction的黑名單!')
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="抱歉!", value=f"沒有權限執行這條指令!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@rr.command()
async def rolebladd(ctx, msgid, emoji, tag):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        au = ctx.author
        roles = au.roles
        isa = 0
        for a in roles:
            for c in a.permissions:
                if c[0] == 'administrator' and c[1] == True:
                    isa = 1
        if isa == 1:
            userid = str(tag).replace('<', '').replace('@', '').replace('&', '').replace('>', '')
            wt1 = loadset(ctx.guild.id)
            tf22 = False
            for r in wt1['rr']:
                if str(r['msgid']) == str(msgid) and str(r['emoji']) == str(emoji):
                    tf22 = True
                    break
            if tf22 == False:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="錯誤!", value=f"指定的訊息與Reaction並沒有被設定reaction roles!", inline=True)
                await ctx.send(embed=embed)
            else:
                wt1['rolerrbl'].append({'msgid':msgid, 'emoji':str(emoji), 'roleid':userid})
                writeset(ctx.guild.id, wt1)
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="成功!", value=f"已成功將身分組id{str(userid)}加入指定訊息的Reaction的黑名單!", inline=True)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="抱歉!", value=f"沒有權限執行這條指令!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@rr.command()
async def rolebldelete(ctx, msgid, emoji, tag):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        au = ctx.author
        roles = au.roles
        isa = 0
        for a in roles:
            for c in a.permissions:
                if c[0] == 'administrator' and c[1] == True:
                    isa = 1
        if isa == 1:
            userid = str(tag).replace('<', '').replace('@', '').replace('&', '').replace('>', '')
            wt1 = loadset(ctx.guild.id)
            tf22 = False
            rr2 = []
            for r in wt1['rolerrbl']:
                if str(r['msgid']) == str(msgid) and str(r['emoji']) == str(emoji) and userid == str(r['roleid']):
                    tf22 = True
                    continue
                rr2.append(r)
            if tf22 == False:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="錯誤!", value=f"指定的訊息與Reaction並沒有被設定reaction roles!", inline=True)
                await ctx.send(embed=embed)
            else:
                wt1['rolerrbl'] = rr2
                writeset(ctx.guild.id, wt1)
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="成功!", value=f"已成功將身分組id{str(userid)}從指定訊息的Reaction的黑名單中移除!", inline=True)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="抱歉!", value=f"沒有權限執行這條指令!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@rr.command()
async def userbldelete(ctx, msgid, emoji, tag):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        au = ctx.author
        roles = au.roles
        isa = 0
        for a in roles:
            for c in a.permissions:
                if c[0] == 'administrator' and c[1] == True:
                    isa = 1
        if isa == 1:
            userid = str(tag).replace('<', '').replace('@', '').replace('!', '').replace('>', '')
            wt1 = loadset(ctx.guild.id)
            tf22 = False
            rr2 = []
            for r in wt1['rrbl']:
                if str(r['msgid']) == str(msgid) and str(r['emoji']) == str(emoji) and userid == str(r['userid']):
                    tf22 = True
                    continue
                rr2.append(r)
            if tf22 == False:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="錯誤!", value=f"指定的訊息與Reaction並沒有被設定reaction roles!", inline=True)
                await ctx.send(embed=embed)
            else:
                wt1['rrbl'] = rr2
                writeset(ctx.guild.id, wt1)
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="成功!", value=f"已成功將身分組id{str(userid)}從指定訊息的Reaction的黑名單中移除!", inline=True)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="抱歉!", value=f"沒有權限執行這條指令!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@rr.command()
async def bllist(ctx):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        au = ctx.author
        roles = au.roles
        isa = 0
        for a in roles:
            for c in a.permissions:
                if c[0] == 'administrator' and c[1] == True:
                    isa = 1
        if isa == 1:
            wt1 = loadset(ctx.guild.id)
            msg = 'Reaction Roles黑名單\n用戶黑名單\n訊息id/Emoji/用戶\n'
            for bl in wt1['rrbl']:
                msg += f'{bl["msgid"]}/{bl["emoji"]}/{bl["userid"]}\n'
            msg += '身分組黑名單\n訊息id/Emoji/身分組\n'
            for bl in wt1['rolerrbl']:
                msg += f'{bl["msgid"]}/{bl["emoji"]}/{bl["roleid"]}\n'
            await ctx.send(msg)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="抱歉!", value=f"沒有權限執行這條指令!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
    
@bot.event
async def on_raw_reaction_add(payload):
    try:
        wt1 = loadset(int(payload.guild_id))
        tr = None
        for r in wt1['rr']:
            if r['msgid'] == payload.message_id and r['emoji'] == payload.emoji.name:
                tr = r
                break
        if tr != None:
            canpick = True
            for bl in wt1['rrbl']:
                if int(bl['msgid']) == int(payload.message_id) and str(bl['emoji']) == str(payload.emoji.name) and int(bl['userid']) == int(payload.member.id):
                    canpick = False
            if canpick == True:
                au = payload.member
                roles = au.roles
                for bl in wt1['rolerrbl']:
                    for r in roles:
                        if int(bl['msgid']) == int(payload.message_id) and str(bl['emoji']) == str(payload.emoji.name) and int(bl['roleid']) == int(r.id):
                            canpick = False
            if canpick == True:
                guild = bot.get_guild(int(payload.guild_id))
                role = guild.get_role(tr['role'])
                if role != None:
                    await payload.member.add_roles(role, atomic = True)
    except:
        pass
@bot.event
async def on_raw_reaction_remove(payload):
    try:
        wt1 = loadset(int(payload.guild_id))
        tr = None
        for r in wt1['rr']:
            if r['msgid'] == payload.message_id and r['emoji'] == payload.emoji.name:
                tr = r
                break
        if tr != None:
            guild = bot.get_guild(int(payload.guild_id))
            members = guild.members
            member = None
            for m in members:
                if m.id == payload.user_id:
                    member = m
                    break
            canpick = True
            for bl in wt1['rrbl']:
                if int(bl['msgid']) == int(payload.message_id) and str(bl['emoji']) == str(payload.emoji.name) and int(bl['userid']) == int(member.id):
                    canpick = False
            if canpick == True:
                au = member
                roles = au.roles
                for bl in wt1['rolerrbl']:
                    for r in roles:
                        if int(bl['msgid']) == int(payload.message_id) and str(bl['emoji']) == str(payload.emoji.name) and int(bl['roleid']) == int(member.id):
                            canpick = False
            if canpick == True:
                guild = bot.get_guild(int(payload.guild_id))
                role = guild.get_role(tr['role'])
                if role != None:
                    members = guild.members
                    member = None
                    for m in members:
                        if m.id == payload.user_id:
                            member = m
                            break
                    if member != None:
                        await member.remove_roles(role, atomic = True)
    except:
        pass

@bot.group()
async def br(ctx):
    pass
@br.command()
async def new(ctx, role, title:str, *, content:str):
    try:
        au = ctx.author
        roles = au.roles
        isa = 0
        for a in roles:
            for c in a.permissions:
                if c[0] == 'administrator' and c[1] == True:
                    isa = 1
        if isa == 1:
            view = View(timeout = None)
            async def interaction_callback(interaction):
                try:
                    guild = bot.get_guild(int(ctx.guild.id))
                    roleid = int(str(role).replace('<', '').replace('@', '').replace('&', '').replace('>', ''))
                    role2 = guild.get_role(roleid)
                    member = guild.get_member(interaction.user.id)
                    roles = member.roles
                    rem = False
                    for a in roles:
                        if a.id == role2.id:
                            rem = True
                            break
                    if rem == False:
                        await member.add_roles(role2, atomic = True)
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name="Button Roles", value=f"已獲得 {role2.name} 身分組", inline=True)
                        await interaction.response.send_message(embed = embed, ephemeral=True)
                    else:
                        await member.remove_roles(role2, atomic = True)
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name="Button Roles", value=f"已移除 {role2.name} 身分組", inline=True)
                        await interaction.response.send_message(embed = embed, ephemeral=True)
                except:
                    embed=discord.Embed(color=0xee4f9e)
                    embed.add_field(name="Button Roles", value=f"獲取身分組時發生錯誤!", inline=True)
                    await interaction.response.send_message(embed = embed, ephemeral=True)

            guild = bot.get_guild(int(ctx.guild.id))
            roleid = int(str(role).replace('<', '').replace('@', '').replace('&', '').replace('>', ''))
            role2 = guild.get_role(roleid)
            try:
                button = Button(label = role2.name, style = discord.ButtonStyle.green)
            except:
                button = Button(label = role2.name, style = discord.ButtonStyle.green)
            button.callback = interaction_callback
            view.add_item(button)
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name=title, value=content, inline=True)
            await ctx.send(view = view, embed = embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="抱歉!", value=f"你沒有權限執行這條指令!", inline=True)
            await ctx.send(embed=embed)
    except:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="錯誤!", value=f"執行指令時發生錯誤!", inline=True)
        await ctx.send(embed=embed)

@bot.group()
async def welcome(ctx):
    pass
@welcome.command()
async def edit(ctx, *, msg:str):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        au = ctx.author
        roles = au.roles
        isa = 0
        for a in roles:
            for c in a.permissions:
                if c[0] == 'administrator' and c[1] == True:
                    isa = 1
        if isa == 1:
            wt1 = loadset(ctx.guild.id)
            wt1['welcome']['welmsg'] = msg
            writeset(ctx.guild.id, wt1)
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="成功!", value=f"歡迎訊息設定完成!", inline=True)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="抱歉!", value=f"沒有權限執行這條指令!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@welcome.command()
async def clear(ctx):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        au = ctx.author
        roles = au.roles
        isa = 0
        for a in roles:
            for c in a.permissions:
                if c[0] == 'administrator' and c[1] == True:
                    isa = 1
        if isa == 1:
            wt1 = loadset(ctx.guild.id)
            tfwel = False
            for wel in wt1['welcome']:
                if wel == "welmsg":
                    tfwel = True
            if tfwel == True:
                wt1['welcome']['welmsg'] = ""
                writeset(ctx.guild.id, wt1)
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="成功!", value=f'歡迎訊息已清除。', inline=True)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="抱歉!", value=f"沒有權限執行這條指令!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@welcome.command()
async def show(ctx):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        wt1 = loadset(ctx.guild.id)
        msg = ""
        tfwel = False
        for wel in wt1['welcome']:
            if wel == 'welmsg':
                tfwel = True
                msg = wt1['welcome']['welmsg']
        if tfwel == True:
            if msg == "":
                msg = '此伺服器尚未設置歡迎訊息!'
        else:
            msg = '此伺服器尚未設置歡迎訊息!'
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="目前的歡迎訊息", value=msg, inline=True)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@welcome.command()
async def toggle(ctx, option:str):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        au = ctx.author
        roles = au.roles
        isa = 0
        for a in roles:
            for c in a.permissions:
                if c[0] == 'administrator' and c[1] == True:
                    isa = 1
        if isa == 1:
            if option == 'True' or option == 'False':
                wt1 = loadset(ctx.guild.id)
                wt1['welcome']['weltoggle'] = option
                writeset(ctx.guild.id, wt1)
                ctf = ""
                if option == 'False':
                    ctf = '關閉'
                elif option == 'True':
                    ctf = '開啟'
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="已成功將歡迎訊息設定為", value=ctf, inline=True)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="錯誤", value='請輸入正確的參數(True或是False)!', inline=True)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="抱歉!", value=f"沒有權限執行這條指令!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@welcome.command()
async def channel(ctx):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        au = ctx.author
        roles = au.roles
        isa = 0
        for a in roles:
            for c in a.permissions:
                if c[0] == 'administrator' and c[1] == True:
                    isa = 1
        if isa == 1:
            wt1 = loadset(ctx.guild.id)
            wt1['welcome']['channel'] = ctx.channel.id
            writeset(ctx.guild.id, wt1)
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="成功!", value=f'已成功將歡迎訊息的頻道為:{ctx.channel.mention}', inline=True)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="抱歉!", value=f"沒有權限執行這條指令!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@welcome.command()
async def showch(ctx):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        try:
            wt1 = loadset(ctx.guild.id)
            tf2 = False
            for wel in wt1['welcome']:
                if wel == 'channel':
                    tf2 = True
            if tf2 == True:
                channel = bot.get_channel(wt1['welcome']['channel'])
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="目前的歡迎訊息頻道", value=f'{channel.mention}', inline=True)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="錯誤", value=f'歡迎訊息頻道尚未設定!', inline=True)
                await ctx.send(embed=embed)
        except:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="錯誤", value=f'執行指令時發生錯誤!', inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)

@welcome.command()
async def welrole(ctx, role):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        au = ctx.author
        roles = au.roles
        isa = 0
        for a in roles:
            for c in a.permissions:
                if c[0] == 'administrator' and c[1] == True:
                    isa = 1
        if isa == 1:
            wt1 = loadset(ctx.guild.id)
            wt1['welcome']['welrole'] = int(str(role).replace('<', '').replace('>', '').replace('@', '').replace('&', ''))
            writeset(ctx.guild.id, wt1)
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="設定完成!", value=f'成員一進去就可以領到的身分組', inline=True)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="抱歉!", value=f"沒有權限執行這條指令!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@welcome.command()
async def showrole(ctx):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        wt1 = loadset(ctx.guild.id)
        msg = ""
        tfwel = False
        for wel in wt1['welcome']:
            if wel == 'welrole':
                tfwel = True
                role = ctx.guild.get_role(int(wt1['welcome']['welrole']))
                msg = role.name
        if tfwel == True:
            if msg == "":
                msg = '此伺服器尚未設置!'
        else:
            msg = '此伺服器尚未設置!'
        await ctx.send(f'目前成員一進去就可以領到的身分組:{msg}')
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@welcome.command()
async def roletoggle(ctx, option:str):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        au = ctx.author
        roles = au.roles
        isa = 0
        for a in roles:
            for c in a.permissions:
                if c[0] == 'administrator' and c[1] == True:
                    isa = 1
        if isa == 1:
            if option == 'True' or option == 'False':
                wt1 = loadset(ctx.guild.id)
                wt1['welcome']['roletoggle'] = option
                writeset(ctx.guild.id, wt1)
                tf3 = ""
                if option == 'False':
                    tf3 = '關閉'
                elif option == 'True':
                    tf3 = '開啟'
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="已成功將成員一進去就可以領到的身分組的功能", value=f"{tf3}", inline=True)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="錯誤", value=f"請輸入正確的參數(True或是False)", inline=True)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="抱歉!", value=f"沒有權限執行這條指令!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@welcome.command()
async def weldm(ctx, *, msg:str):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        au = ctx.author
        roles = au.roles
        isa = 0
        for a in roles:
            for c in a.permissions:
                if c[0] == 'administrator' and c[1] == True:
                    isa = 1
        if isa == 1:
            wt1 = loadset(ctx.guild.id)
            wt1['welcome']['weldm'] = msg
            writeset(ctx.guild.id, wt1)
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="成功!", value=f"私人歡迎訊息設定完成!", inline=True)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="抱歉!", value=f"沒有權限執行這條指令!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@welcome.command()
async def dmshow(ctx):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        wt1 = loadset(ctx.guild.id)
        msg = ""
        tfwel = False
        for wel in wt1['welcome']:
            if wel == 'weldm':
                tfwel = True
                msg = wt1['welcome']['weldm']
        if tfwel == True:
            if msg == "":
                msg = '此伺服器尚未設置私人歡迎訊息!'
        else:
            msg = '此伺服器尚未設置私人歡迎訊息!'
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="目前的私人歡迎訊息", value=f"{msg}", inline=True)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@welcome.command()
async def dmtoggle(ctx, option:str):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        au = ctx.author
        roles = au.roles
        isa = 0
        for a in roles:
            for c in a.permissions:
                if c[0] == 'administrator' and c[1] == True:
                    isa = 1
        if isa == 1:
            if option == 'True' or option == 'False':
                wt1 = loadset(ctx.guild.id)
                wt1['welcome']['dmtoggle'] = option
                writeset(ctx.guild.id, wt1)
                tf3 = ''
                if option == 'False':
                    tf3 = '關閉'
                elif option == 'True':
                    tf3 = '開啟'
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="已成功將私人歡迎訊息設定為", value=f"{tf3}", inline=True)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="錯誤", value=f"請輸入正確的參數(True或是False)!", inline=True)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="抱歉!", value=f"沒有權限執行這條指令!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)

@bot.event
async def on_member_join(member):
    wt1 = loadset(member.guild.id)
    cando = [False, False, False]
    for wel in wt1['welcome']:
        if wel == 'welmsg':
            cando[0] = True
        if wel == 'weltoggle':
            cando[1] = True
        if wel == 'channel':
            cando[2] = True
    if cando == [True, True, True]:
        if wt1['welcome']['weltoggle'] == "True" and wt1['welcome']['welmsg'] != '':
            msg = wt1['welcome']['welmsg'].replace('>gname<', member.guild.name).replace('>tagm<', member.mention).replace('>mname<', member.name)
            channel = bot.get_channel(wt1['welcome']['channel'])
            await channel.send(msg)
    
    cando = [False, False]
    for wel in wt1['welcome']:
        if wel == 'welrole':
            cando[0] = True
        if wel == 'roletoggle':
            cando[1] = True
    if cando == [True, True]:
        if wt1['welcome']['roletoggle'] == "True" and wt1['welcome']['welrole'] != '':
            role = member.guild.get_role(int(wt1['welcome']['welrole']))
            await member.add_roles(role, atomic = True)
    
    cando = [False, False]
    for wel in wt1['welcome']:
        if wel == 'weldm':
            cando[0] = True
        if wel == 'dmtoggle':
            cando[1] = True
    if cando == [True, True]:
        if wt1['welcome']['dmtoggle'] == "True" and wt1['welcome']['weldm'] != '':
            user = bot.get_user(member.id)
            if user is not None:
                if user.dm_channel is None:
                    await user.create_dm()
                msg = wt1['welcome']['weldm'].replace('>gname<', member.guild.name).replace('>tagm<', member.mention).replace('>mname<', member.name)

                view = View()
                view.add_item(Button(label="來自:"+member.guild.name, style = discord.ButtonStyle.green, disabled=True))

                await user.dm_channel.send(msg, view = view)

@bot.group()
async def leave(ctx):
    pass
@leave.command()
async def edit(ctx, *, msg:str):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        au = ctx.author
        roles = au.roles
        isa = 0
        for a in roles:
            for c in a.permissions:
                if c[0] == 'administrator' and c[1] == True:
                    isa = 1
        if isa == 1:
            wt1 = loadset(ctx.guild.id)
            wt1['leave']['msg'] = msg
            writeset(ctx.guild.id, wt1)
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="成功!", value=f"離開訊息設定完成!", inline=True)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="抱歉!", value=f"沒有權限執行這條指令!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@leave.command()
async def clear(ctx):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        au = ctx.author
        roles = au.roles
        isa = 0
        for a in roles:
            for c in a.permissions:
                if c[0] == 'administrator' and c[1] == True:
                    isa = 1
        if isa == 1:
            wt1 = loadset(ctx.guild.id)
            tfwel = False
            for wel in wt1['leave']:
                if wel == "msg":
                    tfwel = True
            if tfwel == True:
                wt1['leave']['msg'] = ""
                writeset(ctx.guild.id, wt1)
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="成功!", value=f"離開訊息已清除!", inline=True)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="抱歉!", value=f"沒有權限執行這條指令!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@leave.command()
async def show(ctx):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        wt1 = loadset(ctx.guild.id)
        msg = ""
        tfwel = False
        for wel in wt1['leave']:
            if wel == 'msg':
                tfwel = True
                msg = wt1['leave']['msg']
        if tfwel == True:
            if msg == "":
                msg = '此伺服器尚未設置離開訊息!'
        else:
            msg = '此伺服器尚未設置離開訊息!'
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="目前的離開訊息", value=f"{msg}", inline=True)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@leave.command()
async def toggle(ctx, option:str):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        au = ctx.author
        roles = au.roles
        isa = 0
        for a in roles:
            for c in a.permissions:
                if c[0] == 'administrator' and c[1] == True:
                    isa = 1
        if isa == 1:
            if option == 'True' or option == 'False':
                wt1 = loadset(ctx.guild.id)
                wt1['leave']['toggle'] = option
                writeset(ctx.guild.id, wt1)
                ctf = ""
                if option == 'False':
                    ctf = '關閉'
                elif option == 'True':
                    ctf = '開啟'
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="已成功將離開訊息設定為", value=f"{ctf}", inline=True)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="錯誤", value=f"請輸入正確的參數(True或是False)!", inline=True)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="抱歉!", value=f"沒有權限執行這條指令!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@leave.command()
async def channel(ctx):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        au = ctx.author
        roles = au.roles
        isa = 0
        for a in roles:
            for c in a.permissions:
                if c[0] == 'administrator' and c[1] == True:
                    isa = 1
        if isa == 1:
            wt1 = loadset(ctx.guild.id)
            wt1['leave']['channel'] = ctx.channel.id
            writeset(ctx.guild.id, wt1)
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="已成功將離開訊息的頻道為", value=f"{ctx.channel.mention}", inline=True)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="抱歉!", value=f"沒有權限執行這條指令!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@leave.command()
async def showch(ctx):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        try:
            wt1 = loadset(ctx.guild.id)
            tf2 = False
            for wel in wt1['leave']:
                if wel == 'channel':
                    tf2 = True
            if tf2 == True:
                channel = bot.get_channel(wt1['leave']['channel'])
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="目前的離開訊息頻道", value=f"{channel.mention}", inline=True)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="錯誤", value=f"離開訊息頻道尚未設定!", inline=True)
                await ctx.send(embed=embed)
        except:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="錯誤", value=f"執行指令時發生錯誤", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)

@leave.command()
async def dm(ctx, *, msg:str):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        au = ctx.author
        roles = au.roles
        isa = 0
        for a in roles:
            for c in a.permissions:
                if c[0] == 'administrator' and c[1] == True:
                    isa = 1
        if isa == 1:
            wt1 = loadset(ctx.guild.id)
            wt1['leave']['dm'] = msg
            writeset(ctx.guild.id, wt1)
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="成功", value=f"私人離開訊息設定完成!", inline=True)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="抱歉!", value=f"沒有權限執行這條指令!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@leave.command()
async def dmshow(ctx):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        wt1 = loadset(ctx.guild.id)
        msg = ""
        tfwel = False
        for wel in wt1['leave']:
            if wel == 'dm':
                tfwel = True
                msg = wt1['leave']['dm']
        if tfwel == True:
            if msg == "":
                msg = '此伺服器尚未設置私人離開訊息!'
        else:
            msg = '此伺服器尚未設置私人離開訊息!'
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="目前的私人離開訊息", value=f"{msg}", inline=True)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)
@leave.command()
async def dmtoggle(ctx, option:str):
    if os.path.exists(f'settings/{str(ctx.guild.id)}.json'):
        au = ctx.author
        roles = au.roles
        isa = 0
        for a in roles:
            for c in a.permissions:
                if c[0] == 'administrator' and c[1] == True:
                    isa = 1
        if isa == 1:
            if option == 'True' or option == 'False':
                wt1 = loadset(ctx.guild.id)
                wt1['leave']['dmtoggle'] = option
                writeset(ctx.guild.id, wt1)
                tf3 = ''
                if option == 'False':
                    tf3 = '關閉'
                elif option == 'True':
                    tf3 = '開啟'
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="已成功將私人離開訊息設定為", value=f"{tf3}", inline=True)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="錯誤", value=f"請輸入正確的參數(True或是False)!", inline=True)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="抱歉!", value=f"沒有權限執行這條指令!", inline=True)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="設定檔遺失!", value=f"請使用>>resetup建立設定檔", inline=True)
        await ctx.send(embed=embed)

@bot.event
async def on_member_remove(member):
    wt1 = loadset(member.guild.id)
    cando = [False, False, False]
    for wel in wt1['leave']:
        if wel == 'msg':
            cando[0] = True
        if wel == 'toggle':
            cando[1] = True
        if wel == 'channel':
            cando[2] = True
    if cando == [True, True, True]:
        if wt1['leave']['toggle'] == "True" and wt1['leave']['msg'] != '':
            msg = wt1['leave']['msg'].replace('>gname<', member.guild.name).replace('>mname<', member.name)
            channel = bot.get_channel(wt1['leave']['channel'])
            await channel.send(msg)
    
    cando = [False, False]
    for wel in wt1['leave']:
        if wel == 'dm':
            cando[0] = True
        if wel == 'dmtoggle':
            cando[1] = True
    if cando == [True, True]:
        if wt1['leave']['dmtoggle'] == "True" and wt1['leave']['dm'] != '':
            user = bot.get_user(member.id)
            if user is not None:
                if user.dm_channel is None:
                    await user.create_dm()
                msg = wt1['leave']['dm'].replace('>gname<', member.guild.name).replace('>tagm<', member.mention).replace('>mname<', member.name)
                
                view = View()
                view.add_item(Button(label="來自:"+member.guild.name, style = discord.ButtonStyle.green, disabled=True))
                
                await user.dm_channel.send(msg, view = view)

@bot.group()
async def admin(ctx):
    await ctx.message.delete()
@admin.command()
async def sudo(ctx, guild:int, command):
    if ctx.author.id == bot.owner_id:
        if command == 'resetup':
            tguild = bot.get_guild(guild)
            gid = tguild.id
            try:
                lan_set = loadset(gid)
                langpack = loadlang(lan_set["lang"])
            except:
                langpack = loadlang('zh-tw.json')
                try:
                    gname  = str(tguild)
                    wd1 = {"leave":{}, "welcome":{}, "rolerrbl":[], "rrbl":[],"rr":[], "tvc":[], "lang":"eng.json", "timearea":None, "reminds": [],"guildmon":0, "botexp":0,"channelid": 0, "ytchannelid":[]}
                    dumpdata3 = json.dumps(wd1)
                    with open(f'settings/{str(gid)}.json', 'w', encoding = 'utf-8') as f:
                        f.write(dumpdata3)
                    embed=discord.Embed(title=langpack["resetup.success"], color=0xee2f9f)
                    embed.add_field(name=langpack["desetup.success.name"], value=f"{gname}", inline=True)
                    embed.add_field(name=langpack["desetup.success.id"], value=f"{str(gid)}", inline=True)
                    
                    user = ctx.author
                    if user is not None:
                        if user.dm_channel is None:
                            await user.create_dm()
                        await user.dm_channel.send(embed=embed)
                except:
                    embed=discord.Embed(color=0xee4f9e)
                    embed.add_field(name="ERROR!", value=langpack["err.message"], inline=True)
                    user = ctx.author
                    if user is not None:
                        if user.dm_channel is None:
                            await user.create_dm()
                        await user.dm_channel.send(embed=embed)
@admin.command()
async def guilds(ctx):
    if ctx.author.id == bot.owner_id:
        guilds = bot.guilds
        msg = "使用團子機器人的伺服器\n"
        n = 1
        msgs = []
        for g in guilds:
            msg += f'[{str(n)}]{g.name}({str(g.id)})\n'
            if n % 10 == 0:
                msgs.append(msg)
                msg = ""
            n += 1
        if n % 10 != 0:
            msgs.append(msg)
        user = ctx.author
        if user is not None:
            if user.dm_channel is None:
                await user.create_dm()
            for m in msgs:
                await user.dm_channel.send(m)
@admin.command()
async def ginfo(ctx, id:int):
    if ctx.author.id == bot.owner_id:
        gid = ctx.guild.id
        lan_set = loadset(gid)
        langpack = loadlang(lan_set["lang"])
        
        guild = bot.get_guild(id)
        owner = bot.get_user(guild.owner_id)
        embed=discord.Embed(title=str(guild), description=f"id:{str(guild.id)}", color=0xee4f9e)
        embed.set_thumbnail(url=guild.icon)
        embed.add_field(name=langpack['guildinfo.member'], value=len(guild.members), inline=True)
        embed.add_field(name=langpack["guildinfo.channel"], value=len(guild.channels), inline=True)
        embed.add_field(name = '伺服器擁有者', value = f'{str(owner)}({str(owner.id)})', inline = True)
        embed.add_field(name = '伺服器橫幅', value = f'{str(guild.banner)}', inline = True)
        embed.add_field(name = '身分組數量', value = f'{str(len(guild.roles))}', inline = True)
        embed.add_field(name = '創建時間', value = f"{str((guild.created_at).strftime('%Y/%m/%d %H:%M:%S'))} UTC+0", inline = True)
        user = ctx.author
        if user is not None:
            if user.dm_channel is None:
                await user.create_dm()
            await user.dm_channel.send(embed = embed)
        text = f"""Information of {str(guild)}
AFK Channel:{str(guild.afk_channel)}
AFK Timeout:{str(guild.afk_channel)}
伺服器成員上限:{str(guild.max_members)}
伺服器存在上限:{str(guild.max_presences)}
伺服器視訊人數上限:{str(guild.max_video_channel_users)}
伺服器表情符號數量:{str(len(guild.emojis))}
伺服器敘述:{str(guild.description)}
mfa等級:{str(guild.mfa_level)}
驗證等級:{str(guild.verification_level)}
訊息內容過濾器:{str(guild.explicit_content_filter)}
伺服器通知設定:{str(guild.default_notifications)}
加成等級:{str(guild.premium_tier)}
加成次數:{str(guild.premium_subscription_count)}
首選語言環境:{str(guild.preferred_locale)}
大型伺服器:{str(guild.preferred_locale)}
語音頻道數量:{str(len(guild.voice_channels))}
舞台頻道數量:{str(len(guild.stage_channels))}
文字頻道數量:{str(len(guild.text_channels))}
類別數量:{str(len(guild.categories))}
系統訊息頻道:{str(guild.system_channel)}
規則頻道:{str(guild.rules_channel)}
Discord系統訊息頻道:{str(guild.public_updates_channel)}
表情符號數量限制:{str(guild.emoji_limit)}
語音頻道音訊品質限制:{str(guild.bitrate_limit)}
檔案大小限制:{str(guild.filesize_limit)}
chunked:{str(guild.chunked)}"""
            
        with open('guildinfo.txt', 'w', encoding = 'utf8') as f:
            f.write(text)
        file = discord.File('guildinfo.txt')
        user = ctx.author
        if user is not None:
            if user.dm_channel is None:
                await user.create_dm()
            await user.dm_channel.send(file = file)
        os.remove('guildinfo.txt')

@bot.command()
async def pupload(ctx, tag:str):
    try:
        names = ctx.message.attachments
        for n in names:
            tname = n.url
            filename = tname.split('/')[-1]
            if (".png" in filename) or (".jpg" in filename) or (".gif" in filename) or (".jfif" in filename):
                req = urllib.request.Request(
                tname, 
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
                }
                )
                image = urllib.request.urlopen(req)
                with open(f'waitforcheck/{tag}/{filename}', 'wb') as f:
                    f.write(image.read())
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="成功", value=f"檔案上傳成功!", inline=True)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="失敗", value=f"檔案格式錯誤!", inline=True)
                await ctx.send(embed=embed)
    except:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="錯誤", value=f"執行指令時發生錯誤!", inline=True)
        await ctx.send(embed=embed)

@bot.group()
async def ox(ctx):
    if not os.path.exists(f'gamer/{str(ctx.author.id)}.json'):
        data = {'ooxx':{'win':0, 'lose':0, 'tie':0, 'noend':0, 'total':0}}
        data2 = json.dumps(data)
        with open(f'gamer/{str(ctx.author.id)}.json', 'w', encoding='utf8') as f:
            f.write(data2)
@ox.command()
async def new(ctx):
    if os.path.exists(f'game/{str(ctx.author.id)}.json'):
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="錯誤", value=f"有尚未結束的遊戲!", inline=True)
        await ctx.send(embed=embed)
    else:
        with open(f'gamer/{str(ctx.author.id)}.json', 'r', encoding='utf8') as f:
            data2 = json.load(f)
        data2['ooxx']['total'] += 1
        data3 = json.dumps(data2)
        with open(f'gamer/{str(ctx.author.id)}.json', 'w', encoding='utf8') as f:
            f.write(data3)
        
        gm = {'ox':[None, None, None ,None,None,None,None,None,None]}
        data1 = json.dumps(gm, ensure_ascii=False)
        with open(f'game/{str(ctx.author.id)}.json', 'w', encoding = 'utf8') as f:
            f.write(data1)
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="井字遊戲", value=f"開始新遊戲!", inline=True)
        await ctx.send(embed=embed)
@ox.command()
async def leave(ctx):
    if os.path.exists(f'game/{str(ctx.author.id)}.json'):
        with open(f'gamer/{str(ctx.author.id)}.json', 'r', encoding='utf8') as f:
            data2 = json.load(f)
        data2['ooxx']['noend'] += 1
        data3 = json.dumps(data2)
        with open(f'gamer/{str(ctx.author.id)}.json', 'w', encoding='utf8') as f:
            f.write(data3)

        os.remove(f'game/{str(ctx.author.id)}.json')
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="井字遊戲", value=f"已離開遊戲!", inline=True)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="錯誤", value=f"你並沒有在一個遊戲中!", inline=True)
        await ctx.send(embed=embed)
@ox.command()
async def view(ctx):
    if os.path.exists(f'game/{str(ctx.author.id)}.json'):
        view = View(timeout = None)

        with open(f'game/{str(ctx.author.id)}.json', 'r', encoding = 'utf8') as f:
            wt1 = json.load(f)
        
        def gene(view, wt1):
            if wt1['ox'][0] == None:
                button1 = Button(label = 'None', style=discord.ButtonStyle.green, row = 0)
                button1.callback = click1
                view.add_item(button1)
            else:
                button1 = Button(label = wt1['ox'][0], style=discord.ButtonStyle.gray, row = 0, disabled=True)
                view.add_item(button1)

            if wt1['ox'][1] == None:
                button2 = Button(label = 'None', style=discord.ButtonStyle.green, row = 0)
                button2.callback = click2
                view.add_item(button2)
            else:
                button2 = Button(label = wt1['ox'][1], style=discord.ButtonStyle.gray, row = 0, disabled=True)
                view.add_item(button2)

            if wt1['ox'][2] == None:
                button3 = Button(label = 'None', style=discord.ButtonStyle.green, row = 0)
                button3.callback = click3
                view.add_item(button3)
            else:
                button3 = Button(label = wt1['ox'][2], style=discord.ButtonStyle.gray, row = 0, disabled=True)
                view.add_item(button3)

            if wt1['ox'][3] == None:
                button4 = Button(label = 'None', style=discord.ButtonStyle.green, row = 1)
                button4.callback = click4
                view.add_item(button4)
            else:
                button4 = Button(label = wt1['ox'][3], style=discord.ButtonStyle.gray, row = 1, disabled=True)
                view.add_item(button4)

            if wt1['ox'][4] == None:
                button5 = Button(label = 'None', style=discord.ButtonStyle.green, row = 1)
                button5.callback = click5
                view.add_item(button5)
            else:
                button5 = Button(label = wt1['ox'][4], style=discord.ButtonStyle.gray, row = 1, disabled=True)
                view.add_item(button5)

            if wt1['ox'][5] == None:
                button6 = Button(label = 'None', style=discord.ButtonStyle.green, row = 1)
                button6.callback = click6
                view.add_item(button6)
            else:
                button6 = Button(label = wt1['ox'][5], style=discord.ButtonStyle.gray, row = 1, disabled=True)
                view.add_item(button6)

            if wt1['ox'][6] == None:
                button7 = Button(label = 'None', style=discord.ButtonStyle.green, row = 2)
                button7.callback = click7
                view.add_item(button7)
            else:
                button7 = Button(label = wt1['ox'][6], style=discord.ButtonStyle.gray, row = 2, disabled=True)
                view.add_item(button7)

            if wt1['ox'][7] == None:
                button8 = Button(label = 'None', style=discord.ButtonStyle.green, row = 2)
                button8.callback = click8
                view.add_item(button8)
            else:
                button8 = Button(label = wt1['ox'][7], style=discord.ButtonStyle.gray, row = 2, disabled=True)
                view.add_item(button8)

            if wt1['ox'][8] == None:
                button9 = Button(label = 'None', style=discord.ButtonStyle.green, row = 2)
                button9.callback = click9
                view.add_item(button9)
            else:
                button9 = Button(label = wt1['ox'][8], style=discord.ButtonStyle.gray, row = 2, disabled=True)
                view.add_item(button9)
            return view
        def wlt(view, wl):
            if wl == "Win":
                with open(f'gamer/{str(ctx.author.id)}.json', 'r', encoding='utf8') as f:
                        data2 = json.load(f)
                data2['ooxx']['win'] += 1
                data3 = json.dumps(data2)
                with open(f'gamer/{str(ctx.author.id)}.json', 'w', encoding='utf8') as f:
                    f.write(data3)
            elif wl == "Lose":
                with open(f'gamer/{str(ctx.author.id)}.json', 'r', encoding='utf8') as f:
                        data2 = json.load(f)
                data2['ooxx']['lose'] += 1
                data3 = json.dumps(data2)
                with open(f'gamer/{str(ctx.author.id)}.json', 'w', encoding='utf8') as f:
                    f.write(data3)
            elif wl == "Tie":
                with open(f'gamer/{str(ctx.author.id)}.json', 'r', encoding='utf8') as f:
                        data2 = json.load(f)
                data2['ooxx']['tie'] += 1
                data3 = json.dumps(data2)
                with open(f'gamer/{str(ctx.author.id)}.json', 'w', encoding='utf8') as f:
                    f.write(data3)
            
            for i in range(3):
                for j in range(3):
                    if wl == "Win":
                        view.add_item(Button(disabled=True, style = discord.ButtonStyle.green, label = '獲勝!!!', row = i))
                    elif wl == "Lose":
                        view.add_item(Button(disabled=True, style = discord.ButtonStyle.danger, label = '落敗...', row = i))
                    elif wl == "Tie":
                        view.add_item(Button(disabled=True, style = discord.ButtonStyle.gray, label = '平局。', row = i))
            return view

        async def click1(interaction):
            if os.path.exists(f'game/{str(interaction.user.id)}.json'):
                with open(f'game/{str(interaction.user.id)}.json', 'r', encoding = 'utf8') as f:
                    wt1 = json.load(f)
                wt1['ox'][0] = 'O'
                tlist = ooxx.ai(wt1['ox'])
                wt1['ox'] = tlist
                data1 = json.dumps(wt1, ensure_ascii=False)
                with open(f'game/{str(interaction.user.id)}.json', 'w', encoding = 'utf8') as f:
                    f.write(data1)

                view = gene(View(), wt1)
                wl = ooxx.wl(wt1['ox'])
                if wl != "Not yet":
                    view = wlt(View(), wl)
                    await interaction.response.edit_message(view = view)
                    os.remove(f'game/{str(interaction.user.id)}.json')
                else:
                    await interaction.response.edit_message(view = view)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="錯誤", value=f"你並沒有在一個遊戲中!", inline=True)
                await interaction.response.edit_message(embed=embed, view = None)
        async def click2(interaction):
            if os.path.exists(f'game/{str(interaction.user.id)}.json'):
                with open(f'game/{str(interaction.user.id)}.json', 'r', encoding = 'utf8') as f:
                    wt1 = json.load(f)
                wt1['ox'][1] = 'O'
                tlist = ooxx.ai(wt1['ox'])
                wt1['ox'] = tlist
                data1 = json.dumps(wt1, ensure_ascii=False)
                with open(f'game/{str(interaction.user.id)}.json', 'w', encoding = 'utf8') as f:
                    f.write(data1)

                view = gene(View(), wt1)
                wl = ooxx.wl(wt1['ox'])
                if wl != "Not yet":
                    view = wlt(View(), wl)
                    await interaction.response.edit_message(view = view)
                    os.remove(f'game/{str(interaction.user.id)}.json')
                else:
                    await interaction.response.edit_message(view = view)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="錯誤", value=f"你並沒有在一個遊戲中!", inline=True)
                await interaction.response.edit_message(embed=embed, view = None)
        async def click3(interaction):
            if os.path.exists(f'game/{str(interaction.user.id)}.json'):
                with open(f'game/{str(interaction.user.id)}.json', 'r', encoding = 'utf8') as f:
                    wt1 = json.load(f)
                wt1['ox'][2] = 'O'
                tlist = ooxx.ai(wt1['ox'])
                wt1['ox'] = tlist
                data1 = json.dumps(wt1, ensure_ascii=False)
                with open(f'game/{str(interaction.user.id)}.json', 'w', encoding = 'utf8') as f:
                    f.write(data1)

                view = gene(View(), wt1)
                wl = ooxx.wl(wt1['ox'])
                if wl != "Not yet":
                    view = wlt(View(), wl)
                    await interaction.response.edit_message(view = view)
                    os.remove(f'game/{str(interaction.user.id)}.json')
                else:
                    await interaction.response.edit_message(view = view)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="錯誤", value=f"你並沒有在一個遊戲中!", inline=True)
                await interaction.response.edit_message(embed=embed, view = None)
        async def click4(interaction):
            if os.path.exists(f'game/{str(interaction.user.id)}.json'):
                with open(f'game/{str(interaction.user.id)}.json', 'r', encoding = 'utf8') as f:
                    wt1 = json.load(f)
                wt1['ox'][3] = 'O'
                tlist = ooxx.ai(wt1['ox'])
                wt1['ox'] = tlist
                data1 = json.dumps(wt1, ensure_ascii=False)
                with open(f'game/{str(interaction.user.id)}.json', 'w', encoding = 'utf8') as f:
                    f.write(data1)

                view = gene(View(), wt1)
                wl = ooxx.wl(wt1['ox'])
                if wl != "Not yet":
                    view = wlt(View(), wl)
                    await interaction.response.edit_message(view = view)
                    os.remove(f'game/{str(interaction.user.id)}.json')
                else:
                    await interaction.response.edit_message(view = view)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="錯誤", value=f"你並沒有在一個遊戲中!", inline=True)
                await interaction.response.edit_message(embed=embed, view = None)
        async def click5(interaction):
            if os.path.exists(f'game/{str(interaction.user.id)}.json'):
                with open(f'game/{str(interaction.user.id)}.json', 'r', encoding = 'utf8') as f:
                    wt1 = json.load(f)
                wt1['ox'][4] = 'O'
                tlist = ooxx.ai(wt1['ox'])
                wt1['ox'] = tlist
                data1 = json.dumps(wt1, ensure_ascii=False)
                with open(f'game/{str(interaction.user.id)}.json', 'w', encoding = 'utf8') as f:
                    f.write(data1)

                view = gene(View(), wt1)
                wl = ooxx.wl(wt1['ox'])
                if wl != "Not yet":
                    view = wlt(View(), wl)
                    await interaction.response.edit_message(view = view)
                    os.remove(f'game/{str(interaction.user.id)}.json')
                else:
                    await interaction.response.edit_message(view = view)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="錯誤", value=f"你並沒有在一個遊戲中!", inline=True)
                await interaction.response.edit_message(embed=embed, view = None)
        async def click6(interaction):
            if os.path.exists(f'game/{str(interaction.user.id)}.json'):
                with open(f'game/{str(interaction.user.id)}.json', 'r', encoding = 'utf8') as f:
                    wt1 = json.load(f)
                wt1['ox'][5] = 'O'
                tlist = ooxx.ai(wt1['ox'])
                wt1['ox'] = tlist
                data1 = json.dumps(wt1, ensure_ascii=False)
                with open(f'game/{str(interaction.user.id)}.json', 'w', encoding = 'utf8') as f:
                    f.write(data1)

                view = gene(View(), wt1)
                wl = ooxx.wl(wt1['ox'])
                if wl != "Not yet":
                    view = wlt(View(), wl)
                    await interaction.response.edit_message(view = view)
                    os.remove(f'game/{str(interaction.user.id)}.json')
                else:
                    await interaction.response.edit_message(view = view)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="錯誤", value=f"你並沒有在一個遊戲中!", inline=True)
                await interaction.response.edit_message(embed=embed, view = None)
        async def click7(interaction):
            if os.path.exists(f'game/{str(interaction.user.id)}.json'):
                with open(f'game/{str(interaction.user.id)}.json', 'r', encoding = 'utf8') as f:
                    wt1 = json.load(f)
                wt1['ox'][6] = 'O'
                tlist = ooxx.ai(wt1['ox'])
                wt1['ox'] = tlist
                data1 = json.dumps(wt1, ensure_ascii=False)
                with open(f'game/{str(interaction.user.id)}.json', 'w', encoding = 'utf8') as f:
                    f.write(data1)

                view = gene(View(), wt1)
                wl = ooxx.wl(wt1['ox'])
                if wl != "Not yet":
                    view = wlt(View(), wl)
                    await interaction.response.edit_message(view = view)
                    os.remove(f'game/{str(interaction.user.id)}.json')
                else:
                    await interaction.response.edit_message(view = view)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="錯誤", value=f"你並沒有在一個遊戲中!", inline=True)
                await interaction.response.edit_message(embed=embed, view = None)
        async def click8(interaction):
            if os.path.exists(f'game/{str(interaction.user.id)}.json'):
                with open(f'game/{str(interaction.user.id)}.json', 'r', encoding = 'utf8') as f:
                    wt1 = json.load(f)
                wt1['ox'][7] = 'O'
                tlist = ooxx.ai(wt1['ox'])
                wt1['ox'] = tlist
                data1 = json.dumps(wt1, ensure_ascii=False)
                with open(f'game/{str(interaction.user.id)}.json', 'w', encoding = 'utf8') as f:
                    f.write(data1)

                view = gene(View(), wt1)
                wl = ooxx.wl(wt1['ox'])
                if wl != "Not yet":
                    view = wlt(View(), wl)
                    await interaction.response.edit_message(view = view)
                    os.remove(f'game/{str(interaction.user.id)}.json')
                else:
                    await interaction.response.edit_message(view = view)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="錯誤", value=f"你並沒有在一個遊戲中!", inline=True)
                await interaction.response.edit_message(embed=embed, view = None)
        async def click9(interaction):
            if os.path.exists(f'game/{str(interaction.user.id)}.json'):
                with open(f'game/{str(interaction.user.id)}.json', 'r', encoding = 'utf8') as f:
                    wt1 = json.load(f)
                wt1['ox'][8] = 'O'
                tlist = ooxx.ai(wt1['ox'])
                wt1['ox'] = tlist
                data1 = json.dumps(wt1, ensure_ascii=False)
                with open(f'game/{str(interaction.user.id)}.json', 'w', encoding = 'utf8') as f:
                    f.write(data1)

                view = gene(View(), wt1)
                wl = ooxx.wl(wt1['ox'])
                if wl != "Not yet":
                    view = wlt(View(), wl)
                    await interaction.response.edit_message(view = view)
                    os.remove(f'game/{str(interaction.user.id)}.json')
                else:
                    await interaction.response.edit_message(view = view)
            else:
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="錯誤", value=f"你並沒有在一個遊戲中!", inline=True)
                await interaction.response.edit_message(embed=embed, view = None)

        if wt1['ox'][0] == None:
            button1 = Button(label = 'None', style=discord.ButtonStyle.green, row = 0)
            button1.callback = click1
            view.add_item(button1)
        else:
            button1 = Button(label = wt1['ox'][0], style=discord.ButtonStyle.gray, row = 0, disabled=True)
            view.add_item(button1)

        if wt1['ox'][1] == None:
            button2 = Button(label = 'None', style=discord.ButtonStyle.green, row = 0)
            button2.callback = click2
            view.add_item(button2)
        else:
            button2 = Button(label = wt1['ox'][1], style=discord.ButtonStyle.gray, row = 0, disabled=True)
            view.add_item(button2)

        if wt1['ox'][2] == None:
            button3 = Button(label = 'None', style=discord.ButtonStyle.green, row = 0)
            button3.callback = click3
            view.add_item(button3)
        else:
            button3 = Button(label = wt1['ox'][2], style=discord.ButtonStyle.gray, row = 0, disabled=True)
            view.add_item(button3)
        
        if wt1['ox'][3] == None:
            button4 = Button(label = 'None', style=discord.ButtonStyle.green, row = 1)
            button4.callback = click4
            view.add_item(button4)
        else:
            button4 = Button(label = wt1['ox'][3], style=discord.ButtonStyle.gray, row = 1, disabled=True)
            view.add_item(button4)

        if wt1['ox'][4] == None:
            button5 = Button(label = 'None', style=discord.ButtonStyle.green, row = 1)
            button5.callback = click5
            view.add_item(button5)
        else:
            button5 = Button(label = wt1['ox'][4], style=discord.ButtonStyle.gray, row = 1, disabled=True)
            view.add_item(button5)

        if wt1['ox'][5] == None:
            button6 = Button(label = 'None', style=discord.ButtonStyle.green, row = 1)
            button6.callback = click6
            view.add_item(button6)
        else:
            button6 = Button(label = wt1['ox'][5], style=discord.ButtonStyle.gray, row = 1, disabled=True)
            view.add_item(button6)

        if wt1['ox'][6] == None:
            button7 = Button(label = 'None', style=discord.ButtonStyle.green, row = 2)
            button7.callback = click7
            view.add_item(button7)
        else:
            button7 = Button(label = wt1['ox'][6], style=discord.ButtonStyle.gray, row = 2, disabled=True)
            view.add_item(button7)

        if wt1['ox'][7] == None:
            button8 = Button(label = 'None', style=discord.ButtonStyle.green, row = 2)
            button8.callback = click8
            view.add_item(button8)
        else:
            button8 = Button(label = wt1['ox'][7], style=discord.ButtonStyle.gray, row = 2, disabled=True)
            view.add_item(button8)

        if wt1['ox'][8] == None:
            button9 = Button(label = 'None', style=discord.ButtonStyle.green, row = 2)
            button9.callback = click9
            view.add_item(button9)
        else:
            button9 = Button(label = wt1['ox'][8], style=discord.ButtonStyle.gray, row = 2, disabled=True)
            view.add_item(button9)

        await ctx.send(view = view)
    else:
        embed=discord.Embed(color=0xee4f9e)
        embed.add_field(name="錯誤", value=f"你並沒有在一個遊戲中!", inline=True)
        await ctx.send(embed = embed)

#播放直播
#播放播放清單的
@bot.command()
async def join(ctx):
    if ctx.author.voice != None:
        allow  = True
        for vc in bot.voice_clients:
            print(vc)
            if vc.guild.id == ctx.guild.id:
                allow = False
                break
        if allow == True:
            tdd1 = {"queue":[], "loop":False, "playing":0, 'stopped':False, 'skipmsg':'', 'cantplay':'', "loop":"關閉", "random": False}
            dumpdata = json.dumps(tdd1, ensure_ascii = False)
            with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                f.write(dumpdata)
            
            channel = ctx.author.voice.channel
            await channel.connect()
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="成功", value=f"已加入語音頻道!", inline=True)
            await ctx.send(embed = embed)
        else:
            embed=discord.Embed(color=0xff0000)
            embed.add_field(name="錯誤", value=f"我已經在語音頻道內!", inline=True)
            await ctx.send(embed = embed)
    else:
        embed=discord.Embed(color=0xff0000)
        embed.add_field(name="錯誤", value=f"請先加入一個語音頻道!", inline=True)
        await ctx.send(embed = embed)

@bot.command()
async def play(ctx, url):
    with open(f'music/{str(ctx.guild.id)}.json', 'r', encoding = 'utf-8') as f:
        d1 = json.load(f)
    if d1['cantplay'] == "":
        allow  = False
        for vc in bot.voice_clients:
            if vc.guild.id == ctx.guild.id:
                ttvc = vc
                allow = True
        if allow == True:
            if ctx.author.voice != None:
                if ctx.author.voice.channel.id == ttvc.channel.id:
                    rms = re.findall(r'[watch?v=]*[\w-]*', url)
                    for rm in rms:
                        if "watch?v=" in rm:
                            watch = rm.replace("watch?v=", "")
                            break
                    result3 = requests.get('https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={}&key={}'.format(watch, api_key))
                    data3 = result3.json()
                    vtitle = str(data3["items"][0]["snippet"]["title"])
                    voice = get(bot.voice_clients, guild=ctx.guild)
                    if not voice.is_playing() and voice.is_paused() == False:
                        with open(f'music/{str(ctx.guild.id)}.json', 'r', encoding = 'utf-8') as f:
                            d1 = json.load(f)
                        if d1['playing'] != 0:
                            d1['playing'] += 1
                        d1['queue'].append((url, vtitle, data3["items"][0]["snippet"]["channelTitle"], data3["items"][0]["snippet"]["thumbnails"]['default']['url']))
                        dumpdata = json.dumps(d1, ensure_ascii = False)
                        with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                            f.write(dumpdata)
                        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
                        FFMPEG_OPTIONS = {
                            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
                        with YoutubeDL(YDL_OPTIONS) as ydl:
                            info = ydl.extract_info(url, download=False)
                        URL = info['url']
                        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name="開始播放!", value=f'**{data3["items"][0]["snippet"]["channelTitle"]}**\n{vtitle}', inline=True)
                        embed.set_image(url = data3["items"][0]["snippet"]["thumbnails"]['default']['url'])
                        await ctx.send(embed = embed)

                        with open(f'music/{str(ctx.guild.id)}.json', 'r', encoding = 'utf-8') as f:
                            d1 = json.load(f)
                        running = True
                        while running:
                            yskip = False
                            with open(f'music/{str(ctx.guild.id)}.json', 'r', encoding = 'utf-8') as f:
                                d1 = json.load(f)
                            if d1['skipmsg'] == "True":
                                yskip = True
                                voice.stop()
                                d1['skipmsg'] = ''
                                dumpdata = json.dumps(d1, ensure_ascii = False)
                                with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                                    f.write(dumpdata)
                            if voice.is_playing() == False and voice.is_paused() == False and d1['stopped'] == False:
                                if d1['random'] == False:
                                    if not(d1['playing']+1 > len(d1['queue'])-1):
                                        d1['cantplay'] = "True"
                                        dumpdata = json.dumps(d1, ensure_ascii = False)
                                        with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                                            f.write(dumpdata)
                                        await asyncio.sleep(5)
                                        d1['cantplay'] = ""
                                        dumpdata = json.dumps(d1, ensure_ascii = False)
                                        with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                                            f.write(dumpdata)
                                        if d1['loop'] == "單首" and yskip == False:
                                            pass
                                        else:
                                            d1['playing'] += 1
                                        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
                                        FFMPEG_OPTIONS = {
                                            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
                                        with YoutubeDL(YDL_OPTIONS) as ydl:
                                            info = ydl.extract_info(d1['queue'][d1['playing']][0], download=False)
                                        URL = info['url']
                                        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                                        dumpdata = json.dumps(d1, ensure_ascii = False)
                                        with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                                            f.write(dumpdata)
                                        embed=discord.Embed(color=0xee4f9e)
                                        embed.add_field(name="開始播放!", value=f"**{d1['queue'][d1['playing']][2]}**\n{d1['queue'][d1['playing']][1]}", inline=True)
                                        embed.set_image(url = d1['queue'][d1['playing']][3])
                                        await ctx.send(embed = embed)
                                    else:
                                        if d1['loop'] == "關閉":
                                            running = False
                                        elif d1['loop'] == "全部":
                                            d1['playing'] = 0
                                            dumpdata = json.dumps(d1, ensure_ascii = False)
                                            with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                                                f.write(dumpdata)

                                            d1['cantplay'] = "True"
                                            dumpdata = json.dumps(d1, ensure_ascii = False)
                                            with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                                                f.write(dumpdata)
                                            await asyncio.sleep(5)
                                            d1['cantplay'] = ""
                                            dumpdata = json.dumps(d1, ensure_ascii = False)
                                            with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                                                f.write(dumpdata)

                                            YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
                                            FFMPEG_OPTIONS = {
                                                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
                                            with YoutubeDL(YDL_OPTIONS) as ydl:
                                                info = ydl.extract_info(d1['queue'][d1['playing']][0], download=False)
                                            URL = info['url']
                                            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                                            dumpdata = json.dumps(d1, ensure_ascii = False)
                                            with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                                                f.write(dumpdata)
                                            embed=discord.Embed(color=0xee4f9e)
                                            embed.add_field(name="開始播放!", value=f"**{d1['queue'][d1['playing']][2]}**\n{d1['queue'][d1['playing']][1]}", inline=True)
                                            embed.set_image(url = d1['queue'][d1['playing']][3])
                                            await ctx.send(embed = embed)
                                        elif d1['loop'] == "單首" and yskip == False:
                                            d1['cantplay'] = "True"
                                            dumpdata = json.dumps(d1, ensure_ascii = False)
                                            with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                                                f.write(dumpdata)
                                            await asyncio.sleep(5)
                                            d1['cantplay'] = ""
                                            dumpdata = json.dumps(d1, ensure_ascii = False)
                                            with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                                                f.write(dumpdata)

                                            YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
                                            FFMPEG_OPTIONS = {
                                                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
                                            with YoutubeDL(YDL_OPTIONS) as ydl:
                                                info = ydl.extract_info(d1['queue'][d1['playing']][0], download=False)
                                            URL = info['url']
                                            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                                            dumpdata = json.dumps(d1, ensure_ascii = False)
                                            with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                                                f.write(dumpdata)
                                            embed=discord.Embed(color=0xee4f9e)
                                            embed.add_field(name="開始播放!", value=f"**{d1['queue'][d1['playing']][2]}**\n{d1['queue'][d1['playing']][1]}", inline=True)
                                            embed.set_image(url = d1['queue'][d1['playing']][3])
                                            await ctx.send(embed = embed)
                                        elif d1['loop'] == "單首":
                                            d1['cantplay'] = "True"
                                            dumpdata = json.dumps(d1, ensure_ascii = False)
                                            with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                                                f.write(dumpdata)
                                            await asyncio.sleep(5)
                                            d1['cantplay'] = ""
                                            dumpdata = json.dumps(d1, ensure_ascii = False)
                                            with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                                                f.write(dumpdata)

                                            YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
                                            FFMPEG_OPTIONS = {
                                                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
                                            with YoutubeDL(YDL_OPTIONS) as ydl:
                                                info = ydl.extract_info(d1['queue'][d1['playing']][0], download=False)
                                            URL = info['url']
                                            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                                            dumpdata = json.dumps(d1, ensure_ascii = False)
                                            with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                                                f.write(dumpdata)
                                            embed=discord.Embed(color=0xee4f9e)
                                            embed.add_field(name="開始播放!", value=f"**{d1['queue'][d1['playing']][2]}**\n{d1['queue'][d1['playing']][1]}", inline=True)
                                            embed.set_image(url = d1['queue'][d1['playing']][3])
                                            await ctx.send(embed = embed)
                                else:
                                    d1['cantplay'] = "True"
                                    dumpdata = json.dumps(d1, ensure_ascii = False)
                                    with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                                        f.write(dumpdata)
                                    await asyncio.sleep(5)
                                    d1['cantplay'] = ""
                                    dumpdata = json.dumps(d1, ensure_ascii = False)
                                    with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                                        f.write(dumpdata)
                                    
                                    d1['playing'] = random.randint(0, len(d1['queue'])-1)
                                    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
                                    FFMPEG_OPTIONS = {
                                        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
                                    with YoutubeDL(YDL_OPTIONS) as ydl:
                                        info = ydl.extract_info(d1['queue'][d1['playing']][0], download=False)
                                    URL = info['url']
                                    voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                                    dumpdata = json.dumps(d1, ensure_ascii = False)
                                    with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                                        f.write(dumpdata)
                                    embed=discord.Embed(color=0xee4f9e)
                                    embed.add_field(name="開始播放!", value=f"**{d1['queue'][d1['playing']][2]}**\n{d1['queue'][d1['playing']][1]}", inline=True)
                                    embed.set_image(url = d1['queue'][d1['playing']][3])
                                    await ctx.send(embed = embed)
                            await asyncio.sleep(1)
                    else:
                        with open(f'music/{str(ctx.guild.id)}.json', 'r', encoding = 'utf-8') as f:
                            d1 = json.load(f)
                        d1['queue'].append((url, vtitle, data3["items"][0]["snippet"]["channelTitle"], data3["items"][0]["snippet"]["thumbnails"]['default']['url']))
                        dumpdata = json.dumps(d1, ensure_ascii = False)
                        with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                            f.write(dumpdata)

                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name="已加入播放清單!", value=f'**{data3["items"][0]["snippet"]["channelTitle"]}**\n{vtitle}', inline=True)
                        embed.set_image(url = data3["items"][0]["snippet"]["thumbnails"]['default']['url'])
                        await ctx.send(embed = embed)
                else:
                    embed=discord.Embed(color=0xff0000)
                    embed.add_field(name="錯誤", value=f"你跟機器人並不在同一個語音頻道內!", inline=True)
                    await ctx.send(embed = embed)
            else:
                embed=discord.Embed(color=0xff0000)
                embed.add_field(name="錯誤", value=f"你跟機器人並不在同一個語音頻道內!", inline=True)
                await ctx.send(embed = embed)
        else:
            embed=discord.Embed(color=0xff0000)
            embed.add_field(name="錯誤", value=f"我並沒有在一個語音頻道內!", inline=True)
            await ctx.send(embed = embed)
@bot.command()
async def prandom(ctx):
    allow = False
    for vc in bot.voice_clients:
        if vc.guild.id == ctx.guild.id:
            ttvc = vc
            allow = True
    if allow == True:
        if ctx.author.voice != None:
            if ctx.author.voice.channel.id == ttvc.channel.id:
                with open(f'music/{str(ctx.guild.id)}.json', 'r', encoding = 'utf-8') as f:
                    d1 = json.load(f)
                mmsg = ""
                if d1['random'] == True:
                    d1['random'] = False
                    mmsg = "關閉"
                else:
                    d1['random'] = True
                    mmsg = "開啟"
                dumpdata = json.dumps(d1, ensure_ascii = False)
                with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                    f.write(dumpdata)
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="隨機播放", value=f"``{mmsg}``", inline=True)
                await ctx.send(embed = embed)
            else:
                embed=discord.Embed(color=0xff0000)
                embed.add_field(name="錯誤", value=f"你跟機器人並不在同一個語音頻道內!", inline=True)
                await ctx.send(embed = embed)
        else:
            embed=discord.Embed(color=0xff0000)
            embed.add_field(name="錯誤", value=f"你跟機器人並不在同一個語音頻道內!", inline=True)
            await ctx.send(embed = embed)
    else:
        embed=discord.Embed(color=0xff0000)
        embed.add_field(name="錯誤", value=f"我並沒有在一個語音頻道內!", inline=True)
        await ctx.send(embed = embed)
@bot.command()
async def loop(ctx, sta:str):
    allow = False
    for vc in bot.voice_clients:
        if vc.guild.id == ctx.guild.id:
            ttvc = vc
            allow = True
    if allow == True:
        if ctx.author.voice != None:
            if ctx.author.voice.channel.id == ttvc.channel.id:
                with open(f'music/{str(ctx.guild.id)}.json', 'r', encoding = 'utf-8') as f:
                    d1 = json.load(f)
                cando = True
                if sta == "n":
                    d1['loop'] = "關閉"
                elif sta == "a":
                    d1['loop'] = "全部"
                elif sta == "o":
                    d1['loop'] = "單首"
                else:
                    cando = False
                dumpdata = json.dumps(d1, ensure_ascii = False)
                with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                    f.write(dumpdata)
                if cando == True:
                    embed=discord.Embed(color=0xee4f9e)
                    embed.add_field(name="已將音樂循環設定為", value=d1['loop'], inline=True)
                    await ctx.send(embed = embed)
                else:
                    embed=discord.Embed(color=0xee4f9e)
                    embed.add_field(name="錯誤!", value='參數錯誤!', inline=True)
                    await ctx.send(embed = embed)
            else:
                embed=discord.Embed(color=0xff0000)
                embed.add_field(name="錯誤", value=f"你跟機器人並不在同一個語音頻道內!", inline=True)
                await ctx.send(embed = embed)
        else:
            embed=discord.Embed(color=0xff0000)
            embed.add_field(name="錯誤", value=f"你跟機器人並不在同一個語音頻道內!", inline=True)
            await ctx.send(embed = embed)
    else:
        embed=discord.Embed(color=0xff0000)
        embed.add_field(name="錯誤", value=f"我並沒有在一個語音頻道內!", inline=True)
        await ctx.send(embed = embed)
@bot.command()
async def queue(ctx):
    allow = False
    for vc in bot.voice_clients:
        if vc.guild.id == ctx.guild.id:
            ttvc = vc
            allow = True
    if allow == True:
        if ctx.author.voice != None:
            if ctx.author.voice.channel.id == ttvc.channel.id:
                with open(f'music/{str(ctx.guild.id)}.json', 'r', encoding = 'utf-8') as f:
                    d1 = json.load(f)
                msg = ""
                for i, d in enumerate(d1['queue']):
                    if i == d1['playing']:
                        msg += f"[*]{d[1]} - {d[2]}\n"
                    elif i != d1['playing']:
                        msg += f"[{str(i+1)}]{d[1]} - {d[2]}\n"
                if msg == "":
                    msg = "清單內沒有歌曲!"
                embed=discord.Embed(color=0xee4f9e)
                embed.add_field(name="播放清單", value=f"{msg}", inline=True)
                await ctx.send(embed = embed)
            else:
                embed=discord.Embed(color=0xff0000)
                embed.add_field(name="錯誤", value=f"你跟機器人並不在同一個語音頻道內!", inline=True)
                await ctx.send(embed = embed)
        else:
            embed=discord.Embed(color=0xff0000)
            embed.add_field(name="錯誤", value=f"你跟機器人並不在同一個語音頻道內!", inline=True)
            await ctx.send(embed = embed)
    else:
        embed=discord.Embed(color=0xff0000)
        embed.add_field(name="錯誤", value=f"我並沒有在一個語音頻道內!", inline=True)
        await ctx.send(embed = embed)
@bot.command()
async def skip(ctx):
    allow = False
    for vc in bot.voice_clients:
        if vc.guild.id == ctx.guild.id:
            ttvc = vc
            allow = True
    if allow == True:
        if ctx.author.voice != None:
            if ctx.author.voice.channel.id == ttvc.channel.id:
                voice = get(bot.voice_clients, guild=ctx.guild)
                with open(f'music/{str(ctx.guild.id)}.json', 'r', encoding = 'utf-8') as f:
                    d1 = json.load(f)
                voice.stop()
                if d1['loop'] != "全部" and (len(d1['queue'])-1) < (d1['playing']+1):
                    if d1['loop'] == "關閉":
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name="播放清單已到盡頭", value=f"已停止音樂", inline=True)
                        await ctx.send(embed = embed)
                    else:
                        d1['loop'] = "關閉"
                        dumpdata = json.dumps(d1, ensure_ascii = False)
                        with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                            f.write(dumpdata)
                        embed=discord.Embed(color=0xee4f9e)
                        embed.add_field(name="播放清單已到盡頭", value=f"已停止音樂", inline=True)
                        await ctx.send(embed = embed)
                        await asyncio.sleep(2)
                        d1['loop'] = "單首"
                        dumpdata = json.dumps(d1, ensure_ascii = False)
                        with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                            f.write(dumpdata)
                else:
                    d1['skipmsg'] = 'True'
                    dumpdata = json.dumps(d1, ensure_ascii = False)
                    with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                        f.write(dumpdata)
            else:
                embed=discord.Embed(color=0xff0000)
                embed.add_field(name="錯誤", value=f"你跟機器人並不在同一個語音頻道內!", inline=True)
                await ctx.send(embed = embed)
        else:
            embed=discord.Embed(color=0xff0000)
            embed.add_field(name="錯誤", value=f"你跟機器人並不在同一個語音頻道內!", inline=True)
            await ctx.send(embed = embed)
    else:
        embed=discord.Embed(color=0xff0000)
        embed.add_field(name="錯誤", value=f"我並沒有在一個語音頻道內!", inline=True)
        await ctx.send(embed = embed)
@bot.command()
async def resume(ctx):
    allow = False
    for vc in bot.voice_clients:
        if vc.guild.id == ctx.guild.id:
            ttvc = vc
            allow = True
    if allow == True:
        if ctx.author.voice != None:
            if ctx.author.voice.channel.id == ttvc.channel.id:
                voice = get(bot.voice_clients, guild=ctx.guild)
                if voice.is_paused():
                    voice.resume()
    
                    embed=discord.Embed(color=0xee4f9e)
                    embed.add_field(name="成功!", value=f"繼續播放", inline=True)
                    await ctx.send(embed = embed)
                else:
                    embed=discord.Embed(color=0xff0000)
                    embed.add_field(name="錯誤!", value=f"音樂已在播放", inline=True)
                    await ctx.send(embed = embed)
            else:
                embed=discord.Embed(color=0xff0000)
                embed.add_field(name="錯誤", value=f"你跟機器人並不在同一個語音頻道內!", inline=True)
                await ctx.send(embed = embed)
        else:
            embed=discord.Embed(color=0xff0000)
            embed.add_field(name="錯誤", value=f"你跟機器人並不在同一個語音頻道內!", inline=True)
            await ctx.send(embed = embed)
    else:
        embed=discord.Embed(color=0xff0000)
        embed.add_field(name="錯誤", value=f"我並沒有在一個語音頻道內!", inline=True)
        await ctx.send(embed = embed)
@bot.command()
async def clearqueue(ctx):
    with open(f'music/{str(ctx.guild.id)}.json', 'r', encoding = 'utf-8') as f:
        d1 = json.load(f)
    tdd1 = {"queue":[d1['queue'][d1['playing']]], "loop":d1['loop'], "playing":0, 'stopped':False, 'skipmsg':d1['skipmsg'], 'cantplay':d1['cantplay'], 'loop':d1['loop'], "random": d1['random']}
    dumpdata = json.dumps(tdd1, ensure_ascii = False)
    with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
        f.write(dumpdata)
    embed=discord.Embed(color=0xee4f9e)
    embed.add_field(name="成功!", value=f"清除播放清單", inline=True)
    await ctx.send(embed = embed)
@bot.command()
async def pause(ctx):
    allow = False
    for vc in bot.voice_clients:
        if vc.guild.id == ctx.guild.id:
            ttvc = vc
            allow = True
    if allow == True:
        if ctx.author.voice != None:
            if ctx.author.voice.channel.id == ttvc.channel.id:
                voice = get(bot.voice_clients, guild=ctx.guild)
                if voice.is_playing():
                    voice.pause()
                    embed=discord.Embed(color=0xee4f9e)
                    embed.add_field(name="成功!", value=f"音樂已暫停", inline=True)
                    await ctx.send(embed = embed)
                else:
                    embed=discord.Embed(color=0xff0000)
                    embed.add_field(name="錯誤!", value=f"音樂已經暫停/停止!", inline=True)
                    await ctx.send(embed = embed)
            else:
                embed=discord.Embed(color=0xff0000)
                embed.add_field(name="錯誤", value=f"你跟機器人並不在同一個語音頻道內!", inline=True)
                await ctx.send(embed = embed)
        else:
            embed=discord.Embed(color=0xff0000)
            embed.add_field(name="錯誤", value=f"你跟機器人並不在同一個語音頻道內!", inline=True)
            await ctx.send(embed = embed)
    else:
        embed=discord.Embed(color=0xff0000)
        embed.add_field(name="錯誤", value=f"我並沒有在一個語音頻道內!", inline=True)
        await ctx.send(embed = embed)

@bot.command()
async def stop(ctx):
    allow = False
    for vc in bot.voice_clients:
        if vc.guild.id == ctx.guild.id:
            ttvc = vc
            allow = True
    if allow == True:
        if ctx.author.voice != None:
            if ctx.author.voice.channel.id == ttvc.channel.id:
                voice = get(bot.voice_clients, guild=ctx.guild)
                if voice.is_playing():
                    with open(f'music/{str(ctx.guild.id)}.json', 'r', encoding = 'utf-8') as f:
                        d1 = json.load(f)
                    dan = False
                    if d1['loop'] == "單首":
                        dan = True
                        d1['loop'] = "關閉"
                        dumpdata = json.dumps(d1, ensure_ascii = False)
                        with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                            f.write(dumpdata)
                    dan2 = False
                    if d1['random'] == True:
                        dan2 = True
                        d1['random'] = False
                        dumpdata = json.dumps(d1, ensure_ascii = False)
                        with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                            f.write(dumpdata)
                    voice.stop()
                    embed=discord.Embed(color=0xee4f9e)
                    embed.add_field(name="成功!", value=f"音樂已停止", inline=True)
                    await ctx.send(embed = embed)
                    with open(f'music/{str(ctx.guild.id)}.json', 'r', encoding = 'utf-8') as f:
                        d1 = json.load(f)
                    d1['stopped'] = True
                    dumpdata = json.dumps(d1, ensure_ascii = False)
                    with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                        f.write(dumpdata)
                    await asyncio.sleep(2)
                    if dan == True:
                        d1['loop'] = "單首"
                    if dan2 == True:
                        d1['random'] = True
                    dumpdata = json.dumps(d1, ensure_ascii = False)
                    with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                        f.write(dumpdata)
                else:
                    embed=discord.Embed(color=0xff0000)
                    embed.add_field(name="錯誤!", value=f"音樂已經暫停/停止!", inline=True)
                    await ctx.send(embed = embed)
            else:
                embed=discord.Embed(color=0xff0000)
                embed.add_field(name="錯誤", value=f"你跟機器人並不在同一個語音頻道內!", inline=True)
                await ctx.send(embed = embed)
        else:
            embed=discord.Embed(color=0xff0000)
            embed.add_field(name="錯誤", value=f"你跟機器人並不在同一個語音頻道內!", inline=True)
            await ctx.send(embed = embed)
    else:
        embed=discord.Embed(color=0xff0000)
        embed.add_field(name="錯誤", value=f"我並沒有在一個語音頻道內!", inline=True)
        await ctx.send(embed = embed)

@bot.command()
async def vleave(ctx):
    if ctx.author.voice != None:
        allow  = False
        for vc in bot.voice_clients:
            print(vc)
            if vc.guild.id == ctx.guild.id:
                allow = True
                break
        if allow == True:
            voice = get(bot.voice_clients, guild=ctx.guild)
            await voice.disconnect()
            tdd1 = {"queue":[], "loop":False, "playing":0, 'stopped':False, 'skipmsg':'', 'cantplay':'', "loop":"關閉", "random": False}
            dumpdata = json.dumps(tdd1, ensure_ascii = False)
            with open(f'music/{str(ctx.guild.id)}.json', 'w', encoding = 'utf-8') as f:
                f.write(dumpdata)

            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="成功", value=f"已離開語音頻道!", inline=True)
            await ctx.send(embed = embed)
        else:
            embed=discord.Embed(color=0xff0000)
            embed.add_field(name="錯誤", value=f"我並不在一個語音頻道內!", inline=True)
            await ctx.send(embed = embed)
    else:
        embed=discord.Embed(color=0xff0000)
        embed.add_field(name="錯誤", value=f"請先加入一個語音頻道!", inline=True)
        await ctx.send(embed = embed)

@bot.command()
async def exam(ctx):
    async def refresh(interaction):
        langpack = loadlang('zh-tw.json')
        try:
            gettime.gettime(+8, '%Y/%m/%d %H:%M:%S')
            with open('time.txt', 'r', encoding = 'utf-8') as f:
                content1 = f.readlines()
                zoned_time1 = content1[0]
            time_1 = datetime.strptime(zoned_time1,"%Y/%m/%d %H:%M:%S")
            time_2 = datetime.strptime('2023/05/20 00:00:00',"%Y/%m/%d %H:%M:%S")

            time_interval = time_2 - time_1
            
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="112年國中教育會考倒數", value=f"**{str(time_interval)}**\n``112年國中教育會考將在:112年5月20、21日舉辦``\n\n*倒數計時器以Asia/Taipei時區計算", inline=True)
            await interaction.response.edit_message(embed = embed, view = view)
        except:
            embed=discord.Embed(color=0xee4f9e)
            embed.add_field(name="ERROR!", value=langpack['err.message'], inline=True)
            await interaction.response.edit_message(embed = embed)
    gettime.gettime(8, '%Y/%m/%d %H:%M:%S')
    with open('time.txt', 'r', encoding = 'utf-8') as f:
        content1 = f.readlines()
        zoned_time1 = content1[0]
    time_1 = datetime.strptime(zoned_time1,"%Y/%m/%d %H:%M:%S")
    time_2 = datetime.strptime('2023/05/20 00:00:00',"%Y/%m/%d %H:%M:%S")

    time_interval = time_2 - time_1
    
    view = View(timeout = None)
    button = Button(label = '更新', style = discord.ButtonStyle.green, emoji="🔃")
    button.callback = refresh
    view.add_item(button)

    embed=discord.Embed(color=0xee4f9e)
    embed.add_field(name="112年國中教育會考倒數", value=f"**{str(time_interval)}**\n``112年國中教育會考將在:112年5月20、21日舉辦``\n\n*倒數計時器以Asia/Taipei時區計算", inline=True)
    await ctx.send(embed = embed, view = view)























#更改機器人資訊、版本資訊
#上面是測試機器人的，下面是團子機器人
#bot.run(botsetting['token'][1])
bot.run(botsetting['token'][0])