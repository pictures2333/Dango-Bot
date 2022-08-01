from time import sleep
import glob, json

while True:
    files = glob.glob('RPG/*.json')
    for f2 in files:
        with open(f2, 'r', encoding = 'utf-8') as f:
            d1 = json.load(f)
        d1['body'] += 1
        if d1['body'] > 20:
            d1['body'] = 20
        dumpdata = json.dumps(d1, ensure_ascii = False)
        with open(f2, 'w', encoding = 'utf-8') as f:
            f.write(dumpdata)
    sleep(30)
