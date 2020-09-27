#!/usr/bin/env python3.8

import logging
from datetime import *
logging.basicConfig(filename='Hud.log', filemode='a+', format='%(asctime)s - %(message)s', datefmt='%b/%d/%y %H:%M:%S')


def log(tag, data):
    """Takes a tag and the data to log, prints as 'tag: data'"""
    row = tag+': ' + str(data) + ' '
    logging.info(row)


def clearLine():
    """Clears log entry's that are over an hour old"""
    with open('Hud.log', 'r') as x:
        data = x.read().splitlines(True)
    with open('Hud.log', 'w') as z:
        z.writelines(data[1:])


def getInfo():
    """Returns data from the log in the form of a list\nMAY NOT WORK, CURRENTLY UNUSED"""
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
