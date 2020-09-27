#!/usr/bin/python3
# Python 3.7.3

from tkinter import Tk, Label, Button, StringVar
import can
import canInterface

bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate='500000')


class CAN:
    def __init__(self, master):
        self.master = master
        master.attributes('-fullscreen', True)  # Start in fullscreen with no borders

        # Column 0
        self.int = Label(master, text="Test int")
        self.int.grid(row=0, column=0)

        self.int_text = StringVar()
        self.int_text.set('---')
        self.int_label = Label(master, textvariable=self.int_text)
        self.int_label.grid(row=1, column=0)

        # Column 1
        self.temp1 = Label(master, text="Temp 1")
        self.temp1.grid(row=0, column=1)

        self.temp1_text = StringVar()
        self.temp1_text.set('---')
        self.temp1_label = Label(master, textvariable=self.temp1_text)
        self.temp1_label.grid(row=1, column=1)

        # Exit button since there is now window border
        self.exit = Button(master, text="Quit", command=master.destroy)
        self.exit.grid(row=0, column=2)

    def update_field(self, data, can_id, byteorder='big'):
        """Update field based on CAN ID"""
        num = int.from_bytes(data, byteorder)
        if can_id == 0x102:
            self.temp1_text.set("%02.1f", num / 10)
            canInterface.log("temp1", num / 10)  # logs without formatting
        elif can_id == 0x104:
            self.int_text.set("%03d" % num)
            canInterface.log("int text", num)  # logs without formatting


root = Tk()
can = CAN(root)
root.update()  # Sets fields to default values
for msg in bus:  # On each CAN message
    can.update_field(msg.data, msg.arbitration_id)  # Pass data and CAN ID to function for conversion
    root.update()  # Update the window
