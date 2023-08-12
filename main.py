import discord, json, asyncio, random, urllib, re, psutil, ooxx, os, requests, glob, yaml
from bot_functions import *
from discord.ui import Button, View, Select, Modal
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timezone, timedelta
from typing import List
from yaml import CLoader as Loader

# 檔案載入 & 參數預建
with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
color = 0xee4f9e
testingmode = False

# 創建機器人
bot = commands.Bot(command_prefix=globaldata['PREFIX'], help_command=None, intents = discord.Intents.all())

# CommandTree建立
try: tree = app_commands.CommandTree(bot)
except: tree = bot.tree

# 機器人準備
@bot.event
async def on_ready():
    print(f"> Logged as {str(bot.user)}")
    try: 
        await bot.tree.sync()
        print("> CommandTree Synced!")
    except: print("> [!]Failed to Sync CommandTree")

    await bot.wait_until_ready()
    await asyncio.sleep(1)
    game = discord.Game(globaldata['status'])
    await bot.change_presence(status=discord.Status.online, activity=game)

    thechannel = bot.get_channel(globaldata['STARTLOGCH'])
    botguilds = bot.guilds
    embed=discord.Embed(title=loadlang("startlog")['title'], color=color)
    timestamp = str(int(round(datetime.now().timestamp())))
    embed.add_field(name = loadlang("startlog")['time'], value=f"<t:{timestamp}:F> | <t:{timestamp}:R>", inline = False)
    embed.add_field(name=loadlang("startlog")['guilds'], value=f"{str(len(botguilds))}", inline=False)
    embed.add_field(name=loadlang("startlog")['member'], value=f"{str(len(bot.users))}", inline=False)
    embed.set_footer(text=f'{loadlang("startlog")["footer"]}{globaldata["VERSION"]}')
    await thechannel.send(embed=embed)

############
##        ##
##  Note  ##
##        ##
############



######################
##                  ##
##  Function:Other  ##
##                  ##
######################
# /fbk
@tree.command(name = "fbk", description=loadlang("fbk")['des'])
async def fbk(interaction:discord.Interaction):
    await interaction.response.send_message(loadlang("fbk")['url'])

# /funstick
@tree.command(name="funstick", description=loadlang("funstick")['des'])
async def funstick(interaction: discord.Interaction):
    lang = loadlang("funstick")
    try:
        number = random.randint(1, 3)
        if number == 1: await interaction.response.send_message(content = lang['got'])
        else: await interaction.response.send_message(content = lang['fail'])
    except: await interaction.response.send_message(content=lang['error'], ephemeral=True)

# /hi
@tree.command(name = "hi", description=loadlang("hi")['des'])
async def hi(interaction: discord.Interaction):
    lang = loadlang("hi")
    try:
        r2 = random.randint(1, 3)
        if r2 == 1: await interaction.response.send_message(lang['h1'])
        elif r2 == 2: await interaction.response.send_message(lang['h2'])
        elif r2 == 3: await interaction.response.send_message(lang['h3'])
    except: await interaction.response.send_message(content=lang['error'], ephemeral=True)

# /hug
@tree.command(name = "hug", description=loadlang("hug")['des'])
async def hug(interaction: discord.Interaction):
    lang = loadlang("hug")
    try:
        button = Button(label = lang['button'], style = discord.ButtonStyle.blurple)
        view = View(timeout = None)
        async def inte1(interaction):
            try:
                button1 = Button(label = lang['button'], style = discord.ButtonStyle.blurple, disabled=True)
                view1 = View(timeout=None)
                view1.add_item(button1)
                await interaction.response.edit_message(content = lang['hugre'], view = view1)
            except: await interaction.response.edit_message(content=lang['error'], view = None)
        button.callback = inte1
        view.add_item(button)
        await interaction.response.send_message(lang['hug'], view = view, ephemeral=True)
    except: await interaction.response.send_message(content=lang['error'], ephemeral=True)

########################
##                    ##
##  Function:General  ##
##                    ##
########################

# /picgoogle
@tree.command(name =  "picgoogle", description=loadlang("picgoogle")['des'])
@app_commands.describe(msg = loadlang("picgoogle")['msgvar'])
async def picgoogle(interaction: discord.Interaction, msg: str):
    lang = loadlang("picgoogle")
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
       imageList = re.findall(r'(https:[^\s]*?(jpg|png|gif))"',page)
       x = 0
       while not x>1 :
         try:
           x = x + 1
         except:
           continue
       return imageList
    if __name__ == '__main__':
       try:
        encodedStr = f'https://{msg}.com'
        url = urllib.parse.quote(encodedStr).replace('https://', '').replace('.com', '')
        page = getHtmlCode(f'https://www.google.com/search?q={url}&tbm=isch')
        imageList = getImage(page)
        turl = str(imageList[random.randint(0, len(imageList)-1)][0])
        await interaction.response.send_message(f"{msg}\n{turl}")
       except: await interaction.response.send_message(content=lang['error'], ephemeral=True)

# /info
@tree.command(name = "info", description=loadlang("info")['des'])
async def info(interaction: discord.Interaction):
    lang = loadlang("info")
    def infoc():
        lang = loadlang("info")

        botguilds = bot.guilds
        embed=discord.Embed(title=f"**{lang['botname']}**", description=lang['ver']+globaldata['VERSION'],color=color)

        embed.add_field(name=lang['bot'], value=f"""
{lang['guilds']}:``{str(len(botguilds))}``
{lang['users']}:``{str(len(bot.users))}``""", inline=True)

        cpu = str(psutil.cpu_percent(interval=None))
        embed.add_field(name=lang['cpu'], value=f"""{lang['cores']}:``{str(psutil.cpu_count(logical=True))}``
{lang['cpup']}:``{str(cpu)}%``""", inline=True)
    
        embed.add_field(name=lang['ram'], value=f"""{lang['cpup']}:``{str(psutil.virtual_memory().percent)}%``
``{str(round(psutil.virtual_memory().used/1024/1024/1024))}GB/{str(round(psutil.virtual_memory().total/1024/1024/1024))}GB``""", inline=True)
    
        embed.add_field(name=lang['ping'], value=f"""{round(bot.latency*1000)}{lang['ms']}""", inline=True)

        return embed
    async def callback(interaction: discord.Interaction): await interaction.response.edit_message(embed = infoc())
    
    button = Button(label = lang['update'], style = discord.ButtonStyle.green)
    button.callback = callback
    view = View(timeout=None)
    view.add_item(button)

    await interaction.response.send_message(embed = infoc(), view = view)

# /ping
@tree.command(name = "ping", description=loadlang("ping")['des'])
async def ping(interaction: discord.Interaction):
    lang = loadlang("ping")
    async def pingtest():
        embed=discord.Embed(color=color)
        embed.add_field(name=lang['title'], value=f"{round(bot.latency*1000)}{lang['ms']}", inline=True)
        button = Button(label = lang['button'], style = discord.ButtonStyle.green, emoji=lang['emoji'])
        button.callback = intwe

        view = View(timeout = None)
        view.add_item(button)

        return embed, view
    async def intwe(interaction):
        try:
            embed, view = await pingtest()
            await interaction.response.edit_message(embed = embed, view = view)
        except: await interaction.response.edit_message(content=lang['error'], view= None, embed = None)
    try:
        embed, view = await pingtest()
        await interaction.response.send_message(embed=embed, view = view)
    except: await interaction.response.send_message(content=lang['error'], ephemeral=True)

# /time
@tree.command(name = "time", description=loadlang("time")['des'])
async def userinfo(interaction: discord.Interaction):
    async def gettime():
        lang = loadlang("time")
        embed=discord.Embed(color=color)
        timestamp = str(int(round(datetime.now().timestamp())))
        embed.add_field(name = lang['timenow'], value=f"<t:{timestamp}:F> | <t:{timestamp}:R>", inline = False)
        embed.add_field(name = lang['timestamp'], value=timestamp, inline = False)
        return embed
    async def buupdate(interaction: discord.Interaction):
        try: await interaction.response.edit_message(embed = await gettime())
        except: await interaction.response.edit_message(content=lang['error'], ephemeral=True, embed = None, view = None)
    lang = loadlang("time")
    try:
        view = View(timeout=None)
        button = Button(label = lang['update'], style = discord.ButtonStyle.green)
        button.callback = buupdate
        view.add_item(button)
        await interaction.response.send_message(embed = await gettime(), view = view)
    except: await interaction.response.send_message(content=lang['error'], ephemeral=True)

# /userinfo
@tree.command(name = "userinfo", description=loadlang("userinfo")['des'])
@app_commands.describe(user = loadlang("userinfo")['uservar'])
async def userinfo(interaction: discord.Interaction, user:discord.User):
    lang = loadlang("userinfo")
    try:
        async def gamerfile(interaction:discord.Interaction):
            lang = loadlang("userinfo")
            if os.path.exists(f'gamer/{str(tuser.id)}.json'):
                with open(f'gamer/{str(tuser.id)}.json', 'r', encoding = 'utf8') as f: wt1 = json.load(f)
                embed2=discord.Embed(title=lang['game']['title'], description=f"{lang['game']['des']}{tuser.name}", color=0xee4f9e)
                msg = f"{lang['game']['total']}{str(wt1['ooxx']['total'])}\n{lang['game']['wins']}{str(wt1['ooxx']['win'])}\n"
                if wt1['ooxx']['total'] != 0: msg += f"{lang['game']['winp']}\n".replace('%WIN%', str(round(wt1['ooxx']['win']/wt1['ooxx']['total']*100)))
                else: msg += f"{lang['game']['winpz']}\n"
                msg += f"{lang['game']['lose']}{str(wt1['ooxx']['lose'])}\n"
                msg += f"{lang['game']['tie']}{str(wt1['ooxx']['tie'])}"
                embed2.add_field(name = lang['game']['ooxxt'], value=msg, inline=False)
                await interaction.response.send_message(embed = embed2, ephemeral=True)
            else: await interaction.response.send_message(content=loadlang("userinfo")['game']['not'], ephemeral=True)
        tuser = user
        embed=discord.Embed(title=str(user.name), description=lang['id']+str(user.id), color=color)
        try: embed.set_thumbnail(url=user.avatar)
        except: pass
        createtime = user.created_at
        embed.add_field(name=lang['createtime'], value=f"<t:{str(int(round(createtime.timestamp())))}:f>", inline=False)
        embed.add_field(name=lang['bot'], value=str(user.bot), inline=False)

        view = View(timeout=None)
        button = Button(label = lang['gamebut'], style = discord.ButtonStyle.gray)
        button.callback = gamerfile
        view.add_item(button)

        await interaction.response.send_message(embed = embed, view = view)
    except: await interaction.response.send_message(content=lang['error'], ephemeral=True)

# /guildinfo
@tree.command(name = "guildinfo", description=loadlang("guildinfo")['des'])
async def guildinfo(interaction: discord.Interaction):
    lang = loadlang("guildinfo")
    try:
        owner = bot.get_user(interaction.guild.owner_id)
        embed=discord.Embed(title=str(interaction.guild.name), description=f"{lang['id']}{str(interaction.guild_id)}", color=color)
        try: embed.set_thumbnail(url=interaction.guild.icon)
        except: pass
        embed.add_field(name=lang['member'], value=int(len(interaction.guild.members)), inline=True)
        embed.add_field(name=lang['channel'], value=len(interaction.guild.channels), inline=True)
        embed.add_field(name = lang['owner'], value = f'{str(owner.name)}\n({str(owner.id)})', inline = True)
        embed.add_field(name = lang['create'], value = f"<t:{str(int(round((interaction.guild.created_at).timestamp())))}:f>", inline = True)
        embed.add_field(name = lang['boost'], value = f'{lang["boost_level"]}{str(interaction.guild.premium_tier)} | {str(interaction.guild.premium_subscription_count)}{lang["boosts"]}', inline = True)
        await interaction.response.send_message(embed = embed)
    except: await interaction.response.send_message(content=lang['error'], ephemeral=True)

# /tztime
@tree.command(name = "tztime", description=loadlang("tztime")['des'])
@app_commands.describe(zone = loadlang("tztime")['tzvar'])
async def userinfo(interaction: discord.Interaction, zone:int):
    async def gettime():
        lang = loadlang("tztime")
        tz = timezone(timedelta(hours=zone))
        zoned_time1 = datetime.today().astimezone(tz).strftime('%Y/%m/%d %H:%M:%S')
        embed=discord.Embed(color=color)
        embed.add_field(name = lang['timenow']+str(zone), value=f"{zoned_time1}", inline = False)
        return embed
    async def buupdate(interaction: discord.Interaction):
        try: await interaction.response.edit_message(embed = await gettime())
        except: await interaction.response.edit_message(content=lang['error'], ephemeral=True, embed = None, view = None)
    lang = loadlang("time")
    try:
        lang = loadlang("tztime")
        view = View(timeout=None)
        button = Button(label = lang['update'], style = discord.ButtonStyle.green)
        button.callback = buupdate
        view.add_item(button)
        await interaction.response.send_message(embed = await gettime(), view = view)
    except: await interaction.response.send_message(content=lang['error'], ephemeral=True)

######################
##                  ##
##  Function:Guild  ##
##                  ##
######################

# /purge
@tree.command(name = "purge", description=loadlang("purge")['des'])
@app_commands.describe(num = loadlang("purge")['numvar'])
@app_commands.checks.has_permissions(administrator = True)
async def purge(interaction: discord.Interaction, num: int):
    lang = loadlang("purge")
    if num > 0:
        try:
            await interaction.response.defer(thinking=False)
            await interaction.channel.purge(limit = num+1)
            embed=discord.Embed(color=color)
            embed.add_field(name=lang['done'], value=f"{str(num)}{lang['done2']}", inline=True)
            await interaction.channel.send(embed = embed)
        except: await interaction.response.send_message(content=lang['error'], ephemeral=True)
    else: await interaction.response.send_message(content = lang['zero'], ephemeral=True)
@purge.error
async def purge_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.errors.MissingPermissions): await interaction.response.send_message(content=loadlang("purge")['lackperm'], ephemeral=True)

# /reset
@tree.command(name = "reset", description=loadlang("reset")['des'])
@app_commands.checks.has_permissions(administrator = True)
@app_commands.describe(confirm = loadlang("reset")['confirmvar'])
async def reset(interaction: discord.Interaction, confirm:str):
    lang = loadlang("reset")
    if confirm == lang['confirmword']:
        with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
        writeset(interaction.guild_id, globaldata['format']['guilds'])
        embed=discord.Embed(title=lang['mtitle'], color=color)
        embed.add_field(name=lang['m1'], value=f"{interaction.guild.name}", inline=True)
        embed.add_field(name=lang['m2'], value=f"{str(interaction.guild_id)}", inline=True)
        await interaction.response.send_message(embed=embed)
    else: await interaction.response.send_message(content = lang['nconfirm'], ephemeral=True)
@reset.error
async def reset_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.errors.MissingPermissions): await interaction.response.send_message(content=loadlang("reset")['lackperm'], ephemeral=True)
    else: await interaction.response.send_message(embed = None, view = None, content=loadlang("reset")['error'], ephemeral=True)

#####################
##                 ##
##  Function:Game  ##
##                 ##
#####################

# /ooxx
@tree.command(name = "ooxx", description=loadlang("ooxx")['des'])
async def ooxx_view(interaction: discord.Interaction):
    # 玩家檔案建置(如果發現未建置)
    if not os.path.exists(f'gamer/{str(interaction.user.id)}.json'):
        data2 = json.dumps(globaldata['format']['gamer'])
        with open(f'gamer/{str(interaction.user.id)}.json', 'w', encoding='utf8') as f: f.write(data2)
    
    # 如果沒有存在的遊戲，就創建一個新的，不然就載入原本的遊戲
    if not os.path.exists(f'game/{str(interaction.user.id)}.json'):
        with open(f'gamer/{str(interaction.user.id)}.json', 'r', encoding='utf8') as f: data2 = json.load(f)
        data2['ooxx']['total'] += 1
        data3 = json.dumps(data2)
        with open(f'gamer/{str(interaction.user.id)}.json', 'w', encoding='utf8') as f: f.write(data3)
        
        gm = globaldata['format']['ooxxgame']
        data1 = json.dumps(gm, ensure_ascii=False)
        with open(f'game/{str(interaction.user.id)}.json', 'w', encoding = 'utf8') as f: f.write(data1)
    
    # 遊戲主體
    view = View(timeout = None)

    with open(f'game/{str(interaction.user.id)}.json', 'r', encoding = 'utf8') as f: wt1 = json.load(f)
        
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
        lang = loadlang("ooxx")
        with open(f'gamer/{str(interaction.user.id)}.json', 'r', encoding='utf8') as f: data2 = json.load(f)
        if wl == "Win":
            data2['ooxx']['win'] += 1
            data3 = json.dumps(data2)
        elif wl == "Lose":
            data2['ooxx']['lose'] += 1
            data3 = json.dumps(data2)
        elif wl == "Tie":
            data2['ooxx']['tie'] += 1
            data3 = json.dumps(data2)
        if wl == "Win" or wl == "Lose" or wl == "Tie": 
            with open(f'gamer/{str(interaction.user.id)}.json', 'w', encoding='utf8') as f: f.write(data3)
            
        for i in range(3):
            for j in range(3):
                if wl == "Win": view.add_item(Button(disabled=True, style = discord.ButtonStyle.green, label = lang['win'], row = i))
                elif wl == "Lose": view.add_item(Button(disabled=True, style = discord.ButtonStyle.danger, label = lang['fail'], row = i))
                elif wl == "Tie": view.add_item(Button(disabled=True, style = discord.ButtonStyle.gray, label = lang['tie'], row = i))
        return view

    async def click1(interaction):
        if os.path.exists(f'game/{str(interaction.user.id)}.json'):
            with open(f'game/{str(interaction.user.id)}.json', 'r', encoding = 'utf8') as f: wt1 = json.load(f)
            wt1['ox'][0] = 'O'
            tlist = ooxx.ai(wt1['ox'])
            wt1['ox'] = tlist
            data1 = json.dumps(wt1, ensure_ascii=False)
            with open(f'game/{str(interaction.user.id)}.json', 'w', encoding = 'utf8') as f: f.write(data1)
            view = gene(View(), wt1)
            wl = ooxx.wl(wt1['ox'])
            if wl != "Not yet":
                view = wlt(View(), wl)
                await interaction.response.edit_message(view = view)
                os.remove(f'game/{str(interaction.user.id)}.json')
            else:
                await interaction.response.edit_message(view = view)
        else:
            embed=discord.Embed(color=color)
            lang = loadlang("ooxx")
            embed.add_field(name=lang['error1'], value=lang['error1-1'], inline=True)
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
                embed=discord.Embed(color=color)
                lang = loadlang("ooxx")
                embed.add_field(name=lang['error1'], value=lang['error1-1'], inline=True)
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
                lang = loadlang("ooxx")
                embed=discord.Embed(color=color)
                embed.add_field(name=lang['error1'], value=lang['error1-1'], inline=True)
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
                lang = loadlang("ooxx")
                embed=discord.Embed(color=color)
                embed.add_field(name=lang['error1'], value=lang['error1-1'], inline=True)
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
                lang = loadlang("ooxx")
                embed=discord.Embed(color=color)
                embed.add_field(name=lang['error1'], value=lang['error1-1'], inline=True)
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
                lang = loadlang("ooxx")
                embed=discord.Embed(color=color)
                embed.add_field(name=lang['error1'], value=lang['error1-1'], inline=True)
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
                lang = loadlang("ooxx")
                embed=discord.Embed(color=color)
                embed.add_field(name=lang['error1'], value=lang['error1-1'], inline=True)
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
                lang = loadlang("ooxx")
                embed=discord.Embed(color=color)
                embed.add_field(name=lang['error1'], value=lang['error1-1'], inline=True)
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
                lang = loadlang("ooxx")
                embed=discord.Embed(color=color)
                embed.add_field(name=lang['error1'], value=lang['error1-1'], inline=True)
                await interaction.response.edit_message(embed=embed, view = None)

    with open(f'game/{str(interaction.user.id)}.json', 'r', encoding = 'utf8') as f: wt1 = json.load(f)
    view = gene(view, wt1)

    await interaction.response.send_message(view = view, ephemeral=True)

####################
##                ##
##  Function:TVC  ##
##                ##
####################

# /tvchadd > TVC添加主程序
@tree.command(name = "tvchadd", description=loadlang("tvc")['tvchadd']['cmddes'])
@app_commands.describe(ch = loadlang("tvc")['tvchadd']['chvar'])
@app_commands.checks.has_permissions(administrator = True)
async def tvchadd(interaction: discord.Interaction, ch: discord.VoiceChannel):
    lang = loadlang("tvc")
    guildadder(interaction.guild)
    wt1 = loadset(interaction.guild_id)
    tid = int(ch.id)

    with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
    if len(wt1['tvc']) < globaldata['TVC_LIMIT']:
        alexist = False
        for chid in wt1['tvc']:
            if int(chid) == int(tid):
                alexist = True
                break
        if alexist == False:
            try: channel = bot.get_channel(int(tid))
            except Exception as e: channel = None
            if channel != None:
                wt1['tvc'].append(int(channel.id))
                writeset(interaction.guild_id, wt1)
                embed=discord.Embed(color=color)
                embed.add_field(name=lang['tvchadd']['add'], value=f"{lang['tvchadd']['addchn']}{channel.name}\n{lang['tvchadd']['addchn2']}{str(channel.id)}", inline=True)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else: await interaction.response.send_message(content = lang['tvchadd']['error'], ephemeral=True)
        else:
            embed=discord.Embed(color=color)
            embed.add_field(name=lang['tvchadd']['error-simple'], value=lang['tvchadd']['already'], inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
    else: 
        embed=discord.Embed(color=color)
        embed.add_field(name=lang['tvchadd']['error-simple'], value=lang['tvchadd']['over'].replace("%LIMIT%",globaldata['TVC_LIMIT']), inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)
@tvchadd.error
async def tvchadd_error(interaction: discord.Interaction, error):
    lang = loadlang("tvc")
    if isinstance(error, discord.app_commands.errors.MissingPermissions): await interaction.response.send_message(content=lang['lackperm'], ephemeral=True)
    else: await interaction.response.send_message(embed = None, view = None, content=lang['tvchadd']["error"], ephemeral=True)
# /tvc
@tree.command(name = "tvc", description=loadlang("tvc")['tvcmain']['cmddes'])
@app_commands.checks.has_permissions(administrator = True)
async def tvcmain(interaction: discord.Interaction):
    # TVC添加
    async def addtvc(interaction: discord.Interaction): await interaction.response.send_message(content = lang['tvcmain']['tvcadd'], ephemeral=True)
    # TVC刪除
    async def tvcdel(interaction: discord.Interaction):
        async def backbut(interaction: discord.Interaction):
            embed, view = await tvcmainmenu(interaction)
            await interaction.response.edit_message(content = None, embed = embed, view = view)
        async def tvcdelmain(interaction: discord.Interaction):
            lang = loadlang("tvc")
            guildadder(interaction.guild)
            wt1 = loadset(interaction.guild_id)

            with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
            wt1 = loadset(interaction.guild_id)
            exist = False
            tvc2 = []
            for chid in wt1['tvc']:
                if int(chid) == int(select.values[0]):
                    exist = True
                    continue
                tvc2.append(chid)
            wt1['tvc'] = tvc2
            writeset(interaction.guild_id, wt1)
            if exist == True:
                embed=discord.Embed(color=color)
                embed.add_field(name=lang['tvcmain']['del'], value=f"{lang['tvcmain']['del-1']}{str(select.values[0])}", inline=True)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed=discord.Embed(color=color)
                embed.add_field(name=lang['tvcmain']['error'], value=lang['tvcmain']['notbe'], inline=True)
                await interaction.response.send_message(embed=embed, ephemeral=True)
        lang = loadlang("tvc")
        guildadder(interaction.guild)
        wt1 = loadset(interaction.guild_id)

        embed = discord.Embed(title = lang['tvcmain']['del-title'], description=lang['tvcmain']['del-des'], color = color)
        embed.set_footer(text = f"{lang['tvcmain']['del-footer']}{globaldata['TVC_LIMIT']}")

        view = View(timeout = None)
        options = []
        for vc in wt1['tvc']: 
            try: 
                v = bot.get_channel(int(vc))
                options.append(discord.SelectOption(label = v.name, emoji=lang['tvcmain']['access-emoji'], description=f"{lang['tvcmain']['access-des']}{str(v.id)}", value=v.id))
            except: options.append(discord.SelectOption(label = lang['tvcmain']['cant-access'], emoji=lang['tvcmain']['cant-access-emoji'], description=f"{lang['tvcmain']['access-des']}{str(vc)}", value=int(vc)))
        if len(options) == 0: view.add_item(Select(placeholder=lang['tvcmain']['nochoice'], disabled=True, options=[discord.SelectOption(label = lang['tvcmain']['nocho-1'], value = lang['tvcmain']['nocho-2'])]))
        elif len(options) > 0 and len(options) <= 25:
            select = Select(placeholder=lang['tvcmain']['selectone'], options = options)
            select.callback = tvcdelmain
            view.add_item(select)
        backbutton = Button(label = lang['tvcmain']['back'], style = discord.ButtonStyle.gray)
        backbutton.callback = backbut
        view.add_item(backbutton)

        await interaction.response.edit_message(embed = embed, view = view)
    
    # TVC列表/主選單
    async def tvcmainmenu(interaction: discord.Interaction):
        lang = loadlang("tvc")
        guildadder(interaction.guild)
        wt1 = loadset(interaction.guild_id)
        with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)

        embed = discord.Embed(title = lang['p1']['title'], color = color)
        text, n = "", 0
        for chid in wt1['tvc']:
            try: channel = bot.get_channel(int(chid))
            except: channel = None
            if channel != None: text += f'[{str(n)}]{str(channel)}({str(channel.id)})\n'
            else: text += f'[{str(n)}]{lang["p1"]["naccess"]}({str(chid)})\n'
            n += 1
        if text == "": text = lang["p1"]["notvc"]
        embed.add_field(name = lang["p1"]["tvclist"], value = text, inline = False)

        view = View(timeout = None)
        button = Button(label = lang["p1"]["add"], style=discord.ButtonStyle.green)
        button2 = Button(label = lang["p1"]["del"], style = discord.ButtonStyle.red)
        button.callback = addtvc
        button2.callback = tvcdel
        view.add_item(button)
        view.add_item(button2)

        return embed, view

    lang = loadlang("tvc")
    guildadder(interaction.guild)
    wt1 = loadset(interaction.guild_id)
    with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)

    embed, view = await tvcmainmenu(interaction)
    await interaction.response.send_message(embed = embed, view = view, ephemeral=True)
@tvcmain.error
async def tvcmain_error(interaction: discord.Interaction, error):
    lang = loadlang("tvc")
    if isinstance(error, discord.app_commands.errors.MissingPermissions): await interaction.response.send_message(content=lang['lackperm'], ephemeral=True)
    else: await interaction.response.send_message(embed = None, view = None, content=lang["tvchadd"]["error"], ephemeral=True)

# TVC voice activity listener
@bot.event
async def on_voice_state_update(member, before, after):
    lang = loadlang("tvc")
    chame = lang['chame']
    guildadder(member.guild)
    wt1 = loadset(member.guild.id)
    with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
    try:
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
                    if v.name == f"{str(member)}{chame}" and str(v.type) == 'voice':
                        await member.move_to(v)
                        found = True
                        break
                if found == False:
                    tcategory = after.channel.category
                    tchannel = await after.channel.guild.create_voice_channel(f"{str(member)}{chame}", category = tcategory)
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
                        if v.name == f"{str(member)}{chame}" and str(v.type) == 'voice':
                            await member.move_to(v)
                            found = True
                            break
                    if found == False:
                        tcategory = after.channel.category
                        tchannel = await after.channel.guild.create_voice_channel(f"{str(member)}{chame}", category = tcategory)
                        await member.move_to(tchannel)
                else:
                    if f"{chame}" in before.channel.name:
                        if len(before.channel.members) == 0: await before.channel.delete()
        if ist == False:
            if f"{chame}" in before.channel.name:
                if len(before.channel.members) == 0: await before.channel.delete()
    except Exception as e: print(f"TVC ERR > {str(e)}")

#######################
##                   ##
##  EVENT LISTENERS  ##
##                   ##
#######################

@bot.event
async def on_guild_join(guild): guildadder(guild)

##################################
##                              ##
##  Function:Welcome and Leave  ##
##                              ##
##################################

# /welcome
# 資料自檢/修復缺漏項
def autofix(interaction: discord.Interaction, wt1: dict):
    wt1 = afx(wt1)
    # 最終寫回 & 回傳修復過的資料
    writeset(interaction.guild_id, wt1)
    return wt1
def autofix2(gid:int, wt1:dict):
    wt1 = afx(wt1)
    # 最終寫回 & 回傳修復過的資料
    writeset(gid, wt1)
    return wt1
def afx(wt1:dict):
    # 歡迎部分
    welmsgnull, weltoggle, welchannel, welrole, weldm, dmtoggle, roletoggle = False, False, False, False, False, False, False
    for w in wt1['welcome']:
        if w == "welmsg": welmsgnull = True
        if w == "weltoggle": weltoggle = True
        if w == "channel": welchannel = True
        if w == "welrole": welrole = True
        if w == "weldm": weldm = True
        if w == "dmtoggle": dmtoggle = True
        if w == "roletoggle": roletoggle = True
    if welmsgnull == False: wt1['welcome']['welmsg'] = ""
    if weltoggle == False: wt1['welcome']['weltoggle'] = False
    else: 
        if wt1['welcome']['weltoggle'] == "true" or wt1['welcome']['weltoggle'] == "True": wt1['welcome']['weltoggle'] = True
        elif wt1['welcome']['weltoggle'] == "false" or wt1['welcome']['weltoggle'] == "False": wt1['welcome']['weltoggle'] = False
    if welchannel == False: wt1['welcome']['channel'] = None
    if welrole == False: wt1['welcome']['welrole'] = None
    if weldm == False: wt1['welcome']['weldm'] = ""
    if dmtoggle == False: wt1['welcome']['dmtoggle'] = False
    else: 
        if wt1['welcome']['dmtoggle'] == "true" or wt1['welcome']['dmtoggle'] == "True": wt1['welcome']['dmtoggle'] = True
        elif wt1['welcome']['dmtoggle'] == "false" or wt1['welcome']['dmtoggle'] == "False": wt1['welcome']['dmtoggle'] = False
    if roletoggle == False: wt1['welcome']['roletoggle'] = False
    else: 
        if wt1['welcome']['roletoggle'] == "true" or wt1['welcome']['roletoggle'] == "True": wt1['welcome']['roletoggle'] = True
        elif wt1['welcome']['roletoggle'] == "false" or wt1['welcome']['roletoggle'] == "False": wt1['welcome']['roletoggle'] = False

    #離開部分
    lefmsgnull, leftoggle, lefchannel = False, False, False
    for w in wt1['leave']:
        if w == "msg": lefmsgnull = True
        if w == "toggle": leftoggle = True
        if w == "channel": lefchannel = True
    if lefchannel == False: wt1['leave']['channel'] = None
    if leftoggle == False: wt1['leave']['toggle'] = False
    else:
        if wt1['leave']['toggle'] == "true" or wt1['leave']['toggle'] == "True": wt1['leave']['toggle'] = True
        elif wt1['leave']['toggle'] == "false" or wt1['leave']['toggle'] == "False": wt1['leave']['toggle'] = False
    if lefmsgnull == False: wt1['leave']['msg'] = ""

    return wt1
# 說明: 變數 - 共用項目
async def variable_notice(interaction: discord.Interaction):
    await interaction.response.send_message(content=loadlang("welcome")['var-notice'], ephemeral=True)
@tree.command(name = "welcome", description=loadlang("welcome")['cmddes'])
@app_commands.checks.has_permissions(administrator = True)
async def welcomemain(interaction: discord.Interaction):
    # 返回 - 共用項目
    async def backmain(interaction: discord.Interaction):
        lang = loadlang("welcome")
        guildadder(interaction.guild)
        wt1 = loadset(interaction.guild_id)
        with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
        wt1 = autofix(interaction, wt1)

        embed, view = mainmenu(interaction)
        await interaction.response.edit_message(embed = embed, view = view)
    # 歡迎訊息介面
    async def welmsg(interaction: discord.Interaction):
        # 歡迎訊息開關
        async def welopen(interaction: discord.Interaction):
            lang = loadlang("welcome")
            guildadder(interaction.guild)
            wt1 = loadset(interaction.guild_id)
            with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
            wt1 = autofix(interaction, wt1)

            wt1['welcome']['weltoggle'] = True
            writeset(interaction.guild_id, wt1)
            embed, view = await welmsgmenu(interaction)
            await interaction.response.edit_message(embed = embed, view = view)
        async def welclose(interaction: discord.Interaction):
            lang = loadlang("welcome")
            guildadder(interaction.guild)
            wt1 = loadset(interaction.guild_id)
            with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
            wt1 = autofix(interaction, wt1)

            wt1['welcome']['weltoggle'] = False
            writeset(interaction.guild_id, wt1)
            embed, view = await welmsgmenu(interaction)
            await interaction.response.edit_message(embed = embed, view = view)
        # 設定歡迎訊息
        class weltextmodal(Modal, title = loadlang("welcome")['welmsg']['setmsg-1']):
            answer = discord.ui.TextInput(label = loadlang("welcome")['welmsg']['setmsg-2'], style=discord.TextStyle.short, placeholder=loadlang("welcome")['welmsg']['setmsg-3'], required=False)
            async def on_submit(self, interaction:discord.Interaction):
                lang = loadlang("welcome")
                guildadder(interaction.guild)
                wt1 = loadset(interaction.guild_id)
                with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
                wt1 = autofix(interaction, wt1)
    
                wt1['welcome']['welmsg'] = str(self.answer.value)
                writeset(interaction.guild_id, wt1)
                embed, view = await welmsgmenu(interaction)
                await interaction.response.edit_message(embed = embed, view = view)   
        async def weltextmod(interaction:discord.Interaction): await interaction.response.send_modal(weltextmodal())
        # 歡迎訊息頻道
        async def welchannel_notice(interaction: discord.Interaction):
            lang = loadlang("welcome")
            guildadder(interaction.guild)
            wt1 = loadset(interaction.guild_id)
            with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
            wt1 = autofix(interaction, wt1)

            await interaction.response.send_message(content = lang['welmsg']['welchannel'], ephemeral=True)
        # 歡迎訊息主介面
        async def welmsgmenu(interaction: discord.Interaction):
            lang = loadlang("welcome")
            guildadder(interaction.guild)
            wt1 = loadset(interaction.guild_id)

            with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)

            # 資料自檢/修復缺漏項
            wt1 = autofix(interaction, wt1)
            # 錯誤檢查
            errmsg = ""
            if wt1['welcome']['weltoggle']:
                if wt1['welcome']['welmsg'] == "": errmsg += lang['welmsg']['err-blank']+"\n"
                if wt1['welcome']['channel'] == None: errmsg += lang['welmsg']['err-channelns']+"\n"
                else: 
                    channel = bot.get_channel(int(wt1['welcome']['channel']))
                    if channel == None: errmsg += lang['welmsg']['err-channelnu']+"\n"

            # 參數準備
            tfopen = lang['welmsg']['toggle-c']
            if wt1['welcome']['weltoggle'] == True: tfopen = lang['welmsg']['toggle-o']
            welmsgcon = wt1['welcome']['welmsg']
            if welmsgcon == "": welmsgcon = lang['welmsg']['msgns']
            if wt1['welcome']['channel'] != None:
                channel = bot.get_channel(int(wt1['welcome']['channel']))
                if channel == None: chmsg = lang['welmsg']['chna']
                else: chmsg = f"{channel.name}({str(channel.id)})"
            else: chmsg = lang['welmsg']['chns']

            # 介面(Embed & View)
            embed = discord.Embed(title = lang['welmsg']['mtitle'], color = color)
            embed.add_field(name = lang['welmsg']['mtoggle'], value=tfopen, inline = False)
            embed.add_field(name = lang['welmsg']['mcontent'], value=welmsgcon, inline = False)
            embed.add_field(name = lang['welmsg']['mchannel'], value=chmsg) # 顯示歡迎訊息頻道
            embed.set_footer(text = errmsg)

            view = View(timeout=None)
            if wt1['welcome']['weltoggle']: 
                button1 = Button(label = lang['welmsg']['btsta-o'], style = discord.ButtonStyle.green)
                button1.callback = welclose
            else: 
                button1 = Button(label = lang['welmsg']['btsta-c'], style = discord.ButtonStyle.red)
                button1.callback = welopen

            button2 = Button(label = lang['welmsg']['btmsg'], style = discord.ButtonStyle.blurple)
            button2.callback = weltextmod
            button3 = Button(label = lang['welmsg']['btch'], style = discord.ButtonStyle.blurple)
            button3.callback = welchannel_notice
            button4 = Button(label = lang['btvar'], style = discord.ButtonStyle.gray)
            button4.callback = variable_notice
            button5 = Button(label = lang['back'], style = discord.ButtonStyle.gray, row = 1)
            button5.callback = backmain

            view.add_item(button1)
            view.add_item(button2)
            view.add_item(button3)
            view.add_item(button4)
            view.add_item(button5)

            return embed, view
        # 主程序
        lang = loadlang("welcome")
        guildadder(interaction.guild)
        wt1 = loadset(interaction.guild_id)

        with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)

        embed, view = await welmsgmenu(interaction)

        await interaction.response.edit_message(embed = embed, view = view)
    ##############################
    # 歡迎私人訊息
    async def welmsgdm(interaction: discord.Interaction): 
        # 歡迎私人訊息開關
        async def weldmopen(interaction: discord.Interaction):
            lang = loadlang("welcome")
            guildadder(interaction.guild)
            wt1 = loadset(interaction.guild_id)
            with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
            wt1 = autofix(interaction, wt1)

            wt1['welcome']['dmtoggle'] = True
            writeset(interaction.guild_id, wt1)
            embed, view = await weldmmsgmenu(interaction)
            await interaction.response.edit_message(embed = embed, view = view)
        async def weldmclose(interaction: discord.Interaction):
            lang = loadlang("welcome")
            guildadder(interaction.guild)
            wt1 = loadset(interaction.guild_id)
            with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
            wt1 = autofix(interaction, wt1)

            wt1['welcome']['dmtoggle'] = False
            writeset(interaction.guild_id, wt1)
            embed, view = await weldmmsgmenu(interaction)
            await interaction.response.edit_message(embed = embed, view = view)
        # 設定歡迎私人訊息
        class weldmtextmodal(Modal, title = loadlang("welcome")['weldm']['setmsg-1']):
            answer = discord.ui.TextInput(label = loadlang("welcome")['weldm']['setmsg-2'], style=discord.TextStyle.short, placeholder=loadlang("welcome")['weldm']['setmsg-3'], required=False)
            async def on_submit(self, interaction:discord.Interaction):
                lang = loadlang("welcome")
                guildadder(interaction.guild)
                wt1 = loadset(interaction.guild_id)
                with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
                wt1 = autofix(interaction, wt1)
    
                wt1['welcome']['weldm'] = str(self.answer.value)
                writeset(interaction.guild_id, wt1)
                embed, view = await weldmmsgmenu(interaction)
                await interaction.response.edit_message(embed = embed, view = view)   
        async def weldmtextmod(interaction:discord.Interaction): await interaction.response.send_modal(weldmtextmodal())
        # 歡迎私人訊息主介面
        async def weldmmsgmenu(interaction: discord.Interaction):
            lang = loadlang("welcome")
            guildadder(interaction.guild)
            wt1 = loadset(interaction.guild_id)

            with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)

            # 資料自檢/修復缺漏項
            wt1 = autofix(interaction, wt1)
            # 錯誤檢查
            errmsg = ""
            if wt1['welcome']['dmtoggle']:
                if wt1['welcome']['weldm'] == "": errmsg += lang['weldm']['err-blank']+"\n"

            # 參數準備
            tfopen = lang['welmsg']['toggle-c']
            if wt1['welcome']['dmtoggle'] == True: tfopen = lang['welmsg']['toggle-o']
            welmsgcon = wt1['welcome']['weldm']
            if welmsgcon == "": welmsgcon = lang['welmsg']['msgns']

            # 介面(Embed & View)
            embed = discord.Embed(title = lang['welmsg']['mtitle'], color = color)
            embed.add_field(name = lang['welmsg']['mtoggle'], value=tfopen, inline = False)
            embed.add_field(name = lang['welmsg']['mcontent'], value=welmsgcon, inline = False)
            embed.set_footer(text = errmsg)

            view = View(timeout=None)
            if wt1['welcome']['dmtoggle']: 
                button1 = Button(label = lang['welmsg']['btsta-o'], style = discord.ButtonStyle.green)
                button1.callback = weldmclose
            else: 
                button1 = Button(label = lang['welmsg']['btsta-c'], style = discord.ButtonStyle.red)
                button1.callback = weldmopen

            button2 = Button(label = lang['welmsg']['btmsg'], style = discord.ButtonStyle.blurple)
            button2.callback = weldmtextmod
            button4 = Button(label = lang['btvar'], style = discord.ButtonStyle.gray)
            button4.callback = variable_notice
            button5 = Button(label = lang['back'], style = discord.ButtonStyle.gray, row = 1)
            button5.callback = backmain

            view.add_item(button1)
            view.add_item(button2)
            view.add_item(button4)
            view.add_item(button5)

            return embed, view
        # 主程序
        lang = loadlang("welcome")
        guildadder(interaction.guild)
        wt1 = loadset(interaction.guild_id)

        with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)

        embed, view = await weldmmsgmenu(interaction)

        await interaction.response.edit_message(embed = embed, view = view)
    ##############################
    # 新人身分組
    async def welrole(interaction: discord.Interaction): 
        # 新人身分組開關
        async def welroleopen(interaction: discord.Interaction):
            lang = loadlang("welcome")
            guildadder(interaction.guild)
            wt1 = loadset(interaction.guild_id)
            with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
            wt1 = autofix(interaction, wt1)

            wt1['welcome']['roletoggle'] = True
            writeset(interaction.guild_id, wt1)
            embed, view = await welrolemenu(interaction)
            await interaction.response.edit_message(embed = embed, view = view)
        async def welroleclose(interaction: discord.Interaction):
            lang = loadlang("welcome")
            guildadder(interaction.guild)
            wt1 = loadset(interaction.guild_id)
            with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
            wt1 = autofix(interaction, wt1)

            wt1['welcome']['roletoggle'] = False
            writeset(interaction.guild_id, wt1)
            embed, view = await welrolemenu(interaction)
            await interaction.response.edit_message(embed = embed, view = view)
        # 設定新人身分組
        async def welrole_notice(interaction: discord.Interaction):
            lang = loadlang("welcome")
            guildadder(interaction.guild)
            wt1 = loadset(interaction.guild_id)
            with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
            wt1 = autofix(interaction, wt1)

            await interaction.response.send_message(content = lang['welrole']['welroleset'], ephemeral=True)
        # 新人身分組主介面
        async def welrolemenu(interaction: discord.Interaction):
            lang = loadlang("welcome")
            guildadder(interaction.guild)
            wt1 = loadset(interaction.guild_id)

            with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)

            # 資料自檢/修復缺漏項
            wt1 = autofix(interaction, wt1)
            # 錯誤檢查
            errmsg = ""
            if wt1['welcome']['roletoggle']:
                if wt1['welcome']['welrole'] == None: errmsg += lang['welrole']['err-ns']+"\n"
                else: 
                    role = interaction.guild.get_role(int(wt1['welcome']['welrole']))
                    if role == None: errmsg += lang['welrole']['err-nu']+"\n"

            # 參數準備
            tfopen = lang['welmsg']['toggle-c']
            if wt1['welcome']['roletoggle'] == True: tfopen = lang['welmsg']['toggle-o']
            if wt1['welcome']['welrole'] != None:
                role = interaction.guild.get_role(int(wt1['welcome']['welrole']))
                if role == None: chmsg = lang['welrole']['rolenu']
                else: chmsg = f"{role.name}({str(role.id)})"
            else: chmsg = lang['welrole']['rolens']

            # 介面(Embed & View)
            embed = discord.Embed(title = lang['welrole']['mtitle'], color = color)
            embed.add_field(name = lang['welrole']['mtoggle'], value=tfopen, inline = False)
            embed.add_field(name = lang['welrole']['mrole'], value=chmsg, inline = False)
            embed.set_footer(text = errmsg)

            view = View(timeout=None)
            if wt1['welcome']['roletoggle']: 
                button1 = Button(label = lang['welmsg']['btsta-o'], style = discord.ButtonStyle.green)
                button1.callback = welroleclose
            else: 
                button1 = Button(label = lang['welmsg']['btsta-c'], style = discord.ButtonStyle.red)
                button1.callback = welroleopen

            button2 = Button(label = lang['btvar'], style = discord.ButtonStyle.blurple)
            button2.callback = welrole_notice
            button5 = Button(label = lang['back'], style = discord.ButtonStyle.gray, row = 1)
            button5.callback = backmain

            view.add_item(button1)
            view.add_item(button2)
            view.add_item(button5)

            return embed, view
        # 主程序
        lang = loadlang("welcome")
        guildadder(interaction.guild)
        wt1 = loadset(interaction.guild_id)

        with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)

        embed, view = await welrolemenu(interaction)

        await interaction.response.edit_message(embed = embed, view = view)

    # 主介面
    def mainmenu(interaction: discord.Interaction):
        lang = loadlang("welcome")
        guildadder(interaction.guild)
        wt1 = loadset(interaction.guild_id)

        with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)

        embed = discord.Embed(title = lang['main']['title'], description=lang['main']['des'], color = color)

        view = View(timeout = None)
        button1 = Button(label = lang['main']['btwelmsg'], style = discord.ButtonStyle.green, row = 0)
        button1.callback = welmsg
        button2 = Button(label = lang['main']['btweldm'], style = discord.ButtonStyle.green, row = 0)
        button2.callback = welmsgdm
        button3 = Button(label = lang['main']['btwelrole'], style = discord.ButtonStyle.green, row = 0)
        button3.callback = welrole
        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)

        return embed, view
    lang = loadlang("welcome")
    guildadder(interaction.guild)
    wt1 = loadset(interaction.guild_id)

    with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)

    embed, view = mainmenu(interaction)

    await interaction.response.send_message(embed = embed, view = view, ephemeral=True)
@welcomemain.error
async def welcomemain_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.errors.MissingPermissions): await interaction.response.send_message(content=loadlang("welcome")['lackperm'], ephemeral=True)
    else: await interaction.response.send_message(embed = None, view = None, content=loadlang("welcome")['error'], ephemeral=True)
# /welchannel
@tree.command(name = "welchannel", description=loadlang("welcome")['welchannel']['cmddes'])
@app_commands.describe(channel = loadlang("welcome")['welchannel']['channelvar'])
@app_commands.checks.has_permissions(administrator = True)
async def welchannel(interaction: discord.Interaction, channel: discord.TextChannel):
    #資料準備
    lang = loadlang("welcome")
    guildadder(interaction.guild)
    wt1 = loadset(interaction.guild_id)
    with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)

    #資料缺漏補
    wt1 = autofix(interaction, wt1)

    # 修改資料
    wt1['welcome']['channel'] = int(channel.id)
    writeset(interaction.guild_id, wt1)

    # response
    embed = discord.Embed(title = lang['welchannel']['mtitle'], color = color)
    embed.add_field(name = lang['welchannel']['mname'], value=f"{channel.name}\n{lang['welchannel']['mdes']}{str(channel.id)}")
    await interaction.response.send_message(embed = embed, ephemeral=True)
@welchannel.error
async def welchannel_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.errors.MissingPermissions): await interaction.response.send_message(content=loadlang("welcome")['lackperm'], ephemeral=True)
    else: await interaction.response.send_message(embed = None, view = None, content=loadlang("welcome")['error'], ephemeral=True)
# /welrole
@tree.command(name = "welrole", description=loadlang("welcome")['welrolecmd']['cmddes'])
@app_commands.describe(role = loadlang("welcome")['welrolecmd']['rolevar'])
@app_commands.checks.has_permissions(administrator = True)
async def welroleadder(interaction: discord.Interaction, role: discord.Role):
    #資料準備
    lang = loadlang("welcome")
    guildadder(interaction.guild)
    wt1 = loadset(interaction.guild_id)
    with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)

    #資料缺漏補
    wt1 = autofix(interaction, wt1)

    # 修改資料
    wt1['welcome']['welrole'] = int(role.id)
    writeset(interaction.guild_id, wt1)

    # response
    embed = discord.Embed(title = lang['welrolecmd']['mtitle'], color = color)
    embed.add_field(name = lang['welrolecmd']['mname'], value=f"{role.name}\n{lang['welrolecmd']['mdes']}{str(role.id)}")
    await interaction.response.send_message(embed = embed, ephemeral=True)
@welroleadder.error
async def welroleadder_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.errors.MissingPermissions): await interaction.response.send_message(content=loadlang("welcome")['lackperm'], ephemeral=True)
    else: await interaction.response.send_message(embed = None, view = None, content=loadlang("welcome")['error'], ephemeral=True)

### Member Join Event Listener
@bot.event
async def on_member_join(member: discord.Member):
    # 資料修復
    try:
        guildadder(member.guild)
        wt1 = loadset(member.guild.id)
        with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
        wt1 = autofix2(member.guild.id, wt1)
    except: pass

    # 歡迎訊息寄送
    try:
        wt1 = loadset(member.guild.id)
        if wt1['welcome']['weltoggle'] == True and wt1['welcome']['welmsg'] != '' and wt1['welcome']['channel'] != None:
            msg = wt1['welcome']['welmsg'].replace('>gname<', member.guild.name).replace('>tagm<', member.mention).replace('>mname<', member.name)
            channel = bot.get_channel(wt1['welcome']['channel'])
            await channel.send(msg)
    except Exception as e: print(f"WELMSG ERR > GUILD({member.guild.id});MEMBER({member.id}) > {str(e)}")
    
    # 新人身分組
    try:
        wt1 = loadset(member.guild.id)
        if wt1['welcome']['roletoggle'] == True and wt1['welcome']['welrole'] != None:
            role = member.guild.get_role(int(wt1['welcome']['welrole']))
            await member.add_roles(role, atomic = True)
    except Exception as e: print(f"WELROLE ERR > GUILD({member.guild.id});MEMBER({member.id}) > {str(e)}")
    
    # 私人歡迎訊息
    try:
        wt1 = loadset(member.guild.id)
        if wt1['welcome']['dmtoggle'] == True and wt1['welcome']['weldm'] != '':
            user = bot.get_user(member.id)
            if user != None:
                if user.dm_channel == None: await user.create_dm()
                msg = wt1['welcome']['weldm'].replace('>gname<', member.guild.name).replace('>tagm<', member.mention).replace('>mname<', member.name)

                view = View()
                view.add_item(Button(label=loadlang("welcome")['listener']['dmfrom']+member.guild.name, style = discord.ButtonStyle.green, disabled=True))

                await user.dm_channel.send(msg, view = view)
    except Exception as e: print(f"WELDM ERR > GUILD({member.guild.id});MEMBER({member.id}) > {str(e)}")

# /leave
@tree.command(name = "leave", description=loadlang("leave")['cmddes'])
@app_commands.checks.has_permissions(administrator = True)
async def leavemain(interaction: discord.Interaction):
    # 離開訊息開關
    async def lefopen(interaction: discord.Interaction):
        lang = loadlang("leave")
        guildadder(interaction.guild)
        wt1 = loadset(interaction.guild_id)
        with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
        wt1 = autofix(interaction, wt1)

        wt1['leave']['toggle'] = True
        writeset(interaction.guild_id, wt1)
        embed, view = await leavemainmenu(interaction)
        await interaction.response.edit_message(embed = embed, view = view)
    async def lefclose(interaction: discord.Interaction):
        lang = loadlang("leave")
        guildadder(interaction.guild)
        wt1 = loadset(interaction.guild_id)
        with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
        wt1 = autofix(interaction, wt1)

        wt1['leave']['toggle'] = False
        writeset(interaction.guild_id, wt1)
        embed, view = await leavemainmenu(interaction)
        await interaction.response.edit_message(embed = embed, view = view)
    # 設定離開訊息
    class leftextmodal(Modal, title = loadlang("leave")['msg']['title']):
        answer = discord.ui.TextInput(label = loadlang("leave")['msg']['name'], style=discord.TextStyle.short, placeholder=loadlang("leave")['msg']['des'], required=False)
        async def on_submit(self, interaction:discord.Interaction):
            lang = loadlang("leave")
            guildadder(interaction.guild)
            wt1 = loadset(interaction.guild_id)
            with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
            wt1 = autofix(interaction, wt1)
    
            wt1['leave']['msg'] = str(self.answer.value)
            writeset(interaction.guild_id, wt1)
            embed, view = await leavemainmenu(interaction)
            await interaction.response.edit_message(embed = embed, view = view)   
    async def leftextmod(interaction:discord.Interaction): await interaction.response.send_modal(leftextmodal())
    # 離開訊息頻道
    async def lefchannel_notice(interaction: discord.Interaction):
        lang = loadlang("leave")
        guildadder(interaction.guild)
        wt1 = loadset(interaction.guild_id)
        with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
        wt1 = autofix(interaction, wt1)

        await interaction.response.send_message(content = lang['channel']['notice'], ephemeral=True)
    
    # 離開訊息主介面
    async def leavemainmenu(interaction: interaction):
        lang = loadlang("leave")
        guildadder(interaction.guild)
        wt1 = loadset(interaction.guild_id)

        with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)

        # 資料自檢/修復缺漏項
        wt1 = autofix(interaction, wt1)
        # 錯誤檢查
        errmsg = ""
        if wt1['leave']['toggle']:
            if wt1['leave']['msg'] == "": errmsg += lang['main']['err-blank']+"\n"
            if wt1['leave']['channel'] == None: errmsg += lang['main']['err-chns']+"\n"
            else: 
                channel = bot.get_channel(int(wt1['leave']['channel']))
                if channel == None: errmsg += lang['main']['err-chnu']+"\n"

        # 參數準備
        tfopen = lang['main']['toggle-c']
        if wt1['leave']['toggle'] == True: tfopen = lang['main']['toggle-o']
        welmsgcon = wt1['leave']['msg']
        if welmsgcon == "": welmsgcon = lang['main']['msgns']
        if wt1['leave']['channel'] != None:
            channel = bot.get_channel(int(wt1['leave']['channel']))
            if channel == None: chmsg = lang['main']['chnu']
            else: chmsg = f"{channel.name}({str(channel.id)})"
        else: chmsg = lang['main']['chns']

        # 介面(Embed & View)
        embed = discord.Embed(title = lang['main']['mtitle'], color = color)
        embed.add_field(name = lang['main']['mtoggle'], value=tfopen, inline = False)
        embed.add_field(name = lang['main']['mcontent'], value=welmsgcon, inline = False)
        embed.add_field(name = lang['main']['mchannel'], value=chmsg)
        embed.set_footer(text = errmsg)

        view = View(timeout=None)
        if wt1['leave']['toggle']: 
            button1 = Button(label = lang['main']['bto'], style = discord.ButtonStyle.green)
            button1.callback = lefclose
        else: 
            button1 = Button(label = lang['main']['btc'], style = discord.ButtonStyle.red)
            button1.callback = lefopen

        button2 = Button(label = lang['main']['btmsg'], style = discord.ButtonStyle.blurple)
        button2.callback = leftextmod
        button3 = Button(label = lang['main']['btch'], style = discord.ButtonStyle.blurple)
        button3.callback = lefchannel_notice
        button4 = Button(label = lang['main']['btvar'], style = discord.ButtonStyle.gray)
        button4.callback = variable_notice

        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)
        view.add_item(button4)

        return embed, view
    lang = loadlang("leave")
    guildadder(interaction.guild)
    wt1 = loadset(interaction.guild_id)
    with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
    wt1 = autofix(interaction, wt1)

    embed, view = await leavemainmenu(interaction)

    await interaction.response.send_message(embed = embed, view = view, ephemeral=True)
@leavemain.error
async def leavemain_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.errors.MissingPermissions): await interaction.response.send_message(content=loadlang("leave")['lackperm'], ephemeral=True)
    else: await interaction.response.send_message(embed = None, view = None, content=loadlang("leave")['err'], ephemeral=True)
# /lefchannel
@tree.command(name = "lefchannel", description=loadlang("leave")['lefch']['cmddes'])
@app_commands.describe(channel = loadlang("leave")['lefch']['channelvar'])
@app_commands.checks.has_permissions(administrator = True)
async def lefchannel(interaction: discord.Interaction, channel: discord.TextChannel):
    #資料準備
    lang = loadlang("leave")
    guildadder(interaction.guild)
    wt1 = loadset(interaction.guild_id)
    with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)

    #資料缺漏補
    wt1 = autofix(interaction, wt1)

    # 修改資料
    wt1['leave']['channel'] = int(channel.id)
    writeset(interaction.guild_id, wt1)

    # response
    embed = discord.Embed(title = lang['lefch']['title'], color = color)
    embed.add_field(name = lang['lefch']['name'], value=f"{channel.name}\n{lang['lefch']['des']}{str(channel.id)}")
    await interaction.response.send_message(embed = embed, ephemeral=True)
@lefchannel.error
async def lefchannel_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.errors.MissingPermissions): await interaction.response.send_message(content=loadlang("leave")['lackperm'], ephemeral=True)
    else: await interaction.response.send_message(embed = None, view = None, content=loadlang("leave")['err'], ephemeral=True)

# Member Leave Event Listener
@bot.event
async def on_member_remove(member):
    # 資料修復
    try:
        guildadder(member.guild)
        wt1 = loadset(member.guild.id)
        with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
        wt1 = autofix2(member.guild.id, wt1)
    except: pass

    # 成員離開訊息寄送
    try:
        wt1 = loadset(member.guild.id)
        
        if wt1['leave']['toggle'] == True and wt1['leave']['msg'] != '' and wt1['leave']['channel'] != None:
            msg = wt1['leave']['msg'].replace('>gname<', member.guild.name).replace('>mname<', member.name)
            channel = bot.get_channel(wt1['leave']['channel'])
            await channel.send(msg)
    except Exception as e: print(f"LEFMSG ERR > GUILD({member.guild.id});MEMBER({member.id}) > {str(e)}")

###############################
##                           ##
##  Function:Reaction Roles  ##
##                           ##
###############################

# /rrnew
@tree.command(name = "rrnew", description=loadlang("rr")['rrnew']['des'])
@app_commands.describe(msg = loadlang("rr")['rrnew']['msgvar'], emoji = loadlang("rr")['rrnew']['emojivar'], role = loadlang("rr")['rrnew']['rolevar'])
@app_commands.checks.has_permissions(administrator = True)
async def rrnew(interaction: discord.Interaction, msg:str, emoji:str, role:discord.Role):
    msgid = int(msg)
    # 資料準備 & 修復
    lang = loadlang("rr")
    guildadder(interaction.guild)
    wt1 = loadset(interaction.guild_id)
    with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)

    # 主要程序
    message = await interaction.channel.fetch_message(msgid)
    await message.add_reaction(emoji)

    # 資料填入
    tdict = globaldata['format']['rr']
    tdict['msgid'] = int(message.id)
    tdict['role'] = int(role.id)
    tdict['emoji'] = str(emoji)
    tdict['ch'] = int(interaction.channel_id)

    # 資料寫入
    wt1 = loadset(interaction.guild_id)
    wt1['rr'].append(tdict)
    writeset(interaction.guild_id, wt1)

    embed = discord.Embed(title = lang['rrnew']['done'], color = color)
    embed.add_field(name = lang['rrnew']['mid'], value=str(msgid))
    embed.add_field(name = lang['rrnew']['memo'], value=str(emoji))
    embed.add_field(name = lang['rrnew']['mrole'], value=role.mention)
    await interaction.response.send_message(embed = embed)
@rrnew.error
async def rrnew_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.errors.MissingPermissions): await interaction.response.send_message(content=loadlang("rr")['lackperm'], ephemeral=True)
    else: await interaction.response.send_message(embed = None, view = None, content=loadlang("rr")['err'], ephemeral=True)

# /rrdel
@tree.command(name = "rrdel", description=loadlang("rr")['rrdel']['des'])
@app_commands.checks.has_permissions(administrator = True)
@app_commands.describe(msg = loadlang("rr")['rrdel']['msgvar'], emoji = loadlang("rr")['rrdel']['emovar'])
async def rrdel(interaction: discord.Interaction, msg:str, emoji:str):
    msgid = int(msg)
    # 資料準備 & 修復
    lang = loadlang("rr")
    guildadder(interaction.guild)
    with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)

    # 主要程序
    wt1 = loadset(interaction.guild_id)
    rr2 = []
    tf = False
    for r in wt1['rr']:
        if r['msgid'] == msgid:
            if r['emoji'] == str(emoji):
                tf = True
                continue
        rr2.append(r)
    if tf == False:
        embed=discord.Embed(color=color)
        embed.add_field(name=lang['rrdel']['err'], value=lang['rrdel']['nbs'], inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        wt1['rr'] = rr2
        writeset(interaction.guild_id, wt1)
        embed=discord.Embed(color=color)
        embed.add_field(name=lang['rrdel']['done'], value=f"{lang['rrdel']['mid']}{str(msgid)}\n{lang['rrdel']['memo']}{str(emoji)}", inline=True)
        await interaction.response.send_message(embed=embed)
@rrdel.error
async def rrdel_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.errors.MissingPermissions): await interaction.response.send_message(content=loadlang("rr")['lackperm'], ephemeral=True)
    else: await interaction.response.send_message(embed = None, view = None, content=loadlang("rr")['err'], ephemeral=True)

# /rrlist
@tree.command(name = "rrlist", description=loadlang("rr")['rrlist']['des'])
@app_commands.checks.has_permissions(administrator = True)
async def rrlist(interaction: discord.Interaction):
    # 資料準備 & 修復
    lang = loadlang("rr")
    guildadder(interaction.guild)
    wt1 = loadset(interaction.guild_id)
    with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
    
    # 主程序
    msg = ''
    for r in wt1['rr']:
        role = lang['rrlist']['naccess']
        try: role = (interaction.guild.get_role(r['role'])).mention
        except: pass

        msg += f"{lang['rrlist']['mid']}{r['msgid']}{lang['line']}{lang['rrlist']['memo']}{r['emoji']}{lang['line']}{lang['rrlist']['mrole']}{role}\n"
    
    if msg == "": msg = lang['rrlist']['norr']
    embed = discord.Embed(title = lang['rrlist']['listitle'], description=msg, color = color)
    await interaction.response.send_message(embed = embed, ephemeral=True)
@rrlist.error
async def rrlist_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.errors.MissingPermissions): await interaction.response.send_message(content=loadlang("rr")['lackperm'], ephemeral=True)
    else: await interaction.response.send_message(embed = None, view = None, content=loadlang("rr")['err'], ephemeral=True)

# /rrbladduser
@tree.command(name = "rrbladduser", description=loadlang("rr")['rrbladduser']['des'])
@app_commands.describe(msg = loadlang("rr")['rrbladduser']['msgvar'], emoji = loadlang("rr")['rrbladduser']['emovar'], user = loadlang("rr")['rrbladduser']['uservar'])
@app_commands.checks.has_permissions(administrator = True)
async def rrbladduser(interaction: discord.Interaction, msg: str, emoji: str, user: discord.User):
    msgid = int(msg)
    userid = user.id
    # 資料準備 & 修復
    lang = loadlang("rr")
    guildadder(interaction.guild)
    wt1 = loadset(interaction.guild_id)
    with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
    
    # 主程序
    tf22 = False
    for r in wt1['rr']:
        if str(r['msgid']) == str(msgid) and str(r['emoji']) == str(emoji):
            tf22 = True
            break
    if tf22 == False:
        embed=discord.Embed(color=color)
        embed.add_field(name=lang['rrbladduser']['err'], value=lang['rrbladduser']['nbs'], inline=True)
        await interaction.response.send_message(ephemeral=True, embed=embed)
    else:
        wt1['rrbl'].append({'msgid':msgid, 'emoji':str(emoji), 'userid':userid})
        writeset(interaction.guild_id, wt1)

        embed = discord.Embed(title = lang['rrbladduser']['mtitle'], description=lang['rrbladduser']['mtype'], color = color)
        embed.add_field(name = lang['rrbladduser']['mid'], value=str(msgid))
        embed.add_field(name = lang['rrbladduser']['memo'], value=str(emoji))
        embed.add_field(name = lang['rrbladduser']['muser'], value = user.mention, inline = False)
        await interaction.response.send_message(embed=embed)
@rrbladduser.error
async def rrbladduser_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.errors.MissingPermissions): await interaction.response.send_message(content=loadlang("rr")['lackperm'], ephemeral=True)
    else: await interaction.response.send_message(embed = None, view = None, content=loadlang("rr")['err'], ephemeral=True)

# /rrbladdrole
@tree.command(name = "rrbladdrole", description=loadlang("rr")['rrbladdrole']['des'])
@app_commands.describe(msg = loadlang("rr")['rrbladdrole']['msgvar'], emoji = loadlang("rr")['rrbladdrole']['emovar'], role = loadlang("rr")['rrbladdrole']['rolevar'])
@app_commands.checks.has_permissions(administrator = True)
async def rrbladdrole(interaction: discord.Interaction, msg:str, emoji:str, role: discord.Role):
    msgid = int(msg)
    userid = role.id
    # 資料準備 & 修復
    lang = loadlang("rr")
    guildadder(interaction.guild)
    wt1 = loadset(interaction.guild_id)
    with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
    
    # 主程序
    tf22 = False
    for r in wt1['rr']:
        if str(r['msgid']) == str(msgid) and str(r['emoji']) == str(emoji):
            tf22 = True
            break
    if tf22 == False:
        embed=discord.Embed(color=color)
        embed.add_field(name=lang['rrbladdrole']['err'], value=lang['rrbladdrole']['nbs'], inline=True)
        await interaction.response.send_message(ephemeral=True, embed=embed)
    else:
        wt1['rolerrbl'].append({'msgid':msgid, 'emoji':str(emoji), 'roleid':userid})
        writeset(interaction.guild_id, wt1)

        embed = discord.Embed(title = lang['rrbladdrole']['mtitle'], description=lang['rrbladdrole']['mtype'], color = color)
        embed.add_field(name = lang['rrbladdrole']['mid'], value=str(msgid))
        embed.add_field(name = lang['rrbladdrole']['memo'], value=str(emoji))
        embed.add_field(name = lang['rrbladdrole']['muser'], value = role.mention, inline = False)
        await interaction.response.send_message(embed=embed)
@rrbladdrole.error
async def rrbladdrole_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.errors.MissingPermissions): await interaction.response.send_message(content=loadlang("rr")['lackperm'], ephemeral=True)
    else: await interaction.response.send_message(embed = None, view = None, content=loadlang("rr")['err'], ephemeral=True)

# /rrbldelrole
@tree.command(name = "rrbldelrole", description=loadlang("rr")['rrbldelrole']['des'])
@app_commands.describe(msg = loadlang("rr")['rrbldelrole']['msgvar'], emoji = loadlang("rr")['rrbldelrole']['emovar'], role = loadlang("rr")['rrbldelrole']['rolevar'])
@app_commands.checks.has_permissions(administrator = True)
async def rrbldelrole(interaction: discord.Interaction, msg:str, emoji:str, role: discord.Role):
    msgid = int(msg)
    userid = role.id
    # 資料準備 & 修復
    lang = loadlang("rr")
    guildadder(interaction.guild)
    wt1 = loadset(interaction.guild_id)
    with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
    
    # 主程序
    tf22 = False
    rr2 = []
    for r in wt1['rolerrbl']:
        if str(r['msgid']) == str(msgid) and str(r['emoji']) == str(emoji) and str(userid) == str(r['roleid']):
            tf22 = True
            continue
        rr2.append(r)
    if tf22 == False:
        embed=discord.Embed(color=color)
        embed.add_field(name=lang['rrbldelrole']['err'], value=lang['rrbldelrole']['nbs'], inline=True)
        await interaction.response.send_message(ephemeral=True, embed=embed)
    else:
        wt1['rolerrbl'] = rr2
        writeset(interaction.guild_id, wt1)

        embed = discord.Embed(title = lang['rrbldelrole']['mtitle'], description=lang['rrbldelrole']['mtype'], color = color)
        embed.add_field(name = lang['rrbldelrole']['mid'], value=str(msgid))
        embed.add_field(name = lang['rrbldelrole']['memo'], value=str(emoji))
        embed.add_field(name = lang['rrbldelrole']['muser'], value = role.mention, inline = False)
        await interaction.response.send_message(embed=embed)
@rrbldelrole.error
async def rrbldelrole_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.errors.MissingPermissions): await interaction.response.send_message(content=loadlang("rr")['lackperm'], ephemeral=True)
    else: await interaction.response.send_message(embed = None, view = None, content=loadlang("rr")['err'], ephemeral=True)

# /rrbldeluser
@tree.command(name = "rrbldeluser", description=loadlang("rr")['rrbldeluser']['des'])
@app_commands.describe(msg = loadlang("rr")['rrbldeluser']['msgvar'], emoji = loadlang("rr")['rrbldeluser']['emovar'], user = loadlang("rr")['rrbldeluser']['uservar'])
@app_commands.checks.has_permissions(administrator = True)
async def rrbldeluser(interaction: discord.Interaction, msg:str, emoji:str, user:discord.User):
    msgid = int(msg)
    userid = user.id
    # 資料準備 & 修復
    lang = loadlang("rr")
    guildadder(interaction.guild)
    wt1 = loadset(interaction.guild_id)
    with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
    
    # 主程序
    tf22 = False
    rr2 = []
    for r in wt1['rrbl']:
        if str(r['msgid']) == str(msgid) and str(r['emoji']) == str(emoji) and str(userid) == str(r['userid']):
            tf22 = True
            continue
        rr2.append(r)
    if tf22 == False:
        embed=discord.Embed(color=color)
        embed.add_field(name=lang['rrbldeluser']['err'], value=lang['rrbldeluser']['nbs'], inline=True)
        await interaction.response.send_message(ephemeral=True, embed=embed)
    else:
        wt1['rrbl'] = rr2
        writeset(interaction.guild_id, wt1)

        embed = discord.Embed(title = lang['rrbldeluser']['mtitle'], description=lang['rrbldeluser']['mtype'], color = color)
        embed.add_field(name = lang['rrbldeluser']['mid'], value=str(msgid))
        embed.add_field(name = lang['rrbldeluser']['memo'], value=str(emoji))
        embed.add_field(name = lang['rrbldeluser']['muser'], value = user.mention, inline = False)
        await interaction.response.send_message(embed=embed)
@rrbldeluser.error
async def rrbldeluser_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.errors.MissingPermissions): await interaction.response.send_message(content=loadlang("rr")['lackperm'], ephemeral=True)
    else: await interaction.response.send_message(embed = None, view = None, content=loadlang("rr")['err'], ephemeral=True)

# /rrblist
@tree.command(name = "rrblist", description=loadlang("rr")['rrblist']['des'])
@app_commands.checks.has_permissions(administrator = True)
async def rrblist(interaction: discord.Interaction):
    # 資料準備 & 修復
    lang = loadlang("rr")
    guildadder(interaction.guild)
    wt1 = loadset(interaction.guild_id)
    with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
    
    # 主程序
    embed = discord.Embed(color = color, title = lang['rrblist']['mtitle'])
    msg = ""
    for bl in wt1['rrbl']: 
        user = lang['rrblist']['mna']
        try: user = (bot.get_user(bl["userid"])).mention
        except: pass
        msg += f"{lang['rrblist']['mid']}{bl['msgid']}{lang['line']}{lang['rrblist']['memoji']}{bl['emoji']}{lang['rrblist']['mtypeu']}{user}{lang['rrblist']['minit']}\n"
    if msg == "": msg = lang['rrblist']['mnr']
    embed.add_field(name = lang['rrblist']['mut'], value = msg, inline = False)

    msg = ""
    for bl in wt1['rolerrbl']:
        role = lang['rrblist']['mna']
        try: role = (interaction.guild.get_role(bl["roleid"])).mention
        except: pass
        msg += f"{lang['rrblist']['mid']}{bl['msgid']}{lang['line']}{lang['rrblist']['memoji']}{bl['emoji']}{lang['rrblist']['mtyper']}{role}{lang['rrblist']['minit']}\n"
    if msg == "": msg = lang['rrblist']['mnr']
    embed.add_field(name = lang['rrblist']['mrt'], value = msg, inline = False)

    await interaction.response.send_message(embed = embed, ephemeral=True)
@rrblist.error
async def rrblist_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.errors.MissingPermissions): await interaction.response.send_message(content=loadlang("rr")['lackperm'], ephemeral=True)
    else: await interaction.response.send_message(embed = None, content=loadlang("rr")['err'], ephemeral=True)

# Reaction Roles Event Listeners
@bot.event
async def on_raw_reaction_add(payload):
    try:guildadder(bot.get_guild(payload.guild_id))
    except:pass
    try:
        wt1 = loadset(int(payload.guild_id))
        tr = None
        for r in wt1['rr']:
            if str(r['msgid']) == str(payload.message_id) and str(r['emoji']) == str(payload.emoji.name):
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
    except Exception as e: print(f"RROLEADD ERR > GUILD({str(payload.guild_id)});MSGID({payload.message_id}) > {str(e)}")
@bot.event
async def on_raw_reaction_remove(payload):
    try:guildadder(bot.get_guild(payload.guild_id))
    except:pass
    try:
        wt1 = loadset(int(payload.guild_id))
        tr = None
        for r in wt1['rr']:
            if str(r['msgid']) == str(payload.message_id) and str(r['emoji']) == str(payload.emoji.name):
                tr = r
                break
        if tr != None:
            guild = bot.get_guild(int(payload.guild_id))
            members = guild.members
            member = None
            for m in members:
                if int(m.id) == int(payload.user_id):
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
    except Exception as e: print(f"RROLEDEL ERR > GUILD({str(payload.guild_id)});MSGID({payload.message_id}) > {str(e)}")

#############################
##                         ##
##  Function:Button Roles  ##
##                         ##
#############################

@tree.command(name = "br", description=loadlang("br")['des'])
@app_commands.describe(msg = loadlang("br")['msgvar'], role = loadlang("br")['rolevar'])
@app_commands.checks.has_permissions(administrator = True)
async def br(interaction: discord.Interaction, msg:str, role: discord.Role):
    # 資料準備 & 修復
    try:guildadder(interaction.guild)
    except: pass

    # 主程序
    view = View(timeout = None)

    # 執行領取身分組的程序
    async def interaction_callback(interaction: discord.Role):
        try:guildadder(interaction.guild)
        except: pass
        try:
            member = interaction.guild.get_member(interaction.user.id)
            roles = member.roles
            rem = False
            for a in roles:
                if a.id == role.id:
                    rem = True
                    break
            if rem == False:
                await member.add_roles(role, atomic = True)

                embed=discord.Embed(color=color)
                embed.add_field(name=loadlang("br")['mtitle'], value=loadlang("br")['mget'].replace("%ROLE%", role.mention), inline=True)
                await interaction.response.send_message(embed = embed, ephemeral=True)
            else:
                await member.remove_roles(role, atomic = True)

                embed=discord.Embed(color=color)
                embed.add_field(name=loadlang("br")['mtitle'], value=loadlang("br")['mdel'].replace("%ROLE%", role.mention), inline=True)
                await interaction.response.send_message(embed = embed, ephemeral=True)
        except:
            embed=discord.Embed(color=color)
            embed.add_field(name=loadlang("br")['mtitle'], value=loadlang("br")['merr'], inline=True)
            await interaction.response.send_message(embed = embed, ephemeral=True)

    # 訊息生成程序
    button = Button(label = loadlang("br")['butget']+role.name, style = discord.ButtonStyle.green)
    button.callback = interaction_callback
    view.add_item(button)

    await interaction.channel.send(msg, view = view)
    await interaction.response.send_message(content=loadlang("br")['done'], ephemeral=True)
@br.error
async def br_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.errors.MissingPermissions): await interaction.response.send_message(content=loadlang("br")['lackperm'], ephemeral=True)
    else: await interaction.response.send_message(embed = None, view = None, content=loadlang("br")['err'], ephemeral=True)

########################
##                    ##
##  Function:YouTube  ##
##                    ##
########################

# /ytchadd
@tree.command(name = "ytchadd", description=loadlang("yt")['ytchadd']['des'])
@app_commands.describe(vid = loadlang("yt")['ytchadd']['vidvar'])
@app_commands.checks.has_permissions(administrator = True)
async def ytchadd(interaction: discord.Interaction, vid:str):
    # 資料準備 & 修復
    lang = loadlang("yt")
    guildadder(interaction.guild)
    with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
    api = globaldata['YTAPI']

    # 主程序
    r3 = requests.get('https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={}&key={}'.format(vid, api))
    d3 = r3.json()

    wt41 = loadset(interaction.guild_id)

    chid = d3['items'][0]['snippet']['channelId']

    r1 = requests.get('https://www.googleapis.com/youtube/v3/channels?part=snippet&id={}&key={}'.format(chid, api))
    data3 = r1.json()
    chname = data3["items"][0]["snippet"]["title"]

    wt41['ytchannelid'].append(chid)
    writeset(interaction.guild_id, wt41)

    embed=discord.Embed(color=color)
    embed.add_field(name=lang['ytchadd']['done'], value=f"{lang['ytchadd']['mname']}``{chname}``\n{lang['ytchadd']['mid']}``{chid}``", inline=False)

    await interaction.response.send_message(embed=embed)
@ytchadd.error
async def ytchadd_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.errors.MissingPermissions): await interaction.response.send_message(content=loadlang("yt")['lackperm'], ephemeral=True)
    else: await interaction.response.send_message(embed = None, content=loadlang("yt")['err'], ephemeral=True)

# /ytchdel
@tree.command(name = "ytchdel", description=loadlang("yt")['ytchdel']['des'])
@app_commands.describe(chid = loadlang("yt")['ytchdel']['chidvar'])
@app_commands.checks.has_permissions(administrator = True)
async def ytchdel(interaction: discord.Interaction, chid:str):
    # 資料準備 & 修復
    lang = loadlang("yt")
    guildadder(interaction.guild)
    with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
    api = globaldata['YTAPI']

    # 主程序
    gid = interaction.guild_id
    wt41 = loadset(gid)
    if wt41['ytchannelid'] != []:
        tlist = []
        for wttt in wt41['ytchannelid']:
            if wttt != chid: tlist.append(wttt)
        if len(wt41['ytchannelid']) > len(tlist):
            wt41['ytchannelid'] = tlist
            writeset(interaction.guild_id, wt41)

            embed=discord.Embed(color=color)
            try:
                result3 = requests.get('https://www.googleapis.com/youtube/v3/channels?part=snippet&id={}&key={}'.format(chid, api))
                data3 = result3.json()
                embed.add_field(name=lang['ytchdel']['done'], value=f'{lang["ytchdel"]["mdes"]} ``{data3["items"][0]["snippet"]["title"]}``\n{lang["ytchdel"]["mdes-2"]}``{chid}``', inline=False)
            except: embed.add_field(name=lang["ytchdel"]["done"], value=f'{lang["ytchdel"]["mdes"]} ``{lang["ytchdel"]["mnoaccess"]}``\n{lang["ytchdel"]["mdes-2"]}``{chid}``', inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            embed=discord.Embed(color=color)
            embed.add_field(name=lang["errsimple"], value=lang["ytchdel"]["nexist"].replace("%CHID%", chid), inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)
    else: await interaction.response.send_message(content = lang["noch"], ephemeral=True)
@ytchdel.error
async def ytchdel_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.errors.MissingPermissions): await interaction.response.send_message(content=loadlang("yt")['lackperm'], ephemeral=True)
    else: await interaction.response.send_message(embed = None, content=loadlang("yt")['err'], ephemeral=True)

# /ytchlist
@tree.command(name = "ytchlist", description=loadlang("yt")['ytchlist']['des'])
async def ytchlist(interaction: discord.Interaction):
    try:
        # 資料準備 & 修復
        lang = loadlang("yt")
        guildadder(interaction.guild)
        with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
        api = globaldata['YTAPI']

        # 主程序
        gid = interaction.guild_id
        wt41 = loadset(gid)
        msg = ""
        for wttt in wt41['ytchannelid']:
            try:
                result3 = requests.get('https://www.googleapis.com/youtube/v3/channels?part=snippet&id={}&key={}'.format(wttt, api))
                data3 = result3.json()
                msg += f'{lang["ytchlist"]["mname"]}{data3["items"][0]["snippet"]["title"]}{lang["line"]}{lang["ytchlist"]["mid"]}{wttt}\n{lang["ytchlist"]["murl"]}' + wttt + '\n\n' 
            except: msg += f"{lang['ytchlist']['mnoaccess']}\n"
        if msg == "": msg = lang["noch"]

        embed=discord.Embed(color=color)
        embed.add_field(name=lang["ytchlist"]["mtitle"], value=f"{msg}", inline=False)
        await interaction.response.send_message(embed=embed)
    except: await interaction.response.send_message(content = loadlang("yt")['ytchlist']['err'], ephemeral=True)

# /chinfo
@tree.command(name = "chinfo", description=loadlang("yt")['chinfo']['des'])
async def chinfo(interaction: discord.Interaction):
    try:
        # 資料準備 & 修復
        lang = loadlang("yt")
        guildadder(interaction.guild)
        with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
        api = globaldata['YTAPI']

        # 主程序
        gid = interaction.guild_id
        wt41 = loadset(gid)

        msg = ""
        for wttt in wt41['ytchannelid']:
            try:
                result3 = requests.get('https://www.googleapis.com/youtube/v3/channels?part=snippet&id={}&key={}'.format(wttt, api))
                data3 = result3.json()
                msg += f'- {data3["items"][0]["snippet"]["title"]} \n{loadlang("yt")["chinfo"]["murl"]}' + wttt + '\n\n' 
            except: msg += f'{loadlang("yt")["chinfo"]["mnoaccess"]}\n'
        embed=discord.Embed(color=color)
        if msg == "": msg = loadlang("yt")["noch"]
        embed.add_field(name=loadlang("yt")["chinfo"]["mtitle"], value=f"{msg}", inline=False)
        await interaction.response.send_message(embed=embed)
    except: await interaction.response.send_message(content = loadlang("yt")['err'], ephemeral=True)

# /newvideo
@tree.command(name = "newvideo", description=loadlang("yt")["newvideo"]["des"])
async def newvideo(interaction: discord.Interaction):
    try:
        # 資料準備 & 修復
        lang = loadlang("yt")
        guildadder(interaction.guild)
        with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
        api = globaldata['YTAPI']
    
        # 主程序
        wt2 = loadset(interaction.guild_id)
        if wt2['ytchannelid'] != []:
            msg = ""
            for chid in wt2['ytchannelid']:
                try:
                    # 獲取頻道
                    result1 = requests.get('https://www.googleapis.com/youtube/v3/channels?part=snippet,contentDetails&id={}&key={}'.format(chid, api))
                    data1 = result1.json()
                    # 獲取影片表
                    result2 = requests.get('https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId={}&key={}'.format(data1['items'][0]['contentDetails']['relatedPlaylists']['uploads'], api))
                    data2 = result2.json()
                    # 獲取最新的影片
                    result3 = requests.get('https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={}&key={}'.format(data2['items'][0]['contentDetails']['videoId'], api))
                    data3 = result3.json()
                    msg += f'{loadlang("yt")["newvideo"]["mname"]}``{data1["items"][0]["snippet"]["title"]}``{loadlang("yt")["newvideo"]["marrow"]}``{data3["items"][0]["snippet"]["title"]}``\n{loadlang("yt")["newvideo"]["murl"]}{data3["items"][0]["id"]}\n\n'
                except: msg += f'{loadlang("yt")["newvideo"]["mchid"]}``{chid}``{loadlang("yt")["newvideo"]["mnaccess"]}\n'
            embed=discord.Embed(color=color)
            embed.add_field(name=loadlang("yt")["newvideo"]["mtitle"], value=msg, inline=True)
            await interaction.response.send_message(embed=embed)
        else: await interaction.response.send_message(content = loadlang("yt")["noch"])
    except: await interaction.response.send_message(content = loadlang("yt")["err"], ephemeral=True)

# /subs
@tree.command(name = "subs", description=loadlang("yt")["subs"]["des"])
async def subs(interaction: discord.Interaction):
    try:
        # 資料準備 & 修復
        lang = loadlang("yt")
        guildadder(interaction.guild)
        with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
        api = globaldata['YTAPI']

        # 主程序
        gid = interaction.guild_id
        wt3 = loadset(gid)
        if wt3['ytchannelid'] != []: 
            msg = ""
            for chid in wt3['ytchannelid']:
                try:
                    result1 = requests.get('https://www.googleapis.com/youtube/v3/channels?part=statistics, snippet&id={}&key={}'.format(str(chid), api))
                    wt4 = result1.json()
                    subs = wt4['items'][0]['statistics']['subscriberCount']
                    msg += f'{loadlang("yt")["subs"]["chname"]}``{wt4["items"][0]["snippet"]["title"]}``{loadlang("yt")["subs"]["chsub"]}{str(subs)}\n'
                except: msg += f'{loadlang("yt")["subs"]["chid"]}``{chid}``{loadlang("yt")["subs"]["chnaccess"]}\n'
            embed=discord.Embed(color=color)
            embed.add_field(name=loadlang("yt")["subs"]["mtitle"], value=msg, inline=True)
            embed.set_footer(text = loadlang("yt")["subs"]["footer"])
            await interaction.response.send_message(embed=embed)
        else: await interaction.response.send_message(content = loadlang("yt")["noch"], ephemeral=True)
    except: await interaction.response.send_message(content = loadlang("yt")["err"], ephemeral=True)

# /subsearch
@tree.command(name = 'subsearch', description=loadlang("yt")["subsearch"]["des"])
@app_commands.describe(vid = loadlang("yt")["subsearch"]["vidvar"])
async def other(interaction: discord.Interaction, vid: str):
    # 資料準備 & 修復
    lang = loadlang("yt")
    guildadder(interaction.guild)
    with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
    api = globaldata['YTAPI']
    
    # 主程序
    gid = interaction.guild_id
    try:
        r3 = requests.get('https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={}&key={}'.format(vid, api))
        d3 = r3.json()

        chid = d3['items'][0]['snippet']['channelId']

        result1 = requests.get('https://www.googleapis.com/youtube/v3/channels?part=statistics, snippet&id={}&key={}'.format(str(chid), api))
        wt4 = result1.json()
        subs = wt4['items'][0]['statistics']['subscriberCount']

        embed=discord.Embed(color=color)
        embed.add_field(name= f'{loadlang("yt")["subsearch"]["chname"]}``{wt4["items"][0]["snippet"]["title"]}``{loadlang("yt")["subsearch"]["chsub"]}', value=f"{str(subs)}", inline=True)
        embed.set_footer(text = loadlang("yt")["subsearch"]["footer"])
        await interaction.response.send_message(embed = embed)
    except: await interaction.response.send_message(content = loadlang("yt")["err"], ephemeral=True)

#####################
##                 ##
##  Function:Help  ##
##                 ##
#####################

# /help
@tree.command(name = "help", description=loadlang("help")['des'])
async def help(interaction: discord.Interaction):
    # 資料修復 & 準備
    guildadder(interaction.guild)
    with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)

    # 主程序
    async def pagecb(interaction: discord.Interaction): 
        # 資料修復 & 準備
        guildadder(interaction.guild)
        with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)

        # 主程序
        with open(f"help/{str(select.values[0])}.yaml", "r", encoding="utf8") as f: data = yaml.load(f, Loader=Loader)
        embed = discord.Embed(color = color, title = data['emoji']+"| "+data['name'], description=data['des'])
        for c in data['cmds']:
            embed.add_field(name = data['cmds'][c]['name'], value=data['cmds'][c]['des'], inline = False)
        embed.set_footer(text = loadlang("help")['var'])

        await interaction.response.send_message(embed = embed, ephemeral=True)

    guildadder(interaction.guild)
    with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)

    embed = discord.Embed(title = loadlang("help")['title'], description=loadlang("help")['titledes'], color = color)
    embed.add_field(name = loadlang("help")['brtitle'], value = loadlang("help")['brdes'], inline = False)
    embed.add_field(name = loadlang("help")['stoptitle'], value = loadlang("help")['stopdes'], inline = False)
    embed.set_footer(text = f"{loadlang('help')['footer']}{globaldata['VERSION']}")

    view = View(timeout = None)
    options = []
    files = glob.glob("help/*.yaml")
    for hf in files:
        with open(hf, "r", encoding="utf8") as f: data = yaml.load(f, Loader=Loader)
        options.append(discord.SelectOption(label = data['name'], description=data['des'], emoji = data['emoji'], value = data['value']))
    select = Select(options = options, placeholder=loadlang("help")['cap'])
    select.callback = pagecb
    view.add_item(select)

    view.add_item(Button(label = loadlang("help")['bt1'], emoji = loadlang("help")['bt1e'], url = globaldata['help']['invite'], row = 1))
    view.add_item(Button(label = loadlang("help")['bt2'], emoji = loadlang("help")['bt2e'], url = globaldata['help']['dc'], row = 1))
    view.add_item(Button(label = loadlang("help")['bt3'], url = globaldata['help']['github'], row = 1))
    view.add_item(Button(label = loadlang("help")['bt4'], style = discord.ButtonStyle.gray, disabled=True, row = 2))
    view.add_item(Button(label = loadlang("help")['bt5'], url = globaldata['help']['dctw'], row = 2))
    
    await interaction.response.send_message(embed = embed, view = view)

###########################
##                       ##
##  Old Commands Notify  ##
##                       ##
###########################

@bot.command(name = "fbk")
async def old_fbk(ctx): await ctx.send("https://tenor.com/view/fox-girl-shirakami-fubuki-fubukishirakami-gif-19974362")

@bot.command(name = "resetup")
async def old_resetup(ctx): await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))

@bot.command(name = "addytchannel")
async def old_addytchannel(ctx): await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))

@bot.group(name = "guildinfo")
async def old_guildinfo(ctx): await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))
@bot.command(name = "userinfo")
async def old_userinfo(ctx): await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))

@bot.command(name = "removeytchannel")
async def old_removeytchannel(ctx): await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))
@bot.command(name = "ytchannellist")
async def old_ytchannellist(ctx): await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))

@bot.command(name = "ping")
async def old_ping(ctx): await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))

@bot.command(name = "help")
async def old_help(ctx): await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))

@bot.command(name = "time")
async def old_time(ctx): await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))
@bot.command(name = "time_other")
async def old_time_other(ctx): await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))

@bot.command(name = "channelinfo")
async def old_channelinfo(ctx): await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))
@bot.command(name = "newvideo")
async def old_newvideo(ctx): await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))

@bot.command(name = "funstick")
async def old_funstick(ctx): await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))
@bot.command(name = "hi")
async def old_hi(ctx): await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))
@bot.command(name = "hug")
async def old_hug(ctx): await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))

@bot.command(name = "picgoogle")
async def old_picgoogle(ctx): await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))

@bot.command(name = "purge")
async def old_purge(ctx): await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))

@bot.command(name = "subs")
async def old_subs(ctx): await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))

@bot.command(name = "tvc")
async def old_tvc(ctx): await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))

@bot.command(name = "rr")
async def old_rr(ctx): await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))

@bot.command(name = "br")
async def old_br(ctx): await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))

@bot.command(name = "welcome")
async def old_welcome(ctx): await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))

@bot.command(name = "leave")
async def old_leave(ctx):await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))

@bot.command(name = "ox")
async def old_ox(ctx): await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))

@bot.command(name = "info")
async def old_info(ctx): await ctx.send(embed = discord.Embed(title = "機器人指令已轉移為斜線指令", description="請使用``/help``查看新版指令查詢介面\n\n這項功能是1.7版本的更新內容", color = color))

# Bot上線
bot.run(globaldata["TOKEN"])