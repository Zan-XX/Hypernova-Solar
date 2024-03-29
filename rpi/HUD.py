# usr bin python3
# Python 3.7.3

from tkinter import Tk, Label, Button, StringVar
import logger as log
import can

# Config
bus = can.interface.Bus(bustype='virtual', channel='can0', bitrate='500000')
timeout = {  # dictionary to count missed packets for each sensor
    0x102: 0,  # (can_id, number missed)
    0x104: 0
}


# GUI
class GUI:
    def __init__(self, master):
        self.master = master

        # Make window fullscreen
        # master.attributes('-fullscreen', True) #Start in fullscreen with no borders

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

        # Exit button since there is no window border
        self.exit = Button(master, text="Quit", command=master.destroy)
        self.exit.grid(row=0, column=2)


# CAN Logic
def update_field(self, data, can_id, byteorder='big'):  # Processes data based on can_id
    num = int.from_bytes(data, byteorder)

    if can_id == 0x102:  # checks message CAN id
        self.temp1_text.set("%02.1f" % (num / 10))  # logic based on the can type of message and/or data processing
        timeout[can_id] = 0  # reset timeout
        log.log("temp1", "%02.1f" % (num / 10))  # log data

    if can_id == 0x104:
        self.int_text.set("%03d" % num)
        timeout[can_id] = 0
        log.log("int_text", "%03d" % num)


def check_timeout(self):  # Checks to see if a sensor timed out and if it does set it as "---"
    for i in timeout:
        timeout[i] += 1
    if timeout[0x102] > 5:
        self.temp1_text.set("---")
        log.log("temp1", "--- Not Responding ---")
    elif timeout[0x104] > 5:
        self.int_text.set("---")
        log.log("int_text", "--- Not Responding ---")


# refresh can messages and HUD
def refresh():
    print('--------------')
    while True:
        msg = bus.recv(timeout=0.1)
        if msg is None:
            print('break')
            break
        print(int.from_bytes(msg.data, byteorder='big'))
        can.update_field(msg.data, msg.arbitration_id)
        can.check_timeout()
        log.clearOld()
    root.after(100, refresh)


root = Tk()
can = GUI(root)
root.after_idle(refresh)

root.mainloop()
