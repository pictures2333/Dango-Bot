def gettime(zone:int, fmt:str):
    from datetime import datetime, timezone, timedelta
    
    tz = timezone(timedelta(hours=zone))
    
    zoned_time1 = datetime.today().astimezone(tz).strftime(fmt)

    with open('time.txt', 'w', encoding = 'utf8') as f:
        f.write(str(zoned_time1))