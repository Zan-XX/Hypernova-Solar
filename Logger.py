import logging

logging.basicConfig(filename='Hud.log', filemode='a+', format='%(asctime)s - %(message)s', datefmt='%b/%d/%y %H:%M:%S')


def log(speed, charge, temp1, temp2):
    logRow = 'Speed: ' + speed + ' Charge: ' + charge + ' Temp1: ' + temp1 + ' Temp2: ' + temp2 + ' '
    logging.error('%s', logRow)


def clearLine():
    with open('Hud.Log', 'r') as x:
        data = x.read().splitlines(True)
    with open('Hud.log', 'w') as z:
        z.writelines(data[1:])


for i in range(2):
    log('60', '100', '90', '92')
