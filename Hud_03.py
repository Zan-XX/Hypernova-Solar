import can
import canInterface
from tkinter import *
bus = can.interface.Bus(channel='can0', bustype='socketcan_native')


def refresh():              #Refresh the gui on receving can message
    msg.set(canInterface.canReceive(bus))
    refresh()


class HypernovaHud:         #Draws the hud gui
    def __init__(self, master):
        self.master = master
        master.title("Hypernova Hud GUI")

        self.label = Label(master, text="This is the CAN message: ")
        self.label.grid(column=1, row=1)

        self.msgLabel = Label(master, text=msg.get())
        self.msgLabel.grid(column=2, row=1)

        self.msgEntry = Entry(master, width=20)
        self.msgEntry.grid(column=1, row=2)

        self.send_button = Button(master, text="Send CAN message", command=canInterface.canSend(bus, 100, bytearray(self.msgEntry.get())))
        self.send_button.grid(column=2, row=2)

        refresh()


canInterface.log(22)    #debug
msg = StringVar()       
msg.set(canInterface.canReceive(bus))
root = Tk()
my_gui = HypernovaHud(root)
root.mainloop()
