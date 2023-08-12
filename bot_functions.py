def loadlang(filename:str):
    import yaml
    from yaml import CLoader as Loader
    with open(f"languages/{filename}.yaml", "r", encoding="utf8") as f: data = yaml.load(f, Loader=Loader)
    return data

import discord
def guildadder(guild: discord.Guild):
    import os, json
    with open("settings.json", "r", encoding="utf8") as f: globaldata = json.load(f)
    if not os.path.exists(f'settings/{str(guild.id)}.json'):
        wd1 = globaldata['format']['guilds']
        dumpdata3 = json.dumps(wd1)
        with open(f'settings/{str(guild.id)}.json', 'w', encoding = 'utf-8') as f: f.write(dumpdata3)

def loadset(ggid):
    import json
    with open(f'settings/{str(ggid)}.json', 'r', encoding = 'utf-8') as f: d1 = json.load(f)
    return d1
def writeset(ggid, ddd1:dict):
    import json
    dumpdata = json.dumps(ddd1, ensure_ascii = False)
    with open(f'settings/{str(ggid)}.json', 'w', encoding = 'utf-8') as f: f.write(dumpdata)