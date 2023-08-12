def ai(wt1):
    import random

    a = random.randint(1, 10)
    if a <= 7:
        if wt1[0] == 'O' and wt1[1] == 'O' and wt1[2] != 'X' and wt1[2] != 'O':
            wt1[2] = 'X'
        elif wt1[0] == 'O' and wt1[2] == 'O' and wt1[1] != 'X' and wt1[1] != 'O':
            wt1[1] = 'X'
        elif wt1[1] == 'O' and wt1[2] == 'O' and wt1[0] != 'X' and wt1[0] != 'O':
            wt1[0] = 'X'
        elif wt1[3] == 'O' and wt1[4] == 'O' and wt1[5] != 'X' and wt1[5] != 'O':
            wt1[5] = 'X'
        elif wt1[3] == 'O' and wt1[5] == 'O' and wt1[4] != 'X' and wt1[4] != 'O':
            wt1[4] = 'X'
        elif wt1[4] == 'O' and wt1[5] == 'O' and wt1[3] != 'X' and wt1[3] != 'O':
            wt1[3] = 'X'
        elif wt1[6] == 'O' and wt1[7] == 'O' and wt1[8] != 'X' and wt1[8] != 'O':
            wt1[8] = 'X'
        elif wt1[6] == 'O' and wt1[8] == 'O' and wt1[7] != 'X' and wt1[7] != 'O':
            wt1[7] = 'X'
        elif wt1[7] == 'O' and wt1[8] == 'O' and wt1[6] != 'X' and wt1[6] != 'O':
            wt1[6] = 'X'
        elif wt1[0] == 'O' and wt1[3] == 'O' and wt1[6] != 'X' and wt1[6] != 'O':
            wt1[6] = 'X'
        elif wt1[0] == 'O' and wt1[6] == 'O' and wt1[3] != 'X' and wt1[3] != 'O':
            wt1[3] = 'X'
        elif wt1[6] == 'O' and wt1[3] == 'O' and wt1[0] != 'X' and wt1[0] != 'O':
            wt1[0] = 'X'
        elif wt1[1] == 'O' and wt1[4] == 'O' and wt1[7] != 'X' and wt1[7] != 'O':
            wt1[7] = 'X'
        elif wt1[1] == 'O' and wt1[7] == 'O' and wt1[4] != 'X' and wt1[4] != 'O':
            wt1[4] = 'X'
        elif wt1[4] == 'O' and wt1[7] == 'O' and wt1[1] != 'X' and wt1[1] != 'O':
            wt1[1] = 'X'
        elif wt1[2] == 'O' and wt1[5] == 'O' and wt1[8] != 'X' and wt1[8] != 'O':
            wt1[8] = 'X'
        elif wt1[2] == 'O' and wt1[8] == 'O' and wt1[5] != 'X' and wt1[5] != 'O':
            wt1[5] = 'X'
        elif wt1[5] == 'O' and wt1[8] == 'O' and wt1[2] != 'X' and wt1[2] != 'O':
            wt1[2] = 'X'
        elif wt1[0] == 'O' and wt1[4] == 'O' and wt1[8] != 'X' and wt1[8] != 'O':
            wt1[8] = 'X'
        elif wt1[0] == 'O' and wt1[8] == 'O' and wt1[4] != 'X' and wt1[4] != 'O':
            wt1[4] = 'X'
        elif wt1[4] == 'O' and wt1[8] == 'O' and wt1[0] != 'X' and wt1[0] != 'O':
            wt1[0] = 'X'
        elif wt1[2] == 'O' and wt1[4] == 'O' and wt1[6] != 'X' and wt1[6] != 'O':
            wt1[6] = 'X'
        elif wt1[2] == 'O' and wt1[6] == 'O' and wt1[4] != 'X' and wt1[4] != 'O':
            wt1[4] = 'X'
        elif wt1[4] == 'O' and wt1[6] == 'O' and wt1[2] != 'X' and wt1[2] != 'O':
            wt1[2] = 'X'
        else:
            for i in range(9):
                if wt1[i] == None:
                    wt1[i] = 'X'
                    break
    else:
        for i in range(9):
            if wt1[i] == None:
                wt1[i] = 'X'
                break
    return wt1

def wl(wt1):
    wl = "Tie"
    if wt1[0] == 'O' and wt1[1] == 'O' and wt1[2] == 'O':
        wl = 'Win'
    elif wt1[3] == 'O' and wt1[4] == 'O' and wt1[5] == 'O':
        wl = 'Win'
    elif wt1[6] == 'O' and wt1[7] == 'O' and wt1[8] == 'O':
        wl = 'Win'
    elif wt1[0] == 'O' and wt1[3] == 'O' and wt1[6] == 'O':
        wl = 'Win'
    elif wt1[1] == 'O' and wt1[4] == 'O' and wt1[7] == 'O':
        wl = 'Win'
    elif wt1[2] == 'O' and wt1[5] == 'O' and wt1[8] == 'O':
        wl = 'Win'
    elif wt1[0] == 'O' and wt1[4] == 'O' and wt1[8] == 'O':
        wl = 'Win'
    elif wt1[2] == 'O' and wt1[4] == 'O' and wt1[6] == 'O':
        wl = 'Win'
    elif wt1[0] == 'X' and wt1[1] == 'X' and wt1[2] == 'X':
        wl = 'Lose'
    elif wt1[3] == 'X' and wt1[4] == 'X' and wt1[5] == 'X':
        wl = 'Lose'
    elif wt1[6] == 'X' and wt1[7] == 'X' and wt1[8] == 'X':
        wl = 'Lose'
    elif wt1[0] == 'X' and wt1[3] == 'X' and wt1[6] == 'X':
        wl = 'Lose'
    elif wt1[1] == 'X' and wt1[4] == 'X' and wt1[7] == 'X':
        wl = 'Lose'
    elif wt1[2] == 'X' and wt1[5] == 'X' and wt1[8] == 'X':
        wl = 'Lose'
    elif wt1[0] == 'X' and wt1[4] == 'X' and wt1[8] == 'X':
        wl = 'Lose'
    elif wt1[2] == 'X' and wt1[4] == 'X' and wt1[6] == 'X':
        wl = 'Lose'
    else:
        tf = False
        for i in wt1:
            if i == None:
                wl = 'Not yet'
                tf = True
                break
        if tf == False:
            wl = "Tie"
    return wl
