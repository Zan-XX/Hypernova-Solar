import can
import logging
from datetime import *
logging.basicConfig(filename='Hud.log', filemode='a+', format='%(asctime)s - %(message)s', datefmt='%b/%d/%y %H:%M:%S')


def canSend(bus, aId, msg):     #Function to send CAN messages
    msg = can.Message(arbitration_id=aId, data=[msg])
    bus.send(msg)


def canReceive(bus):            #Function to check for new CAN messages
    msg = bus.recv(0.1)         # time for refresh
    log(msg)
    return msg


def log(data):                  #Function to log (data) to file
    logRow = 'TestInt: ' + str(data) + ' '
    logging.error('%s', logRow)


def clearLine():                #Function to clear old log entries
    with open('Hud.Log', 'r') as x:
        data = x.read().splitlines(True)
    with open('Hud.log', 'w') as z:
        z.writelines(data[1:])


def getHudInfo():               #Reads in data from log to display to hud gui
    info = []
    f = open('Hud.log', 'r')
    f1 = f.readlines()
    line = f1[-1].split(' ')
    info.append(line[4])
    for dLine in f1:
        top = dLine.split('-')
        now = datetime.strptime(top[0], '%b/%d/%y %H:%M:%S ')
        if now < datetime.now() - timedelta(hours=1):
            clearLine()
        else:
            break
    return info
