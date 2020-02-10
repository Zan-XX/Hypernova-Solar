import can
import Logger
from tkinter import *
from tkinter import ttk


def canSend(temp):
    from can import Message
    Message(data=[temp])
    info = Logger.getHudInfo()
    Logger.log(info[0], info[1], info[2], info[3], temp)


def update():
    can.CanutilsLogWriter('Hud.log', channel='vcan0', append=True)
    info = Logger.getHudInfo()
    ttk.Label(mainframe, text=info[0] + ' MPH').grid(column=1, row=2)
    ttk.Label(mainframe, text=info[1] + '%').grid(column=2, row=2)
    ttk.Label(mainframe, text=info[2] + u'\u00b0F').grid(column=3, row=2)
    ttk.Label(mainframe, text=info[3] + u'\u00b0F').grid(column=4, row=2)
    ttk.Label(mainframe, text=info[4]).grid(column=4, row=4)
    root.after(300, update)


canMsg = IntVar()
root = Tk()
root.title('Hud')
mainframe = ttk.Frame(root, padding='3 3 12 12')
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
ttk.Label(mainframe, text='Speed').grid(column=1, row=1)
ttk.Label(mainframe, text='Battery').grid(column=2, row=1)
ttk.Label(mainframe, text='Temp 1').grid(column=3, row=1)
ttk.Label(mainframe, text='Temp 2').grid(column=4, row=1)
ttk.Label(mainframe, text='Test').grid(column=1, row=3)
ttk.Label(mainframe, text='only int\'s').grid(column=1, row=4)
ttk.Label(mainframe, text='CAN Message').grid(column=1, row=4)
ttk.Entry(mainframe, textvariable=canMsg).grid(column=2, row=4)
ttk.Button(mainframe, text='send', command=canSend(canMsg.get())).grid(column=3, row=4)
for child in mainframe.winfo_children():
    child.grid_configure(padx=20, pady=5)
update()
root.mainloop()
