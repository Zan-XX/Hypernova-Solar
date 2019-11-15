import Logger
from tkinter import *
from tkinter import ttk
from datetime import *


def update():
    global temp1
    global temp2
    f = open('Hud.log', 'r')
    f1 = f.readlines()
    line = f1[-1].split(' ')
    top = f1[0].split('-')
    ttk.Label(mainframe, text=line[4]+' MPH').grid(column=1, row=2)
    ttk.Label(mainframe, text=line[6]+'%').grid(column=2, row=2)
    ttk.Label(mainframe, text=line[8]+u'\u00b0F').grid(column=3, row=2)
    ttk.Label(mainframe, text=line[10]+u'\u00b0F').grid(column=4, row=2)
    now = datetime.strptime(top[0], '%b/%d/%y %H:%M:%S ')
    if now < time:
        Logger.clearLine()
    root.after(300, update)


root = Tk()
root.title('Hud')
temp1 = StringVar()
temp2 = StringVar()
time = datetime.now() - timedelta(hours=1)
mainframe = ttk.Frame(root, padding='3 3 12 12')
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
ttk.Label(mainframe, text='Speed').grid(column=1, row=1)
ttk.Label(mainframe, text='Battery').grid(column=2, row=1)
ttk.Label(mainframe, text='Temp 1').grid(column=3, row=1)
ttk.Label(mainframe, text='Temp 2').grid(column=4, row=1)
for child in mainframe.winfo_children():
    child.grid_configure(padx=20, pady=5)
update()
Logger.clearLine()
root.mainloop()
