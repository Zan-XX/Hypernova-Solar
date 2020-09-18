import Logger
from tkinter import *
from tkinter import ttk


def update():
    info = Logger.getHudInfo()
    ttk.Label(mainframe, text=info[0]).grid(column=1, row=2)
    ttk.Label(mainframe, text=info[1]).grid(column=2, row=2)
    ttk.Label(mainframe, text=info[2]).grid(column=3, row=2)
    ttk.Label(mainframe, text=info[3]).grid(column=4, row=2)
    root.after(300, update)


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
for child in mainframe.winfo_children():
    child.grid_configure(padx=20, pady=5)
update()
root.mainloop()
