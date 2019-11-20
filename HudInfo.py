from datetime import *
import Logger


def getHudInfo():
    info = []
    f = open('Hud.log', 'r')
    f1 = f.readlines()
    line = f1[-1].split(' ')
    info.append(line[4] + ' MPH')
    info.append(line[6] + '%')
    info.append(line[8] + u'\u00b0F')
    info.append(line[10] + u'\u00b0F')

    for dLine in f1:
        top = dLine.split('-')
        now = datetime.strptime(top[0], '%b/%d/%y %H:%M:%S ')
        if now < datetime.now() - timedelta(hours=1):
            Logger.clearLine()
        else:
            break
    return info
